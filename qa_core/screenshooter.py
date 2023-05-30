import os
import time
import allure

from io import BytesIO
from pathlib import Path
from PIL import Image, ImageDraw
from qa_core.qa_core_settings import QaCoreSettings
from qa_core.s3client import S3client
from selenium.webdriver.common.by import By
from itertools import chain


# Пути до изображений в директории
expected_file = ""  # базовое изображение
actual_file = ""  # текущее изображение
mark_file = ""  # маркированное изображение


class ScreenShooter(object):
    def __init__(self):
        self.s3_name = QaCoreSettings.S3_BUCKET_NAME

    @allure.step("Метод сравнения текущего изображения с изображением в хранилище")
    def check_s3_images(
        self,
        browser,
        screen_name,
        width,
        language,
        browser_name,
        element=(By.XPATH, "//div"),
        full_page=False,
    ):
        # Забираем изображение из хранилища, если его там нет, то делаем скрин и помещаем этот скрин в хранилище
        self.check_baseline_s3_element_image(browser, screen_name, width, language, browser_name, *element, full_page)
        # Делаем текущий скриншот элемента
        ScreenShooter.make_actual_element_screenshot(
            browser,
            screen_name,
            width,
            language,
            browser_name,
            element,
            full_page,
        )
        # Сравниваем базовое изображение с текущим скриншотом
        ScreenShooter.compare_screenshots(
            language,
            screen_name,
            browser_name,
            width,
            threshold=ScreenShooter.calculate_distance(),
        )

    @allure.step("Скачиваем базовое изображение из хранилища, если его там нет, то делаем скрин и кладем в хранилище")
    def check_baseline_s3_element_image(
        self,
        browser,
        screen_name,
        width,
        language,
        browser_name,
        how,
        what,
        full_page,
    ):
        s3 = S3client()
        # Путь, по которому должно располагаться ожидаемое изображение
        global expected_file
        expected_file = (
            "./Screenshots/" + browser_name + "/expected/" + language + "/" + screen_name + "_" + width + ".png"
        )
        # Путь, по которому должно располагаться изображение в хранилище
        s3_prefix = self.s3_name + "/" + browser_name + "/" + language + "/" + screen_name + "_" + width + ".png"
        if os.path.exists(expected_file):
            os.remove(expected_file)
        # Убеждаемся, что в проекте есть директория expected, если нет - то создаем ее
        Path("./Screenshots/" + browser_name + "/expected/" + language).mkdir(parents=True, exist_ok=True)
        if not s3.file_exist(bucket=self.s3_name, prefix=s3_prefix):
            time.sleep(2)
            if not full_page:
                browser.find_element(how, what).screenshot(expected_file)
            else:
                browser.save_screenshot(expected_file)
            s3.upload_file(file_name=expected_file, bucket=self.s3_name, object_name=s3_prefix)
        else:
            s3.download_file(self.s3_name, s3_prefix, expected_file)
        with allure.step("Базовый скриншот элемента"):
            ScreenShooter.compress_screenshot("expected")
            allure.attach.file(
                expected_file,
                name="Expected_Screenshot",
                attachment_type=allure.attachment_type.PNG,
            )

    @staticmethod
    @allure.step("Делаем текущий скриншот элемента")
    def make_actual_element_screenshot(browser, screen_name, width, language, browser_name, element, full_page):
        time.sleep(2)
        # Убеждаемся, что в проекте есть директория actual, если нет - то создаем ее
        Path("./Screenshots/" + browser_name + "/actual/" + language).mkdir(parents=True, exist_ok=True)
        global actual_file
        actual_file = (
            "./Screenshots/" + browser_name + "/actual/" + language + "/" + screen_name + "_" + width + ".png"
        )
        if os.path.exists(actual_file):
            os.remove(actual_file)
        if full_page:
            browser.save_screenshot(actual_file)
        else:
            png = browser.find_element(*element).screenshot_as_png  # saves screenshot of element
            im = Image.open(BytesIO(png))  # uses PIL library to open image in memory
            im.save(actual_file)
        with allure.step("Актуальный скриншот элемента"):
            ScreenShooter.compress_screenshot("actual")
            allure.attach.file(
                actual_file,
                name="Actual_Screenshot",
                attachment_type=allure.attachment_type.PNG,
            )

    @staticmethod
    @allure.step("Сравниваем базовое изображение с текущим скриншотом")
    def compare_screenshots(language, screen_name, browser_name, width, threshold):
        expected_image = Image.open(expected_file).convert("RGB")
        actual_image = Image.open(actual_file).convert("RGB")
        # Вычисление разницы в пикселях между скриншотами
        if expected_image.size == actual_image.size:
            diff = ImageDiff(actual_image, expected_image)
            distance = int(abs(diff.get_distance()))
        else:
            # Значит элементы изначально отличаются по размеру
            distance = threshold + 1  # ставим threshold > distance, чтобы зафейлить тесты
        # Если разница в пикселях между скринами больше допустимого значения
        if distance > threshold:
            ScreenShooter.screenshot_marking_analyse(language, screen_name, browser_name, width)
            with allure.step("Скриншот с отличиями"):
                ScreenShooter.compress_screenshot("marked")
                allure.attach.file(
                    mark_file,
                    name="Marked_Screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
            raise AssertionError("Отличие скриншотов > 0.33% пикселей. Разница в пикселях - " + str(distance))
        else:
            with allure.step("Скриншоты сверены корректно"):
                pass

    # Метод вычисления допустимой разницы между текущим и базовым изображениями
    @staticmethod
    def calculate_distance(sensitivity=300):
        """
        Метод вычисления допустимой разницы в пикселях
        :param sensitivity: Чувствительность по умолчанию - 0.33%, чем больше sensitivity, тем ниже процент
        :return: Возвращает допустимое расхождение в количестве пикселей при сравнении скриншотов
        """
        screenshot_staging = Image.open(expected_file)
        screen_width, screen_height = screenshot_staging.size
        return (screen_height * screen_width) / sensitivity

    # Метод маркировки и сохранения скриншота в marked
    @staticmethod
    def screenshot_marking_analyse(language, screen_name, browser_name, width):
        screenshot_staging = Image.open(expected_file)
        screenshot_production = Image.open(actual_file)
        screen_width, screen_height = screenshot_staging.size

        columns = screen_height
        rows = screen_width

        block_width = int(((screen_width - 1) // columns) + 1)
        block_height = int(((screen_height - 1) // rows) + 1)

        for y in range(0, screen_height, block_height + 1):
            for x in range(0, screen_width, block_width + 1):
                region_staging = ScreenShooter.process_region(screenshot_staging, x, y, block_width, block_height)
                region_prod = ScreenShooter.process_region(screenshot_production, x, y, block_width, block_height)

                if region_staging is not None and region_prod is not None and region_prod != region_staging:
                    draw = ImageDraw.Draw(screenshot_staging)
                    draw.rectangle((x, y, x + block_width, y + block_height), outline="red")

        global mark_file
        mark_file = "./Screenshots/" + browser_name + "/marked/" + language + "/" + screen_name + "_" + width + ".png"
        # Убеждаемся, что в проекте есть директория marked, если нет - то создаем ее
        Path("./Screenshots/" + browser_name + "/marked/" + language).mkdir(parents=True, exist_ok=True)
        screenshot_staging.save(mark_file)

    # Метод определяет чувствительность попиксельной проверки скриншотов
    @staticmethod
    def process_region(image, x, y, width, height):
        """
        Метод определяет чувствительность попиксельной проверки скриншотов
        :param image: Скриншот страницы/элемента
        :param x: количество столбцов в изображении
        :param y: Количество строк в изображении
        :param width: Ширина изображения
        :param height: Высота изображения
        :return: Возвращает результат сравнения с множителем точности
        """
        region_total = 0

        # This can be used as the sensitivity factor, the larger it is the less sensitive the comparison
        factor = 100

        for coordinateY in range(y, y + height):
            for coordinateX in range(x, x + width):
                try:
                    pixel = image.getpixel((coordinateX, coordinateY))
                    region_total += sum(pixel) / 4
                except IndexError:
                    pass
                except (FileNotFoundError, IOError):
                    return
        return region_total / factor

    @allure.step("Метод перезаписывает изображение элемента в хранилище")
    def rewrite_s3_element_image(self, browser, element, screen_name, width, language, browser_name):
        s3 = S3client()
        # Убеждаемся, что в проекте есть директория expected, если нет - то создаем ее
        Path("./Screenshots/" + browser_name + "/expected/" + language).mkdir(parents=True, exist_ok=True)
        global expected_file
        expected_file = (
            "./Screenshots/" + browser_name + "/expected/" + language + "/" + screen_name + "_" + width + ".png"
        )
        s3_prefix = self.s3_name + "/" + browser_name + "/" + language + "/" + screen_name + "_" + width + ".png"
        if os.path.exists(expected_file):
            os.remove(expected_file)
        time.sleep(2)
        browser.find_element(*element).screenshot(expected_file)
        s3.upload_file(file_name=expected_file, bucket=self.s3_name, object_name=s3_prefix)

    # Метод сжатия изображения для allure-отчета
    @staticmethod
    def compress_screenshot(sc_type):
        if sc_type == "expected":
            foo = Image.open(expected_file)
            os.remove(expected_file)
            foo.save(expected_file, optimize=True, quality=50)
        elif sc_type == "actual":
            foo = Image.open(actual_file)
            os.remove(actual_file)
            foo.save(actual_file, optimize=True, quality=50)
        elif sc_type == "marked":
            foo = Image.open(mark_file)
            os.remove(mark_file)
            foo.save(mark_file, optimize=True, quality=50)


class ImageDiff(object):
    def __init__(self, image_a, image_b):
        # Размеры изображений равны
        assert image_a.size == image_b.size
        # Цветовая модель изображений одинаковая
        assert image_a.getbands() == image_b.getbands()

        self.image_a = image_a
        self.image_b = image_b

    # Возвращает разницу между двумя изображениями в пикселях
    def get_distance(self):
        a_values = chain(*self.image_a.getdata())
        b_values = chain(*self.image_b.getdata())
        band_len = len(self.image_a.getbands())
        distance = 0
        for a, b in zip(a_values, b_values):
            distance += abs(float(a) / band_len - float(b) / band_len) / 255
        return distance

import argparse
import os
from os.path import basename
from zipfile import ZipFile
from os import path


def main():
    """
    Метод для архивации содержимого папки allure-results
    """
    parser = argparse.ArgumentParser(
        prog="zip-allure-reports, ver.0.1 beta\n",
        add_help=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-n", "--name", required=True, type=str)
    args = parser.parse_args()
    # Check if file exists
    if not path.exists(f"{args.name}"):
        print("no dir")
    else:
        print("yes dir")
        with ZipFile("allure-results.zip", "w") as zipObj:
            # Iterate over all the files in directory
            for folderName, subfolders, filenames in os.walk(f"{args.name}"):
                for filename in filenames:
                    # create complete filepath of file in directory
                    file_path = os.path.join(folderName, filename)
                    # Add file to zip
                    zipObj.write(file_path, basename(file_path))
        print("zip complete")


if __name__ == "__main__":
    main()

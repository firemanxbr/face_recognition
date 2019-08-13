"""
    LFW methods to management the dataset of Veriff challenge.

    This code is following the best practices of PEP 20, PEP 8,
    and 'The Best of the Best Practices (BOBP) Guide for Python'

    Reference: https://gist.github.com/sloria/7001839#file-bobp-python-md
"""
import hashlib
import glob

from shutil import unpack_archive

import requests


def lfw_acquisition(url, md5sum, path=None):
    """
    LFW acquisition is the method to download, validate,
    extract the main LFW dataset.

    :param url: LFW url to download the dataset.
                Included the file name in the url.
    :param md5sum: the md5sum code to validate the dataset file.
    :param path: the path that will be used to extract the content
                 of the dataset. Default value is ".".

    :return: array with all faces/photos in the format of the path
             of files.
    """
    if path is None:
        path = "."

    dataset_file = url.split('/')[-1]
    folder = dataset_file.split('.')[0]

    if url and md5sum and dataset_file:
        req = requests.get(url)

        with open(dataset_file, "wb") as data:
            data.write(req.content)

        get_md5 = hashlib.md5(open(dataset_file, "rb").read()).hexdigest()

        if get_md5 != md5sum:
            raise FileExistsError("The file is not validated")

        unpack_archive(dataset_file, path)
        dataset = []

        files = []

        for fls in glob.glob('{0}/{1}/'.format(path, folder) + "**/*.jpg",
                             recursive=True):
            files.append(fls)

        for fls in files:
            dataset.append(fls)
        
        return dataset

    return AttributeError("Check the parameters passed to the function")

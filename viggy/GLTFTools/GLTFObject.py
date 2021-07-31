from __future__ import annotations

from typing import TYPE_CHECKING, Type, TypeVar

if TYPE_CHECKING:
    from .GLTFFile import GLTFFile


T = TypeVar('T')


def getFromJSONDict(jsonDict: dict, key: str, default=None):
    """
    :param jsonDict:
    :param key: the key of object in jsonDict
    :param default: the value to return in case key does not exist
    :return: object with given key in jsonDict
    """
    if key in jsonDict:
        return jsonDict[key]
    else:
        return default


def createGLTFObject(file: GLTFFile, cls: Type[T], arrayName: str, index: int) -> T:
    """
    should be called whenever creating a GLTFObject child object
    :param file: the GLTFFile object
    :param cls: constructor whose arguments are (file, index) whose meanings are same os GLTFObject
    :param arrayName: the array of the file object in which to check is object was already constructed
    :param index: the index of the array to check
    :return: the new object if not yet created, or reference to created object
    """
    if getattr(file, arrayName)[index] is None:
        return cls(file, index)
    else:
        return getattr(file, arrayName)[index]


class GLTFObject:
    def __init__(self, file: GLTFFile, arrayName: str, index: int):
        """
        :param file: the GLTFFile object
        :param arrayName: the array of file that the object should be put in
        :param index: the index of the array of the file object as well as the raw file
        """
        # set reference to self in appropriate array in file
        getattr(file, arrayName)[index] = self

        self.index: int = index
        self.jsonDict: dict = file.jsonData[arrayName][index]

        self.file = file

        # user defined name
        self.name: str = self.getFromJSONDict("name")

    def getFromJSONDict(self, key: str, default=None):
        return getFromJSONDict(self.jsonDict, key, default)

    def createGLTFObject(self, cls: Type[T], arrayName: str, index: int) -> T:
        return createGLTFObject(self.file, cls, arrayName, index)

from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type, TypeVar, List

if TYPE_CHECKING:
    from .GLTFFile import GLTFFile


T = TypeVar('T')


def getFromJSONDict(jsonDict: dict, key: str, default=None):
    """
    returns jsonDict[key] if key is valid else returns default
    """
    return jsonDict[key] if key in jsonDict else default


def createGLTFObject(file: GLTFFile, cls: Type[T], arrayName: str, index: int, *args, **kwargs) -> Optional[T]:
    """
    returns cls(file, index) if such arguments have not already been passed.
    if arguments already passed, it will be stored in file.<arrayName>[index]

    :param file:
    :param cls: subclass of GLTFObject
    :param arrayName:
    :param index:
    :return: the new object if not yet created, or reference to created object
    """
    if getattr(file, arrayName)[index] is None:
        return cls(file, index, *args, **kwargs)
    else:
        return getattr(file, arrayName)[index]


def createFromKey(file: GLTFFile, cls: Type[T], arrayName: str, jsonDict: dict, key: str,
                  *args, **kwargs) -> Optional[T]:
    return createGLTFObject(file, cls, arrayName, jsonDict[key], *args, **kwargs) if key in jsonDict else None


class GLTFObject:
    def __init__(self, file: GLTFFile, arrayName: str, index: int):
        """
        :param file: the GLTFFile object
        :param arrayName: the name of the array key where the GLTFObject lies
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

    def createFromKey(self, cls: Type[T], arrayName: str, key: str, *args, **kwargs) -> Optional[T]:
        return createFromKey(self.file, cls, arrayName, self.jsonDict, key, *args, **kwargs)

    def createArrayFromKey(self, cls: Type[T], arrayName: str, key: str,
                           *args, **kwargs) -> Optional[List[Optional[T]]]:
        if key in self.jsonDict:
            return [createGLTFObject(self.file, cls, arrayName, i, *args, **kwargs) for i in self.jsonDict[key]]
        else:
            return None

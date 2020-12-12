#!/usr/bin/python3

from context import logging_plus
logger = logging_plus.getLogger(__name__)

class MyClass:
    def __init__(self):
        self.__status = 1
        logger.debug("## A")
    def __del__(self):
        logger.debug("## B")

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    def doSomething(self):
        logger.debug("## C")

class MySpecialClass(MyClass):
    def __init__(self):
        logger.debug("## D")
        super().__init__()

    def __del__(self):
        logger.debug("## E")
        super().__del__()

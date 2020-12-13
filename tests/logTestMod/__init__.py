#!/usr/bin/python3

from context import logging_plus
logger = logging_plus.getLogger(__name__)

class MyClass:
    def __init__(self):
        self.__status = 1
        logger.debug("## Explicit log: A - Initializing MyClass")
        
    def __del__(self):
        logger.debug("## Explicit log: B - Finalizing MyClass")

    @property
    def status(self):
        logger.debug("## Explicit log: C - getter of MyClass")
        return self.__status

    @status.setter
    def status(self, value):
        logger.debug("## Explicit log: D - setter of MyClass")
        self.__status = value

    def doSomething(self):
        logger.debug("## Explicit log: E - MyClass method call")

class MySpecialClass(MyClass):
    def __init__(self):
        logger.debug("## Explicit log: F - Initializing subclass MySpecialClass(MyClass)")
        super().__init__()

    def __del__(self):
        logger.debug("## Explicit log: G - Finalizing subclass MySpecialClass(MyClass)")
        super().__del__()

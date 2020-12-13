#!/usr/bin/python3
"""
Test program for testing logging_plus
"""

import logging
#logging_plus must be imported instead of or in addition to logging
from context import logging_plus

import logTestMod

#A logger used for logging must be instantiated from logging_plus rather than logging
#Handlers and formatters are instantiated from standard logging
logger = logging_plus.getLogger()
mlogger = logging_plus.getLogger(logTestMod.__name__)
handler = logging.StreamHandler()
fhandler = logging.FileHandler("./logTestFull.log","w")
formatter = logging.Formatter('%(asctime)s %(name)-20s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
fhandler.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(fhandler)
logger.setLevel(logging.DEBUG)
mlogger.setLevel(logging.DEBUG)

#The following statement activates automatic logging of function entry and exit
logging_plus.registerAutoLogEntryExit()

#The following statement activates logging also in modules logging, logging_plus and inspect
#Uncomment the following line, if required
logging_plus.noInfrastructureLogging = False


def func(x):
    y = x * x
    logger.debug("## Explicit log: %s ** 2 = %s", x, y)
    return y

logger.debug("## Explicit log: Start")
z = logTestMod.MyClass()
x = logTestMod.MySpecialClass()
y = x.status
x.status = 4
x.doSomething()
func(5)

#Uncommenting the following line causes z to be finalized explicitely
del z

#Commenting the following line causes x to be finalized by garbage collection.
#del x

#!/usr/bin/python3

import logging
from context import logging_plus

import logTestMod

import sys

logger = logging_plus.getLogger()
mlogger = logging_plus.getLogger(logTestMod.__name__)
handler = logging.StreamHandler()
fhandler = logging.FileHandler("./logTest.log","w")
formatter = logging.Formatter('%(asctime)s %(name)-20s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
fhandler.setFormatter(formatter)
logger.addHandler(handler)
logger.addHandler(fhandler)
logger.setLevel(logging.DEBUG)
#mlogger.addHandler(handler)
#mlogger.addHandler(fhandler)
mlogger.setLevel(logging.DEBUG)

logging_plus.registerAutoLogEntryExit()
#loggingext.noInfrastructureLogging = False


def func(x):
    y = x * x
    logger.debug("%s ** 2 = %s", x, y)
    return y

logger.debug("Start")

#m = loggingext.getLogger().manager
#m.cleanupLoggers()

x = logTestMod.MySpecialClass()
y = x.status
x.status = 4
x.doSomething()
func(5)
#del x

# Python logging add-on

This package provides some enhancements to standard Python logging:

- Subclassed Logger allowing customization of logging output
- Automatic indentation depending on call stack level
- Generic logging of function entry and exit
- Standard filter and handler support is preserved

## Content

- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Logging Function Entry and Exit](#logging-function-entry-and-exit)
- [Supressing Entry/Exit Logging in specific Infrastructure Modules](#supressing-entryexit-logging-in-specific-infrastructure-modules)
- [Shutdown Behavior](#shutdown-behavior)
- [Output](#output)

## Installation

__logging_plus__ is available on PyPI.

Use pip to install:

```shell
pip install logging-plus
```

## Basic Usage

In order to use this logging add-on, you only need to import __logging_plus__ in addition to __logging__
and instantiate a Logger instance from __logging_plus__ rather than __logging__.

Then your python code will look, for example, as follows:

```python
#!/usr/bin/python3
import logging
import logging_plus                               #Specific for logging_plus

logger = logging_plus.getLogger('my_logger')      #Specific for logging_plus
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-20s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
```

The only lines which are specific for __logging_plus__ are marked.

## Logging Function Entry and Exit

In order to automatically log entry and exit of functions, the following line needs to be added after the first import of __logging_plus__:

```python
logging_plus.registerAutoLogEntryExit()
```

This can be deactivated through

```python
logging_plus.unregisterAutoLogEntryExit()
```

### Details

Logging of function entry and exit is generic and automatic and does not require any coding.
It is implemented by registering a logging function as system __trace function__ (```sys.settrace(autoLogEntryExit)```).

__ATTENTION:__ Since this function may also be used by Python debuggers, it may be necessary to skip this statement when debugging.

Logging of function entry and exit uses a logger with the name of the module in which the function is located (```__name__```).

Logging of function entry and exit uses __logging.DEBUG__ level

## Supressing Entry/Exit Logging in specific Infrastructure Modules

When activated, the mechanism for automatic logging of function entry and exit is active in __all__ functions within program control flow.

A lot of logging output would, therefore, also be produced by the __logging__ module itself as well as the functions called from there.
Since this is normally not of interest, logging in specific infrastructure modules and subordinate functions is deactivated by default.

The following statement activates entry/exit logging for all modules.

```python
logging_plus.noInfrastructureLogging = False
```

This affects logging in the following modules as well as any functions in a call stack originating from these modules:

- logging
- logging_plus
- inspect

## Shutdown Behavior

During shutdown of the Python interpreter, a special sequence of actions is followed:

1. Stop main thread
2. Close open file handlers
3. Wait for termination of non-daemon threads
4. Execute registered atexit functions
5. Garbage collection
6. Process termination

Automatic logging of function entry and exit may cause issues when this would be tried in functions which are run during the shutdown process.
For example, class finalizers ```__del__()```, called during garbage collection, could cause logging issues if a logging file handler is involved, because at this time the shutdown process has already closed any open file handlers.

To avoid such issues, __logging_plus__ registers two ```atexit``` routines:

- ```atexit.register(removeFileHandlers)```
which removes any file handlers found in any of the active loggers
- ```atexit.register(unregisterAutoLogEntryExit)```
which disables automatic entry/exit logging

These routines are executed in step 4, above, before garbage collection, with the following consequences in case that objects are not finalized explicitely but during garbage collection:

- there is no automatic logging of finalizer (```__del__()```) entry/exit.
- for explicit logs, there is no file output even for loggers for which a file handler has been registered.

__NOTE:__ in case of explicitely finalizing object instances by using ```del myObj``` to remove all references to an instance, logging within ```__del__()``` is done like in any other function.

(see also chapter 3.3 in <https://docs.python.org/3/reference/datamodel.html#index-70>)

## Output

The following is the logging output from the test module under ./tests with automatic entry/exit logging activated.

The file output can be found at ./tests/logTest.log.
The file output for a run with full logging is in ./tests/logTestFull.log

```shell
2020-12-13 12:37:40,048 root                 DEBUG        Start
2020-12-13 12:37:40,057 logTestMod           DEBUG        >>> Entry __init__ (/home/pi/dev/py-logging-plus/tests/logTestMod/__init__.py - line 7 - module logTestMod)
2020-12-13 12:37:40,086 logTestMod           DEBUG            ## Explicit log: A - Initializing MyClass
2020-12-13 12:37:40,093 logTestMod           DEBUG        <<< Exit  __init__ : Return value: None
2020-12-13 12:37:40,095 logTestMod           DEBUG        >>> Entry __init__ (/home/pi/dev/py-logging-plus/tests/logTestMod/__init__.py - line 27 - module logTestMod)
2020-12-13 12:37:40,124 logTestMod           DEBUG            ## Explicit log: F - Initializing subclass MySpecialClass(MyClass)
2020-12-13 12:37:40,132 logTestMod           DEBUG            >>> Entry __init__ (/home/pi/dev/py-logging-plus/tests/logTestMod/__init__.py - line 7 - module logTestMod)
2020-12-13 12:37:40,170 logTestMod           DEBUG                ## Explicit log: A - Initializing MyClass
2020-12-13 12:37:40,177 logTestMod           DEBUG            <<< Exit  __init__ : Return value: None
2020-12-13 12:37:40,179 logTestMod           DEBUG        <<< Exit  __init__ : Return value: None
2020-12-13 12:37:40,180 logTestMod           DEBUG        >>> Entry status (/home/pi/dev/py-logging-plus/tests/logTestMod/__init__.py - line 13 - module logTestMod)
2020-12-13 12:37:40,210 logTestMod           DEBUG            ## Explicit log: C - getter of MyClass
2020-12-13 12:37:40,217 logTestMod           DEBUG        <<< Exit  status : Return value: 1
2020-12-13 12:37:40,219 logTestMod           DEBUG        >>> Entry status (/home/pi/dev/py-logging-plus/tests/logTestMod/__init__.py - line 18 - module logTestMod)
2020-12-13 12:37:40,248 logTestMod           DEBUG            ## Explicit log: D - setter of MyClass
2020-12-13 12:37:40,256 logTestMod           DEBUG        <<< Exit  status : Return value: None
2020-12-13 12:37:40,257 logTestMod           DEBUG        >>> Entry doSomething (/home/pi/dev/py-logging-plus/tests/logTestMod/__init__.py - line 23 - module logTestMod)
2020-12-13 12:37:40,287 logTestMod           DEBUG            ## Explicit log: E - MyClass method call
2020-12-13 12:37:40,295 logTestMod           DEBUG        <<< Exit  doSomething : Return value: None
2020-12-13 12:37:40,296 __main__             DEBUG        >>> Entry func (logTest.py - line 26 - module __main__)
2020-12-13 12:37:40,327 root                 DEBUG            ## Explicit log: 5 ** 2 = 25
2020-12-13 12:37:40,335 __main__             DEBUG        <<< Exit  func : Return value: 25
2020-12-13 12:37:40,337 logTestMod           DEBUG        >>> Entry __del__ (/home/pi/dev/py-logging-plus/tests/logTestMod/__init__.py - line 10 - module logTestMod)
2020-12-13 12:37:40,367 logTestMod           DEBUG            ## Explicit log: B - Finalizing MyClass
2020-12-13 12:37:40,374 logTestMod           DEBUG        <<< Exit  __del__ : Return value: None
2020-12-13 12:37:40,377 threading            DEBUG    >>> Entry _shutdown (/usr/lib/python3.7/threading.py - line 1263 - module threading)
2020-12-13 12:37:40,378 threading            DEBUG        >>> Entry _stop (/usr/lib/python3.7/threading.py - line 968 - module threading)
2020-12-13 12:37:40,380 threading            DEBUG        <<< Exit  _stop : Return value: None
2020-12-13 12:37:40,381 threading            DEBUG        >>> Entry _pickSomeNonDaemonThread (/usr/lib/python3.7/threading.py - line 1284 - module threading)
2020-12-13 12:37:40,383 threading            DEBUG            >>> Entry enumerate (/usr/lib/python3.7/threading.py - line 1244 - module threading)
2020-12-13 12:37:40,384 threading            DEBUG            <<< Exit  enumerate : Return value: [<_MainThread(MainThread, stopped 547789455376)>]
2020-12-13 12:37:40,386 threading            DEBUG            >>> Entry daemon (/usr/lib/python3.7/threading.py - line 1104 - module threading)
2020-12-13 12:37:40,387 threading            DEBUG            <<< Exit  daemon : Return value: False
2020-12-13 12:37:40,389 threading            DEBUG            >>> Entry is_alive (/usr/lib/python3.7/threading.py - line 1080 - module threading)
2020-12-13 12:37:40,391 threading            DEBUG            <<< Exit  is_alive : Return value: False
2020-12-13 12:37:40,392 threading            DEBUG        <<< Exit  _pickSomeNonDaemonThread : Return value: None
2020-12-13 12:37:40,393 threading            DEBUG    <<< Exit  _shutdown : Return value: None
2020-12-13 12:37:40,407 logTestMod           DEBUG        ## Explicit log: G - Finalizing subclass MySpecialClass(MyClass)
2020-12-13 12:37:40,408 logTestMod           DEBUG            ## Explicit log: B - Finalizing MyClass
```

The last two lines in this example originate from explicit logging calls in finalizers called during garbage collection.
In case of an explicit call of ```del obj```, also entry and exit of the finalizers are logged automatically as seen for timestamp 2020-12-13 12:37:40,337.

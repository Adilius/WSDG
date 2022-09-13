import logging

# Create debugv function
def debugv(msg, *args, **kwargs):
    if logging.getLogger().isEnabledFor(9):
        logging.log(9, msg)


# Add DEBUGV level to logger on import
logging.addLevelName(9, "DEBUGV")
logging.debugv = debugv
logging.Logger.debugv = debugv


### Log usage examples
# logging.debugv("Debugv message")
# logging.debug("Debug message")
# logging.info("Info message")
# logging.warning("Warning message")
# logging.error("Error message")
# logging.critical("Critical message")
# logging.debug('AdiliusWSDG starting.')

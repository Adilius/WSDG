import logging

# Create debugv function
def debugv(msg, *args, **kwargs):
    if logging.getLogger().isEnabledFor(9):
        logging.log(9, msg)


# Add DEBUGV level to logger on import
logging.addLevelName(9, "DEBUGV")
logging.debugv = debugv
logging.Logger.debugv = debugv

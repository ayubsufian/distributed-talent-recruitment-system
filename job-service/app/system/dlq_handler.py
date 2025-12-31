import logging

logger = logging.getLogger("DLQHandler")
logging.basicConfig(level=logging.ERROR)


class DeadLetterQueueHandler:
    """
    Handles messages that failed processing in the Job Service.
    """

    async def handle_failure(self, message_body: bytes, error: Exception):
        try:
            payload = message_body.decode()
        except:
            payload = str(message_body)

        logger.error(f"CRITICAL: Message processing failed in Job Service.")
        logger.error(f"ERROR: {str(error)}")
        logger.error(f"PAYLOAD: {payload}")

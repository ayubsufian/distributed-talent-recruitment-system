import logging

# Configure standard python logging to output to stdout
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("AuditLogger")


class SystemAuditLogger:
    """
    Helper to format logs before sending them to the DB via the UseCase.
    """

    @staticmethod
    def log_event(event_type: str, payload: dict):
        logger.info(
            f"AUDIT_EVENT: [{event_type}] - Payload keys: {list(payload.keys())}"
        )

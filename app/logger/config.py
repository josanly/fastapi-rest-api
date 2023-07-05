import logging
import uuid
from fastapi import FastAPI, Request
import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from app.logger.utils import pretty_print_for_dev, pretty_print_json, pretty_print_for_prod
import enum


# creating enumerations using class
class Mode(enum.Enum):
    dev = "dev"
    full = "full"
    prod = "prod"


def get_structlogger():
    return structlog.get_logger()


class StructLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, mode: Mode):
        super().__init__(app)
        self.mode = mode

        # Get config according to mode
        print_fn = self.get_print_fn()
        min_log_level = self.get_min_log_level()

        structlog.configure(
            cache_logger_on_first_use=True,
            wrapper_class=structlog.make_filtering_bound_logger(min_log_level),
            logger_factory=structlog.BytesLoggerFactory(),
            processors=[
                structlog.threadlocal.merge_threadlocal,
                structlog.processors.add_log_level,
                structlog.processors.format_exc_info,
                structlog.processors.TimeStamper(fmt="iso", utc=True),
                print_fn,
            ],
        )
        get_structlogger().info(f"Logger initialized in {self.mode.value} mode.")

    async def dispatch(self, request: Request, call_next):
        """
        Used by FastAPI as middleware.
        It creates a request id and adds it to the log as well as the url and method.
        """

        request_id = str(uuid.uuid4())
        structlog.threadlocal.clear_threadlocal()
        structlog.threadlocal.bind_threadlocal(
            url=request.url.__str__(),
            method=request.method,
            request_id=request_id,
        )

        # process the request and get the response
        response = await call_next(request)
        response.headers["request_id"] = request_id

        # Send data to loki or other indexer
        # logger.info(f"{request.url.__str__()} sent to loki")

        return response

    def get_print_fn(self):
        """Return the print function. Default is printing for full mode."""
        match self.mode:
            case Mode.dev:
                return pretty_print_for_dev
            case Mode.prod:
                return pretty_print_for_prod
            case Mode.full:
                return pretty_print_json
            case _:
                return pretty_print_json

    def get_min_log_level(self):
        """Return the minimum log level. Default is logging.INFO."""
        match self.mode:
            case Mode.dev:
                return logging.DEBUG
            case Mode.prod:
                return logging.ERROR
            case Mode.full:
                return logging.INFO
            case _:
                return logging.INFO

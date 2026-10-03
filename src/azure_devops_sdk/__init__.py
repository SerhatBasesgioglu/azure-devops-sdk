"""Azure DevOps REST SDK."""

import logging

_package_logger = logging.getLogger("azure_devops_sdk")
if not any(isinstance(handler, logging.NullHandler) for handler in _package_logger.handlers):
    _package_logger.addHandler(logging.NullHandler())

from ._transport import ApiResponse, AdoTransport, UNSET
from .client import AdoClient

__all__ = ["AdoClient", "AdoTransport", "ApiResponse", "UNSET"]

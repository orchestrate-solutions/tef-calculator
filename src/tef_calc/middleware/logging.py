"""
LoggingMiddleware - Structured logging for CodeUChain Link execution.

Task #80: Middleware that logs Link entry, exit, and errors without raising exceptions.
"""

import logging
from datetime import datetime
from typing import Any, Optional

from codeuchain.core import Context, Middleware


logger = logging.getLogger('tef_calc.middleware.logging')


class LoggingMiddleware(Middleware):
    """
    Middleware for structured logging of Link execution.
    
    Logs when Links start, complete, and handles errors without raising exceptions.
    This is observability-only middleware - it never interrupts chain execution.
    
    Logs include:
    - Link name
    - Timestamp
    - Status (starting, completed, error)
    - Error details on exception
    """
    
    def __init__(self):
        """Initialize LoggingMiddleware."""
        super().__init__()
        # Ensure logger is configured with a handler if none exists
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '[%(name)s] %(asctime)s - %(levelname)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)
    
    async def before(self, name: str, ctx: Context[Any]) -> None:
        """
        Log before Link execution.
        
        Args:
            name: Name of the Link being executed
            ctx: Context flowing through the Link
        """
        try:
            logger.info(f"[{name}] starting...")
        except Exception:
            # Never raise from middleware
            pass
    
    async def after(self, name: str, ctx: Context[Any]) -> None:
        """
        Log after Link execution completes successfully.
        
        Args:
            name: Name of the Link that executed
            ctx: Context after Link execution
        """
        try:
            logger.info(f"[{name}] completed")
        except Exception:
            # Never raise from middleware
            pass
    
    async def on_error(self, name: str, ctx: Context[Any], err: Exception) -> None:
        """
        Log when a Link raises an exception.
        
        Args:
            name: Name of the Link that raised an exception
            ctx: Context at time of exception
            err: The exception that was raised
        """
        try:
            error_type = type(err).__name__
            error_msg = str(err)
            logger.error(f"[{name}] ERROR: {error_type}: {error_msg}")
        except Exception:
            # Never raise from middleware
            pass

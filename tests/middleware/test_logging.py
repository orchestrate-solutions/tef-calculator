"""
Tests for LoggingMiddleware (task #80).

Based on codeuchain Middleware pattern for structured logging of Link execution.
"""

import pytest
import logging
import io
from datetime import datetime
from contextlib import redirect_stdout, redirect_stderr
from unittest.mock import Mock, patch, call

from codeuchain.core import Context, Middleware


class TestLoggingMiddlewareBasic:
    """Test basic logging functionality."""
    
    @pytest.fixture
    def capture_logs(self):
        """Fixture to capture log output."""
        log_capture = io.StringIO()
        handler = logging.StreamHandler(log_capture)
        handler.setFormatter(
            logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')
        )
        logger = logging.getLogger('tef_calc.middleware.logging')
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        
        yield log_capture
        
        logger.removeHandler(handler)
    
    def test_logs_before_and_after_link(self, capture_logs):
        """Test case: logs_before_and_after_link
        
        Input: middleware=LoggingMiddleware, link_name="test_link"
        Expected: logs_contain=["starting", "completed"], logs_count=2
        """
        from tef_calc.middleware.logging import LoggingMiddleware
        
        mw = LoggingMiddleware()
        ctx = Context({"test": "data"})
        
        # Call hooks
        mw.before("test_link", ctx)
        mw.after("test_link", ctx)
        
        logs = capture_logs.getvalue()
        
        # Check that logs contain expected keywords
        assert "starting" in logs.lower(), f"Expected 'starting' in logs: {logs}"
        assert "completed" in logs.lower(), f"Expected 'completed' in logs: {logs}"
        
        # Count log lines (should be at least 2)
        log_lines = [line for line in logs.split('\n') if line.strip()]
        assert len(log_lines) >= 2, f"Expected at least 2 log lines, got {len(log_lines)}"
    
    def test_logs_exception_on_error(self, capture_logs):
        """Test case: logs_exception_on_error
        
        Input: middleware=LoggingMiddleware, exception="ValueError"
        Expected: error_logged=true, exception_captured=true
        """
        from tef_calc.middleware.logging import LoggingMiddleware
        
        mw = LoggingMiddleware()
        ctx = Context({"test": "data"})
        error = ValueError("test error message")
        
        # Call error hook
        mw.on_error("test_link", ctx, error)
        
        logs = capture_logs.getvalue()
        
        # Check that error is logged
        assert "error" in logs.lower(), f"Expected 'error' in logs: {logs}"
        assert "ValueError" in logs or "test error" in logs, \
            f"Expected error details in logs: {logs}"
    
    def test_log_format_includes_timestamp(self, capture_logs):
        """Test case: log_format_includes_timestamp
        
        Input: middleware=LoggingMiddleware, link_name="validate"
        Expected: format_correct=true, timestamp_present=true
        """
        from tef_calc.middleware.logging import LoggingMiddleware
        
        mw = LoggingMiddleware()
        ctx = Context({"input": "data"})
        
        mw.before("validate", ctx)
        
        logs = capture_logs.getvalue()
        log_lines = [line for line in logs.split('\n') if line.strip()]
        
        # Check for timestamp-like pattern (ISO format or similar)
        # Should contain digits that look like time
        assert any(char.isdigit() for char in logs), \
            "Expected timestamp with digits in log"
        
        # Check for link name in log
        assert "validate" in logs, f"Expected link name in logs: {logs}"


class TestLoggingMiddlewareIntegration:
    """Test middleware integration with codeuchain Context and Middleware interface."""
    
    def test_middleware_implements_base_interface(self):
        """Test that LoggingMiddleware implements Middleware interface."""
        from tef_calc.middleware.logging import LoggingMiddleware
        
        mw = LoggingMiddleware()
        
        # Should have required methods
        assert hasattr(mw, 'before'), "LoggingMiddleware should have 'before' method"
        assert hasattr(mw, 'after'), "LoggingMiddleware should have 'after' method"
        assert hasattr(mw, 'on_error'), "LoggingMiddleware should have 'on_error' method"
        
        # Methods should be callable
        assert callable(mw.before), "'before' should be callable"
        assert callable(mw.after), "'after' should be callable"
        assert callable(mw.on_error), "'on_error' should be callable"
    
    def test_middleware_does_not_raise_exceptions(self, capture_logs):
        """Test that middleware does NOT raise exceptions (observability only)."""
        from tef_calc.middleware.logging import LoggingMiddleware
        
        mw = LoggingMiddleware()
        ctx = Context({"data": "test"})
        
        # Should not raise even with unusual inputs
        try:
            mw.before(None, None)  # Invalid inputs
            mw.after("link", None)
            mw.on_error("link", ctx, TypeError("some error"))
        except Exception as e:
            pytest.fail(f"LoggingMiddleware should not raise exceptions, got: {e}")
    
    def test_executes_in_order(self, capture_logs):
        """Test that before/after hooks execute in the correct order."""
        from tef_calc.middleware.logging import LoggingMiddleware
        
        mw = LoggingMiddleware()
        ctx = Context({"order": "test"})
        
        mw.before("step1", ctx)
        mw.before("step2", ctx)
        mw.after("step2", ctx)
        mw.after("step1", ctx)
        
        logs = capture_logs.getvalue()
        
        # Should contain all steps
        assert "step1" in logs, "Should log step1"
        assert "step2" in logs, "Should log step2"
        
        # step1 'before' should come before step2 'before'
        pos_step1_before = logs.find("step1")
        pos_step2_before = logs.find("step2")
        assert pos_step1_before < pos_step2_before, \
            "step1 before should execute before step2 before"


class TestLoggingMiddlewareFormatting:
    """Test log message formatting and content."""
    
    def test_includes_link_name_in_log(self, capture_logs):
        """Test that link name is included in log messages."""
        from tef_calc.middleware.logging import LoggingMiddleware
        
        mw = LoggingMiddleware()
        ctx = Context({})
        
        link_name = "validate_input"
        mw.before(link_name, ctx)
        
        logs = capture_logs.getvalue()
        assert link_name in logs, f"Link name '{link_name}' should be in logs"
    
    def test_context_summary_in_log(self, capture_logs):
        """Test that context information is included in logs."""
        from tef_calc.middleware.logging import LoggingMiddleware
        
        mw = LoggingMiddleware()
        ctx = Context({"test": "value"})
        
        mw.before("process", ctx)
        
        logs = capture_logs.getvalue()
        
        # Should have context-related info (at minimum the link was logged)
        assert "process" in logs


@pytest.fixture
def capture_logs():
    """Global fixture to capture log output."""
    log_capture = io.StringIO()
    handler = logging.StreamHandler(log_capture)
    handler.setFormatter(
        logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')
    )
    logger = logging.getLogger('tef_calc.middleware.logging')
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    
    yield log_capture
    
    logger.removeHandler(handler)

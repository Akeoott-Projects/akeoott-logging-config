import logging
import sys
from pathlib import Path

_DEFAULT_LOG_FORMAT = '%(levelname)s (%(asctime)s.%(msecs)03d)     %(message)s [Line: %(lineno)d in %(filename)s - %(funcName)s]'
_DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

class LogConfig:
    """
    A class to configure the logging for your python application.
    Allows activation, console output, and file saving for a specific logger instance.
    """
    def __init__(self, logger_name: str = "AkeoottLogger"):
        """
        Initializes the LogConfig instance for a specific logger.

        Args:
            logger_name (str):  A unique name for this logger.
                                If multiple LogConfig instances use the same name,
                                they will configure the same underlying logger.
                                Defaults to "AkeoottLogger".
        """
        self.logger = logging.getLogger(logger_name)
        self.logger.propagate = False

        # Add a NullHandler by default if no handlers are present.
        # This prevents "No handlers could be found for logger..." warnings
        # if the user doesn't configure logging for this specific logger.
        if not self.logger.handlers:
            self.logger.addHandler(logging.NullHandler())

        self._is_configured = False # Track if configuration has been applied

    def setup(self,
              activate_logging: bool = True,
              print_log: bool = True,
              save_log: bool = False,
              log_file_path: str | Path | None = None,
              log_file_name: str = "logs.log",
              log_level: int = logging.INFO,
              log_format: str = _DEFAULT_LOG_FORMAT,
              date_format: str = _DEFAULT_DATE_FORMAT,
              log_file_mode: str = 'a',
              thirdparty_logger_target: str | None = None,
              thirdparty_logger_level: int = logging.CRITICAL + 1,
        ):
        """
        Configures this specific logger instance.

        Args:
            activate_logging (bool): If True, logging is enabled. If False, logging is disabled.
            print_log (bool): If True, log messages are printed to the console.
            save_log (bool): If True, log messages are saved to a file.
            log_file_path (str | Path, optional): The path to the log file.
                                                  - If a directory, a default filename will be used.
                                                  - If 'script_dir', the log file will be placed next to the main script.
                                                  - If None and save_log is True, will use current program directory.
            log_file_name (str): The name of the log file.
            log_level (int): The minimum logging level to capture (logging.DEBUG, logging.INFO etc).
            log_format (str): The format string for log messages.
            date_format (str): The date/time format string.
            log_file_mode (str): Mode for opening the log file (a for append, w for overwrite).
            thirdparty_logger_target (str | None): Name of the targeted third-party logger.
            thirdparty_logger_level (int): Level to set (default disables all logging).
        """
        # Clear existing handlers so no duplicate logs if setup is called multiple times for some reason -_-
        self._clear_handlers()

        if not activate_logging:
            # If logging is explicitly deactivated, set level to beyond CRITICAL
            # and add a NullHandler for no logging output heh.
            self.logger.addHandler(logging.NullHandler())
            self.logger.setLevel(logging.CRITICAL + 1) # Disables all logging
            self._is_configured = True
            return

        self.logger.setLevel(log_level)
        formatter = logging.Formatter(log_format, datefmt=date_format)

        # Console Handler
        if print_log:
            console_handler = logging.StreamHandler(sys.stderr)
            console_handler.setLevel(log_level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            # Use self.logger to log its own config messages
            self.logger.info(f"[{self.logger.name}] Logging to console activated.")

        # File Handler
        if save_log:
            final_log_file_path = self._resolve_log_file_path(log_file_path, log_file_name)

            # Check that directory exists
            final_log_file_path.parent.mkdir(parents=True, exist_ok=True)

            try:
                file_handler = logging.FileHandler(final_log_file_path, mode=log_file_mode, encoding='utf-8')
                file_handler.setLevel(log_level)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
                # Use self.logger to log its own config messages
                self.logger.info(f"[{self.logger.name}] Logging to file '{final_log_file_path}' activated (mode: '{log_file_mode}').")
            except Exception as e:
                # Inform user via console if file logging fails (Hope its not my fault)
                self.logger.error(f"[{self.logger.name}] Failed to set up file logging to '{final_log_file_path}': {e}")
                if not print_log: # If console isn't already active, add a temporary one to report
                    temp_console_handler = logging.StreamHandler(sys.stderr)
                    temp_console_handler.setFormatter(formatter)
                    self.logger.addHandler(temp_console_handler)
                    self.logger.error(f"[{self.logger.name}] File logging failed, reverting to console for this message.")
                    self.logger.removeHandler(temp_console_handler)

        self.silence_thirdparty_loggers(thirdparty_logger_target, thirdparty_logger_level)

        self._is_configured = True
        self.logger.info(f"[{self.logger.name}] Logging configured. Level: {logging.getLevelName(log_level)}")


    def _clear_handlers(self):
        """Removes all handlers from this specific logger."""
        # Using list() to iterate over a copy, as removing handlers modifies the list
        for handler in list(self.logger.handlers):
            self.logger.removeHandler(handler)

    def _resolve_log_file_path(self, log_file_path, log_file_name):
        """Determines the final absolute path for the log file."""
        if log_file_path == 'script_dir':
            # Get the path of the main script that initiated the process
            if hasattr(sys.modules['__main__'], '__file__'):
                script_dir = Path(sys.modules['__main__'].__file__).parent  # type: ignore
                return script_dir / log_file_name
            else:
                # Fallback for interactive sessions
                self.logger.warning(
                    f"[{self.logger.name}] 'script_dir' logging requested but main script directory could not be determined. "
                    "Logging to current directory instead."
                )
                return Path.cwd() / log_file_name
        elif isinstance(log_file_path, (str, Path)):
            potential_path = Path(log_file_path)
            if potential_path.is_dir():
                return potential_path / log_file_name
            else:
                # Assume it's a full file path like "path/to/my_log.log"
                return potential_path
        else: # Default if save_log is True but no path is provided
            self.logger.info(f"[{self.logger.name}] No log_file_path provided, defaulting to current directory.")
            return Path.cwd() / log_file_name
        
    def silence_thirdparty_loggers(self, thirdparty_logger_target: str | None, thirdparty_logger_level: int):
        if not thirdparty_logger_target:
            return
        target_logger = logging.getLogger(thirdparty_logger_target)
        target_logger.setLevel(thirdparty_logger_level)
        for handler in list(target_logger.handlers):
            target_logger.removeHandler(handler)
        target_logger.addHandler(logging.NullHandler())
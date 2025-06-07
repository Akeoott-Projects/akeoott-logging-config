import logging
import sys
from pathlib import Path

_LOGGER_NAME = "LogConfig"

class LogConfig:
    """
    A class to configure the logging for your python application
    Allows activation, console output, and file saving.
    """
    def __init__(self):
        # Get the specific logger or whatever
        self.logger = logging.getLogger(_LOGGER_NAME)
        self.logger.propagate = False

        # Add a NullHandler by default cuz no one likes logs without requesting them.
        # So if the user doesn't configure logging, no messages will be displayed,
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
              log_format: str = '%(levelname)s (%(asctime)s) [Line: %(lineno)d in %(filename)s - %(funcName)s]: %(message)s',
              date_format: str = '%d/%m/%Y %I:%M:%S %p',
              log_file_mode: str = 'a' # Appending ofc
        ):
        """
        Configures the logging for the library.

        Args:
            activate_logging (bool): If True, logging is enabled. If False, logging is disabled.
            print_log (bool): If True, log messages are printed to the console.
            save_log (bool): If True, log messages are saved to a file.
            log_file_path (str | Path, optional): The path to the log file.
                - If a directory, a default filename will be used.
                - If 'script_dir', the log file will be placed next to the main script.
                - If None and save_log is True, will use current program directory.

            log_level (int): The minimum logging level to capture (logging.DEBUG, logging.INFO etc).
            log_format (str): The format string for log messages.
            date_format (str): The date/time format string.
            log_file_mode (str): Mode for opening the log file (a for append, w for overwrite).
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
            self.logger.info("Logging to console activated.")

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
                self.logger.info(f"Logging to file '{final_log_file_path}' activated (mode: '{log_file_mode}').")
            except Exception as e:
                # Inform user via console if file logging fails (Hope its not my fault)
                self.logger.error(f"Failed to set up file logging to '{final_log_file_path}': {e}")
                if not print_log: # If console isn't already active, add a temporary one to report
                    temp_console_handler = logging.StreamHandler(sys.stderr)
                    temp_console_handler.setFormatter(formatter)
                    self.logger.addHandler(temp_console_handler)
                    self.logger.error("File logging failed, reverting to console for this message.")
                    self.logger.removeHandler(temp_console_handler)


        self._is_configured = True
        self.logger.info(f"Library logging configured. Level: {logging.getLevelName(log_level)}")

    def _clear_handlers(self):
        """Removes all handlers from the logger."""
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
                    "'script_dir' logging requested but main script directory could not be determined. "
                    "Logging to current directory instead."
                )
                return Path.cwd() / log_file_name
        elif isinstance(log_file_path, (str, Path)):
            potential_path = Path(log_file_path)
            if potential_path.is_dir():
                return potential_path / log_file_name
            else:
                return potential_path
        else: # Default if save_log is True but no path is provided
            self.logger.info("No log_file_path provided, defaulting to current directory.")
            return Path.cwd() / log_file_name

# Now global instance for easy access
# Do `log_config = LogConfig()` and then call `log_config.setup()` from main application to configure. 
_log_config_instance = LogConfig()

def get_library_logger():
    """Returns the configured logger."""
    return _log_config_instance.logger

def setup_library_logging(
    activate_logging: bool = True,
    print_log: bool = True,
    save_log: bool = False,
    log_file_path: str | Path | None = None,
    log_file_name: str = "log",
    log_level: int = logging.INFO,
    log_format: str = '%(levelname)s (%(asctime)s) [Line: %(lineno)d in %(filename)s - %(funcName)s]: %(message)s',
    date_format: str = '%d/%m/%Y %I:%M:%S %p',
    log_file_mode: str = 'a'
):
    """
    Function to set up logging.
    This is the primary function users should call.
    """
    _log_config_instance.setup(
        activate_logging=activate_logging,
        print_log=print_log,
        save_log=save_log,
        log_file_path=log_file_path,
        log_file_name=log_file_name,
        log_level=log_level,
        log_format=log_format,
        date_format=date_format,
        log_file_mode=log_file_mode
    )
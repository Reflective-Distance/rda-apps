from functools import wraps
import os
from typing import Union, Dict, Optional, Any
from pathlib import Path
from dotenv import load_dotenv
import inspect


class EnvBuilder:
    """
    Builder for constructing environment variables from multiple sources.
    Allows step-by-step configuration file addition with control over override behavior.
    """

    def __init__(self):
        self._config_files = []

    def with_file(self, path: Union[str, Path], override: bool = True) -> "EnvBuilder":
        """
        Add a configuration file to the builder.

        Args:
            path: Path to the configuration file
            override: Whether this file should override existing values

        Returns:
            The builder instance for chaining
        """
        self._config_files.append((str(path), override))
        return self


    def with_defaults(self, base_dir: Optional[str] = None) -> "EnvBuilder":
        """
        Add default configuration files in standard locations.

        Args:
            base_dir: Base directory to look for files (defaults to PYTHONPATH or current directory)
                If PYTHONPATH contains multiple directories, each will be checked.

        Returns:
            The builder instance for chaining
        """
        if base_dir:
            # If base_dir is provided, use it directly
            base = base_dir
            return self.with_file(os.path.join(base, ".config"), override=True).with_file(
                os.path.join(base, ".env"), override=True
            )
        else:
            # Get PYTHONPATH
            pythonpath = os.getenv("PYTHONPATH", ".")

            # Split PYTHONPATH into individual directories
            path_separator = ";" if os.name == "nt" else ":"
            pythonpath_dirs = pythonpath.split(path_separator)

            # Start with the current builder instance
            builder = self

            # Process each directory in PYTHONPATH
            for path_dir in pythonpath_dirs:
                if path_dir.strip():  # Skip empty entries
                    base = os.path.abspath(path_dir.strip())

                    # Add config files with progressive overriding
                    config_path = os.path.join(base, ".config")
                    env_path = os.path.join(base, ".env")

                    # Add files if they exist
                    if os.path.exists(config_path):
                        builder = builder.with_file(config_path, override=True)
                    if os.path.exists(env_path):
                        builder = builder.with_file(env_path, override=True)

            return builder

    def with_config_class(self, config_class: Any) -> "EnvBuilder":
        """
        Add a configuration class to the builder.

        Args:
            config_class: Class or instance with configuration attributes

        Returns:
            The builder instance for chaining
        """
        self._config_class = config_class
        return self

    def build(self) -> Dict[str, str]:
        """
        Build the environment by loading all configured sources.

        Returns:
            Dictionary of all environment variables
        """
        # Load each file according to specified override behavior
        loaded_files = []

        for file_path, override in self._config_files:
            if os.path.exists(file_path):
                load_dotenv(dotenv_path=file_path, override=override)
                loaded_files.append(file_path)

        # Handle config class if provided
        if hasattr(self, "_config_class"):
            self._apply_config_class(self._config_class)

        debug = os.getenv("DEBUG", "false").lower() == "true"

        if debug:
            print(
                f"Environment built with {len(loaded_files)} files and {len(os.environ)} variables"
            )

        return dict(os.environ)

    def _apply_config_class(self, config_class: Any) -> None:
        """Apply a configuration class's attributes to environment variables."""
        # Handle both class and instance input
        if inspect.isclass(config_class):
            # Get class attributes
            attrs = {
                key: value
                for key, value in vars(config_class).items()
                if not key.startswith("_")
            }
        else:
            # Get instance attributes
            attrs = {
                key: value
                for key, value in vars(config_class).items()
                if not key.startswith("_")
            }

        # Add class attributes to environment
        applied = 0
        for key, value in attrs.items():
            if value is not None:  # Only set non-None values
                os.environ[key] = str(value)
                applied += 1


def require(*required_vars):
    """
    A decorator to ensure required environment variables are set.

    Args:
        *required_vars: A list of environment variable names to check.

    Raises:
        EnvironmentError: If any required environment variable is not set.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check if all required environment variables are set
            missing_vars = [var for var in required_vars if os.getenv(var) is None]
            if missing_vars:
                raise EnvironmentError(
                    f"Missing required environment variables: {', '.join(missing_vars)}"
                )
            # Call the original function
            return func(*args, **kwargs)

        return wrapper

    return decorator


def debug_mode() -> bool:
    """Check if the DEBUG flag is set in the environment."""
    return os.getenv("DEBUG", "false").lower() == "true"

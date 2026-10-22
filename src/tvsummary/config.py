"""Read the settings for the TV summary program from a TOML file."""

import tomllib
from dataclasses import dataclass
from pathlib import Path

from tvsummary.errors import SettingsError

DEFAULT_CONFIG_PATH = Path("config/tvsummary.toml")
LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


@dataclass(frozen=True)
class Settings:
    """Every setting the program reads, loaded from one TOML file."""

    source_url: str
    timeout: float
    output_dir: Path
    seed: int
    sample_size: int
    log_level: str


def load_settings(path: Path) -> Settings:
    """Read the settings file and return a Settings object."""
    try:
        with path.open("rb") as handle:
            data = tomllib.load(handle)
    except OSError as error:
        raise SettingsError(
            f"Cannot read the settings file {path}: {error.strerror}"
        ) from error
    except tomllib.TOMLDecodeError as error:
        raise SettingsError(f"{path} is not valid TOML: {error}") from error

    log_level = _read_text(data, "log_level", path).upper()

    if log_level not in LOG_LEVELS:
        raise SettingsError(
            f"log_level in {path} must be one of {', '.join(LOG_LEVELS)}."
        )

    return Settings(
        source_url=_read_text(data, "source_url", path),
        timeout=_read_positive_number(data, "timeout", path),
        output_dir=Path(_read_text(data, "output_dir", path)),
        seed=_read_whole_number(data, "seed", path),
        sample_size=_read_whole_number(data, "sample_size", path),
        log_level=log_level,
    )


def _read_value(data: dict[str, object], name: str, path: Path) -> object:
    """Return one setting, or raise SettingsError when it is missing."""
    if name not in data:
        raise SettingsError(f"{path} is missing the setting {name}.")

    return data[name]


def _read_text(data: dict[str, object], name: str, path: Path) -> str:
    """Return a setting that must be non-empty text."""
    value = _read_value(data, name, path)

    if not isinstance(value, str) or not value.strip():
        raise SettingsError(f"{name} in {path} must be non-empty text.")

    return value.strip()


def _read_whole_number(data: dict[str, object], name: str, path: Path) -> int:
    """Return a setting that must be a whole number of zero or more."""
    value = _read_value(data, name, path)

    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise SettingsError(f"{name} in {path} must be a whole number, 0 or more.")

    return value


def _read_positive_number(data: dict[str, object], name: str, path: Path) -> float:
    """Return a setting that must be a number above zero."""
    value = _read_value(data, name, path)

    if isinstance(value, bool) or not isinstance(value, int | float) or value <= 0:
        raise SettingsError(f"{name} in {path} must be a number above 0.")

    return float(value)

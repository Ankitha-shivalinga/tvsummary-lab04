import dataclasses

import pytest

from tvsummary.config import load_settings
from tvsummary.errors import SettingsError


def test_a_good_file_is_read_into_settings(settings_file):
    settings = load_settings(settings_file)

    assert settings.source_url == "https://example.invalid/shows"
    assert settings.timeout == 5.0
    assert settings.seed == 7
    assert settings.sample_size == 2
    assert settings.log_level == "DEBUG"


def test_settings_cannot_be_changed(settings_file):
    settings = load_settings(settings_file)

    with pytest.raises(dataclasses.FrozenInstanceError):
        settings.seed = 1


def test_a_missing_file_raises_a_settings_error(tmp_path):
    with pytest.raises(SettingsError, match="Cannot read the settings file"):
        load_settings(tmp_path / "none.toml")


def test_a_file_that_is_not_toml_raises_a_settings_error(tmp_path):
    path = tmp_path / "broken.toml"
    path.write_text("seed = = 4", encoding="utf-8")

    with pytest.raises(SettingsError, match="not valid TOML"):
        load_settings(path)


@pytest.mark.parametrize(
    "name", ["source_url", "timeout", "output_dir", "seed", "sample_size", "log_level"]
)
def test_an_incomplete_file_raises_a_settings_error(settings_file, name):
    lines = settings_file.read_text(encoding="utf-8").splitlines()
    kept = [line for line in lines if not line.startswith(f"{name} ")]
    settings_file.write_text("\n".join(kept), encoding="utf-8")

    with pytest.raises(SettingsError, match=f"missing the setting {name}"):
        load_settings(settings_file)


@pytest.mark.parametrize(
    ("old", "new", "message"),
    [
        ("seed = 7", 'seed = "seven"', "seed .* must be a whole number"),
        ("timeout = 5", "timeout = 0", "timeout .* must be a number above 0"),
        ('log_level = "DEBUG"', 'log_level = "LOUD"', "log_level .* must be one of"),
    ],
)
def test_a_bad_value_raises_a_settings_error(settings_file, old, new, message):
    text = settings_file.read_text(encoding="utf-8").replace(old, new)
    settings_file.write_text(text, encoding="utf-8")

    with pytest.raises(SettingsError, match=message):
        load_settings(settings_file)

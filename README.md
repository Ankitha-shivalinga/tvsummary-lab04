# TV Summary

Downloads the first page of shows from the TVMaze API and summarizes them: how many
shows there are, how many fall in each genre and premiere decade, and a short list
of featured shows picked with a fixed seed.

## Setup

```
conda env create -f environment.yml
conda activate tvsummary
pip install -r requirements.txt
pip install -e .
```

## Run

```
python -m tvsummary.main
python -m tvsummary.main --config config/tvsummary.toml
```

Run these from the repository root. The output goes to `data/processed/summary.json`
and `data/processed/run_info.json`.

## Check it

```
python -m ruff format --check .
python -m ruff check .
python -m mypy
python -m pytest
```

## Settings

All settings are in `config/tvsummary.toml`.

- `source_url`: the TVMaze page to download.
- `timeout`: seconds to wait for the API before giving up.
- `output_dir`: folder for `summary.json` and `run_info.json`, relative to where you run the program.
- `seed`: seed for the random generator that picks the featured shows.
- `sample_size`: how many featured shows to pick.
- `log_level`: lowest log level shown: DEBUG, INFO, WARNING, ERROR or CRITICAL.

## Errors and exit codes

| Error class | When it is raised | What the user sees |
|---|---|---|
| `SettingsError` | The settings file is missing, is not valid TOML, leaves out a setting, or has a value of the wrong type | `Error: Cannot read the settings file ...` or a line naming the bad setting |
| `SourceError` | The API cannot be reached, times out, or answers with an HTTP error | `Error: Could not reach ...` or `Error: ... answered with HTTP 503.` |
| `ResponseFormatError` | The response is not JSON, or is not a list of shows | `Error: The response from ... is not valid JSON.` or `Error: Expected a list of shows ...` |
| `ReportError` | The output files cannot be written | `Error: Cannot write ...` |

All four inherit from `TVSummaryError`, and only `main()` catches them. The error is
also logged at ERROR level, and no traceback is shown.

Exit code 0 means the run finished and both files were written. Exit code 1 means
one of the errors above stopped the run. Any other crash is a bug and shows a
traceback.

## Reproducing a run

The seed is in `config/tvsummary.toml`. Each run writes `run_info.json` next to
`summary.json`, recording every setting used, the Python version, and the versions
of requests, pytest, mypy and ruff.

To get exactly the same `featured_shows` list, a classmate needs the same seed and
sample size, the same Python version (random sampling can change between
versions), and the same shows from the API in the same order. The last one is not in
our control: if TVMaze changes page 0, the list can change even with the same seed.
`total_records` and the genre counts in `summary.json` show whether the input
changed.

## What the tests cover

- `ShowRecord` cleaning: missing or bad genres, a missing rating, and records that
  are not dictionaries.
- Both aggregations, using hand-made records, including skipped premiere dates and
  the warning that is logged for them.
- Reading the settings file, including a missing file, broken TOML, every missing
  setting and bad values.
- The seeded featured list: the same seed gives the same list, and seed 42 gives a
  known list.
- The download path with `requests.get` replaced by `monkeypatch`, for a network
  failure, an HTTP error and a non-JSON response.
- Writing `summary.json` and `run_info.json` into `tmp_path`.
- `main()`: exit code 1 and an `Error:` line for a missing settings file and a failed
  download, and exit code 0 for a successful run.

I chose not to test against the real TVMaze API. That test would fail whenever the
network or the API is down, and the data on page 0 can change, so it could not
check exact values anyway.

## Known limitations

- Only one page of shows (page 0) is downloaded.
- Paths in the settings file are relative to the folder the program is run from.
- `featured_shows` can only repeat if the API returns the same data.
- The rating is cleaned and stored on each record, but it is not used in the summary yet.
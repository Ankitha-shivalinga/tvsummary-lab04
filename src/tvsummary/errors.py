"""Errors that the tvsummary package raises on purpose."""


class TVSummaryError(Exception):
    """Base class for every error this package raises on purpose."""


class SourceError(TVSummaryError):
    """The show data could not be downloaded."""


class ResponseFormatError(TVSummaryError):
    """The downloaded data does not have the expected shape."""


class SettingsError(TVSummaryError):
    """The settings file is missing or unusable."""


class ReportError(TVSummaryError):
    """The summary files could not be written."""

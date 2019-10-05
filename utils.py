try:
    from .errors import CsvCreatorError
except ImportError:
    from errors import CsvCreatorError


def check_slice(key):
    if not isinstance(key, slice):
        raise CsvCreatorError(
            msg="Invalid argument. Use slicing",
            desc="Use [int:int:int] or replace some of them with Nones"
        )
    if not isinstance(key.start, int) and key.start is not None:
        raise CsvCreatorError(
            msg="First argument of slice is invalid",
            desc="Should be int or None"
        )
    if not isinstance(key.stop, int) and key.stop is not None:
        raise CsvCreatorError(
            msg="Middle argument of slice is invalid",
            desc="Should be int or None"
        )
    if not isinstance(key.step, int) and key.step is not None:
        raise CsvCreatorError(
            msg="Last argument of slice is invalid",
            desc="Should be int or None"
        )

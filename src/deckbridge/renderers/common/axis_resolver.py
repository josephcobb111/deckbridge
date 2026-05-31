"""Utility functions for resolving shared axis ranges for chart slides.

This module provides helper functions that inspect the data series used in
presentation slides and compute a shared numeric axis range used for
rendering charts. The computed range is padded by 5% on each side and
optionally rounded to a user‑specified granularity.

The public API is the ``resolve_shared_axis_ranges`` function.
"""

import math


def resolve_shared_axis_ranges(slide):  # pylint: disable=R1710
    """Return a shared ``(min, max)`` tuple for the value axis of *slide*.

    The *slide* dictionary may contain a ``"sync_value_axis"`` entry that
    controls how the axis range is derived:

    - ``None`` or a falsy value - No synchronization is requested; the
      function returns ``None``.
    - ``True`` - Synchronize the axis using the automatically computed range.
    - ``tuple`` - The caller supplies an explicit ``(min, max)`` tuple which is
      returned unchanged.
    - ``dict`` - Additional options can be provided. Currently the only
      supported option is ``"round_to"`` which specifies the granularity to
      which the bounds are rounded (default ``10``).

    When synchronization is enabled and the caller does not provide an
    explicit tuple, the function aggregates all numeric values from the chart
    objects present in the slide's ``"content"`` mapping. It then computes the
    minimum and maximum, adds a 5% padding, and rounds the bounds according to
    ``round_to``.

    Args:
        slide (dict): A slide definition containing a ``"content"`` mapping of
            blocks. Each block that has a ``chart`` attribute contributes its data
            series to the range calculation.

    Returns:
        tuple[float, float] | None: A ``(minimum, maximum)`` tuple for the
        shared axis, or ``None`` when no synchronization is required or the
        slide contains no numeric values.
    """
    sync = slide.get("sync_value_axis")

    # No synchronization requested – exit early.
    if not sync:
        return

    # ``True`` means “synchronize using defaults”. Convert to an empty dict to
    # simplify later handling.
    if sync is True:
        sync = {}

    # If the caller already supplied an explicit tuple, trust it.
    if isinstance(sync, tuple):
        return sync

    all_values = []

    # Collect numeric values from every chart in the slide.
    for block in slide["content"].values():
        if not hasattr(block, "chart"):
            continue

        chart = block.chart

        for series in chart.series:
            all_values.extend(chart.data[series["column"]])

    # If there are no values, we cannot compute a range.
    if not all_values:
        return

    min_val = min(all_values)
    max_val = max(all_values)

    # Pad the range by 5 % to give visual breathing room.
    padding = (max_val - min_val) * 0.05

    min_val -= padding
    max_val += padding

    # Round the bounds to a sensible granularity.
    round_to = sync.get("round_to", 10)

    min_val = math.floor(min_val / round_to) * round_to
    max_val = math.ceil(max_val / round_to) * round_to

    return (min_val, max_val)

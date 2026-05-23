import math


def resolve_shared_axis_ranges(slide):

    sync = slide.get("sync_value_axis")

    if not sync:
        return

    if sync is True:
        sync = {}

    if isinstance(sync, tuple):
        return sync
    else:
        all_values = []

        for block in slide["content"].values():
            if not hasattr(block, "chart"):
                continue

            chart = block.chart

            for series in chart.series:
                all_values.extend(chart.data[series["column"]])

        if not all_values:
            return

        min_val = min(all_values)
        max_val = max(all_values)

        padding = (max_val - min_val) * 0.05

        min_val -= padding
        max_val += padding

        round_to = sync.get("round_to", 10)

        min_val = math.floor(min_val / round_to) * round_to
        max_val = math.ceil(max_val / round_to) * round_to

    return (min_val, max_val)

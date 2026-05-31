def deep_merge(a, b):
    """Recursively merges two dictionaries.

    Creates a new dictionary that combines the mappings from ``a`` and ``b``.
    If a key exists in both dictionaries and the corresponding values are
    also dictionaries, the merge is performed recursively; otherwise the value
    from ``b`` overrides the one from ``a``.

    Args:
        a (dict): The base dictionary.
        b (dict): The dictionary whose values will be merged into ``a``.

    Returns:
        dict: A new dictionary containing the merged contents of ``a`` and ``b``.
    """
    result = dict(a)
    for k, v in b.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = deep_merge(result[k], v)
        else:
            result[k] = v
    return result

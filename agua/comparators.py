CHECK_FUNCTIONS = {}


def register(fn):
    CHECK_FUNCTIONS[fn.func_name] = fn
    return fn


@register
def exact(value, test_value):
    return value == test_value or value is test_value


@register
def approximate(value, test_value, delta):
    min_value = float(value) * (1 - delta)
    max_value = float(value) * (1 + delta)
    return min_value <= float(test_value) <= max_value


@register
def string_similarity(value, test_value, min_score, case_sensitive=True):
    import fuzzywuzzy.fuzz
    if not case_sensitive:
        value = value.lower()
        test_value = test_value.lower()
    return fuzzywuzzy.fuzz.ratio(value, test_value) >= min_score

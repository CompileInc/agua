import click
import csv

EMPTY_VALUES = (None, '', [], (), {})

def transform_to_dict(data, key, value):
    _data = {}
    for d in data:
        _data[d[key]] = d[value]
    return _data

def base_check(base_value, test_value):
    return base_value == test_value or base_value is test_value

def evaluate(base_data, test_data, check_function):
    _success = []
    _empty = []
    _error = []

    for k, v in test_data.items():
        base_value = base_data[k]
        if v in EMPTY_VALUES:
            _empty.append({k: v})
        elif check_function(base_value, v):
            _success.append({k: v})
        else:
            _error.append({k: v})
    return {'success': _success,
            'empty': _empty,
            'error': _error}

@click.command()
@click.option('--base', help='Base file to compare against')
@click.option('--test', help='Result file to evaluate')
@click.option('--key', default='id', help='Key')
@click.option('--value', default='value', help='Value')
@click.option('--func', help='Comparison function')
def test(base, test, key, value, func):
    with open(base) as f:
        base_data = transform_to_dict(csv.DictReader(f), key, value)
    with open(test) as f:
        test_data = transform_to_dict(csv.DictReader(f), key, value)

    if func in EMPTY_VALUES:
        check_function = base_check
    else:
        mods = func.split(".")
        func_name = mods[-1]
        mods = ".".join(mods[:-1])
        check_function = getattr(__import__(mods), func_name)

    result = evaluate(base_data, test_data, check_function)
    total = len(test_data)

    def get_result(key, result, total):
        return len(result[key])/float(total) * 100

    print "Total: %s" % (total)
    print "Success: %s%%" % (get_result('success', result, total))
    print "Empty: %s%%" % (get_result('empty', result, total))
    print "Error: %s%%" % (get_result('error', result, total))


if __name__ == '__main__':
    test()


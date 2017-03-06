from agua.utils import get_check_function
from agua.validators import EMPTY_VALUES


def evaluate(data, config):
    result = [None] * len(config)
    for i, c in enumerate(config):
        column = c['base_column']
        check_function = get_check_function(c['comparator'])
        kwargs = c.get('kwargs', {})
        test_column = c.get('test_column', 'test_%s' % column)
        result_column = 'agua_result_%s' % column
        column_result = {'attempted': 0, 'success': 0}
        separator = c.get('separator')
        for row in data:
            r = None
            if row[test_column] not in EMPTY_VALUES:
                column_result['attempted'] += 1
                test_value = row[test_column]
                if separator:
                    base_values = row[column].split(separator)
                else:
                    base_values = [row[column]]
                for base_value in base_values:
                    r = check_function(base_value, test_value, **kwargs)
                    if r:
                        break
                if r:
                    column_result['success'] += 1
            row[result_column] = r
        result[i] = column_result
    return {'data': data, 'result': result}

import importlib
import os

import click
import unicodecsv as csv
import yaml

from termgraph import chart

EMPTY_VALUES = (None, '', [], (), {})
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


def dyn_import(path):
    mods = path.split(".")
    func_name = mods[-1]
    mods = ".".join(mods[:-1])
    return getattr(importlib.import_module(mods), func_name)


def get_check_function(path):
    if path in CHECK_FUNCTIONS:
        return CHECK_FUNCTIONS[path]
    else:
        return dyn_import(path)


def as_percent(n, total):
    return '%.2f' % (float(n)/total * 100)

def label_width(string):
    return "%8s" % (string)


def evaluate(data, config):
    result = {}
    for column, c in config.items():
        check_function = get_check_function(c['comparator'])
        kwargs = c.get('kwargs', {})
        test_column = 'test_%s' % column
        result_column = 'result_%s' % column
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
        result[column] = column_result
    return {'data': data, 'result': result}


@click.group()
def cli():
    '''
    Compare data in columns with other columns with
    the help of comparator functions
    '''


@cli.command('list')
def list_commands():
    '''List built-in check functions'''
    click.echo('\n'.join(f for f in CHECK_FUNCTIONS))


@cli.command()
@click.option('--config', default="agua.yml", help='config for tests', required=True, metavar='<path>')
@click.option('--test', default="", help='file to evaluate', required=True, metavar='<path>')
@click.option('--update', help='update input file with results', default=True, is_flag=True)
@click.option('--format_result', help='output 1/0 instead of True/False in result', default=True, is_flag=True)
def test(config, test, update, format_result):
    '''Run tests'''

    with open(config) as f:
        config = yaml.load(f)
    fname = config.get('test')
    if test not in EMPTY_VALUES:
        fname = test
    config = config['config']
    with open(fname) as f:
        r = csv.DictReader(f)
        fieldnames = r.fieldnames
        data = list(r)

    result = evaluate(data, config)

    total = len(data)
    print("Test results for %s" % (fname))
    labels = [label_width('Total'), label_width('Coverage'), label_width('Accuracy')]
    args = {'width': 50, 'format': '{:>5.0f}', 'suffix': '%', 'verbose': False}

    for column, d in result['result'].items():
        column_str ='\033[1m%s\033[0m' % column
        print(column_str.center(args['width'], "="))
        data = [100, as_percent(d['attempted'], total), as_percent(d['success'], d['attempted'])]
        data = map(float, data)
        chart(labels, data, args)

    if update:
        updated_fieldnames = list(fieldnames)
        for column in config:
            result_column = 'result_%s' % column
            if result_column not in updated_fieldnames:
                updated_fieldnames.insert(updated_fieldnames.index('test_%s' % column) + 1, result_column)
        dirname = os.path.dirname(fname)
        basename = os.path.basename(fname)
        new_file = os.path.join(dirname, 'agua_result_%s' % basename)
        with open(new_file, 'w') as f:
            w = csv.DictWriter(f, fieldnames=updated_fieldnames)
            w.writeheader()
            for row in result['data']:
                if format_result:
                    for column in config:
                        result_column = 'result_%s' % column
                        row[result_column] = int(row[result_column]) if row[result_column] not in EMPTY_VALUES else None
                w.writerow(row)


if __name__ == '__main__':
    cli()

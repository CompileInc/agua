import click
import unicodecsv as csv
import yaml

from agua.comparators import CHECK_FUNCTIONS
from agua.evaluate import evaluate
from agua.termgraph import chart as termchart
from agua.utils import as_percent, label_width, get_result_filename
from agua.validators import EMPTY_VALUES


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

    try:
        with open(config) as f:
            config = yaml.load(f)
    except IOError:
        print("Missing config file: %s " % (config))
        exit()

    fname = config.get('test')
    if test not in EMPTY_VALUES:
        fname = test

    with open(fname) as f:
        r = csv.DictReader(f)
        fieldnames = r.fieldnames
        data = list(r)

    config = config['config']

    result = evaluate(data, config)

    total = len(data)
    print("Test results for %s" % (fname))
    args = {'width': 50, 'format': '{:>8.2f}', 'suffix': '%', 'verbose': False}

    for column, d in result['result'].items():
        print(label_width('Column') + ': ' + column)
        labels = [label_width('Coverage (%s/%s)' % (d['attempted'], total)),
                  label_width('Accuracy (%s/%s)' % (d['success'], d['attempted']))]
        data = [as_percent(d['attempted'], total),
                as_percent(d['success'], d['attempted'])]
        data = map(float, data)
        termchart(labels, data, args)

    if update:
        updated_fieldnames = list(fieldnames)

        for column, c in config.items():
            result_column = 'agua_result_%s' % column
            if result_column not in updated_fieldnames:
                test_column = c.get('test_column', 'test_%s' % column)
                updated_fieldnames.insert(
                    updated_fieldnames.index(test_column) + 1, result_column)

        new_file = get_result_filename(fname)
        with open(new_file, 'w') as f:
            w = csv.DictWriter(f, fieldnames=updated_fieldnames)
            w.writeheader()
            for row in result['data']:
                if format_result:
                    for column in config:
                        result_column = 'agua_result_%s' % column
                        row[result_column] = int(row[result_column]) if row[
                            result_column] not in EMPTY_VALUES else None
                w.writerow(row)


if __name__ == '__main__':
    cli()

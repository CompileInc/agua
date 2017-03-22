import fire
import unicodecsv as csv
import yaml

from agua.comparators import CHECK_FUNCTIONS
from agua.evaluate import evaluate
from agua.termgraph import chart as termchart
from agua.utils import as_percent, label_width, get_result_filename
from agua.validators import EMPTY_VALUES



class Agua(object):
    def list_commands(self):
        '''List built-in check functions'''
        print('\n'.join(f for f in CHECK_FUNCTIONS))


    def test(self, config="agua.yml",
             test="", update=True,
             format_result=True):
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

        for i, d in enumerate(result['result']):
            c = config[i]
            column = c['base_column']
            test_column = c.get('test_column', 'test_%s' % column)
            print(label_width('Column') + ': %s vs %s' % (column, test_column))
            labels = [label_width('Coverage (%s/%s)' % (d['attempted'], total)),
                      label_width('Accuracy (%s/%s)' % (d['success'], d['attempted']))]
            data = [as_percent(d['attempted'], total),
                    as_percent(d['success'], d['attempted'])]
            data = map(float, data)
            termchart(labels, data, args, max_limit=100)

        if update:
            updated_fieldnames = list(fieldnames)

            for c in config:
                column = c['base_column']
                test_column = c.get('test_column', 'test_%s' % column)
                if 'test_column' not in c:
                    c['test_column'] = test_column

                result_column = 'agua_result_%s' % test_column
                if result_column not in updated_fieldnames:
                    updated_fieldnames.insert(
                        updated_fieldnames.index(test_column) + 1, result_column)

            new_file = get_result_filename(fname)
            with open(new_file, 'w') as f:
                w = csv.DictWriter(f, fieldnames=updated_fieldnames)
                w.writeheader()
                for row in result['data']:
                    if format_result:
                        for c in config:
                            column = c['test_column']
                            result_column = 'agua_result_%s' % column
                            row[result_column] = int(row[result_column]) if row[
                                result_column] not in EMPTY_VALUES else None
                    w.writerow(row)

def cli():
    fire.Fire(Agua)

if __name__ == '__main__':
    cli()

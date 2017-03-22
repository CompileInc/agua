class AguaConfigException(Exception):
    pass

def clean_config(config):
    for c in config:
        if 'base_column' not in c:
            raise AguaConfigException("`base_column` missing for config %s" % c)

        if 'comparator' not in c:
            c['comparator'] = 'exact'

        if 'test_column' not in c:
            c['test_column'] = 'test_%s' % c['base_column']

    return config

def get_btr_columns(c):
    return c['base_column'], c['test_column'], 'agua_result_%s' % c['test_column']

![Agua](./logo.svg)
# Agua

A system that helps you test the coverage and accuracy of your data applications.

## Installation

```shell
pip install agua
```

## Example Usage

```shell
cd example
agua test
```

```shell
Test results for example.csv
        Column: name vs final_name
Coverage (3/4): ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇   75.00%
Accuracy (2/3): ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇   66.67%

        Column: age vs test_age
Coverage (4/4): ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇  100.00%
Accuracy (4/4): ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇  100.00%

        Column: fruit vs test_fruit
Coverage (4/4): ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇  100.00%
Accuracy (4/4): ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇  100.00%
```

## Configuration

Check out ```example/agua.yml``` for configuration options.

To compare columns, you may use one of the existing comparators or specify a python path to a callable.
Check out ```agua/comparators.py``` for example comparators.

List built-in comparators with,

```shell
agua list
```

Any keyword arguments that need to be passed to the comparator may be specified with a `kwargs` parameter


Graphs are printed with [termgraph](https://github.com/mkaz/termgraph)

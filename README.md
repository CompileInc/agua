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

## Configuration

Check out ```example/agua.yml``` for configuration options.

To compare columns, you may use one of the existing comparators or specify a python path to a callable.

List built-in comparators with,
```shell
agua list
```
Any keyword arguments that need to be passed to the comparator may be specified with a `kwargs` parameter
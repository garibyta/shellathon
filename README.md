# Shellathon CLI Usage Examples
Based on [example.py](https://github.com/garibyta/shellathon/blob/main/example.py) script.

## No Parameters Example

To run a function with no parameters:

```bash
$ python shellathon/core/run_func.py example.no_params
```

Output:

```
do nothing
```

For help on the command:

```bash
$ python shellathon/core/run_func.py example.no_params -h
```

Output:

```
usage: example.no_params [-h]

no doc

optional arguments:
  -h, --help  show this help message and exit
```

## Parameters Example

To run a function with parameters:

```bash
$ python shellathon/core/run_func.py example.with_params -h
```

Output:

```
usage: example.with_params [-h] --float_param FLOAT_PARAM 
                           [--str_param STR_PARAM] 
                           [--bool_param] 
                           [--with_default WITH_DEFAULT]

some useful doc

optional arguments:
  -h, --help            show this help message and exit
  --float_param FLOAT_PARAM   float param (default: 1.1)
  --str_param STR_PARAM       str param (default: foo)
  --bool_param                bool param (default: False)
  --with_default WITH_DEFAULT not required param (default: bla)
```

### Example with Invalid Float Parameter

```bash
$ python shellathon/core/run_func.py example.with_params --float_param str_instead_of_float
```

Output:

```
usage: example.with_params [-h] --float_param FLOAT_PARAM 
                           [--str_param STR_PARAM] 
                           [--bool_param] 
                           [--with_default WITH_DEFAULT]

example.with_params: error: argument --float_param: invalid float value: 'str_instead_of_float'
```

### Example with Additional Parameters

```bash
$ python shellathon/core/run_func.py example.with_params --float_param 8.6 --extra_param1 5 --extra_param2 bla
```

Output:

```
2024-08-04 20:18:21,690 MainProcess MainThread example INFO (x3) some message
2024-08-04 20:18:21,690 MainProcess MainThread example INFO {'bool_param': False,
2024-08-04 20:18:21,690 MainProcess MainThread example INFO [cont] 'float_param': 8.6,
2024-08-04 20:18:21,690 MainProcess MainThread example INFO [cont] 'str_param': 'foo',
2024-08-04 20:18:21,690 MainProcess MainThread example INFO [cont] 'with_default': 'bla'}
2024-08-04 20:18:21,690 MainProcess MainThread example INFO _rest: ['--extra_param1', '5', '--extra_param2', 'bla']
```

printful
========

### Printful API Client for Python 3

The Printful API client wrapper makes life a bit easier when working with the [API](https://www.theprintful.com/docs/index).
This is an update from the original Python 2.7 client library that was provided [here](https://www.theprintful.com/docs/libraries) .
THe module requires an API key as input.  The key can be generated in the store settings of your Printful account.


Quickstart
==========

```python
from printful import Printful
pf = Printful(key)
orders = pf.get('orders')
```

The Printful class extends the [Requests](http://docs.python-requests.org/en/latest/) library so data, param, json, etc. can be passed just as you would with requests.

```python
address = {
    'recipient': {
        'country_code': 'US',
        'state_code': 'CA'
    },
    'items': [
        {'variant_id': 1, 'quantity': 1},
        {'variant_id': 1118, 'quantity': 2}
    ]
}

pf.post('shipping/rates', json=address)
```

Or, retrieve only certain orders using `offset` and `limit`.

`pf.get('orders', params={'offset': 5, 'limit':10})`

is equivalent to ...

`pf.get('orders&offset=10&limit=5')`

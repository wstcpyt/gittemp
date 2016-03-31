from __future__ import absolute_import

import toolz

import typecheck
import fellow
from .data import test_json
import sklearn as sk
import dill

with open('./ml/city_model.pkl', 'rb') as f:
    citymodel = dill.load(f)
with open('./ml/latlong.pkl', 'rb') as f:
    latlongmodel = dill.load(f)
with open('./ml/cat_transform.pkl', 'rb') as f:
    cat_transform = dill.load(f)
with open('./ml/cat_model.pkl', 'rb') as f:
    cat_model = dill.load(f)
with open('./ml/tfidftransform.pkl', 'rb') as f:
    tfidftransform = dill.load(f)
with open('./ml/attribute_model.pkl', 'rb') as f:
    attribute_model = dill.load(f)
with open('./ml/attribute_transform.pkl', 'rb') as f:
    attribute_transform = dill.load(f)
    
def pick(whitelist, dicts):
    return [toolz.keyfilter(lambda k: k in whitelist, d)
            for d in dicts]

def exclude(blacklist, dicts):
    return [toolz.keyfilter(lambda k: k not in blacklist, d)
            for d in dicts]


@fellow.batch(name="ml.city_model")
@typecheck.test_cases(record=pick({"city"}, test_json))
@typecheck.returns("number")
def city_model(record):
    return citymodel.predict(record['city'])


@fellow.batch(name="ml.lat_long_model")
@typecheck.test_cases(record=pick({"longitude", "latitude"}, test_json))
@typecheck.returns("number")
def lat_long_model(record):
    la = record['latitude']
    lo = record['longitude']
    return latlongmodel.predict([la,lo])[0]


@fellow.batch(name="ml.category_model")
@typecheck.test_cases(record=pick({"categories"}, test_json))
@typecheck.returns("number")
def category_model(record):
    input_dict = record["categories"]
    input_dict = dict(zip(record["categories"],[1 for _ in range(len(input_dict))]))
    x = cat_transform.transform(input_dict)
    x = tfidftransform.transform(x)
    return cat_model.predict(x)[0]


@fellow.batch(name="ml.attribute_knn_model")
@typecheck.test_cases(record=pick({"attributes"}, test_json))
@typecheck.returns("number")
def attribute_knn_model(record):
    import collections
    def flatten(d, parent_key='', sep='_'):
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, collections.MutableMapping):
                items.extend(flatten(v, new_key, sep=sep).items())
            else:
                if isinstance(v, bool):
                    items.append((new_key, int(v)))
                elif isinstance(v, int):
                    items.append((new_key, v))
                else:
                    items.append((new_key + "_" + v, 1))
        return dict(items)
    flat_x = flatten(record["attributes"])
    transformed_x = attribute_transform(flat_x)
    return attribute_model.predict(transformed_x)[0]


@fellow.batch(name="ml.full_model")
@typecheck.test_cases(record=exclude({"stars"}, test_json))
@typecheck.returns("number")
def full_model(record):
    return 0

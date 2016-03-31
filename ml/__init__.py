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
with open('./ml/tfidfdict.pkl', 'rb') as f:
    tfidfdict = dill.load(f)

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
    def get_most_important(x):
        res = "null"
        largest = 0
        for word in x:
            if word not in tfidfdict:
                continue
            word = word.replace(" ","").replace("&","")
            word = word.replace("(","").replace(")","")
            word = word.replace("/","").replace("'","")
            word = word.replace(",","").replace("-","")
            word = word.lower()
            if tfidfdict[word] > largest:
                largest = tfidfdict[word]
                res = word
        return res
    print record
    recordlist = record["categories"]
    tfword = get_most_important(recordlist)
    x = cat_transform.transform({"cat":tfword})
    return cat_model.predict(x)[0]


@fellow.batch(name="ml.attribute_knn_model")
@typecheck.test_cases(record=pick({"attributes"}, test_json))
@typecheck.returns("number")
def attribute_knn_model(record):
    return 0


@fellow.batch(name="ml.full_model")
@typecheck.test_cases(record=exclude({"stars"}, test_json))
@typecheck.returns("number")
def full_model(record):
    return 0

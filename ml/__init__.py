from __future__ import absolute_import

import toolz

import typecheck
import fellow
from .data import test_json
from sklearn.externals import joblib
import sklearn as sk


def pick(whitelist, dicts):
    return [toolz.keyfilter(lambda k: k in whitelist, d)
            for d in dicts]

def exclude(blacklist, dicts):
    return [toolz.keyfilter(lambda k: k not in blacklist, d)
            for d in dicts]


@fellow.batch(name="ml.city_model")
@typecheck.test_cases(record=pick({"city"}, test_json))
@typecheck.returns("number")

# City Model Class
class City_model():
    def fit(self, city_df):
        self.city_grouped = df.groupby('city').agg({'stars':np.mean}).reset_index()
    def predict(self, name):
        return float(self.city_grouped[self.city_grouped.city==name].stars)
    
def city_model(record):
    model = joblib.load("./ml/model/city/city_model.pkl")
    return model.predict(record)


@fellow.batch(name="ml.lat_long_model")
@typecheck.test_cases(record=pick({"longitude", "latitude"}, test_json))
@typecheck.returns("number")
def lat_long_model(record):
    return 0


@fellow.batch(name="ml.category_model")
@typecheck.test_cases(record=pick({"categories"}, test_json))
@typecheck.returns("number")
def category_model(record):
    return 0


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

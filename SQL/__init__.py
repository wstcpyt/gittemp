# -*- coding: utf-8-*-
import fellow
import typecheck
import pickle

@fellow.app.task(name="sql.score_by_zipcode")
@typecheck.returns("92 * (string, number, number, count)")
def score_by_zipcode():
    with open('./SQL/zipcode.pickle', 'rb') as f:
        zipcode = pickle.load(f)
    return zipcode
@fellow.app.task(name="sql.score_by_map")
@typecheck.returns("string")
def score_by_map():
    # must be url of the form https://x.cartodb.com/...
    return "https://wstcpyt.cartodb.com/viz/5053f86a-f2c9-11e5-b66f-0ea31932ec1d/public_map"

@fellow.app.task(name="sql.score_by_borough")
@typecheck.returns("5 * (string, number, number, count)")
def score_by_borough():
    with open('./SQL/boro.pickle', 'rb') as f:
        boro = pickle.load(f)
    return boro

@fellow.app.task(name="sql.score_by_cuisine")
@typecheck.returns("75 * (string, number, number, count)")
def score_by_cuisine():
    with open('./SQL/cui.pickle', 'rb') as f:
        cuis = pickle.load(f)
        cuis[11] = ('Caf\xe9/Coffee/Tea'.decode('iso-8859-1'), 15.994683295044306, 0.10258473259987819, 15235)
    return cuis

@fellow.app.task(name="sql.violation_by_cuisine")
@typecheck.returns("20 * ((string, string), number, count)")
def violation_by_cuisine():
    with open('./SQL/vio.pickle', 'rb') as f:
        vio = pickle.load(f)
        for i in range(len(vio)):
            vio[i] = ((vio[i][0][0],vio[i][0][1].decode('iso-8859-1')),vio[i][1],vio[i][2])
    return vio

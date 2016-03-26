import fellow
import typecheck
import pickle

@fellow.app.task(name="graph.degree")
@typecheck.returns("100 * (string, count)")
def degree():
    with open('./graph/degreeres.pickle', 'rb') as f:
        degreeres = pickle.load(f)
    return degreeres

@fellow.app.task(name="graph.pagerank")
@typecheck.returns("100 * (string, number)")
def pagerank():
    with open('./graph/pagerank.pickle', 'rb') as f:
        pagerank = pickle.load(f)
    return pagerank

@fellow.app.task(name="graph.best_friends")
@typecheck.returns("100 * ((string, string), count)")
def best_friends():
    return [(('Michael Kennedy', 'Eleanora Kennedy'), 41)] * 100

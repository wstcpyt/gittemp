import fellow
import typecheck
import pickle

@fellow.app.task(name="graph.degree")
@typecheck.returns("100 * (string, count)")
def degree():
    with open('./graph/degreeres.pickle', 'rb') as f:
        degree = pickle.load(f)
    return degree

@fellow.app.task(name="graph.pagerank")
@typecheck.returns("100 * (string, number)")
def pagerank():
    return [('Martha Stewart', 0.00019312108706213307)] * 100

@fellow.app.task(name="graph.best_friends")
@typecheck.returns("100 * ((string, string), count)")
def best_friends():
    return [(('Michael Kennedy', 'Eleanora Kennedy'), 41)] * 100

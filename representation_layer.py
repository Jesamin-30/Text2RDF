# representation_layer.py
from rdflib import Graph, URIRef, Namespace
from config import EX_NAMESPACE

EX = Namespace(EX_NAMESPACE)


def build_rdf_graph(triples, entities, predicates):
    g = Graph()
    g.bind("ex", EX)

    for s, p, o in triples:
        try:
            # Local URIS
            s_LOCAL = s.replace(" ", "_")
            p_LOCAL = p.replace(" ", "_")
            o_LOCAL = o.replace(" ", "_")

            # URIs si están linkeadas
            s_uri = URIRef(entities.get(s, f"{EX_NAMESPACE}{s_LOCAL}"))
            p_uri = URIRef(predicates.get(p, f"{EX_NAMESPACE}{p_LOCAL}"))
            o_uri = URIRef(entities.get(o, f"{EX_NAMESPACE}{o_LOCAL}"))

            triple = (s_uri, p_uri, o_uri)
            g.add(triple)
        except Exception as e:
            print(f"Error en línea: {s, p, o} - {e}")
            continue

    return g

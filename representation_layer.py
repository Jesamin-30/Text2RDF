# representation_layer.py
from rdflib import Graph, URIRef, Namespace
from config import EX_NAMESPACE

EX = Namespace(EX_NAMESPACE)

def build_rdf_graph(triples, entity_links, predicate_mappings):
    g = Graph()
    g.bind("ex", EX)

    for line in triples:
        try:
            s, p, o = line.strip("()").split(",", 2)
            s = s.strip().strip('"').replace(" ", "_")
            p = p.strip().strip('"').replace(" ", "_")
            o = o.strip().strip('"').replace(" ", "_")

            # URIs si están linkeadas
            s_uri = URIRef(entity_links.get(s, f"{EX_NAMESPACE}{s}"))
            p_uri = URIRef(predicate_mappings.get(p, f"{EX_NAMESPACE}{p}"))
            o_uri = URIRef(entity_links.get(o, f"{EX_NAMESPACE}{o}"))

            g.add((s_uri, p_uri, o_uri))
        except Exception as e:
            print(f"Error en línea: {line} - {e}")
            continue

    return g

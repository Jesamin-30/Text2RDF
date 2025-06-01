# main.py
from data_layer import load_text, preprocess_text
from knowledge_extraction import extend_text_llm, extract_triplets_llm, entity_linking_dbpedia, predicate_mapping_lov
# from representation_layer import build_rdf_graph


def main():
    path = "document.txt"  # Cambia por tu archivo de resumen
    raw_text = load_text(path)

    # extend_text = extend_text_llm(raw_text)
    # sentences = preprocess_text(extend_text)
    # print(sentences)

    all_triples = []
    entity_mentions = set()
    predicates = set()

    # Extraer tripletas
    sentences = ['Marie Curie discovered radium and polonium.']
    for sent in sentences:
        raw_triples = extract_triplets_llm(sent)
        triples = raw_triples.splitlines()
        all_triples.extend(triples)
        for t in triples:
            try:
                s, p, o = t.strip("()").split(",", 2)
                s = s.strip().strip('"')
                p = p.strip().strip('"')
                o = o.strip().strip('"')
                entity_mentions.update([s, o])
                predicates.add(p)
            except:
                continue

    print(entity_mentions)
    # Entity linking y mapping semántico
    entity_links = {}
    for mention in entity_mentions:
        entity_links.update(entity_linking_dbpedia(mention))

    print(entity_links)
    """ predicate_mappings = {}
    for p in predicates:
        uri = predicate_mapping_lov(p)
        if uri:
            predicate_mappings[p] = uri

    # Grafo RDF
    g = build_rdf_graph(all_triples, entity_links, predicate_mappings)
    print(g.serialize(format="turtle")) """


if __name__ == "__main__":
    main()

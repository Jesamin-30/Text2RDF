# main.py
import sys
import argparse
from data_layer import load_text, preprocess_text
from knowledge_extraction import extend_text_llm, extract_triplets_llm, entity_linking_babelfy, predicate_mapping_lov
from representation_layer import build_rdf_graph


def main(path):
    name = path.rsplit("/", 1)[1]
    raw_text = load_text(path)

    extend_text = extend_text_llm(raw_text)
    print("raw_text:", raw_text)
    print("extend_text:", extend_text)
    sentences = preprocess_text(extend_text)

    all_triples = []
    entity_mentions = set()
    predicates = set()

    # Extraer tripletas
    # sentences = ['Marie Curie discovered radium and polonium.']
    print(sentences)
    for sent in sentences:
        raw_triples = extract_triplets_llm(sent)
        triples = raw_triples.splitlines()
        print(triples)
        for triple in triples:
            try:
                s, p, o = triple.strip("()").split(",", 2)
                s = s.strip().strip('"')
                p = p.strip().strip('"')
                o = o.strip().strip('"')

                entity_mentions.update([s, o])
                predicates.add(p)
                all_triples.append((s, p, o))
            except:
                continue

    print("entity_mentions: ", entity_mentions)
    print("predicates: ", predicates)

    # Entity linking y mapping semántico
    entity_links = {}
    for mention in entity_mentions:
        tmp = entity_linking_babelfy(mention)
        if tmp:
            entity_links[mention] = tmp

    predicate_mappings = {}
    for p in predicates:
        uri = predicate_mapping_lov(p)
        if uri:
            predicate_mappings[p] = uri

    # Grafo RDF
    print("\n")
    print("All triples", all_triples)
    print("Entity links", entity_links)
    print("Predicate mappings", predicate_mappings)

    output_name = "output/" + name.split(".")[0] + ".ttl"
    g = build_rdf_graph(all_triples, entity_links, predicate_mappings)
    print(g.serialize(format="turtle"))
    g.serialize(destination=output_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Text To RDF',
        description='Run program'
    )

    parser.add_argument('-file', action="store", default="data/doc.txt")
    args = parser.parse_args()
    filename = args.file

    main(filename)

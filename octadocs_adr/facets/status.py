from more_itertools import first
from octadocs.octiron import Octiron
from rdflib import URIRef


def status(octiron: Octiron, iri: URIRef):
    """Render ADR document status."""
    meta = first(
        octiron.query(
            '''
            SELECT * WHERE {
                ?status rdfs:label ?label .
                
                OPTIONAL {
                    ?status octa:symbol ?symbol .
                }
            } ORDER BY DESC(?symbol)
            ''',
            status=iri,
        ),
        None,
    )

    if not meta:
        return f'<em>[Cannot render status]</em> {iri}'

    label = meta['label']
    if symbol := meta.get('symbol'):
        label = f'{symbol} {label}'

    return label

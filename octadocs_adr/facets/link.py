from dominate.tags import a, code
from more_itertools import first
from octadocs.octiron import Octiron
from rdflib import URIRef


def link_to_adr(octiron: Octiron, iri: URIRef) -> a:
    """Link to an ADR document given by the IRI."""
    descriptions = octiron.query(
        '''
        SELECT * WHERE {
            ?page
                octa:url ?url ;
                octa:title ?label ;
                adr:number ?number .
            
            OPTIONAL {
                ?page adr:status / octa:symbol ?symbol .
            }
        } ORDER BY ?number LIMIT 1
        ''',
        page=iri,
    )
    location = first(descriptions, None)

    if not location:
        raise ValueError(f'Page not found by IRI: {iri}')

    number = location['number'].value
    readable_number = f'ADR{number:03}'

    if symbol := location.get('symbol'):
        readable_number = f'{symbol} {readable_number}'

    return a(
        code(readable_number),
        ' ',
        location['label'],
        href=location['url'],
    )

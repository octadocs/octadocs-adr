from octadocs.octiron import Octiron
from rdflib import URIRef
from dominate.tags import table, thead, tr, th, tbody, td, code


def build_table_row(status) -> tr:
    raw = str(status['status']).replace('local:', '')

    label = status['label']

    if symbol := status.get('symbol'):
        label = f'{symbol} {label}'

    return tr(
        td(code(raw)),
        td(label),
    )


def status_class(octiron: Octiron, iri: URIRef):
    """Visualize all available status values as a table."""
    choices = octiron.query(
        '''
        SELECT ?status ?label ?symbol WHERE {
            ?status
                a adr:Status ;
                rdfs:label ?label .
            
            OPTIONAL {
                ?status octa:symbol ?symbol .
            }
        } ORDER BY ?label
        '''
    )

    rows = map(build_table_row, choices)

    return table(
        thead(
            tr(
                th('Code'),
                th('Label'),
            )
        ),
        tbody(*rows)
    )

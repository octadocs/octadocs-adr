from octadocs.octiron import Octiron
from rdflib import URIRef
from dominate.tags import table, thead, tr, th, tbody, td, code, a


def build_table_row(status) -> tr:
    raw = str(status['status']).replace('local:', '')

    label = status['label']

    if symbol := status.get('symbol'):
        label = f'{symbol} {label}'

    defined_by_label = status.get('defined_by_label')

    if defined_by_url := status.get('defined_by_url'):
        defined_by = a(
            defined_by_label or defined_by_url,
            href=defined_by_url,
            target='_blank',
        )

    elif defined_by_label:
        defined_by = defined_by_label

    else:
        defined_by = code(status['defined_by_iri'])

    return tr(
        td(code(raw)),
        td(label),
        td(defined_by or '')
    )


def status_class(octiron: Octiron, iri: URIRef):
    """Visualize all available status values as a table."""
    choices = octiron.query(
        '''
        SELECT
            ?status ?label ?symbol
            ?defined_by_iri ?defined_by_url ?defined_by_label
        WHERE {
            ?status a adr:Status .

            GRAPH ?defined_by_iri {
                ?status rdfs:label ?label .

                OPTIONAL {
                   ?status octa:symbol ?symbol .
                }
            }
            
            OPTIONAL {
                ?defined_by_iri octa:url ?defined_by_url .
            }
            
            OPTIONAL {
                ?defined_by_iri rdfs:label ?defined_by_label .
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
                th('Defined By'),
            )
        ),
        tbody(*rows)
    )

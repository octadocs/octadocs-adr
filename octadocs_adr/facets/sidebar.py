import itertools
import operator

from octadocs.octiron import Octiron
from rdflib import URIRef


def retrieve_properties_by_page(octiron: Octiron, iri: URIRef):
    about_this_page = octiron.query(
        '''
        SELECT ?property ?value WHERE {
            ?page ?property ?value .

            ?property a adr:PageProperty .

            OPTIONAL {
                ?property octa:position ?explicit_position .
            }

            BIND(COALESCE(?explicit_position, 0) as ?position)
        } ORDER BY ?position ?property
        ''',
        page=iri,
    )

    groups = itertools.groupby(
        about_this_page,
        key=operator.itemgetter('property'),
    )

    return dict({
        grouper: list(map(
            operator.itemgetter('value'),
            group_items,
        ))
        for grouper, group_items in groups
    })


def page_sidebar(octiron: Octiron, iri: URIRef):
    """Draw list of all ADR documents."""
    properties_and_values = retrieve_properties_by_page(
        octiron=octiron,
        iri=iri,
    )

    for property_iri, property_values in properties_and_values.items():
        # FIXME this is THE problem. How do we customize rendering of a property
        ...

    return str(properties_and_values)

import itertools
import operator
from dataclasses import dataclass
from typing import List, Dict, Iterable

from documented import DocumentedError
from dominate.tags import ul, li, strong
from more_itertools import first
from octadocs.iolanta import render
from octadocs.octiron import Octiron
from rdflib import URIRef
from rdflib.term import Node

from octadocs_adr.models import ADR


def retrieve_properties_by_page(octiron: Octiron, iri: URIRef):
    about_this_page = octiron.query(
        '''
        SELECT ?property ?value WHERE {
            ?page ?property ?value .

            ?property a adr:ADRProperty .

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


def render_property_values(
    property_values: List[Node],
    octiron: Octiron,
) -> str:
    rendered_values = [
        render(
            node=property_value,
            octiron=octiron,
            environment=ADR.term('sidebar-property-value'),
        )
        for property_value in property_values
    ]

    if len(rendered_values) == 1:
        return rendered_values[0]

    return ul(*map(li, rendered_values))


def render_properties_and_values(
    properties_and_values: Dict[URIRef, List[Node]],
    octiron: Octiron,
) -> Iterable[li]:
    for property_iri, property_values in properties_and_values.items():
        rendered_property = render(
            node=property_iri,
            octiron=octiron,
            environment=ADR.term('sidebar-property'),
        )

        rendered_values = render_property_values(
            property_values=property_values,
            octiron=octiron,
        )

        yield li(
            rendered_property,
            rendered_values,
            cls='md-nav__item md-nav__link',
        )


def page_sidebar(octiron: Octiron, iri: URIRef):
    """Draw list of all ADR documents."""
    properties_and_values = retrieve_properties_by_page(
        octiron=octiron,
        iri=iri,
    )

    return '\n'.join(map(str, render_properties_and_values(
        properties_and_values=properties_and_values,
        octiron=octiron,
    )))


@dataclass
class PropertyNotRenderable(DocumentedError):
    """
    Cannot render property for ADR page.

        Property IRI: {self.iri}

    Please ensure that the property has a proper `rdfs:label` assigned to it.
    """

    iri: URIRef


def sidebar_property(octiron: Octiron, iri: URIRef) -> str:
    """Render name of the property of the ADR page."""
    rows = octiron.query(
        '''
        SELECT * WHERE {
            ?property rdfs:label ?label .
            
            OPTIONAL {
                ?property octa:symbol ?symbol .
            }
        } LIMIT 1
        ''',
        property=iri,
    )

    try:
        row = first(rows)
    except ValueError as err:
        raise PropertyNotRenderable(iri=iri) from err

    label = row['label']
    if symbol := row.get('symbol'):
        label = f'{symbol} {label}'

    return strong(f'{label}: ')

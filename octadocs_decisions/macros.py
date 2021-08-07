import itertools
import json
import operator
import pydoc
from dataclasses import dataclass
from functools import cached_property
from typing import Dict, List, Optional, Callable

from documented import DocumentedError
from dominate import tags
from mkdocs.structure.pages import Page
from more_itertools import first
from octadocs.octiron import Octiron
from rdflib import URIRef
from rdflib.term import Node, Literal
import logging

from urlpath import URL

from octadocs_decisions.facets.default import default

logger = logging.getLogger(__name__)


@dataclass
class FacetNotCallable(DocumentedError):
    """
    Python facet not callable.

      - Import path: {self.path}
      - Object imported: {self.facet}

    The imported Python object is not a callable and thus cannot be used as a
    facet.
    """

    path: str
    facet: object


def app_by_property(octiron: Octiron) -> Dict[URIRef, URIRef]:
    """Find apps connected to properties."""
    pairs = octiron.query(
        '''
        SELECT ?property ?app WHERE {
            ?property iolanta:app ?app .
            ?app iolanta:supports <https://adr.octadocs.io/sidebar> .
        }
        '''
    )
    return {
        row['property']: row['app']
        for row in pairs
    }


def find_facet_for(octiron: Octiron, node: Node) -> Optional[URIRef]:
    """
    Find the facet for the node in question.

    :param octiron: Octiron instance representing the graph.
    :param node: most commonly a URIRef.
    :return: IRI of the facet, if found.
    """
    choices = octiron.query(
        '''
        SELECT ?facet WHERE {
            ?node iolanta:app ?facet .
        }
        ''',
        node=node,
    )

    facets = map(operator.itemgetter('facet'), choices)
    return first(facets, None)


def resolve_facet(iri: URIRef) -> Callable[[Octiron, Node], str]:
    url = URL(str(iri))

    if url.scheme != 'python':
        raise Exception(
            'Octadocs only supports facets which are importable Python '
            'callables. The URLs of such facets must start with `python://`, '
            'which {url} does not comply to.'.format(
                url=url,
            )
        )

    facet = pydoc.locate(url.hostname)

    if not callable(facet):
        raise FacetNotCallable(
            path=url,
            facet=facet,
        )

    return facet


def render(octiron: Octiron, node: Node) -> str:
    """
    Given an IRI, render it on a MkDocs page.

    For that, find an appropriate facet and execute it.
    """
    facet_iri = find_facet_for(octiron=octiron, node=node)

    if facet_iri is None:
        # Fall back to the default facet.
        return default(octiron=octiron, node=node)

    facet = resolve_facet(facet_iri)
    return facet(octiron, node)


def default_property_facet(
    octiron: Octiron,
    property_iri: URIRef,
    property_values: List[Node],
) -> Optional[str]:
    """Default facet to render a property with its values."""
    label = first(
        map(
            operator.itemgetter('label'),
            octiron.query(
                '''
                SELECT ?label WHERE {
                    ?property rdfs:label ?label .
                } ORDER BY ?label LIMIT 1
                ''',
                property=property_iri,
            ),
        ),
        None,
    )

    if label is None:
        return

    if len(property_values) > 1:
        raise Exception('Too many values')

    property_value = property_values[0]

    if isinstance(property_value, Literal):
        return f'<strong>{label}</strong>: {property_value}'

    rendered_value = render(octiron=octiron, node=property_value)
    return f'<strong>{label}</strong>: {rendered_value}'


@dataclass
class DecisionContext:
    """Context for the Decision template."""

    page: Page
    octiron: Octiron

    @cached_property
    def iri(self) -> URIRef:
        """Retrieve the IRI of current page."""
        return self.page.iri

    @cached_property
    def status(self) -> str:
        status_choices = self.octiron.query('''
            SELECT ?label ?symbol WHERE {
                ?page decisions:status [
                    rdfs:label ?label ;
                    octa:symbol ?symbol
                ] .
            }
        ''', page=self.iri)

        if not status_choices:
            return ''

        elif len(status_choices) < 2:
            status, = status_choices
            label = status['label']
            symbol = status['symbol']
            return f'{symbol} {label}'

        raise ValueError(
            f'This page has too many status values: {status_choices}',
        )

    @cached_property
    def author(self):
        authors = self.octiron.query('''
            SELECT ?name ?url WHERE {
                ?page decisions:author [
                    schema:name ?name ;
                    schema:url ?url
                ] .
            }
        ''', page=self.iri)

        if not authors:
            return ''

        if len(authors) < 2:
            author, = authors

            dom = tags.li(
                tags.a(
                    tags.strong('Author: '),
                    author['name'],

                    cls='md-nav__link',
                    href=author['url'],
                    target='_blank',
                ),
                cls='md-nav__item',
            )

            return str(dom)

        raise ValueError('page has too many authors!')

    @cached_property
    def date(self) -> str:
        date_choice = self.octiron.query('''
            SELECT ?date WHERE {
                ?page decisions:date ?date .
            }
        ''', page=self.iri).first

        if not date_choice:
            return ''

        return date_choice['date'].value

    def describe_this_page(self) -> Dict[URIRef, List[Node]]:
        """List all properties of current page that can be rendered."""
        about_this_page = self.octiron.query(
            '''
            SELECT ?property ?value WHERE {
                ?page ?property ?value .
                
                ?property a decisions:PageProperty .

                OPTIONAL {
                    ?property octa:position ?explicit_position .
                }

                BIND(COALESCE(?explicit_position, 0) as ?position)
            } ORDER BY ?position ?property
            ''',
            page=self.page.iri,
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

    def page_properties(self):
        """Render page properties block."""
        properties_and_apps = app_by_property(self.octiron)
        properties_and_values = self.describe_this_page()

        for property_iri, property_values in properties_and_values.items():
            if attached_app_iri := properties_and_apps.get(property_iri):
                raise ValueError(f'Attached app: {attached_app_iri}')

            rendered_facet = default_property_facet(
                octiron=self.octiron,
                property_iri=property_iri,
                property_values=property_values,
            )

            yield f'<li class="md-nav__item md-nav__link">{rendered_facet}</li>'

    @property
    def render_page_properties(self):
        return '\n'.join(filter(None, self.page_properties()))

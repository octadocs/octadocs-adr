from dataclasses import dataclass
from functools import cached_property

from dominate import tags
from mkdocs.structure.pages import Page
from octadocs.octiron import Octiron
from rdflib import URIRef


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

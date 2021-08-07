from dataclasses import dataclass

from documented import DocumentedError
from more_itertools import first
from octadocs.octiron import Octiron
from rdflib import URIRef
from rdflib.term import Node
from urlpath import URL


@dataclass
class StatusNotFound(DocumentedError):
    """`{self.readable_status}` is not a valid ADR document status."""

    status: Node

    @property
    def readable_status(self) -> str:
        """Render status in a readable form."""
        url = URL(str(self.status))

        if url.scheme == 'local':
            return url.path

        return str(url)


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
        raise StatusNotFound(status=iri)

    label = meta['label']
    if symbol := meta.get('symbol'):
        label = f'{symbol} {label}'

    return label

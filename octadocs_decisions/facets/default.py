import operator

from more_itertools import first
from octadocs.octiron import Octiron
from rdflib.term import Node


def default(octiron: Octiron, node: Node) -> str:
    """
    Default facet to render an arbitrary object.

    Relies upon rdfs:label.
    """
    rows = octiron.query(
        'SELECT ?label WHERE { ?node rdfs:label ?label }',
        node=node,
    )

    labels = map(
        operator.itemgetter('label'),
        rows,
    )

    return first(labels, '[No Label]')

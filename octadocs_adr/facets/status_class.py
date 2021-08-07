from octadocs.octiron import Octiron
from rdflib import URIRef


def status_class(octiron: Octiron, iri: URIRef):
    """Visualize all available status values as a table."""
    rows = octiron.query(
        '''
        SELECT ?status ?label ?symbol WHERE {
            ?status
                a decisions:Status ;
                rdfs:label ?label .
            
            OPTIONAL {
                ?status octa:symbol ?symbol .
            }
        }
        '''
    )

    raise Exception(rows)

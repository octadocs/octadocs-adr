from pathlib import Path
from typing import Dict, Any

from mkdocs.plugins import BasePlugin
from mkdocs.structure.pages import Page
from octadocs.octiron.context_loaders import context_from_yaml
from octadocs.plugin import cached_octiron
from rdflib import Namespace, URIRef

from octadocs_adr.macros import DecisionContext

ADR = Namespace('https://adr.octadocs.io/')


class ADRPlugin(BasePlugin):
    """Decisions plugin automatically presents MkDocs pages as ADR documents."""

    @property
    def templates_path(self) -> Path:
        """Templates associated with the plugin."""
        return Path(__file__).parent / 'templates'

    def load_context(self):
        """Load YAML-LD context."""
        return context_from_yaml(Path(__file__).parent / 'yaml/ctx.yaml')

    def on_config(self, config, **kwargs):
        """Adjust configuration."""
        # Make plugin's templates available to MkDocs
        config['theme'].dirs.append(str(self.templates_path))

        named_context = self.load_context()

        try:
            contexts = config['extra']['named_contexts']
        except KeyError:
            contexts = config['extra']['named_contexts'] = {}

        contexts['decisions'] = named_context

        docs_dir = Path(config['docs_dir'])

        self.octiron = cached_octiron(
            docs_dir=docs_dir,
        )

        # Prefix
        self.octiron.graph.bind('adr', ADR)

        # Load the triples
        self.octiron.update_from_file(
            path=Path(__file__).parent / 'yaml/octadocs-adr.yaml',
            local_iri=URIRef(ADR),
            global_url='/octadocs-adr.yaml',
            named_contexts=config['extra']['named_contexts'],
        )

    def on_page_context(
        self,
        context: Dict[str, Any],
        page: Page,
        **kwargs,
    ):
        """Make custom functions available to the template."""
        context.update({
            'decision': DecisionContext(
                page=page,
                octiron=self.octiron,
            ),
            'adr': ADR,
        })

        return context

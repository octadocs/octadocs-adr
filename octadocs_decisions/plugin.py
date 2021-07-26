from pathlib import Path

from mkdocs.plugins import BasePlugin
from octadocs.octiron.context_loaders import context_from_yaml


class DecisionsPlugin(BasePlugin):
    """Decisions plugin automatically presents MkDocs pages as ADR documents."""

    @property
    def templates_path(self) -> Path:
        """Templates associated with the plugin."""
        return Path(__file__).parent / 'templates'

    def load_context(self):
        """Load YAML-LD context."""
        return context_from_yaml(Path(__file__).parent / 'yaml/context.yaml')

    def on_config(self, config, **kwargs):
        """Adjust configuration."""
        # Make plugin's templates available to MkDocs
        config['theme'].dirs.append(str(self.templates_path))

        named_context = self.load_context()
        try:
            contexts = config['extra']['named_contexts']
        except KeyError:
            contexts = config['extra']['named_contexts'] = {}

        contexts['octadocs_decisions'] = named_context

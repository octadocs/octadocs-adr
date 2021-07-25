from pathlib import Path

from mkdocs.plugins import BasePlugin


class DecisionsPlugin(BasePlugin):
    """Decisions plugin automatically presents MkDocs pages as ADR documents."""

    @property
    def templates_path(self) -> Path:
        """Templates associated with the plugin."""
        return Path(__file__).parent / 'templates'

    def on_config(self, config, **kwargs):
        """Make the plugin's templates available to MkDocs."""
        config['theme'].dirs.append(str(self.templates_path))

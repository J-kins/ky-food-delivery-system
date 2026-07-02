from renderers.aspose_renderer import BaseAsposeBuilder
import logging

log = logging.getLogger(__name__)

class InfluenceNetworkBuilder(BaseAsposeBuilder):
    def __init__(self, config):
        super().__init__(config)
        self.nodes = config.get("influence_network", {}).get("nodes", [])
        self.edges = config.get("influence_network", {}).get("edges", [])
        
    def build(self):
        log.debug(f"[dry-run] Building Influence Network ({len(self.nodes)} nodes, {len(self.edges)} edges)")

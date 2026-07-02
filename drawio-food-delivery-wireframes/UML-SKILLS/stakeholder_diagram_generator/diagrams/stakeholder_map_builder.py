from renderers.aspose_renderer import BaseAsposeBuilder
import logging

log = logging.getLogger(__name__)

class StakeholderMapBuilder(BaseAsposeBuilder):
    def __init__(self, config):
        super().__init__(config)
        self.map_data = config.get("stakeholder_map", {})
        
    def build(self):
        log.debug(f"[dry-run] Building Stakeholder Map (Concentric Rings)")

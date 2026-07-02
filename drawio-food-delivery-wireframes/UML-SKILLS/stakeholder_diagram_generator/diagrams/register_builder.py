from renderers.aspose_renderer import BaseAsposeBuilder
import logging

log = logging.getLogger(__name__)

class StakeholderRegisterBuilder(BaseAsposeBuilder):
    def __init__(self, config):
        super().__init__(config)
        self.stakeholders = config.get("stakeholder_register", {}).get("stakeholders", [])
        
    def build(self):
        log.debug(f"[dry-run] Building Stakeholder Register with {len(self.stakeholders)} stakeholders")
        for s in self.stakeholders:
            name = s.get('name', 'Unknown')
            strategy = s.get('engagement_strategy', 'auto')
            log.debug(f" - {name} ({strategy})")

from renderers.aspose_renderer import BaseAsposeBuilder
import logging

log = logging.getLogger(__name__)

class SalienceModelBuilder(BaseAsposeBuilder):
    def __init__(self, config):
        super().__init__(config)
        self.salience = config.get("salience_model", {})
        
    def build(self):
        log.debug(f"[dry-run] Building Salience Model")

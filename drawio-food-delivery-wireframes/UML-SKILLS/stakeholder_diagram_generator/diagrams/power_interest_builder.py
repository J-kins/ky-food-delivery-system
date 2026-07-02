from renderers.aspose_renderer import BaseAsposeBuilder
import logging

log = logging.getLogger(__name__)

class PowerInterestMatrixBuilder(BaseAsposeBuilder):
    def __init__(self, config, stakeholders=None):
        super().__init__(config)
        self.quadrants = config.get("power_interest_matrix", {}).get("quadrants", {})
        self.stakeholders = stakeholders or []
        
        # Populate from register if needed
        if self.stakeholders:
            self.matrix = self._generate_matrix_from_register()
        else:
            self.matrix = {
                'key_players': self.quadrants.get('key_players', {}).get('stakeholders', []),
                'keep_satisfied': self.quadrants.get('keep_satisfied', {}).get('stakeholders', []),
                'keep_informed': self.quadrants.get('keep_informed', {}).get('stakeholders', []),
                'monitor': self.quadrants.get('monitor', {}).get('stakeholders', []),
            }
            
    def _generate_matrix_from_register(self):
        matrix = {
            'key_players': [],
            'keep_satisfied': [],
            'keep_informed': [],
            'monitor': []
        }
        for s in self.stakeholders:
            power = s.get('power', 'Low')
            interest = s.get('interest', 'Low')
            
            if power == 'High' and interest == 'High':
                matrix['key_players'].append(s['id'])
            elif power == 'High' and interest in ['Medium', 'Low']:
                matrix['keep_satisfied'].append(s['id'])
            elif power in ['Medium', 'Low'] and interest == 'High':
                matrix['keep_informed'].append(s['id'])
            else:
                matrix['monitor'].append(s['id'])
        return matrix
        
    def build(self):
        log.debug(f"[dry-run] Building Power-Interest Matrix")
        log.debug(f" - Key Players: {self.matrix['key_players']}")
        log.debug(f" - Keep Satisfied: {self.matrix['keep_satisfied']}")
        log.debug(f" - Keep Informed: {self.matrix['keep_informed']}")
        log.debug(f" - Monitor: {self.matrix['monitor']}")

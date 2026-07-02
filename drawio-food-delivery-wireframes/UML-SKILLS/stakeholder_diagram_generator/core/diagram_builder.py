from typing import Dict, List, Optional
from renderers.aspose_renderer import Diagram, SaveFileFormat
from diagrams.register_builder import StakeholderRegisterBuilder
from diagrams.power_interest_builder import PowerInterestMatrixBuilder
from diagrams.influence_network_builder import InfluenceNetworkBuilder
from diagrams.salience_builder import SalienceModelBuilder
from diagrams.stakeholder_map_builder import StakeholderMapBuilder


class StakeholderDiagramBuilder:
    def __init__(self, config: Dict):
        self.config = config
        self.builders: Dict[str, object] = {}
        self._init_builders()

    def _init_builders(self) -> None:
        if "stakeholder_register" in self.config and self.config["stakeholder_register"]:
            self.builders["register"] = StakeholderRegisterBuilder(self.config)

        if "power_interest_matrix" in self.config and self.config["power_interest_matrix"]:
            register_builder = self.builders.get("register")
            stakeholders = (
                register_builder.stakeholders if register_builder else None
            )
            self.builders["power_interest"] = PowerInterestMatrixBuilder(
                self.config, stakeholders=stakeholders
            )

        if "influence_network" in self.config and self.config["influence_network"]:
            self.builders["influence"] = InfluenceNetworkBuilder(self.config)

        if "salience_model" in self.config and self.config["salience_model"]:
            self.builders["salience"] = SalienceModelBuilder(self.config)

        if "stakeholder_map" in self.config and self.config["stakeholder_map"]:
            self.builders["stakeholder_map"] = StakeholderMapBuilder(self.config)

    def build_all(self) -> None:
        for name, builder in self.builders.items():
            builder.build()

    def save_all(self, output_dir: str) -> None:
        import os
        file_map = {
            "register":       "01_stakeholder_register.vsdx",
            "power_interest": "02_power_interest_matrix.vsdx",
            "influence":      "03_influence_network.vsdx",
            "salience":       "04_salience_model.vsdx",
            "stakeholder_map":"05_stakeholder_map.vsdx",
        }
        for name, builder in self.builders.items():
            path = os.path.join(output_dir, file_map.get(name, f"{name}.vsdx"))
            builder.save(path)

    def save_combined(self, output_path: str) -> None:
        pass

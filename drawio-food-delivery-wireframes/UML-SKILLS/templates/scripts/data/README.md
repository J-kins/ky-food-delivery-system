# Data Template Converters Module

Converts data-driven SVG templates to Visio template files (.vstx) for database design, data architecture, and data pipeline documentation.

## Diagram Types

### 1. ERD Diagram (erd_diagram.py)
**Entity Relationship Diagram** - Logical relationships between business entities

```python
from data import ERDDiagramConverter

converter = ERDDiagramConverter(svg_path, json_data)
converter.convert_to_visio("output.vstx")
```

**Data Structure:**
- Entities with attributes
- 1:N, N:M relationships
- Primary/foreign key indicators
- Cardinality labels

### 2. Conceptual Data Model (data_model_conceptual.py)
**High-level business concepts** - No implementation details

```python
from data import ConceptualDataModelConverter

converter = ConceptualDataModelConverter(svg_path, json_data)
converter.convert_to_visio("output.vstx")
```

**Data Structure:**
- Business entities
- Entity relationships
- Business attributes
- No technical details

### 3. Logical Data Model (data_model_logical.py)
**Database tables and columns** - Implementation-agnostic

```python
from data import LogicalDataModelConverter

converter = LogicalDataModelConverter(svg_path, json_data)
converter.convert_to_visio("output.vstx")
```

**Data Structure:**
- Tables with columns
- Data types
- Primary/foreign keys
- Relationships and cardinality

### 4. Physical Data Model (data_model_physical.py)
**Database-specific implementation** - MySQL, PostgreSQL, Oracle, etc.

```python
from data import PhysicalDataModelConverter

converter = PhysicalDataModelConverter(svg_path, json_data)
converter.convert_to_visio("output.vstx")
```

**Data Structure:**
- Specific column types (BIGINT, VARCHAR, etc.)
- Storage engines
- Indexes and constraints
- Partitioning strategies
- Character sets and collations

### 5. Data Pipeline Architecture (data_pipeline.py)
**ETL data flow** - Sources to analytics

```python
from data import DataPipelineConverter

converter = DataPipelineConverter(svg_path, json_data)
converter.convert_to_visio("output.vstx")
```

**Data Structure:**
- Source systems (Database, APIs, Logs)
- Ingestion layer (Kafka, Kinesis, etc.)
- Processing layer (Spark, dbt)
- Storage layer (Data Lake, Warehouse)
- Analytics layer (BI tools, ML models)
- Dataflows between stages

### 6. Data Lakehouse Architecture (data_lakehouse.py)
**Unified data platform** - Delta Lake, Apache Iceberg

```python
from data import DataLakehouseConverter

converter = DataLakehouseConverter(svg_path, json_data)
converter.convert_to_visio("output.vstx")
```

**Data Structure:**
- Bronze Zone (Raw Data)
- Silver Zone (Cleaned/Deduplicated)
- Gold Zone (Business-Ready)
- Serving Layer (APIs, BI, ML)
- Technology stack metadata

## Usage Examples

### Single File Conversion
```bash
python main.py -i erd-diagram-dynamic.svg -o output.vstx
python main.py -i data-pipeline-architecture-dynamic.svg -o pipeline.vstx
python main.py -i data-lakehouse-architecture-dynamic.svg -o lakehouse.vstx
```

### Auto-Detection
```bash
# Automatically detects type from filename
python main.py -i data-model-physical-dynamic.svg -o output.vstx
```

### Batch Processing
```bash
python main.py --batch /path/to/data/templates --output-dir /path/to/vstx/output
```

### Verbose Logging
```bash
python main.py -i template.svg -o output.vstx -v
```

## JSON Data Format

All templates contain embedded JSON in `<script type="application/json">` tags.

### ERD Example
```json
{
  "diagramType": "Entity Relationship Diagram",
  "entities": [
    {
      "id": "users",
      "name": "Users",
      "attributes": ["user_id (PK)", "name", "email"],
      "position": {"x": 240, "y": 320}
    }
  ],
  "relationships": [
    {
      "from": "users",
      "to": "orders",
      "name": "places",
      "type": "one_to_many"
    }
  ]
}
```

### Data Model Example
```json
{
  "tables": [
    {
      "id": "users",
      "name": "users",
      "position": {"x": 240, "y": 300},
      "columns": [
        {"name": "user_id", "type": "BIGINT", "pk": true},
        {"name": "email", "type": "VARCHAR(255)", "unique": true}
      ]
    }
  ]
}
```

### Pipeline Example
```json
{
  "layers": [
    {
      "layer": "Source Systems",
      "components": [
        {
          "id": "src1",
          "name": "Production DB",
          "technology": "MySQL",
          "type": "source"
        }
      ]
    }
  ],
  "flows": [
    {"from": "src1", "to": "kafka"}
  ]
}
```

## Design Tokens

All templates support light/dark mode:

```json
"designTokens": {
  "lightMode": {
    "canvas": "#FFFFFF",
    "fill": "#E5E5E5",
    "stroke": "#1A1A1A"
  },
  "darkMode": {
    "canvas": "#0D0D0D",
    "fill": "#1E1E1E",
    "stroke": "#F2F2F2"
  }
}
```

## Visio Output Features

- **Shapes**: Entity boxes, relationship connectors, flow arrows
- **Styling**: Colors, stroke widths, text formatting (per design tokens)
- **Metadata**: Entity/table details, column types, technology names
- **Layout**: Positioned elements, aligned connectors, readable diagrams
- **Template Format**: .vstx allows reuse across projects

## Extending Converters

Create custom converter by extending `BaseDiagramConverter`:

```python
from base.diagram_converter import BaseDiagramConverter
from base.visio_builder import VisioBuilder

class CustomDataConverter(BaseDiagramConverter):
    def convert_to_visio(self, output_path):
        builder = VisioBuilder()
        page = builder.create_page("Custom Diagram")
        # Add your rendering logic
        builder.save_as_template(output_path)
        return output_path
```

Register in `main.py`:
```python
CONVERTER_REGISTRY = {
    "custom-diagram": CustomDataConverter,
}
```

## Testing

```bash
# Test single converters
python -m pytest tests/test_data_converters.py

# Test batch processing
python main.py --batch test/data/templates --output-dir test/output
```

## Troubleshooting

**Missing JSON data:** Ensure SVG contains valid JSON in `<script type="application/json">` tag
**Invalid positions:** Check x, y coordinates in position objects
**Type detection:** Filename must contain diagram type keyword (erd, logical, physical, pipeline, lakehouse)

## Performance Notes

- ERD with 50+ entities: ~2-3 seconds
- Physical models with detailed schemas: ~1-2 seconds
- Pipelines with 30+ components: ~2-3 seconds
- Lakehouse with metadata: ~1-2 seconds

## Dependencies

- python-pptx (for shape rendering)
- lxml (for SVG/XML parsing)
- zipfile (for .vstx packaging)

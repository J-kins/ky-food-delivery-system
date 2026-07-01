#!/usr/bin/env python3
"""
Generate JSON Schemas from KY Food Delivery Domain Entity Design Markdown
"""

import os
import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MD_FILE = ROOT.parent / "drawio-food-delivery-wireframes" / "KY_Food_Delivery_Domain_Entity_Design.md"
DEF_DIR = ROOT / "database" / "schema" / "definitions"
TYPES_DIR = ROOT / "database" / "schema" / "types"

def sql_to_json_type(sql_type):
    sql_type = sql_type.upper()
    if 'INT' in sql_type:
        return {"type": "integer"}
    elif 'REAL' in sql_type or 'DECIMAL' in sql_type or 'FLOAT' in sql_type or 'NUMERIC' in sql_type:
        return {"type": "number"}
    elif 'BOOL' in sql_type:
        return {"type": "boolean"}
    elif 'DATETIME' in sql_type or 'TIMESTAMP' in sql_type:
        return {"type": "string", "format": "date-time"}
    elif 'DATE' in sql_type:
        return {"type": "string", "format": "date"}
    elif 'TIME' in sql_type:
        return {"type": "string", "format": "time"}
    elif 'JSON' in sql_type:
        return {"type": ["object", "array", "null"]}
    else:
        return {"type": "string"}

def parse_markdown():
    with open(MD_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    entities = {}
    current_entity = None
    in_table = False

    for line in lines:
        line = line.strip()
        
        # Match Entity Header: ### Entity: `Roles` or ### Entity: Roles
        m = re.match(r'^###\s+Entity:\s+`?([A-Za-z0-9_]+)`?', line)
        if m:
            current_entity = m.group(1).lower()
            entities[current_entity] = {
                "title": current_entity,
                "type": "object",
                "properties": {},
                "required": []
            }
            in_table = False
            continue

        if current_entity:
            # Start of a table
            if line.startswith('| Attribute |'):
                in_table = True
                continue
            
            # Divider row
            if in_table and line.startswith('|---'):
                continue
            
            # End of table or blank line
            if in_table and not line.startswith('|'):
                in_table = False
                current_entity = None
                continue
                
            if in_table and line.startswith('|'):
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 5:
                    attr_name = parts[1].replace('`', '').strip()
                    sql_type = parts[2].strip()
                    constraints = parts[3].strip().upper()
                    description = parts[4].strip()
                    
                    if not attr_name:
                        continue
                        
                    schema_prop = sql_to_json_type(sql_type)
                    
                    # Check nullable vs not null
                    if 'NOT NULL' in constraints or 'PK' in constraints:
                        entities[current_entity]['required'].append(attr_name)
                    else:
                        # Allow null if not explicitly NOT NULL
                        if isinstance(schema_prop["type"], str):
                            schema_prop["type"] = [schema_prop["type"], "null"]
                        elif isinstance(schema_prop["type"], list) and "null" not in schema_prop["type"]:
                            schema_prop["type"].append("null")
                            
                    full_desc = []
                    if constraints:
                        full_desc.append(f"Constraints: {constraints}")
                    if description:
                        full_desc.append(description)
                        
                    if full_desc:
                        schema_prop["description"] = " | ".join(full_desc)
                        
                    entities[current_entity]['properties'][attr_name] = schema_prop

    return entities


def generate_schemas():
    DEF_DIR.mkdir(parents=True, exist_ok=True)
    TYPES_DIR.mkdir(parents=True, exist_ok=True)
    
    entities = parse_markdown()
    print(f"Found {len(entities)} entities.")
    
    for entity_name, schema in entities.items():
        # Ensure array is sorted / deduped
        schema['required'] = sorted(list(set(schema['required'])))
        if not schema['required']:
            del schema['required']
            
        final_schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            **schema
        }
        
        file_path = DEF_DIR / f"{entity_name}.json"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(final_schema, f, indent=2)
            
        print(f"Wrote {file_path}")

    # Generate basic types files
    with open(TYPES_DIR / "enums.json", 'w') as f:
        json.dump({
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "Global Enums",
            "type": "object",
            "properties": {
                "OrderStatus": {
                    "type": "string",
                    "enum": ["Pending", "Accepted", "Preparing", "Ready", "Out for Delivery", "Delivered", "Cancelled"]
                },
                "PaymentStatus": {
                    "type": "string",
                    "enum": ["Pending", "Completed", "Failed", "Refunded"]
                }
            }
        }, f, indent=2)

    with open(TYPES_DIR / "custom_types.json", 'w') as f:
        json.dump({
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "Custom Types",
            "type": "object",
            "properties": {
                "MonetaryAmount": {
                    "type": "number",
                    "description": "Monetary value represented as a float"
                }
            }
        }, f, indent=2)


if __name__ == "__main__":
    generate_schemas()

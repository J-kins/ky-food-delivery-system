# Dashboard Header Files - Visio Parser API

## Overview

This directory contains the complete C API for parsing Visio (.vsdx) files and converting them to JSON. The API is organized into 5 modular headers that work together to provide a complete diagram parsing and serialization system.

## Header Files

### 1. `config.h` - Configuration & Constants
- Feature flags (enable/disable parsing features)
- Memory limits (max shapes, connectors, pages)
- Buffer sizes for strings
- Allocation strategy (growth factors)

**Key Defines:**
- `MAX_SHAPES_PER_PAGE` - Maximum shapes on one page
- `MAX_PAGES` - Maximum pages in document
- `ENABLE_PROPERTY_EXTRACTION` - Extract visual properties
- `ENABLE_HIERARCHY_SUPPORT` - Support nested shapes

### 2. `errors.h` - Error Handling
- Standardized error codes
- Error context and reporting
- Error convenience macros

**Key Functions:**
- `error_get_last()` - Get last error
- `error_set()` - Set error with code and message
- `error_print()` - Print error to stderr
- `ERROR_SET()` macro - Quick error setting

**Error Codes:**
```c
VISIO_OK                      // No error
VISIO_ERR_FILE_NOT_FOUND      // File missing
VISIO_ERR_INVALID_FILE        // Not a valid .vsdx
VISIO_ERR_PARSE_FAILED        // Parse failure
VISIO_ERR_MEMORY_ALLOCATION   // Out of memory
VISIO_ERR_LIBVISIO_FAILED     // libvisio error
VISIO_ERR_JSON_GENERATION     // JSON export error
VISIO_ERR_INVALID_ARGUMENT    // Bad function args
```

### 3. `types.h` - Core Data Structures
- Shape, Connector, Page structures
- Property lists for attributes
- Document hierarchy
- Memory management functions

**Key Structures:**
```c
typedef struct {
  double x, y;
} Point;

typedef struct {
  double width, height;
} Size;

typedef struct {
  char *id;
  char *text;
  Point position;
  Size size;
  char *type;              // "rectangle", "circle", etc.
  char *parent_id;        // For hierarchy
  PropertyList *properties;
  char **children_ids;
} Shape;

typedef struct {
  char *id;
  char *from_shape_id;
  char *to_shape_id;
  char *text;            // Label
  PropertyList *properties;
} Connector;

typedef struct {
  char *name;
  char *id;
  Shape **shapes;
  Connector **connectors;
} Page;

typedef struct {
  char *filename;
  Page **pages;
} VisioDocument;
```

**Key Functions:**
- `property_list_create()` / `property_list_free()`
- `shape_create()` / `shape_free()`
- `connector_create()` / `connector_free()`
- `page_create()` / `page_free()`
- `document_create()` / `document_free()`

### 4. `visio_parser.h` - Main Parser API
- Parse .vsdx files
- Query shapes, connectors, pages
- Find shapes by ID, type, property, text
- Extract hierarchy relationships
- Find connections between shapes

**Key Functions:**

**Parsing:**
```c
VisioDocument* visio_parser_parse(const char *filepath);
```

**Page Queries:**
```c
Page** visio_parser_get_pages(VisioDocument *doc, size_t *count);
Page* visio_parser_find_page(VisioDocument *doc, const char *page_name);
```

**Shape Queries:**
```c
Shape** visio_parser_get_shapes(Page *page, size_t *count);
Shape* visio_parser_find_shape(VisioDocument *doc, const char *shape_id);
Shape** visio_parser_find_shapes_by_type(VisioDocument *doc, const char *type, size_t *count);
Shape** visio_parser_find_shapes_by_text(VisioDocument *doc, const char *text, size_t *count);
Shape** visio_parser_find_shapes_by_property(VisioDocument *doc, const char *prop_name, const char *value, size_t *count);
```

**Hierarchy:**
```c
Shape* visio_parser_get_parent(VisioDocument *doc, Shape *shape);
Shape** visio_parser_get_children(VisioDocument *doc, Shape *shape, size_t *count);
int visio_parser_is_nested(VisioDocument *doc, Shape *container, Shape *shape);
```

**Connectors:**
```c
Connector** visio_parser_get_connectors(Page *page, size_t *count);
Connector** visio_parser_get_outgoing_connectors(VisioDocument *doc, Shape *shape, size_t *count);
Connector** visio_parser_get_incoming_connectors(VisioDocument *doc, Shape *shape, size_t *count);
int visio_parser_is_connected(VisioDocument *doc, Shape *shape1, Shape *shape2);
```

**Statistics:**
```c
size_t visio_parser_shape_count(VisioDocument *doc);
size_t visio_parser_connector_count(VisioDocument *doc);
size_t visio_parser_page_count(VisioDocument *doc);
```

### 5. `json_exporter.h` - JSON Serialization
- Convert VisioDocument to JSON
- Export to string, file, or stream
- Configure output format
- Control what's included (properties, hierarchy, metadata)

**Key Functions:**
```c
char* json_exporter_document(VisioDocument *doc);
int json_exporter_to_file(VisioDocument *doc, const char *filepath);
int json_exporter_to_stream(VisioDocument *doc, FILE *stream);

char* json_exporter_page(Page *page);
char* json_exporter_shape(Shape *shape);
char* json_exporter_connector(Connector *connector);
```

**Configuration:**
```c
void json_exporter_set_pretty_print(int enabled);
void json_exporter_set_indent_size(int spaces);
void json_exporter_set_include_properties(int enabled);
void json_exporter_set_include_hierarchy(int enabled);
void json_exporter_set_include_metadata(int enabled);
```

## Usage Examples

### Basic Parse and Export
```c
#include "dashboard/visio_parser.h"
#include "dashboard/json_exporter.h"
#include "dashboard/errors.h"

int main(int argc, char *argv[]) {
    // Parse Visio file
    VisioDocument *doc = visio_parser_parse("diagram.vsdx");
    if (!doc) {
        error_print();
        return 1;
    }
    
    // Export to JSON file
    if (json_exporter_to_file(doc, "output.json") < 0) {
        error_print();
        return 1;
    }
    
    printf("Exported %zu pages, %zu shapes\n",
           visio_parser_page_count(doc),
           visio_parser_shape_count(doc));
    
    document_free(doc);
    return 0;
}
```

### Find Specific Shapes
```c
// Find all rectangles
size_t count;
Shape **rectangles = visio_parser_find_shapes_by_type(doc, "rectangle", &count);
printf("Found %zu rectangles\n", count);
for (size_t i = 0; i < count; i++) {
    printf("  - %s at (%.0f, %.0f)\n", 
           rectangles[i]->text,
           rectangles[i]->position.x,
           rectangles[i]->position.y);
}
visio_parser_free_shape_array(rectangles, count);
```

### Find Connections
```c
// Find what connects from a shape
Shape *start = visio_parser_find_shape(doc, "shape1");
if (start) {
    size_t conn_count;
    Connector **outgoing = visio_parser_get_outgoing_connectors(doc, start, &conn_count);
    
    for (size_t i = 0; i < conn_count; i++) {
        Shape *target = visio_parser_find_shape(doc, outgoing[i]->to_shape_id);
        printf("Connects to: %s\n", target->text);
    }
    
    visio_parser_free_connector_array(outgoing, conn_count);
}
```

### Hierarchy Navigation
```c
// Get children of a shape
Shape *parent = visio_parser_find_shape(doc, "container");
if (parent) {
    size_t child_count;
    Shape **children = visio_parser_get_children(doc, parent, &child_count);
    
    printf("Container has %zu children:\n", child_count);
    for (size_t i = 0; i < child_count; i++) {
        printf("  - %s\n", children[i]->text);
    }
    
    visio_parser_free_shape_array(children, child_count);
}
```

### Custom JSON Output
```c
// Configure JSON export
json_exporter_set_pretty_print(1);
json_exporter_set_indent_size(4);
json_exporter_set_include_properties(1);
json_exporter_set_include_hierarchy(1);

char *json = json_exporter_document(doc);
if (json) {
    printf("%s\n", json);
    free(json);
}
```

## Memory Management

All allocation is handled by the library:
- Use `document_free()` to release entire document
- Use `visio_parser_free_shape_array()` for shape search results
- Use `visio_parser_free_connector_array()` for connector search results
- All other structures are freed with document

## Error Handling

Always check for NULL returns and use error functions:
```c
VisioDocument *doc = visio_parser_parse("file.vsdx");
if (!doc) {
    VisioError *err = error_get_last();
    fprintf(stderr, "Error: %s\n", err->message);
    error_print();
    return 1;
}
```

## Dependencies

**Required Libraries:**
- `libvisio2` - Visio file format support
- `json-c` - JSON serialization
- Standard C library (C99 or later)

**Optional:**
- libxml2 (used by libvisio2)

## Building

See parent directory CMakeLists.txt for build configuration.

Example compilation:
```bash
gcc -I. -c src/types.c -o build/types.o
gcc -I. -c src/errors.c -o build/errors.o
gcc -I. -c src/visio_parser.c -o build/visio_parser.o -lvisio2 -lxml2
gcc -I. -c src/json_exporter.c -o build/json_exporter.o -ljson-c
gcc -I. -c src/main.c -o build/main.o
gcc build/*.o -o visio_parser -lvisio2 -lxml2 -ljson-c
```

## Architecture Notes

The header structure is organized by responsibility:
- **config.h** - Static configuration
- **errors.h** - Error handling (side effect: sets global error state)
- **types.h** - Pure data structures and memory management
- **visio_parser.h** - Parser interface (reads files, queries data)
- **json_exporter.h** - Export interface (converts to JSON)

Each module is self-contained but can depend on previous modules.

## Feature Support

- ✅ Parse .vsdx files (via libvisio2)
- ✅ Extract shapes with positions, sizes, text
- ✅ Extract properties (colors, fonts, styles)
- ✅ Extract connectors/relationships
- ✅ Multi-page support
- ✅ Hierarchical shapes (nested groups)
- ✅ Shape type detection
- ✅ Powerful search/query API
- ✅ JSON export with configuration
- ✅ Comprehensive error handling

## Next Steps

Implementation files in `src/` directory:
- `src/types.c` - Data structure implementation
- `src/errors.c` - Error handling implementation
- `src/visio_parser.c` - Parser using libvisio2
- `src/json_exporter.c` - JSON serialization using json-c
- `src/main.c` - Command-line tool entry point

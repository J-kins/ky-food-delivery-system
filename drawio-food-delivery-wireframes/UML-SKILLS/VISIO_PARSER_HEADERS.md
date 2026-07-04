# Visio Parser - Header Files Implementation

**Date Created**: 2026-07-04  
**Status**: ✅ Headers Complete - Ready for Implementation  
**Total Header Size**: 1,486 lines of well-documented C API

---

## Quick Summary

Created a complete C API for parsing Visio (.vsdx) files and exporting to JSON. All headers are in place with comprehensive documentation, ready for implementation.

### What Was Built

```
include/dashboard/
├── config.h          - Configuration & feature flags
├── errors.h          - Error handling system
├── types.h           - Core data structures
├── visio_parser.h    - Main parser API
├── json_exporter.h   - JSON export
└── README.md         - Complete documentation
```

---

## Header File Details

### 1. `config.h` (59 lines)
Defines all configurable constants for the system.

**Key Defines:**
- Memory limits: `MAX_SHAPES_PER_PAGE`, `MAX_PAGES`, `MAX_CONNECTORS_PER_PAGE`
- Buffer sizes: `MAX_ID_LENGTH`, `MAX_TEXT_LENGTH`, `MAX_PROPERTY_VALUE_LENGTH`
- Feature flags: `ENABLE_PROPERTY_EXTRACTION`, `ENABLE_HIERARCHY_SUPPORT`, `ENABLE_MULTIPAGE_SUPPORT`
- Growth factors for dynamic arrays: `GROWTH_FACTOR = 1.5`

**When to use:** When adjusting memory constraints or disabling features.

---

### 2. `errors.h` (119 lines)
Comprehensive error handling with standardized error codes.

**Error Codes (10 total):**
- `VISIO_OK` - Success
- `VISIO_ERR_FILE_NOT_FOUND` - File missing
- `VISIO_ERR_INVALID_FILE` - Not a valid .vsdx
- `VISIO_ERR_PARSE_FAILED` - Parsing error
- `VISIO_ERR_MEMORY_ALLOCATION` - Out of memory
- `VISIO_ERR_LIBVISIO_FAILED` - libvisio error
- `VISIO_ERR_JSON_GENERATION` - JSON export error
- `VISIO_ERR_INVALID_ARGUMENT` - Bad arguments
- `VISIO_ERR_FILE_IO` - File I/O error
- `VISIO_ERR_INTERNAL` - Internal parser error

**Key Functions:**
- `error_get_last()` - Get last error
- `error_set()` - Set error
- `error_print()` - Print to stderr
- `ERROR_SET()` macro - Quick setting

**Convenience Macros:**
```c
#define ERROR_SET(code, msg) \
    error_set(code, msg, __func__, __LINE__)

#define ERROR_SET_CONTEXT(code, msg, ctx) \
    error_set_with_context(code, msg, ctx, __func__, __LINE__)
```

---

### 3. `types.h` (349 lines)
Core data structures representing Visio documents.

**Main Structures:**

**Point** - 2D Coordinate
```c
typedef struct {
    double x;
    double y;
} Point;
```

**Size** - 2D Dimensions
```c
typedef struct {
    double width;
    double height;
} Size;
```

**Property** - Single attribute
```c
typedef struct {
    char *name;   // "color", "font", etc.
    char *value;  // Attribute value
} Property;
```

**PropertyList** - Dynamic property array
```c
typedef struct {
    Property *items;
    size_t count;
    size_t capacity;  // For dynamic growth
} PropertyList;
```

**Shape** - Diagram shape/object
```c
typedef struct Shape {
    char *id;           // Unique ID
    char *text;         // Text content
    Point position;     // x, y
    Size size;          // width, height
    char *type;         // "rectangle", "circle", etc.
    char *parent_id;    // For hierarchy
    PropertyList *properties;
    char **children_ids;     // Child IDs
    size_t children_count;
    uint32_t page_index;
    int is_group;       // 1 if group, 0 otherwise
} Shape;
```

**Connector** - Connection between shapes
```c
typedef struct Connector {
    char *id;
    char *from_shape_id;  // Source
    char *to_shape_id;    // Target
    char *text;           // Label
    PropertyList *properties;
    uint32_t page_index;
} Connector;
```

**Page** - Diagram page
```c
typedef struct Page {
    char *name;
    char *id;
    Shape **shapes;
    size_t shapes_count;
    size_t shapes_capacity;
    Connector **connectors;
    size_t connectors_count;
    size_t connectors_capacity;
    uint32_t page_index;
} Page;
```

**VisioDocument** - Complete document
```c
typedef struct VisioDocument {
    char *filename;
    Page **pages;
    size_t pages_count;
    size_t pages_capacity;
    char *creator;
    char *created;
    char *modified;
} VisioDocument;
```

**Key Functions (20+ memory management):**
- Property list: `property_list_create()`, `property_list_add()`, `property_list_get()`, `property_list_free()`
- Shapes: `shape_create()`, `shape_set_parent()`, `shape_add_child()`, `shape_free()`
- Connectors: `connector_create()`, `connector_free()`
- Pages: `page_create()`, `page_add_shape()`, `page_add_connector()`, `page_free()`
- Documents: `document_create()`, `document_add_page()`, `document_free()`

---

### 4. `visio_parser.h` (343 lines)
Main parser API for reading and querying Visio files.

**Core Parsing:**
```c
VisioDocument* visio_parser_parse(const char *filepath);
```

**Page Queries (4 functions):**
- `visio_parser_get_pages()` - Get all pages
- `visio_parser_get_page()` - Get page by index
- `visio_parser_find_page()` - Find page by name
- `visio_parser_page_count()` - Total pages

**Shape Queries (10 functions):**
- `visio_parser_get_shapes()` - Get shapes on page
- `visio_parser_find_shape()` - Find by ID
- `visio_parser_find_shapes_by_property()` - Find by property value
- `visio_parser_find_shapes_by_type()` - Find by type
- `visio_parser_find_shapes_by_text()` - Find by text content
- `visio_parser_shape_count()` - Total shapes
- `visio_parser_page_shape_count()` - Shapes on page
- Plus property getters

**Hierarchy (5 functions):**
- `visio_parser_get_parent()` - Get parent shape
- `visio_parser_get_children()` - Get child shapes
- `visio_parser_is_nested()` - Check if nested
- `shape_add_child()` - Add child
- `shape_set_parent()` - Set parent

**Connectors (8 functions):**
- `visio_parser_get_connectors()` - Get all connectors on page
- `visio_parser_find_connector()` - Find by ID
- `visio_parser_get_outgoing_connectors()` - From shape
- `visio_parser_get_incoming_connectors()` - To shape
- `visio_parser_is_connected()` - Check connection
- `visio_parser_connector_count()` - Total count
- `visio_parser_page_connector_count()` - On page
- Plus validation

**Utility (5 functions):**
- `visio_parser_validate()` - Check integrity
- `visio_parser_print_summary()` - Print stats
- `visio_parser_free_shape_array()` - Free search results
- `visio_parser_free_connector_array()` - Free results

**Total: 30+ public functions**

---

### 5. `json_exporter.h` (263 lines)
JSON serialization and export.

**Export Functions (7):**
- `json_exporter_document()` - Export entire document
- `json_exporter_page()` - Export single page
- `json_exporter_shape()` - Export shape
- `json_exporter_connector()` - Export connector
- `json_exporter_to_file()` - Write to file
- `json_exporter_to_stream()` - Write to FILE*
- `json_exporter_pages_array()` - Export pages array

**Configuration Functions (8):**
- `json_exporter_set_pretty_print()` - Enable indentation
- `json_exporter_set_indent_size()` - Indent size
- `json_exporter_set_include_properties()` - Include properties
- `json_exporter_set_include_hierarchy()` - Include parent/children
- `json_exporter_set_include_metadata()` - Include metadata
- `json_exporter_get_config()` - Get current config
- `json_exporter_set_config()` - Set all options
- `json_exporter_reset_config()` - Reset to defaults

**JSON Output Structure:**
```json
{
  "filename": "diagram.vsdx",
  "metadata": {
    "creator": "...",
    "created": "...",
    "modified": "..."
  },
  "pages": [
    {
      "id": "page1",
      "name": "Page 1",
      "shapes": [
        {
          "id": "shape1",
          "text": "Task A",
          "type": "rectangle",
          "position": {"x": 100, "y": 200},
          "size": {"width": 50, "height": 30},
          "parent_id": null,
          "children_ids": ["shape2"],
          "properties": [
            {"name": "color", "value": "#FF0000"}
          ]
        }
      ],
      "connectors": [
        {
          "id": "conn1",
          "from_shape_id": "shape1",
          "to_shape_id": "shape2",
          "text": "flows to",
          "properties": []
        }
      ]
    }
  ]
}
```

---

## Implementation Requirements

### Dependencies
- **libvisio2** - .vsdx file format support
- **json-c** - JSON serialization
- **libxml2** - XML support (used by libvisio2)
- **Standard C library** - C99 or later

### Compilation Example
```bash
gcc -I. -c src/types.c -o build/types.o
gcc -I. -c src/errors.c -o build/errors.o
gcc -I. -c src/visio_parser.c -o build/visio_parser.o -lvisio2 -lxml2
gcc -I. -c src/json_exporter.c -o build/json_exporter.o -ljson-c
gcc -I. -c src/main.c -o build/main.o
gcc build/*.o -o visio_parser -lvisio2 -lxml2 -ljson-c
```

### CMake Build (Recommended)
```cmake
cmake_minimum_required(VERSION 3.10)
project(visio_parser C)

set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)

find_package(libvisio REQUIRED)
find_package(json-c REQUIRED)
find_package(libxml2 REQUIRED)

add_executable(visio_parser
    src/main.c
    src/types.c
    src/errors.c
    src/visio_parser.c
    src/json_exporter.c
)

target_link_libraries(visio_parser
    libvisio::libvisio
    json-c::json-c
    libxml2::libxml2
)
```

---

## Next Steps - Implementation Phase

### Phase 1: Core Types (src/types.c)
Implement memory management functions:
- Property list operations
- Shape creation and hierarchy
- Connector creation
- Page management
- Document management

### Phase 2: Error Handling (src/errors.c)
Implement error system:
- Thread-local error storage
- Error message mapping
- Error printing

### Phase 3: Parser (src/visio_parser.c)
Implement parsing using libvisio:
- Load .vsdx file (ODF format)
- Extract pages, shapes, connectors
- Build hierarchy relationships
- Extract properties
- Implement query functions

### Phase 4: Exporter (src/json_exporter.c)
Implement JSON generation using json-c:
- Serialize structures to JSON
- Configure output format
- Stream to file/string

### Phase 5: CLI (src/main.c)
Create command-line tool:
```
Usage: visio_parser [OPTIONS] input.vsdx [output.json]

Options:
  -h, --help              Show help
  -p, --pretty            Pretty-print JSON
  -i, --indent SIZE       Indent size (default 2)
  --no-properties         Exclude properties
  --no-hierarchy          Exclude hierarchy info
  --no-metadata           Exclude metadata
  -o, --output FILE       Output file (default stdout)
  -v, --verbose           Verbose output
```

---

## Design Principles

### 1. Memory Safety
- All allocations are predictable
- Clear ownership (caller vs library)
- Freed by appropriate functions
- No memory leaks

### 2. Error Handling
- All errors return error codes or NULL
- Error context always available via `error_get_last()`
- Helpful error messages
- Convenience macros for setting errors

### 3. Flexibility
- Hierarchical and flat query APIs
- Multiple search methods (by ID, type, text, property)
- Configurable JSON output
- Extensible property system

### 4. Performance
- Dynamic arrays with growth factor (avoid repeated allocations)
- Efficient searches (linear but minimal allocations)
- Streaming JSON output option
- Batch operations

### 5. Documentation
- All functions have detailed docstrings
- Usage examples in headers
- README with API overview
- Error codes documented

---

## API Statistics

| Category | Count |
|----------|-------|
| Structures | 9 |
| Total Functions | 50+ |
| Error Codes | 10 |
| Configuration Options | 8 |
| Export Formats | 7 |
| Query Methods | 30+ |
| Memory Mgmt Functions | 20+ |

---

## File Organization

```
drawio-food-delivery-wireframes/UML-SKILLS/
├── include/
│   └── dashboard/                  (Headers)
│       ├── config.h                59 lines
│       ├── errors.h                119 lines
│       ├── types.h                 349 lines
│       ├── visio_parser.h          343 lines
│       ├── json_exporter.h         263 lines
│       └── README.md               348 lines
│
├── src/
│   └── dashboard/                  (Implementation - next)
│       ├── types.c                 (to implement)
│       ├── errors.c                (to implement)
│       ├── visio_parser.c          (to implement)
│       ├── json_exporter.c         (to implement)
│       └── main.c                  (to implement)
│
├── CMakeLists.txt                  (Build config)
└── README.md                       (Project overview)
```

---

## Success Criteria - Headers ✅

- ✅ All 5 header files created
- ✅ All structures defined
- ✅ All function signatures defined
- ✅ Comprehensive documentation
- ✅ Include guards in place
- ✅ Dependency declarations
- ✅ Memory management API
- ✅ Error handling API
- ✅ Query and search API
- ✅ JSON export API
- ✅ Configuration system
- ✅ 1,486 lines of well-documented code

---

## Quick Reference

### Include All Headers
```c
#include "dashboard/config.h"
#include "dashboard/errors.h"
#include "dashboard/types.h"
#include "dashboard/visio_parser.h"
#include "dashboard/json_exporter.h"
```

### Complete Parse & Export Example
```c
// Parse
VisioDocument *doc = visio_parser_parse("diagram.vsdx");
if (!doc) { error_print(); return 1; }

// Configure JSON export
json_exporter_set_pretty_print(1);

// Export to file
if (json_exporter_to_file(doc, "output.json") < 0) {
    error_print();
    return 1;
}

// Print statistics
visio_parser_print_summary(doc);

// Clean up
document_free(doc);
return 0;
```

### Find All Rectangles
```c
size_t count;
Shape **rects = visio_parser_find_shapes_by_type(doc, "rectangle", &count);
for (size_t i = 0; i < count; i++) {
    printf("%s at (%.0f, %.0f)\n", rects[i]->text, 
           rects[i]->position.x, rects[i]->position.y);
}
visio_parser_free_shape_array(rects, count);
```

---

**Status**: Ready for implementation phase  
**Next**: Implement src/types.c, src/errors.c, etc.

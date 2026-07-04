#ifndef DASHBOARD_TYPES_H
#define DASHBOARD_TYPES_H

/**
 * @file types.h
 * @brief Core data structures for Visio document representation
 * 
 * Defines all data types needed to represent Visio documents:
 * shapes, connectors, pages, properties, and the complete document.
 * All structures use dynamic memory for flexibility.
 */

#include <stddef.h>
#include <stdint.h>

/* Forward declarations */
typedef struct Shape Shape;
typedef struct Connector Connector;
typedef struct Page Page;
typedef struct Property Property;
typedef struct PropertyList PropertyList;
typedef struct Point Point;
typedef struct Size Size;
typedef struct VisioDocument VisioDocument;

/**
 * @struct Point
 * @brief 2D coordinate (x, y)
 */
typedef struct {
    double x;
    double y;
} Point;

/**
 * @struct Size
 * @brief 2D dimensions (width, height)
 */
typedef struct {
    double width;
    double height;
} Size;

/**
 * @struct Property
 * @brief Key-value property for shapes/connectors
 * 
 * Represents visual properties like color, font, style, etc.
 */
typedef struct {
    char *name;           /**< Property name (e.g., "color", "font") */
    char *value;          /**< Property value as string */
} Property;

/**
 * @struct PropertyList
 * @brief Dynamic array of properties
 * 
 * Growable list of key-value properties with memory management.
 */
typedef struct {
    Property *items;      /**< Array of properties */
    size_t count;         /**< Number of properties */
    size_t capacity;      /**< Allocated capacity */
} PropertyList;

/**
 * @struct Shape
 * @brief Visio shape object
 * 
 * Represents a shape in the diagram with position, size, text, and properties.
 * Supports hierarchical nesting via parent_id and children_ids.
 */
typedef struct Shape {
    char *id;             /**< Unique shape identifier */
    char *text;           /**< Text content of shape (may be NULL) */
    Point position;       /**< Top-left corner position (x, y) */
    Size size;            /**< Width and height dimensions */
    char *type;           /**< Shape type (e.g., "rectangle", "circle", "diamond") */
    char *parent_id;      /**< Parent shape ID (NULL if top-level) */
    PropertyList *properties;  /**< Shape visual properties */
    
    /* Hierarchy support */
    char **children_ids;  /**< Array of child shape IDs */
    size_t children_count; /**< Number of children */
    size_t children_capacity; /**< Allocated capacity for children */
    
    /* Metadata */
    uint32_t page_index;  /**< Index of page containing this shape */
    int is_group;         /**< 1 if shape is a group, 0 otherwise */
} Shape;

/**
 * @struct Connector
 * @brief Connection between two shapes
 * 
 * Represents a line/arrow connecting two shapes with optional label text.
 */
typedef struct Connector {
    char *id;             /**< Unique connector identifier */
    char *from_shape_id;  /**< Source shape ID */
    char *to_shape_id;    /**< Target shape ID */
    char *text;           /**< Label text on connector (may be NULL) */
    PropertyList *properties;  /**< Connector visual properties */
    
    /* Metadata */
    uint32_t page_index;  /**< Index of page containing this connector */
} Connector;

/**
 * @struct Page
 * @brief Single page/diagram within a Visio document
 * 
 * A Visio document can contain multiple pages, each with shapes and connectors.
 */
typedef struct Page {
    char *name;           /**< Page name/title */
    char *id;             /**< Page identifier */
    
    /* Shapes */
    Shape **shapes;       /**< Array of shapes on this page */
    size_t shapes_count;  /**< Number of shapes */
    size_t shapes_capacity; /**< Allocated capacity */
    
    /* Connectors */
    Connector **connectors; /**< Array of connectors on this page */
    size_t connectors_count; /**< Number of connectors */
    size_t connectors_capacity; /**< Allocated capacity */
    
    /* Metadata */
    uint32_t page_index;  /**< Index of this page in document */
} Page;

/**
 * @struct VisioDocument
 * @brief Complete Visio document
 * 
 * Represents the entire .vsdx file with all pages, shapes, and connectors.
 */
typedef struct VisioDocument {
    char *filename;       /**< Source filename */
    
    /* Pages */
    Page **pages;         /**< Array of pages */
    size_t pages_count;   /**< Number of pages */
    size_t pages_capacity; /**< Allocated capacity */
    
    /* Metadata */
    char *creator;        /**< Document creator (if available) */
    char *created;        /**< Creation date (if available) */
    char *modified;       /**< Last modification date (if available) */
} VisioDocument;

/* ============================================================================
 * PROPERTY LIST FUNCTIONS
 * ============================================================================ */

/**
 * @brief Create a new empty property list
 * 
 * @return New PropertyList, or NULL on allocation failure
 */
PropertyList* property_list_create(void);

/**
 * @brief Add a property to the list
 * 
 * @param list Property list
 * @param name Property name
 * @param value Property value
 * @return 0 on success, -1 on failure
 */
int property_list_add(PropertyList *list, const char *name, const char *value);

/**
 * @brief Get a property by name
 * 
 * @param list Property list
 * @param name Property name
 * @return Property pointer, or NULL if not found
 */
Property* property_list_get(PropertyList *list, const char *name);

/**
 * @brief Free a property list and all its contents
 * 
 * @param list Property list (may be NULL)
 */
void property_list_free(PropertyList *list);

/* ============================================================================
 * SHAPE FUNCTIONS
 * ============================================================================ */

/**
 * @brief Create a new shape
 * 
 * @param id Shape identifier
 * @return New Shape, or NULL on failure
 */
Shape* shape_create(const char *id);

/**
 * @brief Set shape parent
 * 
 * @param shape Shape to modify
 * @param parent_id Parent shape ID
 * @return 0 on success, -1 on failure
 */
int shape_set_parent(Shape *shape, const char *parent_id);

/**
 * @brief Add a child shape ID
 * 
 * @param shape Parent shape
 * @param child_id Child shape ID
 * @return 0 on success, -1 on failure
 */
int shape_add_child(Shape *shape, const char *child_id);

/**
 * @brief Get child shape ID by index
 * 
 * @param shape Shape
 * @param index Child index
 * @return Child shape ID, or NULL if index out of bounds
 */
const char* shape_get_child(Shape *shape, size_t index);

/**
 * @brief Free a shape and all its contents
 * 
 * @param shape Shape (may be NULL)
 */
void shape_free(Shape *shape);

/* ============================================================================
 * CONNECTOR FUNCTIONS
 * ============================================================================ */

/**
 * @brief Create a new connector
 * 
 * @param id Connector identifier
 * @param from_id Source shape ID
 * @param to_id Target shape ID
 * @return New Connector, or NULL on failure
 */
Connector* connector_create(const char *id, const char *from_id, const char *to_id);

/**
 * @brief Free a connector and all its contents
 * 
 * @param connector Connector (may be NULL)
 */
void connector_free(Connector *connector);

/* ============================================================================
 * PAGE FUNCTIONS
 * ============================================================================ */

/**
 * @brief Create a new page
 * 
 * @param name Page name
 * @param id Page identifier
 * @return New Page, or NULL on failure
 */
Page* page_create(const char *name, const char *id);

/**
 * @brief Add a shape to a page
 * 
 * @param page Page
 * @param shape Shape to add
 * @return 0 on success, -1 on failure
 */
int page_add_shape(Page *page, Shape *shape);

/**
 * @brief Add a connector to a page
 * 
 * @param page Page
 * @param connector Connector to add
 * @return 0 on success, -1 on failure
 */
int page_add_connector(Page *page, Connector *connector);

/**
 * @brief Free a page and all its contents
 * 
 * @param page Page (may be NULL)
 */
void page_free(Page *page);

/* ============================================================================
 * DOCUMENT FUNCTIONS
 * ============================================================================ */

/**
 * @brief Create a new empty document
 * 
 * @param filename Source filename
 * @return New VisioDocument, or NULL on failure
 */
VisioDocument* document_create(const char *filename);

/**
 * @brief Add a page to a document
 * 
 * @param doc Document
 * @param page Page to add
 * @return 0 on success, -1 on failure
 */
int document_add_page(VisioDocument *doc, Page *page);

/**
 * @brief Get page by index
 * 
 * @param doc Document
 * @param index Page index
 * @return Page pointer, or NULL if out of bounds
 */
Page* document_get_page(VisioDocument *doc, size_t index);

/**
 * @brief Free a document and all its contents
 * 
 * @param doc Document (may be NULL)
 */
void document_free(VisioDocument *doc);

/**
 * @brief Get total number of shapes in document
 * 
 * @param doc Document
 * @return Total shape count across all pages
 */
size_t document_total_shapes(VisioDocument *doc);

/**
 * @brief Get total number of connectors in document
 * 
 * @param doc Document
 * @return Total connector count across all pages
 */
size_t document_total_connectors(VisioDocument *doc);

/* ============================================================================
 * BUILDER FUNCTIONS - Setters for Shape/Connector Properties
 * ============================================================================ */

/**
 * @brief Set shape text content
 * 
 * @param shape Shape to modify
 * @param text New text content (NULL to clear)
 * @return 0 on success, -1 on failure
 */
int shape_set_text(Shape *shape, const char *text);

/**
 * @brief Set shape type
 * 
 * @param shape Shape to modify
 * @param type Shape type (e.g., "rectangle", "circle")
 * @return 0 on success, -1 on failure
 */
int shape_set_type(Shape *shape, const char *type);

/**
 * @brief Set shape position (x, y coordinates)
 * 
 * @param shape Shape to modify
 * @param x X coordinate
 * @param y Y coordinate
 * @return 0 on success, -1 on failure
 */
int shape_set_position(Shape *shape, double x, double y);

/**
 * @brief Set shape dimensions
 * 
 * @param shape Shape to modify
 * @param width Shape width
 * @param height Shape height
 * @return 0 on success, -1 on failure
 */
int shape_set_size(Shape *shape, double width, double height);

/**
 * @brief Add property to shape
 * 
 * @param shape Shape to modify
 * @param name Property name
 * @param value Property value
 * @return 0 on success, -1 on failure
 */
int shape_add_property(Shape *shape, const char *name, const char *value);

/**
 * @brief Get shape property value
 * 
 * @param shape Shape to query
 * @param name Property name
 * @return Property value string, or NULL if not found
 */
const char* shape_get_property(Shape *shape, const char *name);

/**
 * @brief Set shape as group
 * 
 * @param shape Shape to modify
 * @param is_group 1 if group, 0 otherwise
 */
void shape_set_group(Shape *shape, int is_group);

/**
 * @brief Set connector text label
 * 
 * @param connector Connector to modify
 * @param text Label text (NULL to clear)
 * @return 0 on success, -1 on failure
 */
int connector_set_text(Connector *connector, const char *text);

/**
 * @brief Add property to connector
 * 
 * @param connector Connector to modify
 * @param name Property name
 * @param value Property value
 * @return 0 on success, -1 on failure
 */
int connector_add_property(Connector *connector, const char *name, const char *value);

/**
 * @brief Get connector property value
 * 
 * @param connector Connector to query
 * @param name Property name
 * @return Property value string, or NULL if not found
 */
const char* connector_get_property(Connector *connector, const char *name);

/* ============================================================================
 * QUERY/MODIFICATION FUNCTIONS
 * ============================================================================ */

/**
 * @brief Find shape by ID within a page
 * 
 * @param page Page to search
 * @param shape_id Shape ID to find
 * @return Shape pointer, or NULL if not found
 */
Shape* page_find_shape_by_id(Page *page, const char *shape_id);

/**
 * @brief Find connector by ID within a page
 * 
 * @param page Page to search
 * @param connector_id Connector ID to find
 * @return Connector pointer, or NULL if not found
 */
Connector* page_find_connector_by_id(Page *page, const char *connector_id);

/**
 * @brief Remove shape from page (does not free it)
 * 
 * @param page Page to modify
 * @param shape_id Shape ID to remove
 * @return 0 on success, -1 if not found
 */
int page_remove_shape(Page *page, const char *shape_id);

/**
 * @brief Remove connector from page (does not free it)
 * 
 * @param page Page to modify
 * @param connector_id Connector ID to remove
 * @return 0 on success, -1 if not found
 */
int page_remove_connector(Page *page, const char *connector_id);

/**
 * @brief Clone a shape (deep copy)
 * 
 * @param source Source shape to clone
 * @return New cloned shape, or NULL on failure
 */
Shape* shape_clone(const Shape *source);

/**
 * @brief Clone a connector (deep copy)
 * 
 * @param source Source connector to clone
 * @return New cloned connector, or NULL on failure
 */
Connector* connector_clone(const Connector *source);

#endif /* DASHBOARD_TYPES_H */

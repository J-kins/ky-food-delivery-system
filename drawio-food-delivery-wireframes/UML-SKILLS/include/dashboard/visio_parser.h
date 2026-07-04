#ifndef DASHBOARD_VISIO_PARSER_H
#define DASHBOARD_VISIO_PARSER_H

/**
 * @file visio_parser.h
 * @brief Main API for parsing and querying Visio documents
 * 
 * Provides high-level functions for:
 * - Parsing .vsdx files into VisioDocument structures
 * - Querying shapes, connectors, and pages
 * - Finding shapes by ID, properties, or connectivity
 * - Extracting hierarchical relationships
 */

#include "types.h"

/**
 * @brief Parse a Visio (.vsdx) file
 * 
 * Opens and parses the entire Visio document, extracting all pages,
 * shapes, connectors, and properties. On error, returns NULL and sets
 * error context accessible via error_get_last().
 * 
 * @param filepath Path to .vsdx file
 * @return Parsed VisioDocument, or NULL on error
 * 
 * Example:
 * @code
 * VisioDocument *doc = visio_parser_parse("diagram.vsdx");
 * if (!doc) {
 *     error_print();
 *     return;
 * }
 * // Use document...
 * document_free(doc);
 * @endcode
 */
VisioDocument* visio_parser_parse(const char *filepath);

/* ============================================================================
 * PAGE QUERIES
 * ============================================================================ */

/**
 * @brief Get all pages from a document
 * 
 * @param doc Document
 * @param count Output: number of pages
 * @return Array of Page pointers (internally managed, do not free)
 */
Page** visio_parser_get_pages(VisioDocument *doc, size_t *count);

/**
 * @brief Get page by index
 * 
 * @param doc Document
 * @param index Zero-based page index
 * @return Page pointer, or NULL if out of bounds
 */
Page* visio_parser_get_page(VisioDocument *doc, size_t index);

/**
 * @brief Find page by name
 * 
 * @param doc Document
 * @param page_name Page name to find
 * @return Page pointer, or NULL if not found
 */
Page* visio_parser_find_page(VisioDocument *doc, const char *page_name);

/* ============================================================================
 * SHAPE QUERIES
 * ============================================================================ */

/**
 * @brief Get all shapes on a page
 * 
 * @param page Page
 * @param count Output: number of shapes
 * @return Array of Shape pointers (internally managed, do not free)
 */
Shape** visio_parser_get_shapes(Page *page, size_t *count);

/**
 * @brief Find a shape by ID across entire document
 * 
 * Searches all pages for shape with matching ID.
 * 
 * @param doc Document
 * @param shape_id Shape ID to find
 * @return Shape pointer, or NULL if not found
 */
Shape* visio_parser_find_shape(VisioDocument *doc, const char *shape_id);

/**
 * @brief Find all shapes with a specific property value
 * 
 * Searches all shapes in document for ones with matching property.
 * 
 * @param doc Document
 * @param property_name Property name (e.g., "color")
 * @param property_value Property value to match
 * @param count Output: number of matching shapes
 * @return Array of matching Shape pointers (must be freed by caller)
 */
Shape** visio_parser_find_shapes_by_property(VisioDocument *doc,
                                            const char *property_name,
                                            const char *property_value,
                                            size_t *count);

/**
 * @brief Find all shapes of a specific type
 * 
 * @param doc Document
 * @param shape_type Type to find (e.g., "rectangle")
 * @param count Output: number of matching shapes
 * @return Array of matching Shape pointers (must be freed by caller)
 */
Shape** visio_parser_find_shapes_by_type(VisioDocument *doc,
                                        const char *shape_type,
                                        size_t *count);

/**
 * @brief Find shapes containing specific text
 * 
 * @param doc Document
 * @param text Text to search for
 * @param count Output: number of matching shapes
 * @return Array of matching Shape pointers (must be freed by caller)
 */
Shape** visio_parser_find_shapes_by_text(VisioDocument *doc,
                                        const char *text,
                                        size_t *count);

/* ============================================================================
 * HIERARCHY & RELATIONSHIPS
 * ============================================================================ */

/**
 * @brief Get parent shape
 * 
 * If shape has a parent, returns the parent Shape. Otherwise returns NULL.
 * 
 * @param doc Document (required for lookup)
 * @param shape Shape
 * @return Parent shape, or NULL if no parent or top-level
 */
Shape* visio_parser_get_parent(VisioDocument *doc, Shape *shape);

/**
 * @brief Get all child shapes
 * 
 * Returns all shapes that have this shape as parent.
 * 
 * @param doc Document
 * @param shape Parent shape
 * @param count Output: number of children
 * @return Array of child Shape pointers (must be freed by caller)
 */
Shape** visio_parser_get_children(VisioDocument *doc, Shape *shape, size_t *count);

/**
 * @brief Check if shape is nested inside another
 * 
 * @param doc Document
 * @param container Potential container shape
 * @param shape Shape to check
 * @return 1 if shape is inside container (directly or indirectly), 0 otherwise
 */
int visio_parser_is_nested(VisioDocument *doc, Shape *container, Shape *shape);

/* ============================================================================
 * CONNECTOR QUERIES
 * ============================================================================ */

/**
 * @brief Get all connectors on a page
 * 
 * @param page Page
 * @param count Output: number of connectors
 * @return Array of Connector pointers (internally managed, do not free)
 */
Connector** visio_parser_get_connectors(Page *page, size_t *count);

/**
 * @brief Find connector by ID
 * 
 * @param doc Document
 * @param connector_id Connector ID
 * @return Connector pointer, or NULL if not found
 */
Connector* visio_parser_find_connector(VisioDocument *doc, const char *connector_id);

/**
 * @brief Get all connectors from a shape
 * 
 * Returns all connectors that have shape as source (from_shape_id).
 * 
 * @param doc Document
 * @param shape Source shape
 * @param count Output: number of connectors
 * @return Array of outgoing Connector pointers (must be freed by caller)
 */
Connector** visio_parser_get_outgoing_connectors(VisioDocument *doc,
                                               Shape *shape,
                                               size_t *count);

/**
 * @brief Get all connectors to a shape
 * 
 * Returns all connectors that have shape as target (to_shape_id).
 * 
 * @param doc Document
 * @param shape Target shape
 * @param count Output: number of connectors
 * @return Array of incoming Connector pointers (must be freed by caller)
 */
Connector** visio_parser_get_incoming_connectors(VisioDocument *doc,
                                               Shape *shape,
                                               size_t *count);

/**
 * @brief Check if two shapes are connected
 * 
 * Returns true if there's a connector from shape1 to shape2.
 * 
 * @param doc Document
 * @param shape1 Source shape
 * @param shape2 Target shape
 * @return 1 if connected, 0 if not connected
 */
int visio_parser_is_connected(VisioDocument *doc, Shape *shape1, Shape *shape2);

/* ============================================================================
 * PROPERTY QUERIES
 * ============================================================================ */

/**
 * @brief Get a shape property value
 * 
 * @param shape Shape
 * @param property_name Property name
 * @return Property value, or NULL if not found
 */
const char* visio_parser_get_property(Shape *shape, const char *property_name);

/**
 * @brief Get a connector property value
 * 
 * @param connector Connector
 * @param property_name Property name
 * @return Property value, or NULL if not found
 */
const char* visio_parser_get_connector_property(Connector *connector,
                                               const char *property_name);

/* ============================================================================
 * STATISTICS
 * ============================================================================ */

/**
 * @brief Get total shapes in document
 * 
 * @param doc Document
 * @return Total shape count
 */
size_t visio_parser_shape_count(VisioDocument *doc);

/**
 * @brief Get total connectors in document
 * 
 * @param doc Document
 * @return Total connector count
 */
size_t visio_parser_connector_count(VisioDocument *doc);

/**
 * @brief Get page count
 * 
 * @param doc Document
 * @return Number of pages
 */
size_t visio_parser_page_count(VisioDocument *doc);

/**
 * @brief Get shapes on a page
 * 
 * @param page Page
 * @return Number of shapes
 */
size_t visio_parser_page_shape_count(Page *page);

/**
 * @brief Get connectors on a page
 * 
 * @param page Page
 * @return Number of connectors
 */
size_t visio_parser_page_connector_count(Page *page);

/* ============================================================================
 * UTILITY FUNCTIONS
 * ============================================================================ */

/**
 * @brief Validate document integrity
 * 
 * Checks that all connector endpoints reference valid shapes.
 * Prints warnings for any broken references.
 * 
 * @param doc Document
 * @return 0 if valid, -1 if errors found
 */
int visio_parser_validate(VisioDocument *doc);

/**
 * @brief Print document summary
 * 
 * Prints statistics about the document (page count, shape count, etc.).
 * 
 * @param doc Document
 */
void visio_parser_print_summary(VisioDocument *doc);

/**
 * @brief Free dynamically allocated search results
 * 
 * Use this to free arrays returned by find_*_shapes functions.
 * 
 * @param results Array of Shape pointers
 * @param count Number of items in array
 */
void visio_parser_free_shape_array(Shape **results, size_t count);

/**
 * @brief Free dynamically allocated connector results
 * 
 * @param results Array of Connector pointers
 * @param count Number of items in array
 */
void visio_parser_free_connector_array(Connector **results, size_t count);

/* ============================================================================
 * MODIFICATION OPERATIONS - Creating/Deleting Elements
 * ============================================================================ */

/**
 * @brief Create a new shape and add to document
 * 
 * Creates an empty shape with given ID and adds it to specified page.
 * 
 * @param doc Document to modify
 * @param page_index Index of page to add shape to
 * @param shape_id New shape ID
 * @return New Shape pointer, or NULL on failure
 * 
 * @example
 * Shape *rect = visio_parser_create_shape(doc, 0, "S1");
 * shape_set_type(rect, "rectangle");
 * shape_set_text(rect, "New Task");
 */
Shape* visio_parser_create_shape(VisioDocument *doc, size_t page_index, const char *shape_id);

/**
 * @brief Create a new connector and add to document
 * 
 * Creates a connector between two shapes and adds to specified page.
 * 
 * @param doc Document to modify
 * @param page_index Index of page to add connector to
 * @param connector_id New connector ID
 * @param from_shape_id Source shape ID
 * @param to_shape_id Target shape ID
 * @return New Connector pointer, or NULL on failure
 */
Connector* visio_parser_create_connector(VisioDocument *doc, size_t page_index,
                                        const char *connector_id,
                                        const char *from_shape_id,
                                        const char *to_shape_id);

/**
 * @brief Remove shape from document by ID
 * 
 * Deletes shape and all connected connectors from document.
 * 
 * @param doc Document to modify
 * @param shape_id Shape ID to remove
 * @return 0 on success, -1 if not found
 */
int visio_parser_remove_shape(VisioDocument *doc, const char *shape_id);

/**
 * @brief Remove connector from document by ID
 * 
 * @param doc Document to modify
 * @param connector_id Connector ID to remove
 * @return 0 on success, -1 if not found
 */
int visio_parser_remove_connector(VisioDocument *doc, const char *connector_id);

/**
 * @brief Create a new page and add to document
 * 
 * @param doc Document to modify
 * @param page_name Name for new page
 * @return New Page pointer, or NULL on failure
 */
Page* visio_parser_create_page(VisioDocument *doc, const char *page_name);

/* ============================================================================
 * CLONING OPERATIONS - For Templates
 * ============================================================================ */

/**
 * @brief Clone a shape (deep copy)
 * 
 * Creates a complete independent copy of a shape with new ID.
 * Useful for creating templates and duplicating diagram elements.
 * 
 * @param source Source shape
 * @param new_id ID for cloned shape
 * @return New cloned shape, or NULL on failure
 */
Shape* visio_parser_clone_shape(const Shape *source, const char *new_id);

/**
 * @brief Clone a connector (deep copy)
 * 
 * Creates a complete independent copy of a connector with new ID.
 * 
 * @param source Source connector
 * @param new_id ID for cloned connector
 * @param new_from_id Source shape ID for cloned connector
 * @param new_to_id Target shape ID for cloned connector
 * @return New cloned connector, or NULL on failure
 */
Connector* visio_parser_clone_connector(const Connector *source,
                                       const char *new_id,
                                       const char *new_from_id,
                                       const char *new_to_id);

/**
 * @brief Clone entire page
 * 
 * @param source Source page
 * @param new_name Name for cloned page
 * @return New cloned page, or NULL on failure
 */
Page* visio_parser_clone_page(const Page *source, const char *new_name);

/* ============================================================================
 * TEMPLATE SUPPORT
 * ============================================================================ */

/**
 * @brief Create document from template
 * 
 * Loads a template document and creates a new instance.
 * 
 * @param template_path Path to template .vsdx file
 * @param output_filename Name for new document
 * @return New document based on template, or NULL on failure
 * 
 * @example
 * VisioDocument *doc = visio_parser_from_template("kanban_template.vsdx", "my_kanban.vsdx");
 * // Modify shapes as needed
 * visio_writer_save(doc, "my_kanban.vsdx");
 */
VisioDocument* visio_parser_from_template(const char *template_path,
                                         const char *output_filename);

/**
 * @brief Create document from JSON specification
 * 
 * Generates a Visio document from JSON structure.
 * JSON format matches what json_exporter_document() produces.
 * 
 * @param json_spec JSON string describing diagram
 * @param output_filename Filename for new document
 * @return New document, or NULL on failure
 */
VisioDocument* visio_parser_from_json(const char *json_spec, const char *output_filename);

#endif /* DASHBOARD_VISIO_PARSER_H */

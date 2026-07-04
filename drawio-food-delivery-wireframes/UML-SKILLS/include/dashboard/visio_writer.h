#ifndef DASHBOARD_VISIO_WRITER_H
#define DASHBOARD_VISIO_WRITER_H

/**
 * @file visio_writer.h
 * @brief Write and modify Visio documents
 * 
 * Provides functions to:
 * - Save in-memory documents to .vsdx files
 * - Modify existing documents (update shape properties, delete elements)
 * - Perform batch operations on multiple shapes/connectors
 * 
 * All write operations work on in-memory VisioDocument structures.
 * Use visio_writer_save() to persist changes to disk.
 */

#include "types.h"

/* ============================================================================
 * SAVE OPERATIONS
 * ============================================================================ */

/**
 * @brief Save a document to a .vsdx file
 * 
 * Creates or overwrites the specified file with the document contents.
 * All pages, shapes, connectors, and properties are written.
 * 
 * @param doc Document to save
 * @param filepath Path where file should be written
 * @return 0 on success, -1 on failure (see error_get_last() for details)
 * 
 * @example
 * VisioDocument *doc = document_create("new.vsdx");
 * Page *page = page_create("Sheet.1", "Page-1");
 * Shape *rect = shape_create("S1");
 * shape_set_text(rect, "Task");
 * page_add_shape(page, rect);
 * document_add_page(doc, page);
 * visio_writer_save(doc, "output.vsdx");
 * document_free(doc);
 */
int visio_writer_save(VisioDocument *doc, const char *filepath);

/**
 * @brief Save a single page to a new .vsdx file
 * 
 * Creates a new document containing only the specified page.
 * 
 * @param page Page to save
 * @param filepath Path where file should be written
 * @return 0 on success, -1 on failure
 */
int visio_writer_save_page(Page *page, const char *filepath);

/* ============================================================================
 * MODIFICATION OPERATIONS - In-Memory
 * ============================================================================ */

/**
 * @brief Delete a shape from a document
 * 
 * Removes the shape from its page. Also removes all connectors connected
 * to this shape (preserving document integrity).
 * Does NOT free the shape - you must do that separately if needed.
 * 
 * @param doc Document containing the shape
 * @param shape_id Shape ID to delete
 * @return 0 on success, -1 if shape not found
 * 
 * @example
 * VisioDocument *doc = visio_parser_parse("diagram.vsdx");
 * visio_writer_delete_shape(doc, "S1");
 * visio_writer_save(doc, "diagram.vsdx");
 * document_free(doc);
 */
int visio_writer_delete_shape(VisioDocument *doc, const char *shape_id);

/**
 * @brief Delete a connector from a document
 * 
 * Removes the connector from its page.
 * Does NOT free the connector - you must do that separately if needed.
 * 
 * @param doc Document containing the connector
 * @param connector_id Connector ID to delete
 * @return 0 on success, -1 if connector not found
 */
int visio_writer_delete_connector(VisioDocument *doc, const char *connector_id);

/**
 * @brief Delete all shapes matching a type
 * 
 * Finds and removes all shapes of a given type from all pages.
 * Automatically removes connected connectors.
 * 
 * @param doc Document
 * @param shape_type Shape type to match (e.g., "rectangle", "circle")
 * @return Number of shapes deleted, or -1 on error
 */
int visio_writer_delete_shapes_by_type(VisioDocument *doc, const char *shape_type);

/**
 * @brief Delete all shapes matching a text pattern
 * 
 * Finds and removes all shapes whose text content matches (contains) the pattern.
 * 
 * @param doc Document
 * @param text_pattern Text pattern to match (substring match)
 * @return Number of shapes deleted, or -1 on error
 */
int visio_writer_delete_shapes_by_text(VisioDocument *doc, const char *text_pattern);

/* ============================================================================
 * BATCH OPERATIONS
 * ============================================================================ */

/**
 * @struct BatchUpdate
 * @brief Single update operation for batch processing
 */
typedef struct {
    char *shape_id;       /**< Target shape ID */
    const char *property_name;  /**< Property to update */
    const char *property_value; /**< New property value */
} BatchUpdate;

/**
 * @brief Update properties on multiple shapes by type
 * 
 * Finds all shapes matching a type and applies property updates.
 * 
 * @param doc Document
 * @param shape_type Type to match
 * @param updates Array of updates to apply
 * @param update_count Number of updates in array
 * @return Number of shapes updated, or -1 on error
 * 
 * @example
 * Property updates[] = {
 *     {"color", "#FF0000"},
 *     {"font-size", "12"}
 * };
 * visio_writer_batch_update_by_type(doc, "rectangle", updates, 2);
 */
int visio_writer_batch_update_by_type(VisioDocument *doc, const char *shape_type,
                                      const Property *updates, size_t update_count);

/**
 * @brief Update properties on multiple shapes by property value
 * 
 * Finds all shapes where a property matches a value, applies updates.
 * 
 * @param doc Document
 * @param filter_prop Property name to filter on
 * @param filter_value Property value to match
 * @param updates Array of updates to apply
 * @param update_count Number of updates in array
 * @return Number of shapes updated, or -1 on error
 */
int visio_writer_batch_update_by_property(VisioDocument *doc,
                                          const char *filter_prop,
                                          const char *filter_value,
                                          const Property *updates,
                                          size_t update_count);

/**
 * @brief Apply same update to all shapes
 * 
 * Updates a property on every shape in the document.
 * 
 * @param doc Document
 * @param property_name Property to update
 * @param property_value New value
 * @return Number of shapes updated, or -1 on error
 */
int visio_writer_update_all_shapes(VisioDocument *doc,
                                   const char *property_name,
                                   const char *property_value);

/* ============================================================================
 * COPY/TEMPLATE OPERATIONS
 * ============================================================================ */

/**
 * @brief Copy all shapes from one page to another
 * 
 * Clones all shapes from source_page to dest_page.
 * Connectors are not copied.
 * 
 * @param src_page Source page
 * @param dest_page Destination page
 * @return 0 on success, -1 on failure
 */
int visio_writer_copy_shapes(Page *src_page, Page *dest_page);

/**
 * @brief Duplicate a shape multiple times on a page
 * 
 * Creates multiple copies of a shape with offset positions.
 * 
 * @param page Page to modify
 * @param source_shape_id Shape ID to duplicate
 * @param count Number of copies to create
 * @param offset_x X offset for each copy
 * @param offset_y Y offset for each copy
 * @return Number of shapes created, or -1 on failure
 * 
 * @example
 * // Create 3 copies of shape S1, each offset (100, 0)
 * visio_writer_duplicate_shape(page, "S1", 3, 100, 0);
 */
int visio_writer_duplicate_shape(Page *page, const char *source_shape_id,
                                size_t count, double offset_x, double offset_y);

/* ============================================================================
 * VALIDATION & INTEGRITY
 * ============================================================================ */

/**
 * @brief Validate document integrity
 * 
 * Checks that:
 * - All shape IDs are unique
 * - All connector IDs are unique
 * - No orphaned connectors
 * - All referenced shapes exist
 * 
 * @param doc Document to validate
 * @return 0 if valid, >0 for number of errors found
 */
int visio_writer_validate(VisioDocument *doc);

/**
 * @brief Generate unique shape ID
 * 
 * Creates a new ID that doesn't conflict with existing shapes.
 * Returns allocated string - caller must free.
 * 
 * @param doc Document (for uniqueness checking)
 * @param prefix ID prefix (e.g., "S", "Shape")
 * @return New ID string, or NULL on failure
 */
char* visio_writer_generate_shape_id(VisioDocument *doc, const char *prefix);

/**
 * @brief Generate unique connector ID
 * 
 * Creates a new ID that doesn't conflict with existing connectors.
 * Returns allocated string - caller must free.
 * 
 * @param doc Document (for uniqueness checking)
 * @param prefix ID prefix (e.g., "C", "Connector")
 * @return New ID string, or NULL on failure
 */
char* visio_writer_generate_connector_id(VisioDocument *doc, const char *prefix);

/* ============================================================================
 * EXPORT TO FORMATS
 * ============================================================================ */

/**
 * @brief Export document to SVG format
 * 
 * Converts the Visio document to SVG for web display.
 * 
 * @param doc Document to export
 * @param filepath Path where SVG should be written
 * @return 0 on success, -1 on failure
 */
int visio_writer_export_svg(VisioDocument *doc, const char *filepath);

/**
 * @brief Export document to PDF format
 * 
 * Converts the Visio document to PDF.
 * 
 * @param doc Document to export
 * @param filepath Path where PDF should be written
 * @return 0 on success, -1 on failure
 */
int visio_writer_export_pdf(VisioDocument *doc, const char *filepath);

#endif /* DASHBOARD_VISIO_WRITER_H */

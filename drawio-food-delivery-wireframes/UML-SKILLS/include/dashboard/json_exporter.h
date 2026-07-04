#ifndef DASHBOARD_JSON_EXPORTER_H
#define DASHBOARD_JSON_EXPORTER_H

/**
 * @file json_exporter.h
 * @brief JSON serialization for Visio documents
 * 
 * Provides functions to export VisioDocument structures to JSON format
 * for consumption by frontend applications. Supports pretty-printing
 * and multiple output targets (string, file, stream).
 */

#include "types.h"
#include <stdio.h>

/**
 * @brief Export entire document to JSON string
 * 
 * Converts complete VisioDocument to JSON representation. Caller is
 * responsible for freeing the returned string.
 * 
 * @param doc Document to export
 * @return JSON string (allocated with malloc, must be freed by caller)
 *         NULL on error (check error_get_last() for details)
 * 
 * Example:
 * @code
 * char *json = json_exporter_document(doc);
 * if (!json) {
 *     error_print();
 *     return;
 * }
 * printf("%s\n", json);
 * free(json);
 * @endcode
 */
char* json_exporter_document(VisioDocument *doc);

/**
 * @brief Export single page to JSON string
 * 
 * @param page Page to export
 * @return JSON string (must be freed by caller), NULL on error
 */
char* json_exporter_page(Page *page);

/**
 * @brief Export single shape to JSON string
 * 
 * @param shape Shape to export
 * @return JSON string (must be freed by caller), NULL on error
 */
char* json_exporter_shape(Shape *shape);

/**
 * @brief Export single connector to JSON string
 * 
 * @param connector Connector to export
 * @return JSON string (must be freed by caller), NULL on error
 */
char* json_exporter_connector(Connector *connector);

/**
 * @brief Export document to file
 * 
 * Writes complete document as JSON to specified file.
 * 
 * @param doc Document to export
 * @param filepath Output file path
 * @return 0 on success, -1 on error
 * 
 * Example:
 * @code
 * if (json_exporter_to_file(doc, "output.json") < 0) {
 *     error_print();
 * }
 * @endcode
 */
int json_exporter_to_file(VisioDocument *doc, const char *filepath);

/**
 * @brief Export document to stream
 * 
 * Writes complete document as JSON to specified FILE stream.
 * 
 * @param doc Document to export
 * @param stream Output stream (e.g., stdout, file handle)
 * @return 0 on success, -1 on error
 */
int json_exporter_to_stream(VisioDocument *doc, FILE *stream);

/**
 * @brief Export pages array to JSON string
 * 
 * Exports only the pages portion of the document structure.
 * 
 * @param pages Array of pages
 * @param count Number of pages
 * @return JSON array string (must be freed by caller), NULL on error
 */
char* json_exporter_pages_array(Page **pages, size_t count);

/**
 * @brief Export shapes array to JSON string
 * 
 * Exports only the shapes portion, useful for single-page exports.
 * 
 * @param shapes Array of shapes
 * @param count Number of shapes
 * @return JSON array string (must be freed by caller), NULL on error
 */
char* json_exporter_shapes_array(Shape **shapes, size_t count);

/**
 * @brief Export connectors array to JSON string
 * 
 * @param connectors Array of connectors
 * @param count Number of connectors
 * @return JSON array string (must be freed by caller), NULL on error
 */
char* json_exporter_connectors_array(Connector **connectors, size_t count);

/* ============================================================================
 * FORMATTING OPTIONS
 * ============================================================================ */

/**
 * @brief Enable/disable pretty-printing (indentation)
 * 
 * When enabled, JSON output includes indentation and newlines for readability.
 * When disabled, output is compact. Default is enabled.
 * 
 * @param enabled 1 to enable, 0 to disable
 */
void json_exporter_set_pretty_print(int enabled);

/**
 * @brief Set indentation size for pretty-printing
 * 
 * @param spaces Number of spaces per indent level (typically 2 or 4)
 */
void json_exporter_set_indent_size(int spaces);

/**
 * @brief Enable/disable property inclusion
 * 
 * @param enabled 1 to include properties, 0 to exclude
 */
void json_exporter_set_include_properties(int enabled);

/**
 * @brief Enable/disable hierarchy information
 * 
 * @param enabled 1 to include parent_id/children_ids, 0 to exclude
 */
void json_exporter_set_include_hierarchy(int enabled);

/**
 * @brief Enable/disable metadata inclusion
 * 
 * @param enabled 1 to include creator/created/modified, 0 to exclude
 */
void json_exporter_set_include_metadata(int enabled);

/* ============================================================================
 * EXPECTED JSON STRUCTURE
 * ============================================================================ */

/**
 * Expected JSON output structure for complete document:
 * 
 * {
 *   "filename": "diagram.vsdx",
 *   "metadata": {
 *     "creator": "Microsoft Visio",
 *     "created": "2024-01-01T00:00:00Z",
 *     "modified": "2024-01-02T00:00:00Z"
 *   },
 *   "pages": [
 *     {
 *       "id": "page1",
 *       "name": "Page 1",
 *       "shapes": [
 *         {
 *           "id": "shape1",
 *           "text": "Task A",
 *           "type": "rectangle",
 *           "position": {
 *             "x": 100.0,
 *             "y": 200.0
 *           },
 *           "size": {
 *             "width": 50.0,
 *             "height": 30.0
 *           },
 *           "parent_id": null,
 *           "children_ids": ["shape2"],
 *           "properties": [
 *             {
 *               "name": "color",
 *               "value": "#FF0000"
 *             },
 *             {
 *               "name": "font",
 *               "value": "Arial"
 *             }
 *           ]
 *         }
 *       ],
 *       "connectors": [
 *         {
 *           "id": "conn1",
 *           "from_shape_id": "shape1",
 *           "to_shape_id": "shape2",
 *           "text": "flows to",
 *           "properties": []
 *         }
 *       ]
 *     }
 *   ]
 * }
 */

/* ============================================================================
 * CONFIGURATION CONSTANTS
 * ============================================================================ */

/**
 * @brief Export configuration structure
 * 
 * Aggregates all export options for convenience.
 */
typedef struct {
    int pretty_print;           /**< Enable indentation */
    int indent_size;            /**< Spaces per indent level */
    int include_properties;     /**< Include shape/connector properties */
    int include_hierarchy;      /**< Include parent/children relationships */
    int include_metadata;       /**< Include document metadata */
    int escape_strings;         /**< Escape special characters in text */
} JsonExporterConfig;

/**
 * @brief Get current exporter configuration
 * 
 * @return Current configuration structure
 */
JsonExporterConfig json_exporter_get_config(void);

/**
 * @brief Set exporter configuration
 * 
 * @param config Configuration to apply
 */
void json_exporter_set_config(JsonExporterConfig config);

/**
 * @brief Reset configuration to defaults
 * 
 * Restores default settings (pretty-print enabled, all options on).
 */
void json_exporter_reset_config(void);

#endif /* DASHBOARD_JSON_EXPORTER_H */

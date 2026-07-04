/**
 * @file visio_parser.c
 * @brief Visio file parsing implementation
 * 
 * Uses libvisio2 for reading .vsdx files
 */

#include "../include/dashboard/visio_parser.h"
#include "../include/dashboard/errors.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

/* ============================================================================
 * PARSE OPERATIONS
 * ============================================================================ */

/**
 * @brief Parse a Visio file and create document structure
 * 
 * Note: This is a stub implementation. Full implementation would use libvisio2
 * to actually read the .vsdx file format and extract shapes/connectors.
 */
VisioDocument* visio_parser_parse(const char *filepath) {
    if (!filepath) {
        error_set(ERROR_INVALID_ARGUMENT, "File path cannot be NULL");
        return NULL;
    }
    
    /* TODO: Implement actual libvisio2 parsing */
    error_set(ERROR_FILE_NOT_FOUND, "libvisio2 integration not yet implemented");
    return NULL;
}

/* ============================================================================
 * QUERY OPERATIONS
 * ============================================================================ */

Shape* visio_parser_find_shape_by_id(VisioDocument *doc, const char *shape_id) {
    if (!doc || !shape_id) return NULL;
    
    for (size_t i = 0; i < doc->pages_count; i++) {
        Shape *shape = page_find_shape_by_id(doc->pages[i], shape_id);
        if (shape) return shape;
    }
    return NULL;
}

Shape** visio_parser_find_shapes_by_type(VisioDocument *doc, const char *shape_type, size_t *count) {
    if (!doc || !shape_type || !count) {
        error_set(ERROR_INVALID_ARGUMENT, "Invalid arguments to find_shapes_by_type");
        return NULL;
    }
    
    *count = 0;
    size_t capacity = 10;
    Shape **results = (Shape **)malloc(sizeof(Shape *) * capacity);
    if (!results) {
        error_set(ERROR_OUT_OF_MEMORY, "Failed to allocate results");
        return NULL;
    }
    
    for (size_t i = 0; i < doc->pages_count; i++) {
        for (size_t j = 0; j < doc->pages[i]->shapes_count; j++) {
            Shape *shape = doc->pages[i]->shapes[j];
            if (shape->type && strcmp(shape->type, shape_type) == 0) {
                if (*count >= capacity) {
                    capacity *= 2;
                    Shape **new_results = (Shape **)realloc(results, sizeof(Shape *) * capacity);
                    if (!new_results) {
                        free(results);
                        error_set(ERROR_OUT_OF_MEMORY, "Failed to resize results");
                        return NULL;
                    }
                    results = new_results;
                }
                results[(*count)++] = shape;
            }
        }
    }
    
    return results;
}

Shape** visio_parser_find_shapes_by_text(VisioDocument *doc, const char *text_pattern, size_t *count) {
    if (!doc || !text_pattern || !count) {
        error_set(ERROR_INVALID_ARGUMENT, "Invalid arguments to find_shapes_by_text");
        return NULL;
    }
    
    *count = 0;
    size_t capacity = 10;
    Shape **results = (Shape **)malloc(sizeof(Shape *) * capacity);
    if (!results) {
        error_set(ERROR_OUT_OF_MEMORY, "Failed to allocate results");
        return NULL;
    }
    
    for (size_t i = 0; i < doc->pages_count; i++) {
        for (size_t j = 0; j < doc->pages[i]->shapes_count; j++) {
            Shape *shape = doc->pages[i]->shapes[j];
            if (shape->text && strstr(shape->text, text_pattern)) {
                if (*count >= capacity) {
                    capacity *= 2;
                    Shape **new_results = (Shape **)realloc(results, sizeof(Shape *) * capacity);
                    if (!new_results) {
                        free(results);
                        error_set(ERROR_OUT_OF_MEMORY, "Failed to resize results");
                        return NULL;
                    }
                    results = new_results;
                }
                results[(*count)++] = shape;
            }
        }
    }
    
    return results;
}

Shape** visio_parser_find_shapes_by_property(VisioDocument *doc, const char *property_name,
                                             const char *property_value, size_t *count) {
    if (!doc || !property_name || !property_value || !count) {
        error_set(ERROR_INVALID_ARGUMENT, "Invalid arguments to find_shapes_by_property");
        return NULL;
    }
    
    *count = 0;
    size_t capacity = 10;
    Shape **results = (Shape **)malloc(sizeof(Shape *) * capacity);
    if (!results) {
        error_set(ERROR_OUT_OF_MEMORY, "Failed to allocate results");
        return NULL;
    }
    
    for (size_t i = 0; i < doc->pages_count; i++) {
        for (size_t j = 0; j < doc->pages[i]->shapes_count; j++) {
            Shape *shape = doc->pages[i]->shapes[j];
            const char *value = shape_get_property(shape, property_name);
            if (value && strcmp(value, property_value) == 0) {
                if (*count >= capacity) {
                    capacity *= 2;
                    Shape **new_results = (Shape **)realloc(results, sizeof(Shape *) * capacity);
                    if (!new_results) {
                        free(results);
                        error_set(ERROR_OUT_OF_MEMORY, "Failed to resize results");
                        return NULL;
                    }
                    results = new_results;
                }
                results[(*count)++] = shape;
            }
        }
    }
    
    return results;
}

Connector** visio_parser_get_outgoing_connectors(VisioDocument *doc, const Shape *shape, size_t *count) {
    if (!doc || !shape || !count) {
        error_set(ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return NULL;
    }
    
    *count = 0;
    size_t capacity = 10;
    Connector **results = (Connector **)malloc(sizeof(Connector *) * capacity);
    if (!results) {
        error_set(ERROR_OUT_OF_MEMORY, "Failed to allocate results");
        return NULL;
    }
    
    Page *page = doc->pages[shape->page_index];
    for (size_t i = 0; i < page->connectors_count; i++) {
        if (strcmp(page->connectors[i]->from_shape_id, shape->id) == 0) {
            if (*count >= capacity) {
                capacity *= 2;
                Connector **new_results = (Connector **)realloc(results, sizeof(Connector *) * capacity);
                if (!new_results) {
                    free(results);
                    error_set(ERROR_OUT_OF_MEMORY, "Failed to resize results");
                    return NULL;
                }
                results = new_results;
            }
            results[(*count)++] = page->connectors[i];
        }
    }
    
    return results;
}

Connector** visio_parser_get_incoming_connectors(VisioDocument *doc, const Shape *shape, size_t *count) {
    if (!doc || !shape || !count) {
        error_set(ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return NULL;
    }
    
    *count = 0;
    size_t capacity = 10;
    Connector **results = (Connector **)malloc(sizeof(Connector *) * capacity);
    if (!results) {
        error_set(ERROR_OUT_OF_MEMORY, "Failed to allocate results");
        return NULL;
    }
    
    Page *page = doc->pages[shape->page_index];
    for (size_t i = 0; i < page->connectors_count; i++) {
        if (strcmp(page->connectors[i]->to_shape_id, shape->id) == 0) {
            if (*count >= capacity) {
                capacity *= 2;
                Connector **new_results = (Connector **)realloc(results, sizeof(Connector *) * capacity);
                if (!new_results) {
                    free(results);
                    error_set(ERROR_OUT_OF_MEMORY, "Failed to resize results");
                    return NULL;
                }
                results = new_results;
            }
            results[(*count)++] = page->connectors[i];
        }
    }
    
    return results;
}

Shape* visio_parser_get_parent(VisioDocument *doc, const Shape *shape) {
    if (!doc || !shape || !shape->parent_id) return NULL;
    return visio_parser_find_shape_by_id(doc, shape->parent_id);
}

Shape** visio_parser_get_children(VisioDocument *doc, const Shape *shape, size_t *count) {
    if (!doc || !shape || !count) {
        error_set(ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return NULL;
    }
    
    if (shape->children_count == 0) {
        *count = 0;
        return (Shape **)malloc(sizeof(Shape *)); /* Empty array */
    }
    
    Shape **results = (Shape **)malloc(sizeof(Shape *) * shape->children_count);
    if (!results) {
        error_set(ERROR_OUT_OF_MEMORY, "Failed to allocate results");
        return NULL;
    }
    
    *count = 0;
    for (size_t i = 0; i < shape->children_count; i++) {
        Shape *child = visio_parser_find_shape_by_id(doc, shape->children_ids[i]);
        if (child) {
            results[(*count)++] = child;
        }
    }
    
    return results;
}

/* ============================================================================
 * CREATION OPERATIONS
 * ============================================================================ */

Shape* visio_parser_create_shape(VisioDocument *doc, size_t page_index, const char *shape_id) {
    if (!doc || page_index >= doc->pages_count || !shape_id) {
        error_set(ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return NULL;
    }
    
    Shape *shape = shape_create(shape_id);
    if (!shape) return NULL;
    
    if (page_add_shape(doc->pages[page_index], shape) < 0) {
        shape_free(shape);
        return NULL;
    }
    
    return shape;
}

Connector* visio_parser_create_connector(VisioDocument *doc, size_t page_index,
                                        const char *connector_id,
                                        const char *from_shape_id,
                                        const char *to_shape_id) {
    if (!doc || page_index >= doc->pages_count || !connector_id) {
        error_set(ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return NULL;
    }
    
    Connector *conn = connector_create(connector_id, from_shape_id, to_shape_id);
    if (!conn) return NULL;
    
    if (page_add_connector(doc->pages[page_index], conn) < 0) {
        connector_free(conn);
        return NULL;
    }
    
    return conn;
}

int visio_parser_remove_shape(VisioDocument *doc, const char *shape_id) {
    if (!doc || !shape_id) {
        error_set(ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return -1;
    }
    
    /* Remove from all pages */
    for (size_t i = 0; i < doc->pages_count; i++) {
        Page *page = doc->pages[i];
        
        /* Remove the shape if found */
        if (page_find_shape_by_id(page, shape_id)) {
            page_remove_shape(page, shape_id);
            
            /* Remove all connectors connected to this shape */
            for (size_t j = 0; j < page->connectors_count; ) {
                Connector *conn = page->connectors[j];
                if (strcmp(conn->from_shape_id, shape_id) == 0 ||
                    strcmp(conn->to_shape_id, shape_id) == 0) {
                    page_remove_connector(page, conn->id);
                } else {
                    j++;
                }
            }
            
            return 0;
        }
    }
    
    error_set(ERROR_NOT_FOUND, "Shape not found");
    return -1;
}

int visio_parser_remove_connector(VisioDocument *doc, const char *connector_id) {
    if (!doc || !connector_id) {
        error_set(ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return -1;
    }
    
    for (size_t i = 0; i < doc->pages_count; i++) {
        if (page_find_connector_by_id(doc->pages[i], connector_id)) {
            return page_remove_connector(doc->pages[i], connector_id);
        }
    }
    
    error_set(ERROR_NOT_FOUND, "Connector not found");
    return -1;
}

Page* visio_parser_create_page(VisioDocument *doc, const char *page_name) {
    if (!doc || !page_name) {
        error_set(ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return NULL;
    }
    
    /* Generate page ID */
    char page_id[64];
    snprintf(page_id, sizeof(page_id), "Page-%zu", doc->pages_count + 1);
    
    Page *page = page_create(page_name, page_id);
    if (!page) return NULL;
    
    if (document_add_page(doc, page) < 0) {
        page_free(page);
        return NULL;
    }
    
    return page;
}

/* ============================================================================
 * CLONING OPERATIONS
 * ============================================================================ */

Shape* visio_parser_clone_shape(const Shape *source, const char *new_id) {
    if (!source || !new_id) {
        error_set(ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return NULL;
    }
    
    Shape *clone = shape_create(new_id);
    if (!clone) return NULL;
    
    if (source->text) shape_set_text(clone, source->text);
    if (source->type) shape_set_type(clone, source->type);
    
    shape_set_position(clone, source->position.x, source->position.y);
    shape_set_size(clone, source->size.width, source->size.height);
    
    if (source->parent_id) shape_set_parent(clone, source->parent_id);
    clone->is_group = source->is_group;
    
    /* Copy properties */
    for (size_t i = 0; i < source->properties->count; i++) {
        shape_add_property(clone, source->properties->items[i].name, source->properties->items[i].value);
    }
    
    return clone;
}

Connector* visio_parser_clone_connector(const Connector *source, const char *new_id,
                                       const char *new_from_id, const char *new_to_id) {
    if (!source || !new_id) {
        error_set(ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return NULL;
    }
    
    Connector *clone = connector_create(new_id, new_from_id, new_to_id);
    if (!clone) return NULL;
    
    if (source->text) connector_set_text(clone, source->text);
    
    /* Copy properties */
    for (size_t i = 0; i < source->properties->count; i++) {
        connector_add_property(clone, source->properties->items[i].name, source->properties->items[i].value);
    }
    
    return clone;
}

Page* visio_parser_clone_page(const Page *source, const char *new_name) {
    if (!source || !new_name) {
        error_set(ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return NULL;
    }
    
    char page_id[64];
    snprintf(page_id, sizeof(page_id), "%s-Clone", source->id);
    
    Page *clone = page_create(new_name, page_id);
    if (!clone) return NULL;
    
    /* Clone all shapes */
    for (size_t i = 0; i < source->shapes_count; i++) {
        Shape *cloned_shape = shape_clone(source->shapes[i]);
        if (!cloned_shape || page_add_shape(clone, cloned_shape) < 0) {
            page_free(clone);
            return NULL;
        }
    }
    
    /* Clone all connectors */
    for (size_t i = 0; i < source->connectors_count; i++) {
        Connector *cloned_conn = connector_clone(source->connectors[i]);
        if (!cloned_conn || page_add_connector(clone, cloned_conn) < 0) {
            page_free(clone);
            return NULL;
        }
    }
    
    return clone;
}

/* ============================================================================
 * TEMPLATE OPERATIONS
 * ============================================================================ */

VisioDocument* visio_parser_from_template(const char *template_path, const char *output_filename) {
    if (!template_path || !output_filename) {
        error_set(ERROR_INVALID_ARGUMENT, "Template path and output filename required");
        return NULL;
    }
    
    /* TODO: Load template and create new document from it */
    error_set(ERROR_FILE_NOT_FOUND, "Template loading not yet implemented");
    return NULL;
}

VisioDocument* visio_parser_from_json(const char *json_spec, const char *output_filename) {
    if (!json_spec || !output_filename) {
        error_set(ERROR_INVALID_ARGUMENT, "JSON spec and output filename required");
        return NULL;
    }
    
    /* TODO: Parse JSON and create document */
    error_set(ERROR_PARSE_ERROR, "JSON parsing not yet implemented");
    return NULL;
}

/* ============================================================================
 * MEMORY UTILITIES
 * ============================================================================ */

void visio_parser_free_shape_array(Shape **results, size_t count) {
    /* Note: We do NOT free individual shapes, as they are owned by the document */
    free(results);
}

void visio_parser_free_connector_array(Connector **results, size_t count) {
    /* Note: We do NOT free individual connectors, as they are owned by the document */
    free(results);
}

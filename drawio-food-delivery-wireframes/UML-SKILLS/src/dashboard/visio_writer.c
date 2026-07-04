/**
 * @file visio_writer.c
 * @brief Visio file writing and modification implementation
 * 
 * Uses libvisio2 for writing .vsdx files
 */

#include "../include/dashboard/visio_writer.h"
#include "../include/dashboard/visio_parser.h"
#include "../include/dashboard/errors.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

/* ============================================================================
 * SAVE OPERATIONS
 * ============================================================================ */

int visio_writer_save(VisioDocument *doc, const char *filepath) {
    if (!doc || !filepath) {
        error_set(ERROR_INVALID_ARGUMENT, "Document and filepath cannot be NULL");
        return -1;
    }
    
    /* TODO: Implement actual libvisio2 serialization */
    error_set(ERROR_FILE_WRITE, "libvisio2 write not yet implemented");
    return -1;
}

int visio_writer_save_page(Page *page, const char *filepath) {
    if (!page || !filepath) {
        error_set(ERROR_INVALID_ARGUMENT, "Page and filepath cannot be NULL");
        return -1;
    }
    
    /* Create temporary document */
    VisioDocument *doc = document_create(filepath);
    if (!doc) return -1;
    
    /* Clone the page and add to document */
    Page *cloned_page = visio_parser_clone_page(page, page->name);
    if (!cloned_page || document_add_page(doc, cloned_page) < 0) {
        document_free(doc);
        return -1;
    }
    
    /* Save the document */
    int result = visio_writer_save(doc, filepath);
    document_free(doc);
    return result;
}

/* ============================================================================
 * DELETION OPERATIONS
 * ============================================================================ */

int visio_writer_delete_shape(VisioDocument *doc, const char *shape_id) {
    if (!doc || !shape_id) {
        error_set(ERROR_INVALID_ARGUMENT, "Document and shape_id cannot be NULL");
        return -1;
    }
    
    return visio_parser_remove_shape(doc, shape_id);
}

int visio_writer_delete_connector(VisioDocument *doc, const char *connector_id) {
    if (!doc || !connector_id) {
        error_set(ERROR_INVALID_ARGUMENT, "Document and connector_id cannot be NULL");
        return -1;
    }
    
    return visio_parser_remove_connector(doc, connector_id);
}

int visio_writer_delete_shapes_by_type(VisioDocument *doc, const char *shape_type) {
    if (!doc || !shape_type) {
        error_set(ERROR_INVALID_ARGUMENT, "Document and shape_type cannot be NULL");
        return -1;
    }
    
    size_t count = 0;
    Shape **shapes = visio_parser_find_shapes_by_type(doc, shape_type, &count);
    if (!shapes) return -1;
    
    int deleted = 0;
    for (size_t i = 0; i < count; i++) {
        if (visio_parser_remove_shape(doc, shapes[i]->id) == 0) {
            deleted++;
        }
    }
    
    free(shapes);
    return deleted;
}

int visio_writer_delete_shapes_by_text(VisioDocument *doc, const char *text_pattern) {
    if (!doc || !text_pattern) {
        error_set(ERROR_INVALID_ARGUMENT, "Document and text_pattern cannot be NULL");
        return -1;
    }
    
    size_t count = 0;
    Shape **shapes = visio_parser_find_shapes_by_text(doc, text_pattern, &count);
    if (!shapes) return -1;
    
    int deleted = 0;
    for (size_t i = 0; i < count; i++) {
        if (visio_parser_remove_shape(doc, shapes[i]->id) == 0) {
            deleted++;
        }
    }
    
    free(shapes);
    return deleted;
}

/* ============================================================================
 * BATCH OPERATIONS
 * ============================================================================ */

int visio_writer_batch_update_by_type(VisioDocument *doc, const char *shape_type,
                                      const Property *updates, size_t update_count) {
    if (!doc || !shape_type || !updates) {
        error_set(ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return -1;
    }
    
    size_t count = 0;
    Shape **shapes = visio_parser_find_shapes_by_type(doc, shape_type, &count);
    if (!shapes) return -1;
    
    int updated = 0;
    for (size_t i = 0; i < count; i++) {
        for (size_t j = 0; j < update_count; j++) {
            if (shape_add_property(shapes[i], updates[j].name, updates[j].value) == 0) {
                updated++;
            }
        }
    }
    
    free(shapes);
    return updated;
}

int visio_writer_batch_update_by_property(VisioDocument *doc,
                                          const char *filter_prop,
                                          const char *filter_value,
                                          const Property *updates,
                                          size_t update_count) {
    if (!doc || !filter_prop || !filter_value || !updates) {
        error_set(ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return -1;
    }
    
    size_t count = 0;
    Shape **shapes = visio_parser_find_shapes_by_property(doc, filter_prop, filter_value, &count);
    if (!shapes) return -1;
    
    int updated = 0;
    for (size_t i = 0; i < count; i++) {
        for (size_t j = 0; j < update_count; j++) {
            if (shape_add_property(shapes[i], updates[j].name, updates[j].value) == 0) {
                updated++;
            }
        }
    }
    
    free(shapes);
    return updated;
}

int visio_writer_update_all_shapes(VisioDocument *doc,
                                   const char *property_name,
                                   const char *property_value) {
    if (!doc || !property_name || !property_value) {
        error_set(ERROR_INVALID_ARGUMENT, "Invalid arguments");
        return -1;
    }
    
    int updated = 0;
    for (size_t i = 0; i < doc->pages_count; i++) {
        for (size_t j = 0; j < doc->pages[i]->shapes_count; j++) {
            if (shape_add_property(doc->pages[i]->shapes[j], property_name, property_value) == 0) {
                updated++;
            }
        }
    }
    
    return updated;
}

/* ============================================================================
 * COPY/TEMPLATE OPERATIONS
 * ============================================================================ */

int visio_writer_copy_shapes(Page *src_page, Page *dest_page) {
    if (!src_page || !dest_page) {
        error_set(ERROR_INVALID_ARGUMENT, "Pages cannot be NULL");
        return -1;
    }
    
    for (size_t i = 0; i < src_page->shapes_count; i++) {
        Shape *cloned = shape_clone(src_page->shapes[i]);
        if (!cloned || page_add_shape(dest_page, cloned) < 0) {
            if (cloned) shape_free(cloned);
            return -1;
        }
    }
    
    return 0;
}

int visio_writer_duplicate_shape(Page *page, const char *source_shape_id,
                                size_t count, double offset_x, double offset_y) {
    if (!page || !source_shape_id) {
        error_set(ERROR_INVALID_ARGUMENT, "Page and source_shape_id cannot be NULL");
        return -1;
    }
    
    Shape *source = page_find_shape_by_id(page, source_shape_id);
    if (!source) {
        error_set(ERROR_NOT_FOUND, "Shape not found");
        return -1;
    }
    
    int created = 0;
    for (size_t i = 0; i < count; i++) {
        char new_id[64];
        snprintf(new_id, sizeof(new_id), "%s-Copy%zu", source_shape_id, i + 1);
        
        Shape *copy = shape_clone(source);
        if (!copy) continue;
        
        strcpy(copy->id, new_id);
        copy->position.x += offset_x;
        copy->position.y += offset_y;
        
        if (page_add_shape(page, copy) == 0) {
            created++;
        } else {
            shape_free(copy);
        }
    }
    
    return created;
}

/* ============================================================================
 * VALIDATION & INTEGRITY
 * ============================================================================ */

int visio_writer_validate(VisioDocument *doc) {
    if (!doc) {
        error_set(ERROR_INVALID_ARGUMENT, "Document cannot be NULL");
        return 1;
    }
    
    int errors = 0;
    
    /* Check for duplicate shape IDs */
    for (size_t i = 0; i < doc->pages_count; i++) {
        for (size_t j = 0; j < doc->pages[i]->shapes_count; j++) {
            const char *id = doc->pages[i]->shapes[j]->id;
            
            /* Check within same page */
            for (size_t k = j + 1; k < doc->pages[i]->shapes_count; k++) {
                if (strcmp(id, doc->pages[i]->shapes[k]->id) == 0) {
                    errors++;
                }
            }
        }
    }
    
    /* Check for orphaned connectors */
    for (size_t i = 0; i < doc->pages_count; i++) {
        for (size_t j = 0; j < doc->pages[i]->connectors_count; j++) {
            Connector *conn = doc->pages[i]->connectors[j];
            
            if (!page_find_shape_by_id(doc->pages[i], conn->from_shape_id)) {
                errors++;
            }
            if (!page_find_shape_by_id(doc->pages[i], conn->to_shape_id)) {
                errors++;
            }
        }
    }
    
    return errors;
}

char* visio_writer_generate_shape_id(VisioDocument *doc, const char *prefix) {
    if (!doc || !prefix) {
        error_set(ERROR_INVALID_ARGUMENT, "Document and prefix cannot be NULL");
        return NULL;
    }
    
    char *id = (char *)malloc(64);
    if (!id) {
        error_set(ERROR_OUT_OF_MEMORY, "Failed to allocate ID");
        return NULL;
    }
    
    size_t counter = 1;
    while (1) {
        snprintf(id, 64, "%s%zu", prefix, counter);
        
        /* Check if ID already exists */
        if (!visio_parser_find_shape_by_id(doc, id)) {
            return id;
        }
        counter++;
        
        if (counter > 10000) {
            error_set(ERROR_INVALID_ARGUMENT, "Could not generate unique ID");
            free(id);
            return NULL;
        }
    }
}

char* visio_writer_generate_connector_id(VisioDocument *doc, const char *prefix) {
    if (!doc || !prefix) {
        error_set(ERROR_INVALID_ARGUMENT, "Document and prefix cannot be NULL");
        return NULL;
    }
    
    char *id = (char *)malloc(64);
    if (!id) {
        error_set(ERROR_OUT_OF_MEMORY, "Failed to allocate ID");
        return NULL;
    }
    
    size_t counter = 1;
    while (1) {
        snprintf(id, 64, "%s%zu", prefix, counter);
        
        /* Check if ID already exists in any page */
        int found = 0;
        for (size_t i = 0; i < doc->pages_count; i++) {
            if (page_find_connector_by_id(doc->pages[i], id)) {
                found = 1;
                break;
            }
        }
        
        if (!found) {
            return id;
        }
        counter++;
        
        if (counter > 10000) {
            error_set(ERROR_INVALID_ARGUMENT, "Could not generate unique ID");
            free(id);
            return NULL;
        }
    }
}

/* ============================================================================
 * EXPORT OPERATIONS (Stubs)
 * ============================================================================ */

int visio_writer_export_svg(VisioDocument *doc, const char *filepath) {
    if (!doc || !filepath) {
        error_set(ERROR_INVALID_ARGUMENT, "Document and filepath cannot be NULL");
        return -1;
    }
    
    /* TODO: Implement SVG export */
    error_set(ERROR_FILE_WRITE, "SVG export not yet implemented");
    return -1;
}

int visio_writer_export_pdf(VisioDocument *doc, const char *filepath) {
    if (!doc || !filepath) {
        error_set(ERROR_INVALID_ARGUMENT, "Document and filepath cannot be NULL");
        return -1;
    }
    
    /* TODO: Implement PDF export */
    error_set(ERROR_FILE_WRITE, "PDF export not yet implemented");
    return -1;
}

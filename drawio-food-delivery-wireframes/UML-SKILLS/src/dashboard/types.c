/**
 * @file types.c
 * @brief Implementation of core data structures
 */

#include "../include/dashboard/types.h"
#include "../include/dashboard/errors.h"
#include "../include/dashboard/config.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

/* ============================================================================
 * PROPERTY LIST IMPLEMENTATION
 * ============================================================================ */

PropertyList* property_list_create(void) {
    PropertyList *list = (PropertyList *)malloc(sizeof(PropertyList));
    if (!list) {
        error_set(ERROR_OUT_OF_MEMORY, "Failed to allocate PropertyList");
        return NULL;
    }
    
    list->capacity = CONFIG_INITIAL_PROPERTY_CAPACITY;
    list->count = 0;
    list->items = (Property *)malloc(sizeof(Property) * list->capacity);
    
    if (!list->items) {
        error_set(ERROR_OUT_OF_MEMORY, "Failed to allocate property items");
        free(list);
        return NULL;
    }
    
    return list;
}

int property_list_add(PropertyList *list, const char *name, const char *value) {
    if (!list || !name || !value) {
        error_set(ERROR_INVALID_ARGUMENT, "NULL pointer in property_list_add");
        return -1;
    }
    
    /* Resize if needed */
    if (list->count >= list->capacity) {
        size_t new_capacity = list->capacity * CONFIG_GROWTH_FACTOR;
        Property *new_items = (Property *)realloc(list->items, sizeof(Property) * new_capacity);
        
        if (!new_items) {
            error_set(ERROR_OUT_OF_MEMORY, "Failed to resize property list");
            return -1;
        }
        
        list->items = new_items;
        list->capacity = new_capacity;
    }
    
    /* Allocate and copy name */
    list->items[list->count].name = (char *)malloc(strlen(name) + 1);
    if (!list->items[list->count].name) {
        error_set(ERROR_OUT_OF_MEMORY, "Failed to allocate property name");
        return -1;
    }
    strcpy(list->items[list->count].name, name);
    
    /* Allocate and copy value */
    list->items[list->count].value = (char *)malloc(strlen(value) + 1);
    if (!list->items[list->count].value) {
        error_set(ERROR_OUT_OF_MEMORY, "Failed to allocate property value");
        free(list->items[list->count].name);
        return -1;
    }
    strcpy(list->items[list->count].value, value);
    
    list->count++;
    return 0;
}

Property* property_list_get(PropertyList *list, const char *name) {
    if (!list || !name) return NULL;
    
    for (size_t i = 0; i < list->count; i++) {
        if (strcmp(list->items[i].name, name) == 0) {
            return &list->items[i];
        }
    }
    return NULL;
}

void property_list_free(PropertyList *list) {
    if (!list) return;
    
    if (list->items) {
        for (size_t i = 0; i < list->count; i++) {
            free(list->items[i].name);
            free(list->items[i].value);
        }
        free(list->items);
    }
    free(list);
}

/* ============================================================================
 * SHAPE IMPLEMENTATION
 * ============================================================================ */

Shape* shape_create(const char *id) {
    if (!id) {
        error_set(ERROR_INVALID_ARGUMENT, "Shape ID cannot be NULL");
        return NULL;
    }
    
    Shape *shape = (Shape *)malloc(sizeof(Shape));
    if (!shape) {
        error_set(ERROR_OUT_OF_MEMORY, "Failed to allocate Shape");
        return NULL;
    }
    
    /* Initialize all fields */
    shape->id = (char *)malloc(strlen(id) + 1);
    if (!shape->id) {
        error_set(ERROR_OUT_OF_MEMORY, "Failed to allocate shape ID");
        free(shape);
        return NULL;
    }
    strcpy(shape->id, id);
    
    shape->text = NULL;
    shape->type = NULL;
    shape->parent_id = NULL;
    shape->position.x = 0.0;
    shape->position.y = 0.0;
    shape->size.width = 100.0;
    shape->size.height = 50.0;
    shape->is_group = 0;
    shape->page_index = 0;
    shape->children_count = 0;
    shape->children_capacity = CONFIG_INITIAL_CHILDREN_CAPACITY;
    
    shape->children_ids = (char **)malloc(sizeof(char *) * shape->children_capacity);
    if (!shape->children_ids) {
        error_set(ERROR_OUT_OF_MEMORY, "Failed to allocate children array");
        free(shape->id);
        free(shape);
        return NULL;
    }
    
    shape->properties = property_list_create();
    if (!shape->properties) {
        free(shape->children_ids);
        free(shape->id);
        free(shape);
        return NULL;
    }
    
    return shape;
}

int shape_set_text(Shape *shape, const char *text) {
    if (!shape) {
        error_set(ERROR_INVALID_ARGUMENT, "Shape cannot be NULL");
        return -1;
    }
    
    if (shape->text) free(shape->text);
    
    if (text) {
        shape->text = (char *)malloc(strlen(text) + 1);
        if (!shape->text) {
            error_set(ERROR_OUT_OF_MEMORY, "Failed to allocate shape text");
            return -1;
        }
        strcpy(shape->text, text);
    } else {
        shape->text = NULL;
    }
    
    return 0;
}

int shape_set_type(Shape *shape, const char *type) {
    if (!shape || !type) {
        error_set(ERROR_INVALID_ARGUMENT, "Shape or type cannot be NULL");
        return -1;
    }
    
    if (shape->type) free(shape->type);
    
    shape->type = (char *)malloc(strlen(type) + 1);
    if (!shape->type) {
        error_set(ERROR_OUT_OF_MEMORY, "Failed to allocate shape type");
        return -1;
    }
    strcpy(shape->type, type);
    return 0;
}

int shape_set_position(Shape *shape, double x, double y) {
    if (!shape) {
        error_set(ERROR_INVALID_ARGUMENT, "Shape cannot be NULL");
        return -1;
    }
    shape->position.x = x;
    shape->position.y = y;
    return 0;
}

int shape_set_size(Shape *shape, double width, double height) {
    if (!shape) {
        error_set(ERROR_INVALID_ARGUMENT, "Shape cannot be NULL");
        return -1;
    }
    if (width <= 0 || height <= 0) {
        error_set(ERROR_INVALID_ARGUMENT, "Width and height must be positive");
        return -1;
    }
    shape->size.width = width;
    shape->size.height = height;
    return 0;
}

int shape_add_property(Shape *shape, const char *name, const char *value) {
    if (!shape || !name || !value) {
        error_set(ERROR_INVALID_ARGUMENT, "Shape, name, and value cannot be NULL");
        return -1;
    }
    return property_list_add(shape->properties, name, value);
}

const char* shape_get_property(Shape *shape, const char *name) {
    if (!shape || !name) return NULL;
    
    Property *prop = property_list_get(shape->properties, name);
    return prop ? prop->value : NULL;
}

int shape_set_parent(Shape *shape, const char *parent_id) {
    if (!shape) {
        error_set(ERROR_INVALID_ARGUMENT, "Shape cannot be NULL");
        return -1;
    }
    
    if (shape->parent_id) free(shape->parent_id);
    
    if (parent_id) {
        shape->parent_id = (char *)malloc(strlen(parent_id) + 1);
        if (!shape->parent_id) {
            error_set(ERROR_OUT_OF_MEMORY, "Failed to allocate parent ID");
            return -1;
        }
        strcpy(shape->parent_id, parent_id);
    } else {
        shape->parent_id = NULL;
    }
    
    return 0;
}

int shape_add_child(Shape *shape, const char *child_id) {
    if (!shape || !child_id) {
        error_set(ERROR_INVALID_ARGUMENT, "Shape and child_id cannot be NULL");
        return -1;
    }
    
    /* Resize if needed */
    if (shape->children_count >= shape->children_capacity) {
        size_t new_capacity = shape->children_capacity * CONFIG_GROWTH_FACTOR;
        char **new_children = (char **)realloc(shape->children_ids, sizeof(char *) * new_capacity);
        
        if (!new_children) {
            error_set(ERROR_OUT_OF_MEMORY, "Failed to resize children array");
            return -1;
        }
        
        shape->children_ids = new_children;
        shape->children_capacity = new_capacity;
    }
    
    shape->children_ids[shape->children_count] = (char *)malloc(strlen(child_id) + 1);
    if (!shape->children_ids[shape->children_count]) {
        error_set(ERROR_OUT_OF_MEMORY, "Failed to allocate child ID");
        return -1;
    }
    
    strcpy(shape->children_ids[shape->children_count], child_id);
    shape->children_count++;
    return 0;
}

const char* shape_get_child(Shape *shape, size_t index) {
    if (!shape || index >= shape->children_count) return NULL;
    return shape->children_ids[index];
}

void shape_set_group(Shape *shape, int is_group) {
    if (shape) {
        shape->is_group = is_group ? 1 : 0;
    }
}

Shape* shape_clone(const Shape *source) {
    if (!source) {
        error_set(ERROR_INVALID_ARGUMENT, "Source shape cannot be NULL");
        return NULL;
    }
    
    Shape *clone = shape_create(source->id);
    if (!clone) return NULL;
    
    if (source->text && shape_set_text(clone, source->text) < 0) goto cleanup;
    if (source->type && shape_set_type(clone, source->type) < 0) goto cleanup;
    
    shape_set_position(clone, source->position.x, source->position.y);
    shape_set_size(clone, source->size.width, source->size.height);
    
    if (source->parent_id && shape_set_parent(clone, source->parent_id) < 0) goto cleanup;
    
    clone->is_group = source->is_group;
    clone->page_index = source->page_index;
    
    /* Copy properties */
    for (size_t i = 0; i < source->properties->count; i++) {
        if (property_list_add(clone->properties, 
                            source->properties->items[i].name,
                            source->properties->items[i].value) < 0) {
            goto cleanup;
        }
    }
    
    /* Copy children */
    for (size_t i = 0; i < source->children_count; i++) {
        if (shape_add_child(clone, source->children_ids[i]) < 0) {
            goto cleanup;
        }
    }
    
    return clone;

cleanup:
    shape_free(clone);
    return NULL;
}

void shape_free(Shape *shape) {
    if (!shape) return;
    
    free(shape->id);
    free(shape->text);
    free(shape->type);
    free(shape->parent_id);
    
    if (shape->children_ids) {
        for (size_t i = 0; i < shape->children_count; i++) {
            free(shape->children_ids[i]);
        }
        free(shape->children_ids);
    }
    
    property_list_free(shape->properties);
    free(shape);
}

/* ============================================================================
 * CONNECTOR IMPLEMENTATION
 * ============================================================================ */

Connector* connector_create(const char *id, const char *from_id, const char *to_id) {
    if (!id || !from_id || !to_id) {
        error_set(ERROR_INVALID_ARGUMENT, "Connector IDs cannot be NULL");
        return NULL;
    }
    
    Connector *conn = (Connector *)malloc(sizeof(Connector));
    if (!conn) {
        error_set(ERROR_OUT_OF_MEMORY, "Failed to allocate Connector");
        return NULL;
    }
    
    conn->id = (char *)malloc(strlen(id) + 1);
    conn->from_shape_id = (char *)malloc(strlen(from_id) + 1);
    conn->to_shape_id = (char *)malloc(strlen(to_id) + 1);
    
    if (!conn->id || !conn->from_shape_id || !conn->to_shape_id) {
        error_set(ERROR_OUT_OF_MEMORY, "Failed to allocate connector fields");
        free(conn->id);
        free(conn->from_shape_id);
        free(conn->to_shape_id);
        free(conn);
        return NULL;
    }
    
    strcpy(conn->id, id);
    strcpy(conn->from_shape_id, from_id);
    strcpy(conn->to_shape_id, to_id);
    
    conn->text = NULL;
    conn->page_index = 0;
    
    conn->properties = property_list_create();
    if (!conn->properties) {
        free(conn->id);
        free(conn->from_shape_id);
        free(conn->to_shape_id);
        free(conn);
        return NULL;
    }
    
    return conn;
}

int connector_set_text(Connector *conn, const char *text) {
    if (!conn) {
        error_set(ERROR_INVALID_ARGUMENT, "Connector cannot be NULL");
        return -1;
    }
    
    if (conn->text) free(conn->text);
    
    if (text) {
        conn->text = (char *)malloc(strlen(text) + 1);
        if (!conn->text) {
            error_set(ERROR_OUT_OF_MEMORY, "Failed to allocate connector text");
            return -1;
        }
        strcpy(conn->text, text);
    } else {
        conn->text = NULL;
    }
    
    return 0;
}

int connector_add_property(Connector *conn, const char *name, const char *value) {
    if (!conn || !name || !value) {
        error_set(ERROR_INVALID_ARGUMENT, "Connector, name, and value cannot be NULL");
        return -1;
    }
    return property_list_add(conn->properties, name, value);
}

const char* connector_get_property(Connector *conn, const char *name) {
    if (!conn || !name) return NULL;
    
    Property *prop = property_list_get(conn->properties, name);
    return prop ? prop->value : NULL;
}

Connector* connector_clone(const Connector *source) {
    if (!source) {
        error_set(ERROR_INVALID_ARGUMENT, "Source connector cannot be NULL");
        return NULL;
    }
    
    Connector *clone = connector_create(source->id, source->from_shape_id, source->to_shape_id);
    if (!clone) return NULL;
    
    if (source->text && connector_set_text(clone, source->text) < 0) {
        connector_free(clone);
        return NULL;
    }
    
    clone->page_index = source->page_index;
    
    /* Copy properties */
    for (size_t i = 0; i < source->properties->count; i++) {
        if (property_list_add(clone->properties,
                            source->properties->items[i].name,
                            source->properties->items[i].value) < 0) {
            connector_free(clone);
            return NULL;
        }
    }
    
    return clone;
}

void connector_free(Connector *conn) {
    if (!conn) return;
    
    free(conn->id);
    free(conn->from_shape_id);
    free(conn->to_shape_id);
    free(conn->text);
    property_list_free(conn->properties);
    free(conn);
}

/* ============================================================================
 * PAGE IMPLEMENTATION
 * ============================================================================ */

Page* page_create(const char *name, const char *id) {
    if (!name || !id) {
        error_set(ERROR_INVALID_ARGUMENT, "Page name and ID cannot be NULL");
        return NULL;
    }
    
    Page *page = (Page *)malloc(sizeof(Page));
    if (!page) {
        error_set(ERROR_OUT_OF_MEMORY, "Failed to allocate Page");
        return NULL;
    }
    
    page->name = (char *)malloc(strlen(name) + 1);
    page->id = (char *)malloc(strlen(id) + 1);
    
    if (!page->name || !page->id) {
        error_set(ERROR_OUT_OF_MEMORY, "Failed to allocate page fields");
        free(page->name);
        free(page->id);
        free(page);
        return NULL;
    }
    
    strcpy(page->name, name);
    strcpy(page->id, id);
    
    page->page_index = 0;
    page->shapes_count = 0;
    page->shapes_capacity = CONFIG_INITIAL_SHAPES_CAPACITY;
    page->connectors_count = 0;
    page->connectors_capacity = CONFIG_INITIAL_CONNECTORS_CAPACITY;
    
    page->shapes = (Shape **)malloc(sizeof(Shape *) * page->shapes_capacity);
    page->connectors = (Connector **)malloc(sizeof(Connector *) * page->connectors_capacity);
    
    if (!page->shapes || !page->connectors) {
        error_set(ERROR_OUT_OF_MEMORY, "Failed to allocate shape/connector arrays");
        free(page->name);
        free(page->id);
        free(page->shapes);
        free(page->connectors);
        free(page);
        return NULL;
    }
    
    return page;
}

int page_add_shape(Page *page, Shape *shape) {
    if (!page || !shape) {
        error_set(ERROR_INVALID_ARGUMENT, "Page and shape cannot be NULL");
        return -1;
    }
    
    if (page->shapes_count >= page->shapes_capacity) {
        size_t new_capacity = page->shapes_capacity * CONFIG_GROWTH_FACTOR;
        Shape **new_shapes = (Shape **)realloc(page->shapes, sizeof(Shape *) * new_capacity);
        
        if (!new_shapes) {
            error_set(ERROR_OUT_OF_MEMORY, "Failed to resize shapes array");
            return -1;
        }
        
        page->shapes = new_shapes;
        page->shapes_capacity = new_capacity;
    }
    
    page->shapes[page->shapes_count] = shape;
    shape->page_index = page->page_index;
    page->shapes_count++;
    return 0;
}

int page_add_connector(Page *page, Connector *conn) {
    if (!page || !conn) {
        error_set(ERROR_INVALID_ARGUMENT, "Page and connector cannot be NULL");
        return -1;
    }
    
    if (page->connectors_count >= page->connectors_capacity) {
        size_t new_capacity = page->connectors_capacity * CONFIG_GROWTH_FACTOR;
        Connector **new_connectors = (Connector **)realloc(page->connectors,
                                                          sizeof(Connector *) * new_capacity);
        
        if (!new_connectors) {
            error_set(ERROR_OUT_OF_MEMORY, "Failed to resize connectors array");
            return -1;
        }
        
        page->connectors = new_connectors;
        page->connectors_capacity = new_capacity;
    }
    
    page->connectors[page->connectors_count] = conn;
    conn->page_index = page->page_index;
    page->connectors_count++;
    return 0;
}

Shape* page_find_shape_by_id(Page *page, const char *shape_id) {
    if (!page || !shape_id) return NULL;
    
    for (size_t i = 0; i < page->shapes_count; i++) {
        if (strcmp(page->shapes[i]->id, shape_id) == 0) {
            return page->shapes[i];
        }
    }
    return NULL;
}

Connector* page_find_connector_by_id(Page *page, const char *connector_id) {
    if (!page || !connector_id) return NULL;
    
    for (size_t i = 0; i < page->connectors_count; i++) {
        if (strcmp(page->connectors[i]->id, connector_id) == 0) {
            return page->connectors[i];
        }
    }
    return NULL;
}

int page_remove_shape(Page *page, const char *shape_id) {
    if (!page || !shape_id) {
        error_set(ERROR_INVALID_ARGUMENT, "Page and shape_id cannot be NULL");
        return -1;
    }
    
    for (size_t i = 0; i < page->shapes_count; i++) {
        if (strcmp(page->shapes[i]->id, shape_id) == 0) {
            /* Shift remaining shapes */
            for (size_t j = i; j < page->shapes_count - 1; j++) {
                page->shapes[j] = page->shapes[j + 1];
            }
            page->shapes_count--;
            return 0;
        }
    }
    return -1;
}

int page_remove_connector(Page *page, const char *connector_id) {
    if (!page || !connector_id) {
        error_set(ERROR_INVALID_ARGUMENT, "Page and connector_id cannot be NULL");
        return -1;
    }
    
    for (size_t i = 0; i < page->connectors_count; i++) {
        if (strcmp(page->connectors[i]->id, connector_id) == 0) {
            /* Shift remaining connectors */
            for (size_t j = i; j < page->connectors_count - 1; j++) {
                page->connectors[j] = page->connectors[j + 1];
            }
            page->connectors_count--;
            return 0;
        }
    }
    return -1;
}

void page_free(Page *page) {
    if (!page) return;
    
    free(page->name);
    free(page->id);
    
    if (page->shapes) {
        for (size_t i = 0; i < page->shapes_count; i++) {
            shape_free(page->shapes[i]);
        }
        free(page->shapes);
    }
    
    if (page->connectors) {
        for (size_t i = 0; i < page->connectors_count; i++) {
            connector_free(page->connectors[i]);
        }
        free(page->connectors);
    }
    
    free(page);
}

/* ============================================================================
 * DOCUMENT IMPLEMENTATION
 * ============================================================================ */

VisioDocument* document_create(const char *filename) {
    if (!filename) {
        error_set(ERROR_INVALID_ARGUMENT, "Filename cannot be NULL");
        return NULL;
    }
    
    VisioDocument *doc = (VisioDocument *)malloc(sizeof(VisioDocument));
    if (!doc) {
        error_set(ERROR_OUT_OF_MEMORY, "Failed to allocate VisioDocument");
        return NULL;
    }
    
    doc->filename = (char *)malloc(strlen(filename) + 1);
    if (!doc->filename) {
        error_set(ERROR_OUT_OF_MEMORY, "Failed to allocate filename");
        free(doc);
        return NULL;
    }
    
    strcpy(doc->filename, filename);
    
    doc->pages_count = 0;
    doc->pages_capacity = CONFIG_INITIAL_PAGES_CAPACITY;
    doc->creator = NULL;
    doc->created = NULL;
    doc->modified = NULL;
    
    doc->pages = (Page **)malloc(sizeof(Page *) * doc->pages_capacity);
    if (!doc->pages) {
        error_set(ERROR_OUT_OF_MEMORY, "Failed to allocate pages array");
        free(doc->filename);
        free(doc);
        return NULL;
    }
    
    return doc;
}

int document_add_page(VisioDocument *doc, Page *page) {
    if (!doc || !page) {
        error_set(ERROR_INVALID_ARGUMENT, "Document and page cannot be NULL");
        return -1;
    }
    
    if (doc->pages_count >= doc->pages_capacity) {
        size_t new_capacity = doc->pages_capacity * CONFIG_GROWTH_FACTOR;
        Page **new_pages = (Page **)realloc(doc->pages, sizeof(Page *) * new_capacity);
        
        if (!new_pages) {
            error_set(ERROR_OUT_OF_MEMORY, "Failed to resize pages array");
            return -1;
        }
        
        doc->pages = new_pages;
        doc->pages_capacity = new_capacity;
    }
    
    page->page_index = doc->pages_count;
    doc->pages[doc->pages_count] = page;
    doc->pages_count++;
    return 0;
}

Page* document_get_page(VisioDocument *doc, size_t index) {
    if (!doc || index >= doc->pages_count) return NULL;
    return doc->pages[index];
}

size_t document_total_shapes(VisioDocument *doc) {
    if (!doc) return 0;
    
    size_t total = 0;
    for (size_t i = 0; i < doc->pages_count; i++) {
        total += doc->pages[i]->shapes_count;
    }
    return total;
}

size_t document_total_connectors(VisioDocument *doc) {
    if (!doc) return 0;
    
    size_t total = 0;
    for (size_t i = 0; i < doc->pages_count; i++) {
        total += doc->pages[i]->connectors_count;
    }
    return total;
}

void document_free(VisioDocument *doc) {
    if (!doc) return;
    
    free(doc->filename);
    free(doc->creator);
    free(doc->created);
    free(doc->modified);
    
    if (doc->pages) {
        for (size_t i = 0; i < doc->pages_count; i++) {
            page_free(doc->pages[i]);
        }
        free(doc->pages);
    }
    
    free(doc);
}

#ifndef DASHBOARD_CONFIG_H
#define DASHBOARD_CONFIG_H

/**
 * @file config.h
 * @brief Configuration constants and feature flags for Visio parser
 * 
 * This header defines all configurable constants, memory limits, buffer sizes,
 * and feature flags for the Visio parser system.
 */

/* Version Information */
#define VISIO_PARSER_VERSION "1.0.0"
#define VISIO_PARSER_NAME "Visio Dashboard Parser"

/* Memory Limits */
#define MAX_SHAPES_PER_PAGE 10000
#define MAX_PAGES 100
#define MAX_PROPERTIES_PER_SHAPE 50
#define MAX_CHILDREN_PER_SHAPE 1000
#define MAX_CONNECTORS_PER_PAGE 5000

/* Buffer Sizes */
#define MAX_ID_LENGTH 256
#define MAX_TEXT_LENGTH 4096
#define MAX_PROPERTY_NAME_LENGTH 128
#define MAX_PROPERTY_VALUE_LENGTH 512
#define MAX_PAGE_NAME_LENGTH 256
#define MAX_SHAPE_TYPE_LENGTH 128
#define MAX_ERROR_MESSAGE_LENGTH 512

/* Feature Flags */
#define ENABLE_PROPERTY_EXTRACTION 1
#define ENABLE_HIERARCHY_SUPPORT 1
#define ENABLE_MULTIPAGE_SUPPORT 1
#define ENABLE_JSON_PRETTY_PRINT 1
#define ENABLE_SHAPE_SEARCH 1
#define ENABLE_CONNECTOR_VALIDATION 1

/* Debug & Logging */
#define DEBUG_VERBOSE 0
#define ENABLE_MEMORY_TRACKING 0
#define ENABLE_PERFORMANCE_METRICS 0

/* Allocation Strategy */
#define INITIAL_SHAPES_CAPACITY 100
#define INITIAL_CONNECTORS_CAPACITY 50
#define INITIAL_PROPERTIES_CAPACITY 10
#define INITIAL_CHILDREN_CAPACITY 20
#define INITIAL_PAGES_CAPACITY 5

/* Capacity Growth Factor (1.5x when full) */
#define GROWTH_FACTOR 1.5

/* File I/O */
#define MAX_FILE_PATH_LENGTH 1024
#define JSON_INDENT_SIZE 2

#endif /* DASHBOARD_CONFIG_H */

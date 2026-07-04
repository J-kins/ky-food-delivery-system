#ifndef DASHBOARD_ERRORS_H
#define DASHBOARD_ERRORS_H

/**
 * @file errors.h
 * @brief Error handling and reporting for Visio parser
 * 
 * Provides standardized error codes, error context, and error reporting
 * mechanisms for the Visio parser system.
 */

#include <stdint.h>

/**
 * @enum VisioErrorCode
 * @brief Standard error codes for Visio parser operations
 */
typedef enum {
    VISIO_OK = 0,                      /**< No error, operation successful */
    VISIO_ERR_FILE_NOT_FOUND = 1,      /**< Input file does not exist */
    VISIO_ERR_INVALID_FILE = 2,        /**< File is not a valid .vsdx file */
    VISIO_ERR_PARSE_FAILED = 3,        /**< Failed to parse Visio file */
    VISIO_ERR_MEMORY_ALLOCATION = 4,   /**< Memory allocation failed */
    VISIO_ERR_LIBVISIO_FAILED = 5,     /**< libvisio library error */
    VISIO_ERR_JSON_GENERATION = 6,     /**< JSON generation failed */
    VISIO_ERR_INVALID_ARGUMENT = 7,    /**< Invalid function argument */
    VISIO_ERR_FILE_IO = 8,             /**< File I/O operation failed */
    VISIO_ERR_INTERNAL = 9,            /**< Internal parser error */
    VISIO_ERR_UNKNOWN = 99             /**< Unknown error */
} VisioErrorCode;

/**
 * @struct VisioError
 * @brief Error information and context
 */
typedef struct {
    VisioErrorCode code;               /**< Error code */
    char message[512];                 /**< Error message */
    char *context;                     /**< Additional context information */
    int line;                          /**< Source code line number */
    const char *function;              /**< Function name where error occurred */
} VisioError;

/**
 * @brief Get the last error that occurred
 * 
 * Thread-safe access to the last error in the current thread.
 * 
 * @return Pointer to VisioError structure (never NULL)
 */
VisioError* error_get_last(void);

/**
 * @brief Set an error with code and message
 * 
 * @param code Error code
 * @param message Error message (will be copied)
 * @param function Function name (typically __func__)
 * @param line Line number (typically __LINE__)
 */
void error_set(VisioErrorCode code, const char *message, const char *function, int line);

/**
 * @brief Set error with additional context
 * 
 * @param code Error code
 * @param message Error message
 * @param context Additional context (will be copied)
 * @param function Function name
 * @param line Line number
 */
void error_set_with_context(VisioErrorCode code, const char *message, 
                           const char *context, const char *function, int line);

/**
 * @brief Clear the last error
 */
void error_clear(void);

/**
 * @brief Get human-readable error message for error code
 * 
 * @param code Error code
 * @return String description of error code
 */
const char* error_get_message(VisioErrorCode code);

/**
 * @brief Print last error to stderr
 * 
 * Prints error code, message, context, and location information.
 */
void error_print(void);

/**
 * @brief Print formatted error message to stderr
 * 
 * @param format Printf-style format string
 * @param ... Format arguments
 */
void error_printf(const char *format, ...);

/**
 * @brief Check if last error is fatal
 * 
 * @return 1 if fatal (memory, file not found, etc.), 0 if recoverable
 */
int error_is_fatal(void);

/**
 * @brief Convenience macros for error setting
 */
#define ERROR_SET(code, msg) \
    error_set(code, msg, __func__, __LINE__)

#define ERROR_SET_CONTEXT(code, msg, ctx) \
    error_set_with_context(code, msg, ctx, __func__, __LINE__)

#endif /* DASHBOARD_ERRORS_H */

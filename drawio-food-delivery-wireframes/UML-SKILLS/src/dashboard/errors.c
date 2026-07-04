/**
 * @file errors.c
 * @brief Error handling implementation
 */

#include "../include/dashboard/errors.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <pthread.h>

/* Thread-local error context storage */
static pthread_key_t error_key;
static pthread_once_t error_once = PTHREAD_ONCE_INIT;

typedef struct {
    int code;
    char message[ERROR_MESSAGE_MAX];
} ErrorContext;

static void error_destructor(void *ctx) {
    free(ctx);
}

static void error_key_init(void) {
    pthread_key_create(&error_key, error_destructor);
}

static ErrorContext* get_error_context(void) {
    pthread_once(&error_once, error_key_init);
    
    ErrorContext *ctx = (ErrorContext *)pthread_getspecific(error_key);
    if (!ctx) {
        ctx = (ErrorContext *)malloc(sizeof(ErrorContext));
        if (ctx) {
            ctx->code = ERROR_NONE;
            ctx->message[0] = '\0';
            pthread_setspecific(error_key, ctx);
        }
    }
    return ctx;
}

void error_set(int code, const char *message) {
    ErrorContext *ctx = get_error_context();
    if (!ctx) return;
    
    ctx->code = code;
    if (message) {
        strncpy(ctx->message, message, ERROR_MESSAGE_MAX - 1);
        ctx->message[ERROR_MESSAGE_MAX - 1] = '\0';
    } else {
        ctx->message[0] = '\0';
    }
}

int error_get_code(void) {
    ErrorContext *ctx = get_error_context();
    return ctx ? ctx->code : ERROR_UNKNOWN;
}

const char* error_get_message(void) {
    ErrorContext *ctx = get_error_context();
    return (ctx && ctx->message[0]) ? ctx->message : "Unknown error";
}

void error_clear(void) {
    ErrorContext *ctx = get_error_context();
    if (ctx) {
        ctx->code = ERROR_NONE;
        ctx->message[0] = '\0';
    }
}

const char* error_to_string(int code) {
    switch (code) {
        case ERROR_NONE:
            return "No error";
        case ERROR_OUT_OF_MEMORY:
            return "Out of memory";
        case ERROR_INVALID_ARGUMENT:
            return "Invalid argument";
        case ERROR_FILE_NOT_FOUND:
            return "File not found";
        case ERROR_FILE_WRITE:
            return "File write error";
        case ERROR_FILE_READ:
            return "File read error";
        case ERROR_PARSE_ERROR:
            return "Parse error";
        case ERROR_INVALID_FORMAT:
            return "Invalid format";
        case ERROR_NOT_FOUND:
            return "Not found";
        case ERROR_UNKNOWN:
        default:
            return "Unknown error";
    }
}

void error_print(FILE *stream) {
    if (!stream) stream = stderr;
    
    int code = error_get_code();
    const char *msg = error_get_message();
    
    fprintf(stream, "Error [%d]: %s\n", code, error_to_string(code));
    if (msg && msg[0]) {
        fprintf(stream, "Details: %s\n", msg);
    }
}

void error_print_to_buffer(char *buffer, size_t size) {
    if (!buffer || size == 0) return;
    
    int code = error_get_code();
    const char *msg = error_get_message();
    
    snprintf(buffer, size, "Error [%d]: %s - %s",
             code, error_to_string(code), msg);
}

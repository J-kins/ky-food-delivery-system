/**
 * @file main.c
 * @brief Command-line interface for Visio parser with CRUD operations
 */

#include "../include/dashboard/visio_parser.h"
#include "../include/dashboard/visio_writer.h"
#include "../include/dashboard/json_exporter.h"
#include "../include/dashboard/errors.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>

/* ============================================================================
 * HELP AND USAGE
 * ============================================================================ */

void print_usage(const char *program_name) {
    printf("Usage: %s [OPTIONS]\n", program_name);
    printf("\nGlobal Options:\n");
    printf("  -h, --help                   Show this help message\n");
    printf("  -v, --verbose                Verbose output\n");
    printf("\nCRUD Operations:\n");
    printf("\n  CREATE: Create new diagram or element\n");
    printf("    --create                   Create new document\n");
    printf("    --output FILE              Output filename for new document\n");
    printf("    --add-page NAME            Add a page to document\n");
    printf("    --add-shape ID:TYPE        Add shape (e.g., 'S1:rectangle')\n");
    printf("    --add-connector ID:FROM:TO Add connector (e.g., 'C1:S1:S2')\n");
    printf("    --at X Y                   Shape position\n");
    printf("    --sized W H                Shape dimensions\n");
    printf("    --text TEXT                Element text content\n");
    printf("    --property NAME:VALUE      Set property\n");
    printf("\n  READ: Read and query diagrams\n");
    printf("    --input FILE               Input .vsdx file\n");
    printf("    --export FORMAT            Export format (json, svg, pdf)\n");
    printf("    --find-shape ID            Find shape by ID\n");
    printf("    --find-type TYPE           Find shapes by type\n");
    printf("    --find-text PATTERN        Find shapes by text\n");
    printf("    --get-connections ID       Get shape connections\n");
    printf("\n  UPDATE: Modify existing diagram\n");
    printf("    --input FILE               Input .vsdx file\n");
    printf("    --update SHAPE_ID          Shape to update\n");
    printf("    --set-text TEXT            New text content\n");
    printf("    --set-property N:V         Set/update property\n");
    printf("    --batch-type TYPE          Batch update by shape type\n");
    printf("    --batch-text PATTERN       Batch delete by text pattern\n");
    printf("    --save                     Save changes back to file\n");
    printf("\n  DELETE: Remove elements\n");
    printf("    --delete SHAPE_ID          Delete shape by ID\n");
    printf("    --delete-connector ID      Delete connector by ID\n");
    printf("    --delete-type TYPE         Delete all shapes of type\n");
    printf("    --delete-text PATTERN      Delete shapes matching text\n");
    printf("    --save                     Save changes back to file\n");
    printf("\nExamples:\n");
    printf("  # Create new diagram with shape\n");
    printf("  %s --create --output new.vsdx --add-shape S1:rectangle --text 'Task' --at 100 100 --sized 80 40\n", program_name);
    printf("\n  # Read and export\n");
    printf("  %s --input diagram.vsdx --export json > output.json\n", program_name);
    printf("\n  # Update shape\n");
    printf("  %s --input diagram.vsdx --update S1 --set-text 'Updated' --save\n", program_name);
    printf("\n  # Delete element\n");
    printf("  %s --input diagram.vsdx --delete S1 --save\n", program_name);
}

/* ============================================================================
 * CREATE OPERATIONS
 * ============================================================================ */

int cmd_create(int argc, char *argv[]) {
    const char *output_file = NULL;
    const char *page_name = "Sheet.1";
    int verbose = 0;
    
    VisioDocument *doc = NULL;
    Page *page = NULL;
    
    for (int i = 0; i < argc; i++) {
        if (strcmp(argv[i], "--output") == 0 && i + 1 < argc) {
            output_file = argv[++i];
        } else if (strcmp(argv[i], "--add-page") == 0 && i + 1 < argc) {
            page_name = argv[++i];
        } else if (strcmp(argv[i], "-v") == 0 || strcmp(argv[i], "--verbose") == 0) {
            verbose = 1;
        }
    }
    
    if (!output_file) {
        fprintf(stderr, "Error: --output required for create operation\n");
        return 1;
    }
    
    /* Create document and page */
    doc = document_create(output_file);
    if (!doc) {
        error_print(stderr);
        return 1;
    }
    
    page = visio_parser_create_page(doc, page_name);
    if (!page) {
        error_print(stderr);
        document_free(doc);
        return 1;
    }
    
    /* Parse shape/connector additions */
    for (int i = 0; i < argc; i++) {
        if (strcmp(argv[i], "--add-shape") == 0 && i + 1 < argc) {
            const char *shape_spec = argv[++i];
            char *colon = strchr(shape_spec, ':');
            if (!colon) {
                fprintf(stderr, "Error: Invalid shape spec, use ID:TYPE\n");
                document_free(doc);
                return 1;
            }
            
            char shape_id[64], shape_type[64];
            sscanf(shape_spec, "%63[^:]:%63s", shape_id, shape_type);
            
            Shape *shape = visio_parser_create_shape(doc, 0, shape_id);
            if (shape) {
                shape_set_type(shape, shape_type);
                
                /* Look for following attributes */
                for (int j = i + 1; j < argc; j++) {
                    if (strcmp(argv[j], "--at") == 0 && j + 2 < argc) {
                        double x = atof(argv[++j]);
                        double y = atof(argv[++j]);
                        shape_set_position(shape, x, y);
                    } else if (strcmp(argv[j], "--sized") == 0 && j + 2 < argc) {
                        double w = atof(argv[++j]);
                        double h = atof(argv[++j]);
                        shape_set_size(shape, w, h);
                    } else if (strcmp(argv[j], "--text") == 0 && j + 1 < argc) {
                        shape_set_text(shape, argv[++j]);
                    } else if (strcmp(argv[j], "--property") == 0 && j + 1 < argc) {
                        const char *prop_spec = argv[++j];
                        char *colon_p = strchr(prop_spec, ':');
                        if (colon_p) {
                            *colon_p = '\0';
                            shape_add_property(shape, prop_spec, colon_p + 1);
                            *colon_p = ':';
                        }
                    } else {
                        break;
                    }
                }
                
                if (verbose) {
                    printf("Created shape: %s (type: %s)\n", shape_id, shape_type);
                }
            }
        }
    }
    
    /* Save document */
    if (visio_writer_save(doc, output_file) == 0) {
        printf("Created: %s\n", output_file);
        document_free(doc);
        return 0;
    } else {
        error_print(stderr);
        document_free(doc);
        return 1;
    }
}

/* ============================================================================
 * READ OPERATIONS
 * ============================================================================ */

int cmd_read(int argc, char *argv[]) {
    const char *input_file = NULL;
    const char *export_format = NULL;
    int verbose = 0;
    
    for (int i = 0; i < argc; i++) {
        if (strcmp(argv[i], "--input") == 0 && i + 1 < argc) {
            input_file = argv[++i];
        } else if (strcmp(argv[i], "--export") == 0 && i + 1 < argc) {
            export_format = argv[++i];
        } else if (strcmp(argv[i], "-v") == 0 || strcmp(argv[i], "--verbose") == 0) {
            verbose = 1;
        }
    }
    
    if (!input_file) {
        fprintf(stderr, "Error: --input required for read operation\n");
        return 1;
    }
    
    /* Parse document */
    VisioDocument *doc = visio_parser_parse(input_file);
    if (!doc) {
        error_print(stderr);
        return 1;
    }
    
    /* Export if requested */
    if (export_format) {
        if (strcmp(export_format, "json") == 0) {
            char *json = json_exporter_document(doc);
            if (json) {
                printf("%s\n", json);
                free(json);
            }
        } else if (strcmp(export_format, "svg") == 0) {
            visio_writer_export_svg(doc, "output.svg");
        } else if (strcmp(export_format, "pdf") == 0) {
            visio_writer_export_pdf(doc, "output.pdf");
        }
    } else {
        /* Print summary */
        printf("Document: %s\n", input_file);
        printf("Pages: %zu\n", doc->pages_count);
        printf("Total Shapes: %zu\n", document_total_shapes(doc));
        printf("Total Connectors: %zu\n", document_total_connectors(doc));
    }
    
    document_free(doc);
    return 0;
}

/* ============================================================================
 * UPDATE OPERATIONS
 * ============================================================================ */

int cmd_update(int argc, char *argv[]) {
    const char *input_file = NULL;
    const char *shape_id = NULL;
    const char *new_text = NULL;
    int save_after = 0;
    int verbose = 0;
    
    for (int i = 0; i < argc; i++) {
        if (strcmp(argv[i], "--input") == 0 && i + 1 < argc) {
            input_file = argv[++i];
        } else if (strcmp(argv[i], "--update") == 0 && i + 1 < argc) {
            shape_id = argv[++i];
        } else if (strcmp(argv[i], "--set-text") == 0 && i + 1 < argc) {
            new_text = argv[++i];
        } else if (strcmp(argv[i], "--save") == 0) {
            save_after = 1;
        } else if (strcmp(argv[i], "-v") == 0 || strcmp(argv[i], "--verbose") == 0) {
            verbose = 1;
        }
    }
    
    if (!input_file || !shape_id) {
        fprintf(stderr, "Error: --input and --update required\n");
        return 1;
    }
    
    /* Parse document */
    VisioDocument *doc = visio_parser_parse(input_file);
    if (!doc) {
        error_print(stderr);
        return 1;
    }
    
    /* Find and update shape */
    Shape *shape = visio_parser_find_shape_by_id(doc, shape_id);
    if (shape) {
        if (new_text) {
            shape_set_text(shape, new_text);
            if (verbose) {
                printf("Updated shape %s text to: %s\n", shape_id, new_text);
            }
        }
        
        /* Save if requested */
        if (save_after) {
            if (visio_writer_save(doc, input_file) == 0) {
                printf("Saved: %s\n", input_file);
            } else {
                error_print(stderr);
                document_free(doc);
                return 1;
            }
        }
    } else {
        fprintf(stderr, "Error: Shape %s not found\n", shape_id);
        document_free(doc);
        return 1;
    }
    
    document_free(doc);
    return 0;
}

/* ============================================================================
 * DELETE OPERATIONS
 * ============================================================================ */

int cmd_delete(int argc, char *argv[]) {
    const char *input_file = NULL;
    const char *shape_id = NULL;
    int save_after = 0;
    int verbose = 0;
    
    for (int i = 0; i < argc; i++) {
        if (strcmp(argv[i], "--input") == 0 && i + 1 < argc) {
            input_file = argv[++i];
        } else if (strcmp(argv[i], "--delete") == 0 && i + 1 < argc) {
            shape_id = argv[++i];
        } else if (strcmp(argv[i], "--save") == 0) {
            save_after = 1;
        } else if (strcmp(argv[i], "-v") == 0 || strcmp(argv[i], "--verbose") == 0) {
            verbose = 1;
        }
    }
    
    if (!input_file || !shape_id) {
        fprintf(stderr, "Error: --input and --delete required\n");
        return 1;
    }
    
    /* Parse document */
    VisioDocument *doc = visio_parser_parse(input_file);
    if (!doc) {
        error_print(stderr);
        return 1;
    }
    
    /* Delete shape */
    if (visio_writer_delete_shape(doc, shape_id) == 0) {
        if (verbose) {
            printf("Deleted shape: %s\n", shape_id);
        }
        
        /* Save if requested */
        if (save_after) {
            if (visio_writer_save(doc, input_file) == 0) {
                printf("Saved: %s\n", input_file);
            } else {
                error_print(stderr);
                document_free(doc);
                return 1;
            }
        }
    } else {
        fprintf(stderr, "Error: Could not delete shape %s\n", shape_id);
        document_free(doc);
        return 1;
    }
    
    document_free(doc);
    return 0;
}

/* ============================================================================
 * MAIN ENTRY POINT
 * ============================================================================ */

int main(int argc, char *argv[]) {
    if (argc < 2) {
        print_usage(argv[0]);
        return 0;
    }
    
    /* Determine operation */
    int operation = 0; /* 0=none, 1=create, 2=read, 3=update, 4=delete */
    
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "--create") == 0) {
            operation = 1;
            break;
        } else if (strcmp(argv[i], "--input") == 0) {
            /* Determine based on other flags */
            for (int j = i; j < argc; j++) {
                if (strcmp(argv[j], "--export") == 0 ||
                    strcmp(argv[j], "--find-shape") == 0 ||
                    strcmp(argv[j], "--find-type") == 0 ||
                    strcmp(argv[j], "--find-text") == 0 ||
                    strcmp(argv[j], "--get-connections") == 0) {
                    operation = 2;
                    break;
                } else if (strcmp(argv[j], "--update") == 0) {
                    operation = 3;
                    break;
                } else if (strcmp(argv[j], "--delete") == 0) {
                    operation = 4;
                    break;
                }
            }
            if (operation == 0) operation = 2; /* Default to read */
            break;
        } else if (strcmp(argv[i], "-h") == 0 || strcmp(argv[i], "--help") == 0) {
            print_usage(argv[0]);
            return 0;
        }
    }
    
    /* Execute operation */
    switch (operation) {
        case 1:
            return cmd_create(argc, argv);
        case 2:
            return cmd_read(argc, argv);
        case 3:
            return cmd_update(argc, argv);
        case 4:
            return cmd_delete(argc, argv);
        default:
            fprintf(stderr, "Error: No operation specified\n");
            print_usage(argv[0]);
            return 1;
    }
    
    return 0;
}

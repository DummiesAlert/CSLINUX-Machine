#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#include <limits.h>

#include <unistd.h>
#include <dirent.h>
#include <sys/stat.h>

typedef struct {
    bool verbose;
    bool recursive;

    char target[PATH_MAX];
} arg_t;

typedef struct {
    long long dir_size;
    int file_count;
    int dir_count;
} dir_t;

// Takes the args from argv and parses them into an arg_t structure
void parse_args(arg_t* args, int argc, char *argv[]) {
    args->verbose = false;
    args->recursive = false;
    args->target[0] = '\0';

    for (int i = 1; i < argc; ++i) {
        char *a = argv[i];
        if (a[0] == '-' && a[1] != '\0') {
            for (int j = 1; a[j] != '\0'; ++j) {
                if (a[j] == 'v') args->verbose = true;
                else if (a[j] == 'r') args->recursive = true;
                /* ignore unknown options */
            }
        } else {
            /* first non-option is target */
            if (args->target[0] == '\0') {
                strncpy(args->target, a, PATH_MAX - 1);
                args->target[PATH_MAX - 1] = '\0';
            }
        }
    }

    if (args->target[0] == '\0') {
        /* default to current directory */
        strncpy(args->target, ".", PATH_MAX - 1);
        args->target[PATH_MAX - 1] = '\0';
    }
}

// Prints the arg_t structure for debugging purposes
int args_string(char* str, arg_t* args) {
    if (!str || !args) return -1;
    snprintf(str, PATH_MAX + 64, "verbose=%d recursive=%d target=%s",
             args->verbose ? 1 : 0, args->recursive ? 1 : 0, args->target);
    return 0;
}

//Prints the directory information
int string_dir(char* str, dir_t* dir) {

    snprintf(str, 4098, "%lld %d %d", dir->dir_size, dir->file_count, dir->dir_count);

    return 0;

}

//Manages finding, listing and calculating the regular files and directories for dirinfo
int list (arg_t* args, dir_t* dir_info) {
    if (!args || !dir_info) return -1;

    /* initialize */
    dir_info->dir_size = 0;
    dir_info->file_count = 0;
    dir_info->dir_count = 0;

    /* recursive scanner */
    int scan_dir(const char *path) {
        DIR *d = opendir(path);
        if (!d) return -1;
        struct dirent *entry;
        while ((entry = readdir(d)) != NULL) {
            /* skip . and .. */
            if (strcmp(entry->d_name, ".") == 0 || strcmp(entry->d_name, "..") == 0)
                continue;

            char full[PATH_MAX];
            int n = snprintf(full, PATH_MAX, "%s/%s", path, entry->d_name);
            if (n >= PATH_MAX) {
                /* truncated, skip */
                continue;
            }

            struct stat st;
            if (stat(full, &st) == -1) {
                /* unable to stat, skip */
                continue;
            }

            if (S_ISREG(st.st_mode)) {
                dir_info->file_count += 1;
                dir_info->dir_size += (long long)st.st_size;
                if (args->verbose) {
                    printf("file: %s (%lld bytes)\n", full, (long long)st.st_size);
                }
            } else if (S_ISDIR(st.st_mode)) {
                dir_info->dir_count += 1;
                if (args->verbose) {
                    printf("dir: %s\n", full);
                }
                if (args->recursive) {
                    scan_dir(full);
                }
            } else {
                /* other types ignored for counting/size */
                if (args->verbose) {
                    printf("other: %s\n", full);
                }
            }
        }
        closedir(d);
        return 0;
    }

    /* start scanning at target */
    struct stat stt;
    if (stat(args->target, &stt) == -1) return -1;
    if (S_ISREG(stt.st_mode)) {
        /* target is a file */
        dir_info->file_count = 1;
        dir_info->dir_size = (long long)stt.st_size;
        dir_info->dir_count = 0;
        if (args->verbose) printf("file: %s (%lld bytes)\n", args->target, (long long)stt.st_size);
        return 0;
    } else if (S_ISDIR(stt.st_mode)) {
        /* count the starting directory? treat it as one directory */
        dir_info->dir_count += 1;
        return scan_dir(args->target);
    }

    /* other type */
    return 0;
}


int main(int argc, char *argv[]) {
    printf("dirinfo:\n");

    arg_t args;
    dir_t info;
    char buf[4096];

    parse_args(&args, argc, argv);

    if (args.verbose) {
        if (args_string(buf, &args) == 0) {
            printf("args: %s\n", buf);
        }
    }

    if (list(&args, &info) != 0) {
        fprintf(stderr, "Error scanning target: %s\n", args.target);
        return 1;
    }

    if (string_dir(buf, &info) == 0) {
        printf("%s\n", buf);
    }

    return 0;
}
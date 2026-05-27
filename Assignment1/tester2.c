#include <stdio.h>
#include <string.h>

#include <limits.h>
#include <stdbool.h> // New
#include <stdlib.h> // New

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
    /* default target */
    strncpy(args->target, ".", PATH_MAX - 1);
    args->target[PATH_MAX - 1] = '\0';

    int opt;
    while ((opt = getopt(argc, argv, "vr")) != -1) {
        switch (opt) {
            case 'v':
                args->verbose = true;
                break;
            case 'r':
                args->recursive = true;
                break;
            default:
                /* ignore unknown options */
                break;
        }
    }

    if (optind < argc) {
        strncpy(args->target, argv[optind], PATH_MAX - 1);
        args->target[PATH_MAX - 1] = '\0';
    }
}

// Prints the arg_t structure for debugging purposes
int args_string(char* str, arg_t* args) {
    if (!str || !args) return -1;
    snprintf(str, PATH_MAX + 64, "verbose=%d recursive=%d target=%s",
             args->verbose ? 1 : 0,
             args->recursive ? 1 : 0,
             args->target);
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

    dir_info->dir_size = 0;
    dir_info->file_count = 0;
    dir_info->dir_count = 0;

    struct stat st;
    if (stat(args->target, &st) != 0) {
        return -1;
    }

    /* if target is a regular file, count it and return */
    if (S_ISREG(st.st_mode)) {
        dir_info->dir_size += (long long)st.st_size;
        dir_info->file_count += 1;
        if (args->verbose) {
            printf("%s\t%lld\n", args->target, (long long)st.st_size);
        }
        return 0;
    }

    /* if not a directory, nothing to do */
    if (!S_ISDIR(st.st_mode)) {
        return -1;
    }

    DIR *d = opendir(args->target);
    if (!d) return -1;

    struct dirent *ent;
    char path[PATH_MAX];

    while ((ent = readdir(d)) != NULL) {
        /* skip self and parent */
        if (strcmp(ent->d_name, ".") == 0 || strcmp(ent->d_name, "..") == 0) continue;

        /* build full path */
        int n = snprintf(path, PATH_MAX, "%s/%s", args->target, ent->d_name);
        if (n >= PATH_MAX) continue; /* path too long, skip */

        /* lstat to preserve behavior for symlinks if needed */
        if (lstat(path, &st) != 0) continue;

        if (S_ISREG(st.st_mode)) {
            dir_info->dir_size += (long long)st.st_size;
            dir_info->file_count += 1;
            if (args->verbose) {
                printf("%s\t%lld\n", path, (long long)st.st_size);
            }
        } else if (S_ISDIR(st.st_mode)) {
            /* directory found */
            dir_info->dir_count += 1;
            if (args->recursive) {
                /* recurse into subdirectory */
                arg_t next_args = *args;
                strncpy(next_args.target, path, PATH_MAX - 1);
                next_args.target[PATH_MAX - 1] = '\0';

                dir_t sub_info = {0, 0, 0};
                if (list(&next_args, &sub_info) == 0) {
                    dir_info->dir_size += sub_info.dir_size;
                    dir_info->file_count += sub_info.file_count;
                    dir_info->dir_count += sub_info.dir_count;
                }
            } else {
                if (args->verbose) {
                    printf("%s/\n", path);
                }
            }
        } else {
            /* ignore other file types */
        }
    }

    closedir(d);
    return 0;
}


int main(int argc, char *argv[]) {
    printf("dirinfo:\n");

    return 0;
}
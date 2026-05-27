#include <stdio.h>
#include <string.h>

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
}

// Prints the arg_t structure for debugging purposes
int args_string(char* str, arg_t* args) {
}

//Prints the directory information
int string_dir(char* str, dir_t* dir) {

	snprintf(str, 4098, "%lld %d %d", dir->dir_size, dir->file_count, dir->dir_count);

	return 0;

}

//Manages finding, listing and calculating the regular files and directories for dirinfo
int list (arg_t* args, dir_t* dir_info) {
}


int main(int argc, char *argv[]) {
	printf("dirinfo:\n");

	return 0;
}
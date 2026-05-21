// Write a C program which echoes all command line argument to the screen

#include <stdio.h>

int main(int argc, char *argv[]) {
    for (int i = 0; i < argc; i++) {
        printf("The Argument %d: %s\n", i, argv[i]);
    }

    return 0;
}
// Write a C program which echoes all command line argument to the screen

#include <stdio.h>

int main(int argc, char *argv[]) {
    for (int i = 0; i < argc; i++) {
        printf("Argument %d: %s\n", i, argv[i]);
    }

    return 0;
}

/*

Output:

gcc Stage1_EchoCommandLineArgs.c -o 1.out
./1.out banana and cookie

Argument 1: banana
Argument 2: and
Argument 3: cookie

*/
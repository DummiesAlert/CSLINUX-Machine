// Write a C program which echoes all command line arguments which begin with a vowel

#include <stdio.h>

int main(int argc, char *argv[]) {
    for (int i = 1; i < argc; i++) {
        char firstChar = argv[i][0];
        if (firstChar == 'A' || firstChar == 'E' || firstChar == 'I' || firstChar == 'O' || firstChar == 'U' ||
            firstChar == 'a' || firstChar == 'e' || firstChar == 'i' || firstChar == 'o' || firstChar == 'u') {
            printf("Argument %d: %s\n", i, argv[i]);
        }
    }

    return 0;
}

/*

Output:

gcc Stage2_EchoCommandLineArgsWithVowel.c -o 2.out
./2.out banana and cookie

Argument 2: and

*/
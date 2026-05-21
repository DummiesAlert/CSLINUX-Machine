// Write a C program which takes several flags (-a, -b, and -c) and prints which flags were set on the command line and echoes all
    // other command line arguments. You should handle both separate flags being set -a -b abd grouped flags -ab.

#include <stdio.h>

int main(int argc, char *argv[]) {

    int flagA = 0;
    int flagB = 0;
    int flagC = 0;

    printf("Begin: ");

    for (int i = 1; i < argc; i++) {
        if (argv[i][0] == '-') {
            for (int j = 1; argv[i][j] != '\0'; j++) {
                switch (argv[i][j]) {
                    case 'a':
                        flagA = 1;
                        break;
                    case 'b':
                        flagB = 1;
                        break;
                    case 'c':
                        flagC = 1;
                        break;
                    default:
                        printf("Error/Unknown flag: -%c\n", argv[i][j]);
                }
            }
        } else {
            printf("Argument %d: %s\n", i, argv[i]);
        }
    }

    if (flagA) printf("Flag found: -a ");
    if (flagB) printf("Flag found: -b ");
    if (flagC) printf("Flag found: -c ");
    printf("\n");

    return 0;
}

/*

Output:

gcc Stage3_FlagsAndCommandLineArguments.c -o 3.out
./3.out -a banana and -b cookie

Argument 2: and

*/
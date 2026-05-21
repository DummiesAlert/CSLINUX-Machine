// Write a C program which takes several flags (-a, -b, and -c) and prints which flags were set on the command line and echoes all
    // other command line arguments. You should handle both separate flags being set -a -b abd grouped flags -ab.

#include <stdio.h>

int main(int argc, char *argv[]) {

    int flagA = 0;
    int flagB = 0;
    int flagC = 0;

    printf("Arguments: \n");

    for (int i = 1; i < argc; i++) {
        if (argv[i][0] == '-') {
            for (int j = 1; argv[i][j] != '\0'; j++) {
                
                printf("Flag found: %s\n", argv[i]);

                switch (argv[i][j]) {
                    case 'a':
                        printf("Flag found: -a \n");
                        break;
                    case 'b':
                        printf("Flag found: -b \n");
                        break;
                    case 'c':
                        printf("Flag found: -c \n");
                        break;
                    default:
                        printf("Error/Unknown flag: -%c\n", argv[i][j]);
                }
            }
        } else {
            printf("Argument %d: %s\n", i, argv[i]);
        }
    }

    return 0;
}

/*

Output:

gcc Stage3_FlagsAndCommandLineArguments.c -o 3.out
./3.out -a banana -ab and cookie

Arguments:
Argument 2: banana
Argument 4: banana
Argument 5: banana

Flags:
Flag found: -a
Flag found: -b

*/
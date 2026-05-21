// Write a C program which takes several flags (-a, -b, and -c) and prints which flags were set on the command line and echoes all
    // other command line arguments. You should handle both separate flags being set -a -b abd grouped flags -ab.

#include <stdio.h>

int main(int argc, char *argv[]) {

    for (int i = 1; i < argc; i++) {
        if ((argv[i][0] == '-' && argv[i][1] != '-') && argv[i][0] != '\0') {
            printf("Flag set: %s\n", argv[i]);
        } else {
            printf("Argument %d: %s\n", i, argv[i]);
        }
    }
    return 0;
}

/*

Output:

gcc Stage3_FlagsAndCommandLineArguments.c -o 3.out
./3.out -a banana -ab and --b cookie

Flag set: -a
Argument 2: banana
Flag set; -ab
Argument 4: and
Argument 5: --b
Argument 6: cookie

*/
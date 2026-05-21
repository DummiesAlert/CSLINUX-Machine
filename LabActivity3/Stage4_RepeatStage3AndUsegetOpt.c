// Repeat Stage 3, but use the getOpt library to process your arguments instead.

#include <stdio.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    int opt;
    while ((opt = getopt(argc, argv, "abc")) != -1) {

        if (opt != '?') {
            printf("Flag set: -%c\n", opt);
        } else {
            printf("Unknown/Error set: -%c\n", optopt);
        }
    }

    for (int i = optind; i < argc; i++) {
        printf("Argument %d: %s\n", i, argv[i]);
    }

    return 0;
}

/*

Output:

gcc Stage4_FlagsAndCommandLineArguments.c -o 4.out
./4.out -a banana -ab and --b cookie

Flag set: -a
Flag set: -a
Flag set: -b
./4.out: invalid option -- '-'
Unknown/Error set: --
Flag set: -b
Argument 4: banana
Argument 5: and
Argument 6: cookie

*/
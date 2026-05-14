#include <stdio.h>
#include <stdlib.h>

int main(void) {
    FILE *file = fopen("Stage3_Characters.txt", "r");
    if (file == NULL) {
        perror("Unable to Open Such File or Does not Exist!!");
        return EXIT_FAILURE;
    }

    int characterCount = 0;
    char characters;

    while (characters = fgetc(file) != EOF) {
        if (characters >= 'A' && characters <= 'Z') {
            characterCount++;
        }
        else if (characters >= 'a' && characters <= 'z') {
            characterCount++;
        }
    }

    fclose(file);
    printf("The total of the characters in the file is: %d\n", characterCount);
    return EXIT_SUCCESS;
}
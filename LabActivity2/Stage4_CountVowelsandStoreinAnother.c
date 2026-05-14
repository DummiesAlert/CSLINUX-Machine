#include <stdio.h>
#include <stdlib.h>

int main(void) {
    FILE *inputFile = fopen("Stage4_Words.txt", "r");
    if (inputFile == NULL) {
        perror("Unable to Stage4_Words.txt file or Does not Exist!!");
        return EXIT_FAILURE;
    }

    FILE *outputFile = fopen("Stage4_vowelCount.txt", "w");
    if (outputFile == NULL) {
        perror("Unable to open Stage4_vowelCount.txt or Does not Exist!!");
        fclose(inputFile);
        return EXIT_FAILURE;
    }

    int vowelCount = 0;
    char vowel;
    
    while ((vowel = fgetc(inputFile)) != EOF) {
        if (vowel == 'a' || vowel == 'e' || vowel == 'i' || vowel == 'o' || vowel == 'u' ||
            vowel == 'A' || vowel == 'E' || vowel == 'I' || vowel == 'O' || vowel == 'U') {
            vowelCount++;
        }
    }

    fprintf(outputFile, "The number of vowels in the file is: %d\n", vowelCount);

    fclose(inputFile);
    fclose(outputFile);
    return EXIT_SUCCESS;
}
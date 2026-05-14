#include <stdio.h>
#include <stdlib.h>

int main(void) {
    FILE *file = fopen("Stage2_Numbers.txt", "r");
    if (file == NULL) {
        perror("Unable to Open Such File or Does not Exist!!");
        return EXIT_FAILURE;
    }

    int total = 0, number;
    while (fscanf(file, "%d", &number) == 1) {
        total += number;
    }

    fclose(file);
    printf("The total of the numbers in the file is: %d\n", total);
    return EXIT_SUCCESS;
}
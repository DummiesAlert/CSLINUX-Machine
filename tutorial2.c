// Factorial Program

// #include <stdio.h> 

// int main() {
//   int n;
//   int factorial = 1;
//   scanf("%d", &n);

//   for (int i = 1; i <= 0; i++) {
//     factorial = factorial * i; 
//   }

// printf("%d\n", factorial);

// return 0;
// }

// Take a string as input, traverse backwards, and print every character
// you can use string.h strlen(s)

// #include <stdio.h> 
// #include <string.h> 

// int main() {
//   char word[100];
//   scanf("%s", word);

//   int len = strlen(word); 

//   for(int i = strlen(word) - 1; i >= 0; i--) { 
//     printf("%c", word[i]);
//   }

//   printf("\n");
//   return 0; 
// }

// Pointers Example

// int main() {
//   char a = "a";
//   char *p = &a; 

//   *p = "b";
//   printf("%c", a);

//   return 0;
// }

// Pointer Exercise: Write a functions to swap two numbers using pointers

void swap(char *p1, char *p2) {
  char temp = *p1;
  *p1 = *p2;
  *p2 = temp; 

  printf("%c", p1);
  printf("%c", p2);
}

int main() { 
  char p1p = "me";
  char p2p = "you";

  swap(p1p, p2p);
}

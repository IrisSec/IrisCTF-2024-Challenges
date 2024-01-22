#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

const char* names[] = {
    "Alice", "Emma",
    "James", "William",
};

const char* colors[] = {
    "red", "blue",
    "green", "yellow",
};

const char* foods[] = {
    "pizza", "pasta",
    "steak", "chicken",
};

// in order of names
int chosenColors[4];
int chosenFoods[4];

void check() {
    bool check = true;
    check &= chosenFoods[2] != 2 && chosenFoods[3] != 2;
    check &= chosenColors[1] != 1;
    check &= chosenColors[0] != 3 && chosenColors[1] != 3;
    check &= chosenFoods[0] == 4;
    check &= chosenFoods[3] != 3;
    check &= chosenColors[2] != 4;
    check &= chosenColors[3] == 2;

    if (check) {
	printf("Correct!\n");
        system("cat flag.txt");
    } else {
        printf("Incorrect.\n");
    }
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    printf("Welcome to the Johnson's family!\n");
    printf("You have gotten to know each person decently well, so let's see if you remember all of the facts.\n");
    printf("(Remember that each of the members like different things from each other.)\n");

    int i = 0;
    while (i < 4) {
        printf("Please choose %s's favorite color: ", names[i]);
        
        char input[100];
        scanf("%99s", input);
        
        int choice = 0;
        if (strcmp(input, colors[0]) == 0) {
            choice = 1;
        } else if (strcmp(input, colors[1]) == 0) {
            choice = 2;
        } else if (strcmp(input, colors[2]) == 0) {
            choice = 3;
        } else if (strcmp(input, colors[3]) == 0) {
            choice = 4;
        } else {
            printf("Invalid color!\n");
            continue;
        }

        if (chosenColors[0] == choice || chosenColors[1] == choice
         || chosenColors[2] == choice || chosenColors[3] == choice) {
            printf("That option was already chosen!\n");
            continue;
        }

        chosenColors[i] = choice;
        i++;
    }

    i = 0;
    while (i < 4) {
        printf("Please choose %s's favorite food: ", names[i]);
        
        char input[100];
        scanf("%99s", input);
        
        int choice = 0;
        if (strcmp(input, foods[0]) == 0) {
            choice = 1;
        } else if (strcmp(input, foods[1]) == 0) {
            choice = 2;
        } else if (strcmp(input, foods[2]) == 0) {
            choice = 3;
        } else if (strcmp(input, foods[3]) == 0) {
            choice = 4;
        } else {
            printf("Invalid food!\n");
            continue;
        }

        if (chosenFoods[0] == choice || chosenFoods[1] == choice
         || chosenFoods[2] == choice || chosenFoods[3] == choice) {
            printf("That option was already chosen!\n");
            continue;
        }

        chosenFoods[i] = choice;
        i++;
    }
    
    check();

    return 0;
}

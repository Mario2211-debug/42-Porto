#include <unistd.h>
#include <stdio.h>

void putstr(char *str)
{
    int i;

    i = 0;
    while(str[i])
    {
        write(1, &str[i], 1);
        i++;
    }
    write(1, "\n", 1);
}


void swap(int *a, int *b)
{
    int tmp;

    tmp = *a;
    *a = *b;
    *b = tmp;
}

void sort_tab(int *arr, int len)
{
    int i;
    int swp;

    i = 0;
    swp = 1;
    while(swp == 1)
    {
        swp = 0;
        while(i < len - 1)
        {
            if(arr[i] > arr[i + 1])
            {
                swap(&arr[i], &arr[i + 1]);
                swp = 1;
            }
            i++;
        }
        if (swp == 1)
            i = 0;
    }
}


int main()
{
    int i;
    int len;
    int arr[] = {1, 3, 77, 8, 9, 98, 33, 12, 23, 43, 4, 
        12, 4, 56, 7, 78, 899, 9, 0};
    // putstr("Hola");
    i = 0;
    len = sizeof(arr) / sizeof(int);
    sort_tab(arr, len);
    while(i < len)
    {
        printf("%d\n", arr[i]);
        i++;
    }
    return 0;
}
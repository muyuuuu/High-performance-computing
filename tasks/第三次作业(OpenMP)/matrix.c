#include <stdio.h>
#include <stdlib.h>
#include <time.h> 
#include <omp.h>

#define row1 978
#define col1 967
#define col2 997

float m1[row1][col1];
float m2[col1][col2];
float r1[row1][col2];
float r2[row1][col2];

void init_randon_matrix(float *arr, int row, int col){
    srand(time(0));
    for (int i = 0; i < row; i++){
        for (int j = 0; j < col; j++){
            *((arr+i*col) + j) = (4.0 * rand() / RAND_MAX) - 2.0;
        }
    }
}

float calc(int i, int j){
    float temp = 0;
    for (int k = 0; k < col1; k++){
        temp += m1[i][k] * m2[k][j];
    }
    // printf("%f\n", temp);
    return temp;
}

void matirxMulti(){
    for (int i = 0; i < row1; i++){
        for (int j = 0; j < col2; j++){
            r1[i][j] = calc(i, j);
        }
    }
}

void matrixMultiOMP(int num){
    omp_set_num_threads(num);
    {
        #pragma omp parallel for num_threads(num) 
        for (int i = 0; i < row1; i++){
            for (int j = 0; j < col2; j++){
                r2[i][j] = calc(i, j);
            }
        }
    }
}

int main(int argc, char const *argv[])
{   
    clock_t start, end;  
    init_randon_matrix((float *)m1, row1, col1);
    init_randon_matrix((float *)m2, col1, col2);

    int num_threads = 4;
    start = clock(); 
    matrixMultiOMP(num_threads);
    end = clock();  
    printf("time=%f\n", (double)(end-start) / 1000 );  
    
    start = clock(); 
    matirxMulti();
    end = clock();  
    printf("time=%f\n", (double)(end-start) / 1000 );  
    return 0;
}

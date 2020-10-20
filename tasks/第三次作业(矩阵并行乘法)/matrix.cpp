#include <stdio.h>
#include <stdlib.h>
#include <chrono> 
#include <math.h>
#include <omp.h>
#include <iostream>

// 第一个矩阵的维度是：[row1, col1]
// 第二个矩阵的维度是：[col1, col2]
#define row1 2213
#define col1 3124
#define col2 2569

using namespace std;

// 第一个矩阵
float m1[row1][col1];
// 第二个矩阵
float m2[col1][col2];
// 存储串行乘法执行的结果
float r1[row1][col2];
// 存储并行乘法执行的结果
float r2[row1][col2];

// 初始化矩阵元素的值，类型 float，取值范围 [-2, 2]
void init_randon_matrix(float *arr, int row, int col){
    srand(time(0));
    for (int i = 0; i < row; i++){
        for (int j = 0; j < col; j++){
            *((arr+i*col) + j) = (4.0 * rand() / RAND_MAX) - 2.0;
        }
    }
}

// 矩阵乘法的实现
float calc(int i, int j){
    float temp = 0;
    for (int k = 0; k < col1; k++){
        temp += m1[i][k] * m2[k][j];
    }
    // printf("%f\n", temp);
    return temp;
}

//  串行矩阵乘法
void matirxMulti(){
    for (int i = 0; i < row1; i++){
        for (int j = 0; j < col2; j++){
            r1[i][j] = calc(i, j);
        }
    }
}

// 并行矩阵乘法
void matrixMultiOMP(int num){
    {
        #pragma omp parallel for num_threads(num) 
        for (int i = 0; i < row1; i++){
            for (int j = 0; j < col2; j++){
                r2[i][j] = calc(i, j);
            }
        }
    }
}

//  判断串行结果和并行结果是否一致
int judge_euqal(){
    int flag = 0;
    for (int i = 0; i < row1; i++){
        for (int j = 0; j < col2; j++){
            if (abs(r1[i][j] - r2[i][j]) > 1e-6){
                flag = 1;
            }
        }
    }
    return flag;
}

int main(int argc, char const *argv[])
{   
    printf("[%d, %d] X [%d, %d] : \n", row1, col1, col1, col2);
    // 初始化矩阵 
    init_randon_matrix((float *)m1, row1, col1);
    init_randon_matrix((float *)m2, col1, col2);

    // 线程数量
    int num_threads = 12;

    // 串行计时
    auto start = std::chrono::system_clock::now();
    matirxMulti();
    auto end  = std::chrono::system_clock::now();
    std::chrono::duration<double> time_span = std::chrono::duration_cast<std::chrono::duration<double>>(end - start);
    printf("1 thread runs in %.2f seconds.\n", time_span);

    // 从 2 个线程一直到 12 个线程，纪录实验结果
    for (int num = 2; num <= num_threads; num++){        
        // 并行计时
        start = std::chrono::system_clock::now();
        matrixMultiOMP(num);
        end = std::chrono::system_clock::now();
        time_span = std::chrono::duration_cast<std::chrono::duration<double>>(end - start);
        printf("%d thread runs in %.2f seconds.\n", num, time_span);
    }
    
    //  判断串行结果和并行结果是否一致
    int flag = judge_euqal();

    flag == 0 ? printf("Result is Correct") : printf("Result is Error");

    return 0;
}

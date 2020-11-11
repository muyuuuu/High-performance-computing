#include <iostream>
#include <cstdlib>
#include <vector>
#include <time.h> 

using namespace std;

struct Matrix
{
    int width;
    int height;
    float *elements;
};

const int width = 1200;
const int height = 1200;

float M1[height][width];
float M2[height][width];
float M3[height][width];

// 获取矩阵A的(row, col)元素
__device__ float getElement(Matrix *A, int row, int col)
{
	return A->elements[row * A->width + col];
}

// 为矩阵A的(row, col)元素赋值
__device__ void setElement(Matrix *A, int row, int col, float value)
{
	A->elements[row * A->width + col] = value;
}

// 矩阵相乘kernel，2-D，每个线程计算一个元素
__global__ void matMulKernel(Matrix *A, Matrix *B, Matrix *C)
{
	float Cvalue = 0.0;
	int row = threadIdx.y + blockIdx.y * blockDim.y;
	int col = threadIdx.x + blockIdx.x * blockDim.x;
	for (int i = 0; i < A->width; ++i)
	{
		Cvalue += getElement(A, row, i) * getElement(B, i, col);
	}
	setElement(C, row, col, Cvalue);
}

__host__ float hostgetElement(Matrix *A, int row, int col)
{
    cout << A->elements[1];
	return A->elements[row * A->width + col];
}

// 为矩阵A的(row, col)元素赋值
__host__ void hostsetElement(Matrix *A, int row, int col, float value)
{
	A->elements[row * A->width + col] = value;
}

int main()
{
    printf("Computing Complexity(Matrix dimension) is [%d, %d] X [%d, %d]\n", width, width, width, width);
    Matrix *A, *B, *C;
    // 申请托管内存
    clock_t start, end;
    start = clock();
    cudaMallocManaged((void**)&A, sizeof(Matrix));
    cudaMallocManaged((void**)&B, sizeof(Matrix));
    cudaMallocManaged((void**)&C, sizeof(Matrix));
    int nBytes = width * height * sizeof(float);
    cudaMallocManaged((void**)&A->elements, nBytes);
    cudaMallocManaged((void**)&B->elements, nBytes);
    cudaMallocManaged((void**)&C->elements, nBytes);

    // 初始化数据
    A->height = height;
    A->width = width;
    B->height = height;
    B->width = width;
    C->height = height;
    C->width = width;

    for (int i = 0; i < width * height; ++i)
    {
        float a = (4.0 * rand() / RAND_MAX) - 2.0;
        float b = (4.0 * rand() / RAND_MAX) - 2.0;
        A->elements[i] = a;
        B->elements[i] = b;
        M1[i%height][i%width] = a;
        M2[i%height][i%width] = b;
    }

    // 定义kernel的执行配置
    dim3 blockSize(32, 32);
    dim3 gridSize((width + blockSize.x - 1) / blockSize.x, 
        (height + blockSize.y - 1) / blockSize.y);
    // 执行kernel
    matMulKernel << < gridSize, blockSize >> >(A, B, C);

    // 同步device 保证结果能正确访问
    cudaDeviceSynchronize();

    // 并行计时
    end = clock();
    float t1 = (double)(end-start)/CLOCKS_PER_SEC;
    printf("Cuda program runs in %.2f seconds.\n", t1);

    float temp = 0;
    start = clock();
    for (int i = 0; i < width; i++)
    {
        for (int j = 0; j < width; j++)
        {
            for (int k = 0; k < width; k++)
            {
                temp += M1[i][k] * M2[k][j];
            }
            M3[i][j] = temp;
            temp = 0;
        }
    }
    end = clock();
    float t2 = (double)(end-start)/CLOCKS_PER_SEC;
    printf("Serial program runs in %.2f seconds.\n", t2);
    printf("Speedup is %.2f\n", (t2/t1));
    return 0;
}
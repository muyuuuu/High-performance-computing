运行 OpenMP 的程序，多线程记录结果。

完成矩阵并行乘法。


- gcc:10.2.0
- OS: Manjaro Linux 20.1.1

编译选项：`gcc -fopenmp code.c`
执行：`./a.out`

代码：

```C
#include <stdio.h>
#include <omp.h>

int main(int argc, char const *argv[])
{
    int nthreads, thread_id;
    printf("I am the main thread.\n");
    omp_set_num_threads(20);
    # pragma omp parallel
    {  
        nthreads = omp_get_num_threads();
        thread_id = omp_get_thread_num();
        printf("Thread id is %d, thread nums is %d\n", thread_id, nthreads);
    }
    printf("Back to main thread.");
    return 0;
}
```

输出：

```bash
I am the main thread.
Thread id is 6, thread nums is 20
Thread id is 13, thread nums is 20
Thread id is 0, thread nums is 20
Thread id is 4, thread nums is 20
Thread id is 3, thread nums is 20
Thread id is 1, thread nums is 20
Thread id is 5, thread nums is 20
Thread id is 10, thread nums is 20
Thread id is 12, thread nums is 20
Thread id is 8, thread nums is 20
Thread id is 11, thread nums is 20
Thread id is 2, thread nums is 20
Thread id is 16, thread nums is 20
Thread id is 18, thread nums is 20
Thread id is 19, thread nums is 20
Thread id is 14, thread nums is 20
Thread id is 15, thread nums is 20
Thread id is 17, thread nums is 20
Thread id is 7, thread nums is 20
Thread id is 9, thread nums is 20
Back to main thread.
```


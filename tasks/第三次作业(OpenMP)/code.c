#include <stdio.h>
#include <omp.h>

int main(int argc, char const *argv[])
{
    int nthreads, thread_id;
    printf("I am the main thread.\n");
    omp_set_num_threads(20);
    # pragma omp parallel private(nthreads, thread_id)
    {  
        nthreads = omp_get_num_threads();
        thread_id = omp_get_thread_num();
        printf("Thread id is %d, thread nums is %d\n", thread_id, nthreads);
    }
    printf("Back to main thread.");
    return 0;
}


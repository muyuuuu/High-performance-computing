#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>   
#include <semaphore.h>   //导入 信号量 的包

#define NUM_THREADS 200
pthread_t tid[NUM_THREADS];

int count = 0;
// 声明信号量 
// 其中 sem_t 可视作 unsigned int
sem_t count_sem;

// 多线程要执行的函数
void *thread_func(void *arg)
{
    sem_wait(&count_sem);
        count++;
    sem_post(&count_sem);
}

int main(int argc, char *argv[])
{
    // 初始换信号量
    if (sem_init(&count_sem, 0, 1) == -1)
    {
        printf("sem_init: failed\n");
    }

    int i = 0;
    int err;

    // 10次执行 多次执行观察结果
    for (int j = 0; j < 10; j++){
        // 创建多线程的任务
        while(i < NUM_THREADS)
        {
            err = pthread_create(&(tid[i]), NULL, &thread_func, NULL);
            if (err != 0)
                printf("\ncan't create thread :[%s]", strerror(err));
            i++;
        }

        // 等待线程释放
        i = 0;
        while (i < NUM_THREADS)
        {
            pthread_join(tid[i], NULL);
            i++;
        }
        
        printf("%d\n", count);
        count = 0;
        i = 0;
    }

    // 销毁信号量
    sem_destroy(&count_sem);
    return 0;
}


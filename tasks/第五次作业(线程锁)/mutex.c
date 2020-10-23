#include <stdio.h>
#include <string.h>
#include <pthread.h>

// 初始化线程数量
#define NUM_THREADS 200
pthread_t tid[NUM_THREADS];
// 要计算的量
int counter = 0;
// 互斥量
pthread_mutex_t lock;

// 多个线程要执行的代码
void *thread_func(void *arg)
{
    pthread_mutex_lock(&lock);
    counter += 1;
    pthread_mutex_unlock(&lock);
}

int main()
{
    int i = 0;
    int err;

    // 初始换互斥量
    if (pthread_mutex_init(&lock, NULL) != 0)
    {
        printf("\n mutex init failed\n");
        return 1;
    }

    // 10次循环执行，多次执行 观察结果
    for (int j = 0; j < 10; j++)
    {
        // 创建线程 分配任务
        while (i < NUM_THREADS)
        {
            err = pthread_create(&(tid[i]), NULL, &thread_func, NULL);
            if (err != 0)
                printf("\ncan't create thread :[%s]", strerror(err));
            i++;
        }

        // 等待线程执行完毕 
        i = 0;
        while (i < NUM_THREADS)
        {
            pthread_join(tid[i], NULL);
            i++;
        }

        // 打印变量
        printf("%d\n", counter);

        // 变量清空
        counter = 0;
        i = 0;
    }

    // 销毁互斥量
    pthread_mutex_destroy(&lock);
    return 0;
}
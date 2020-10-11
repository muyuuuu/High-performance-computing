#include <stdio.h>
#include <pthread.h>

#define NUM_THREADS 20
 
int g = 0;

// 线程的运行函数
void* count(void* args){
    g++;
}
 
int main(){
    // 定义线程的 id 变量，多个变量使用数组
    pthread_t tids[NUM_THREADS];
    for(int i = 0; i < NUM_THREADS; ++i)
    {
        //参数依次是：创建的线程id，线程参数，调用的函数，传入的函数参数
        int ret = pthread_create(&tids[i], NULL, count, NULL);
        if (ret != 0){
            printf("pthread_create error: error_code = %d", ret);
        }
    }
    printf("g = %d", g);
}
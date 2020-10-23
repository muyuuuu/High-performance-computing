#include <pthread.h>
#include <stdio.h>
#include <unistd.h>
#include <assert.h>

// 创建 100 个线程
int NUMTHREADS = 100;
int count = 0;
// 互斥锁
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
// 条件变量
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;

// 信号量满足条件时执行的任务
void *ThreadEntry()
{
	// 获取锁
	pthread_mutex_lock(&mutex);
	count++;
	// 叫 5 次，每个20回叫一次
	if (count % 20 == 0 && count != 0){
		printf("count is now %d. Signalling cond.\n", count);
		// 每次完成加法后发送信号
		pthread_cond_broadcast(&cond);
	}
	// 最后释放锁
	pthread_mutex_unlock(&mutex);
}

int main(int argc, char **argv)
{
	pthread_t threads[NUMTHREADS];
	// 初始化线程
	for (int t = 0; t < NUMTHREADS; t++)
		pthread_create(&threads[t], NULL, ThreadEntry, NULL);

	// 获取锁
	pthread_mutex_lock(&mutex);

	// 相加到 100 才会满足条件
	while (count != NUMTHREADS)
	{
		printf("[thread main] count is %d which is < %d so waiting on cond\n", count, NUMTHREADS);
		pthread_cond_wait(&cond, &mutex);
	}
	puts("[thread main] wake - cond was signalled.");

	// 在 pthread_cond_wait 返回之前，会再次锁住 mutex
	pthread_mutex_unlock(&mutex);

	// 打印最后结果
	printf("[thread main] count == %d so everyone is count\n", count);

	// 销毁条件变量和互斥量
	pthread_cond_destroy(&cond);
	pthread_mutex_destroy(&mutex);
	return 0;
}
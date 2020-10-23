/**
 *  ./a.out > read_write_lock_result.txt 重定向输出结果，方便分析  
**/

#include <pthread.h> 
#include <stdio.h>
#include <string.h>
#include <unistd.h>  // 延时函数

#define NUM_THREADS 20
pthread_t r[NUM_THREADS], w[NUM_THREADS];

// 创建读写锁
pthread_rwlock_t rwlock;

int count = 0;

// 读任务 加入读写锁
void *rdlockThread(void *arg)
{
	printf("%lu thread entered, getting read lock\n", pthread_self());
	pthread_rwlock_wrlock(&rwlock);
	// 在读线程中打印变量，方便观察与分析结果
	printf("===================%d====================\n", count);
	printf("%lu got the rwlock read lock, now unlock\n", pthread_self());
	pthread_rwlock_unlock(&rwlock);
}

// 写任务 加入读写锁
void *wrlockThread(void *arg)
{
	printf("%lu thread entered, getting write lock\n", pthread_self());
	pthread_rwlock_wrlock(&rwlock);
	count++;
	printf("%lu got the rwlock write lock, now unlock\n", pthread_self());
	pthread_rwlock_unlock(&rwlock);
}

int main(int argc, char **argv)
{
	// 初始化
	pthread_rwlock_init(&rwlock, NULL);

	int i = 0;
	int err;

	// 10次执行 多次执行观察结果
	for (int j = 0; j < 10; j++)
	{
		// 创建多线程的任务
		while (i < NUM_THREADS)
		{
			// 创建多个线程，完成读任务
			err = pthread_create(&(r[i]), NULL, &rdlockThread, NULL);
			if (err != 0)
				printf("\ncan't create thread :[%s]", strerror(err));
			// 创建多个线程，完成写任务
			err = pthread_create(&(w[i]), NULL, &wrlockThread, NULL);
			if (err != 0)
				printf("\ncan't create thread :[%s]", strerror(err));
			i++;
		}

		// 等待读任务和写任务的线程释放
		i = 0;
		while (i < NUM_THREADS)
		{
			pthread_join(r[i], NULL);
			pthread_join(w[i], NULL);
			i++;
		}

		// 方便观察结果
		printf("Final, count = %d\n\n\n", count);
		// 结果清空
		count = 0;
		i = 0;
	}

	// 销毁写锁
	pthread_rwlock_destroy(&rwlock);

	return 0;
}

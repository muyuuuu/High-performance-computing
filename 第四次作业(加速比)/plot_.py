import matplotlib.pyplot as plt
import numpy as np

# m1 = 'The complexity of matrix multiplication is: [854, 634] X [634, 732]'
# t1 = [1.29, 0.65, 0.45, 0.35, 0.28, 0.22, 0.28, 0.27, 0.23, 0.24, 0.22, 0.22]

m1 = 'The complexity of matrix multiplication is: [1500, 2000] X [2000, 1200]'
t1 = [17.43, 8.74, 5.79, 4.35, 3.51, 2.97, 3.65, 3.39, 2.97, 2.99, 2.93, 3.14]

vmax = max(t1)

plt.style.use('ggplot')

plt.figure(figsize=(30,8), dpi=200)
plt.subplot(131)

y_pos = np.arange(1, len(t1)+1)

plt.barh(y_pos, t1)
plt.tick_params(labelsize='xx-large')
plt.xlabel('Running time', fontsize=20)
plt.ylabel('Number of threads', fontsize=20)
plt.title('Comparison of the running time of Multi-Threads', fontsize=20)

for i, value in enumerate(t1, 1):
    plt.text(value + vmax * 0.02, i, f'{value:,}s', fontsize = 'xx-large', va = 'center', color = 'black')


plt.subplot(132)

y = [round(t1[0]/t1[i], 2) for i in range(1, len(t1))]
vmax = max(y)
x = np.arange(2, len(y)+2, 1)


plt.plot(x, y, '.-')
plt.xlabel('Number of threads', fontsize=20)
plt.ylabel('Speedup', fontsize=20)
plt.title('Speedup of Multi-Threads', fontsize=20)
plt.tick_params(labelsize='xx-large')
plt.suptitle(m1, fontsize=20)

for i, value in enumerate(y, 2):
    plt.text(i, value - value * 0.0022, f'{value:,}', va = 'center', color = 'black', fontsize = 'xx-large')

plt.subplot(133)

y = [round(t1[0]/t1[i]/(i+1), 2) for i in range(1, len(t1))]
vmax = max(y)
x = np.arange(2, len(y)+2, 1)


plt.plot(x, y, '.-')
plt.xlabel('Number of threads', fontsize=20)
plt.ylabel('Efficiency', fontsize=20)
plt.title('Efficiency of Multi-Threads', fontsize=20)
plt.tick_params(labelsize='xx-large')
plt.suptitle(m1, fontsize=20)

for i, value in enumerate(y, 2):
    plt.text(i, value - value * 0.0022, f'{value:,}', va = 'center', color = 'black', fontsize = 'xx-large')

plt.savefig('2.png', bbox_inches='tight')
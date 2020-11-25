from torch.utils.data import DataLoader
from miniImagenet import MiniImagenet

# 加载测试数据集
mini = MiniImagenet('../mini-imagenet/', mode='train', n_way=n_way, k_shot=k_shot, k_query=k_query,
                            batchsz=10000, resize=224)
# pin_memory 快速的将数据转化为 GPU 可以处理的数据, num_workers 读取数据子线程的数量
db = DataLoader(mini, batchsz, shuffle=True,
                num_workers=8, pin_memory=True)
mini_val = MiniImagenet('../mini-imagenet/', mode='val', n_way=n_way, k_shot=k_shot, k_query=k_query,
                        batchsz=200, resize=224)
db_val = DataLoader(mini_val, batchsz, shuffle=True,
                    num_workers=8, pin_memory=True)
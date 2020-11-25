import torch.distributed as dist
import torch.multiprocessing as mp
from torch.nn.parallel import DistributedDataParallel as DDP

def setup(rank, world_size):
    os.environ['MASTER_ADDR'] = 'localhost'
    os.environ['MASTER_PORT'] = '12355'
    # initialize the process group
    dist.init_process_group("gloo", rank=rank, world_size=world_size)

def cleanup():
    dist.destroy_process_group()

def train(rank, world_size):
    print(f"Running basic DDP example on rank {rank}.")
    setup(rank, world_size)
    net = DDP(Compare(n_way, k_shot).to(rank), device_ids=[rank])
    # 训练阶段。遍历训练数据集中的每一个 batch
    for step, batch in enumerate(db):
        # 支持集合与查询集合
        support_x = Variable(batch[0]).cuda().to(rank)
        support_y = Variable(batch[1]).cuda().to(rank)
        query_x = Variable(batch[2]).cuda().to(rank)
        query_y = Variable(batch[3]).cuda().to(rank)
        # 开始训练
        net.train()
        # 计算 loss
        loss = net(support_x, support_y, query_x, query_y, rank)
        # Multi-GPU support
        loss = loss.mean()
        # 清空优化器之前的梯度
        optimizer.zero_grad()
        # 反向传播
        loss.backward()
        optimizer.step()
    cleanup()  

def run_demo(demo_fn, world_size):
    mp.spawn(demo_fn,
             args=(world_size,),
             nprocs=world_size,
             join=True)

if __name__ == "__main__":
    run_demo(train, 3)
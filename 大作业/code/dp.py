import torch
from torch.autograd import Variable
from torch import optim
from compare import Compare

net = torch.nn.DataParallel(Compare(n_way, k_shot)).cuda()
# 训练阶段。遍历训练数据集中的每一个 batch
for step, batch in enumerate(db):
    # 支持集合与查询集合
    support_x = Variable(batch[0]).cuda()
    support_y = Variable(batch[1]).cuda()
    query_x = Variable(batch[2]).cuda()
    query_y = Variable(batch[3]).cuda()
    # 开始训练
    net.train()
    # 计算 loss
    # print('computing loss....')
    loss = net(support_x, support_y, query_x, query_y)
    # Multi-GPU support
    loss = loss.mean()
    # 清空优化器之前的梯度
    optimizer.zero_grad()
    # 反向传播
    # print('backwarding ...')
    loss.backward()
    optimizer.step()
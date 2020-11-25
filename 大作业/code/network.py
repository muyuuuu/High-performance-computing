# 残差块
class Bottleneck(nn.Module):
    expansion = 4

    def __init__(self, inplanes, planes, stride=1, downsample=None):
        super(Bottleneck, self).__init__()
        self.conv1 = nn.Conv2d(inplanes, planes, kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        self.conv3 = nn.Conv2d(planes, planes * 4, kernel_size=1, bias=False)
        self.bn3 = nn.BatchNorm2d(planes * 4)
        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample
        self.stride = stride

    def forward(self, x):
        residual = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)

        out = self.conv3(out)
        out = self.bn3(out)

        if self.downsample is not None:
            residual = self.downsample(x)

        out += residual
        out = self.relu(out)
        return out

# 训练：开始拼接
def forward(self, support_x, support_y, query_x, query_y, rank, train=True):
    """
    """
    # [多少组数组，每个类的样本数量，3个通道，图片高度，图片宽度]
    batchsz, setsz, c_, h, w = support_x.size()
    # 每组数据中 query 样本的数量
    querysz = query_x.size(1)
    # c 是 batchsize，d 是图片高度
    c, d = self.c, self.d

    # view 重构张量的维度
    # batchsz * setsz 是输入的 batchsize 大小
    # [b, setsz, c_, h, w] => [b*setsz, c_, h, w] => [b*setsz, c, d, d] => [b, setsz, c, d, d]
    support_xf = self.repnet(support_x.view(batchsz * setsz, c_, h, w)).view(batchsz, setsz, c, d, d)
    # [b, querysz, c_, h, w] => [b*querysz, c_, h, w] => [b*querysz, c, d, d] => [b, querysz, c, d, d]
    query_xf = self.repnet(query_x.view(batchsz * querysz, c_, h, w)).view(batchsz, querysz, c, d, d)

    # 按照图片的三个通道，将查询集和测试集拼接起来
    # squeeze：删除维度是 1 的数据
    # unsqueeze：在指定位置插入一维数据
    # expand 在指定维度进行扩展
    # 第一个维度，扩展查询集这么多个。[b, setsz, c, d, d] => [b, 1, setsz, c, d, d] => [b, querysz, setsz, c, d, d]
    support_xf = support_xf.unsqueeze(1).expand(-1, querysz, -1, -1, -1, -1)
    # 第二个维度，扩展支持集这么多个。[b, querysz, c, d, d] => [b, querysz, 1, c, d, d] => [b, querysz, setsz, c, d, d]
    query_xf = query_xf.unsqueeze(2).expand(-1, -1, setsz, -1, -1, -1)
    # cat: [b, querysz, setsz, c, d, d] => [b, querysz, setsz, 2c, d, d]
    comb = torch.cat([support_xf, query_xf], dim=3)

    # print('comb size is {}'.format(comb.size()))

    # print('c = {}'.format(c))
    comb = self.layer5(self.layer4(comb.view(batchsz * querysz * setsz, 2 * c, d, d)))
    # print('layer5 sz:', comb.size())
    comb = F.avg_pool2d(comb, 3)
    # print('avg sz:', comb.size())
    # push to Linear layer
    # [b * querysz * setsz, 256] => [b * querysz * setsz, 1] => [b, querysz, setsz, 1] => [b, querysz, setsz]
    score = self.fc(comb.view(batchsz * querysz * setsz, -1)).view(batchsz, querysz, setsz, 1).squeeze(3)

    # build its label
    # [b, setsz] => [b, 1, setsz] => [b, querysz, setsz]
    support_yf = support_y.unsqueeze(1).expand(batchsz, querysz, setsz)
    # [b, querysz] => [b, querysz, 1] => [b, querysz, setsz]
    query_yf = query_y.unsqueeze(2).expand(batchsz, querysz, setsz)
    # 标签相等，表示查询集属于这个类。和score进行对比
    # eq: [b, querysz, setsz] => [b, querysz, setsz] and convert byte tensor to float tensor
    label = torch.eq(support_yf, query_yf).float()

    # score: [b, querysz, setsz]
    # label: [b, querysz, setsz]
    if train:
        loss = torch.pow(label - score, 2).sum() / batchsz
        return loss

    else:
        # [b, querysz, setsz]
        rn_score_np = score.cpu().data.numpy()
        pred = []
        # [b, setsz]
        support_y_np = support_y.cpu().data.numpy()
        for i, batch in enumerate(rn_score_np):
            for _, query in enumerate(batch):
                # query: [setsz]
                sim = []  # [n_way]
                for way in range(self.n_way):
                    sim.append(np.sum(query[way * self.k_shot: (way + 1) * self.k_shot]))
                idx = np.array(sim).argmax()
                pred.append(support_y_np[i, idx * self.k_shot])
        # pred: [b, querysz]
        pred = Variable(torch.from_numpy(np.array(pred).reshape((batchsz, querysz)))).cuda().to(rank)

        correct = torch.eq(pred, query_y).sum()
        return pred, correct
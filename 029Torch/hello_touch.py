# coding:utf-8
"""
create on Feb 27, 2020 By Wenyan YU
Function:

Hello,Torch!

pip install torch==1.2.0+cu92 torchvision==0.4.0+cu92 -f https://download.pytorch.org/whl/torch_stable.html<br>
没有显卡，尴尬，所以只能装CPU版本的，先不玩了，后面再看吧
pip install torch==1.2.0+cpu torchvision==0.4.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
"""
import torch
x = torch.rand(5, 3)
print(x)
print(torch.cuda.is_available())

# 将变量数据移到GPU
# gpu_info = Variable(torch.randn(3, 3)).cuda()
# cpu_info = gpu_info.cpu()





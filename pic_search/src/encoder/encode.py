import torch.nn as nn
import torchvision.models as models
import torch.cuda
import torchvision.transforms as transforms
from numpy import linalg as LA

from PIL import Image

TARGET_IMG_SIZE = 224
img_to_tensor = transforms.ToTensor()


def img_to_vec(imgpath):
    print(imgpath)
    model = models.vgg16(pretrained=True).features
    model.eval()  # 必须要有，不然会影响特征提取结果

    img = Image.open(imgpath).convert('RGB')  # 读取图片
    img = img.resize((TARGET_IMG_SIZE, TARGET_IMG_SIZE))
    tensor = img_to_tensor(img)  # 将图片转化成tensor
    tensor = tensor.unsqueeze(0)

    result = model(tensor)
    max_pool = nn.MaxPool2d(7, stride=1)

    result = max_pool(result)

    result = torch.squeeze(result)
    result = result.data.cpu().numpy()

    norm_feat = result / LA.norm(result)
    norm_feat = [i.item() for i in norm_feat]
    return norm_feat


# img_path = '/data/shiyu/test/1.png'
# res_feat = extract_feature(img_path)
# print(res_feat.shape)
# print(res_feat)

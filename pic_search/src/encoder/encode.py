import torch.nn as nn
import torchvision.models as models
import torch.cuda
import torch.nn.functional as F
import torchvision.transforms as transforms
from numpy import linalg as LA

from PIL import Image

import base64
from io import BytesIO

TARGET_IMG_SIZE = 224
transform2 = transforms.Compose([
    transforms.Resize((TARGET_IMG_SIZE, TARGET_IMG_SIZE)),
    # transforms.CenterCrop(input_size),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = models.vgg16(pretrained=True).features
model.to(device)
model.eval()


def base64_pil(base64_str):
    image = base64.b64decode(base64_str)
    image = BytesIO(image)
    image = Image.open(image)
    return image


def img_to_vec(base64list):
    img_list = [base64_pil(base64img) for base64img in base64list]

    img_list = [img.convert("RGB") for img in img_list]
    img_list = [transform2(img) for img in img_list]

    img_tensor = torch.stack(img_list, dim=0)
    img_tensor = img_tensor.to(device)

    with torch.no_grad():
        result = model(img_tensor)

    # print(result)
    # print(result.shape)

    result = F.max_pool2d(result, kernel_size=result.size()[3:])

    result = torch.squeeze(result)
    result = result.data.cpu().numpy()

    norm_feat_list = list()

    for i in range(result.shape[0]):
        norm_feat = result[i] / LA.norm(result[i])
        norm_feat = [i.item() for i in norm_feat]
        norm_feat_list.append(norm_feat)

    return norm_feat_list


if __name__ == '__main__':
    def path2base64(img_path):
        with open(img_path, 'rb') as f:
            image = f.read()
            encodestr = str(base64.b64encode(image), 'utf-8')
        return encodestr


    img_path_1 = "test_pic/1.png"
    img_path_2 = "test_pic/2.png"
    img_path_3 = "test_pic/3.png"

    img_list = list()
    img_list.append(path2base64(img_path_1))
    img_list.append(path2base64(img_path_2))
    img_list.append(path2base64(img_path_3))

    norm_feat_list = img_to_vec(img_list)
    print(norm_feat_list)

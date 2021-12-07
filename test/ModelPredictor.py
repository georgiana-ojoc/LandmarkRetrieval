import json

import PIL
import torch
from torchvision import datasets, transforms
import torch.nn.functional as F
from torch.nn.parameter import Parameter


class GeM(torch.nn.Module):
    def __init__(self, p=3.0, eps=1e-6):
        super(GeM, self).__init__()
        self.p = Parameter(torch.ones(1) * p)
        self.eps = eps

    def forward(self, x):
        return F.adaptive_avg_pool2d(x.clamp(min=self.eps).pow(self.p), (1, 1)).pow(1. / self.p)


def get_res_net_ibn(classes: int = 491):
    model = torch.hub.load('XingangPan/IBN-Net','resnet50_ibn_a', pretrained=True, force_reload=True)
    previous_layer = model.fc.in_features
    model.avgpool = GeM()
    model.fc = torch.nn.Linear(previous_layer, classes)
    return model


def pre_init_ibnnet_module():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(device)
    model = get_res_net_ibn()
    return model


class ResNetIbnGeM:
    def __init__(self):
        model = pre_init_ibnnet_module()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = torch.load("models/ResNetIbnGeM.model")
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            )])
        self.model = self.model.to(self.device)
        self.soft_max = torch.nn.Softmax(dim=0)
        self.label_map = json.load(open("label_map.json", "r"))

    def evaluate(self, img: PIL.Image):
        img = self.transform(img)
        img = img.reshape(1, 3, 224, 224)
        img = img.to(self.device)
        results = self.model(img)
        x = results[0]
        x = x - torch.min(x)
        best_values, indices = torch.topk(x, 3)
        best_values = best_values / torch.sum(best_values) * 100
        # best_values = self.soft_max(best_values) * 100
        labels = [v for k, v in self.label_map.items() if int(k) in indices.tolist()]
        return json.dumps([labels, best_values.tolist()])


class ModelPredictor:
    def __init__(self, model: str):
        if model == "ResNetIbnGeM":
            self.model = ResNetIbnGeM()
        else:
            raise "Unknown model"

    def predict(self, img: PIL.Image):
        return self.model.evaluate(img)

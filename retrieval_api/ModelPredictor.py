import json

import PIL
import torch
from torchvision import transforms

from utils import GeM


class ResNetIbnGeM:
    def __init__(self):
        self.recreate_model()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.load_state_dict(torch.load("models/ResNetIbnGeM.pth"))
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            )])
        self.model = self.model.to(self.device)

    def recreate_model(self, classes=491):
        self.model = torch.hub.load('XingangPan/IBN-Net', 'resnet50_ibn_a', pretrained=False, force_reload=True)
        self.model.avgpool = GeM()
        self.model.fc = torch.nn.Linear(self.model.fc.in_features, classes)

    def evaluate(self, img: PIL.Image):
        img = self.transform(img)
        img = img.reshape(1, 3, 224, 224)
        img = img.to(self.device)
        results = self.model(img)
        return results[0]


class ModelPredictor:
    def __init__(self, model: str):
        self.label_map = json.load(open("label_map.json", "r"))

        if model == "ResNetIbnGeM":
            self.model = ResNetIbnGeM()
        else:
            raise "Unknown model"

    def predict(self, img: PIL.Image):
        results = self.model.evaluate(img)
        results = results - torch.min(results)
        best_values, indices = torch.topk(results, 3)
        best_values = best_values / torch.sum(best_values) * 100
        labels = [v for k, v in self.label_map.items() if int(k) in indices.tolist()]
        return labels, best_values.tolist()

import json
from abc import ABC, abstractmethod

import torch
from efficientnet_pytorch import EfficientNet
from torch.nn.functional import adaptive_avg_pool2d
from torch.nn.parameter import Parameter
from torchvision import transforms


class GeM(torch.nn.Module):
    def __init__(self, eps=1e-6, p=3.0):
        super(GeM, self).__init__()
        self.eps = eps
        self.p = Parameter(torch.ones(1) * p)
    def forward(self, x):
        return adaptive_avg_pool2d(x.clamp(min=self.eps).pow(self.p), (1, 1)).pow(1. / self.p)


class Model(ABC):
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = self.load_model()
        self.model.eval()
        self.model = self.model.to(self.device)
        self.transformations = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])

    @abstractmethod
    def load_model(self):
        pass

    def transform_image(self, image):
        image = self.transformations(image).unsqueeze(axis=0)
        return image.to(self.device)

    def predict(self, image):
        with torch.no_grad():
            predictions = self.model(image)[0]
        return predictions


class ResNetIBNGeM(Model):
    def __init__(self):
        super().__init__()

    def load_model(self):
        model = torch.hub.load('XingangPan/IBN-Net', 'resnet50_ibn_a', pretrained=False)
        model.avgpool = GeM()
        model.fc = torch.nn.Linear(model.fc.in_features, 491)
        model.load_state_dict(torch.load('models/resnet_ibn_gen.pt'))
        return model


class ResNetIBNGeMTraining(Model):
    def __init__(self):
        super().__init__()

    def load_model(self):
        model = torch.hub.load('XingangPan/IBN-Net', 'resnet50_ibn_a', pretrained=False)
        model.avgpool = GeM()
        model.fc = torch.nn.Linear(model.fc.in_features, 13018)
        model.load_state_dict(torch.load('models/resnet_training.pt'))
        return model


class ResNetIBNGeMVal(Model):
    def __init__(self):
        super().__init__()

    def load_model(self):
        model = torch.hub.load('XingangPan/IBN-Net', 'resnet50_ibn_a', pretrained=False)
        model.avgpool = GeM()
        model.fc = torch.nn.Linear(model.fc.in_features, 13018)
        model.load_state_dict(torch.load('models/resnet_val.pt'))
        return model


class _EfficientNet(Model):
    def __init__(self):
        super().__init__()

    def load_model(self):
        model = EfficientNet.from_pretrained('efficientnet-b3')
        model.load_state_dict(torch.load('models/efficientnet.pt', map_location=torch.device(self.device)))
        return model


class Predictor:
    def __init__(self, model):
        if model == 'resnet-ibn-gem':
            self.model = ResNetIBNGeM()
            self.labels = json.load(open('labels.json'))
        elif model == 'efficientnet':
            self.model = _EfficientNet()
            self.labels = json.load(open('labels.json'))
        elif model == 'resnet-validation':
            self.model = ResNetIBNGeMVal()
            self.labels = json.load(open('labels_extended.json'))
        elif model == 'resnet-training':
            self.model = ResNetIBNGeMTraining()
            self.labels = json.load(open('labels_extended.json'))
        else:
            self.model = None
            return

        self.storage_url = 'https://landmark-retrieval.s3.eu-central-1.amazonaws.com'

    def predict(self, image):
        if self.model is None:
            return None
        image = self.model.transform_image(image)
        predictions = self.model.predict(image)
        predictions -= torch.min(predictions)
        best_predictions, indices = torch.topk(predictions, 3)
        best_predictions = best_predictions / torch.sum(best_predictions) * 100
        best_predictions = best_predictions.detach().numpy()
        result = []
        for index in range(3):
            result += [{
                'images': [f'{self.storage_url}/{self.labels[indices[index]]}/{image}.jpg'
                           for image in range(10) if indices[index].item() < len(self.labels)],
                'probability': str(best_predictions[index]),
                'label': self.labels[indices[index]] if indices[index].item() < len(self.labels) else None,
            }]
        return result

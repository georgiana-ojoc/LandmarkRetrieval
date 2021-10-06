from abc import ABC, abstractmethod


class Training(ABC):
    def __init__(self):
        pass

    def train(self):
        self.preprocess_dataset()
        self.split_dataset()
        self.create_model()
        self.fit_model()
        self.evaluate_model()

    @abstractmethod
    def preprocess_dataset(self):
        pass

    def split_dataset(self):
        pass

    @abstractmethod
    def create_model(self):
        pass

    def fit_model(self):
        pass

    def evaluate_model(self):
        pass

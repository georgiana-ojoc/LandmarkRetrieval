from abc import ABCMeta, abstractmethod

class IRepository:
    __metaclass__ = ABCMeta

    @abstractmethod
    def add(self, feedback): pass
    @abstractmethod
    def delete(self, feedback): pass
    @abstractmethod
    def get(self, id): pass
    @abstractmethod
    def getAll(self): pass
    @abstractmethod
    def find(self, predicate): pass

class FeedbackRepository(IRepository):
    def __init__(self):
        self.feedbacksList=[]
    def add(self, feedback): pass
    def delete(self, feedback): pass
    def get(self, id): pass
    def getAll(self): pass
    def find(self, predicate): pass

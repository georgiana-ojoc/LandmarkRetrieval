from training.publisher import Publisher


class Checkpoint(Publisher):
    def __init__(self, state, criteria):
        super().__init__()
        self.state = state
        self.criteria = criteria

    def check_state(self):
        """
        If criteria is met, notify subscribers to save model.
        """
        if self.criteria:
            self.notify()

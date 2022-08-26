class Key:
    def __init__(self, date=None, uuid=None):
        self.date = date
        self.uuid = uuid

    def __eq__(self, other):
        return (self.date == other.date) and (self.uuid == other.uuid)

    def __lt__(self, other):
        return (self.date < other.date) or (self.date == other.date and self.uuid < other.uuid)

    def __gt__(self, other):
        return (self.date > other.date) or (self.date == other.date and self.uuid > other.uuid)

    def __ge__(self, other):
        return (self.date >= other.date) or (self.date == other.date and self.uuid >= other.uuid)

    def __le__(self, other):
        return (self.date <= other.date) or (self.date == other.date and self.uuid <= other.uuid)

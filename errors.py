class CsvCreatorError(Exception):
    def __init__(self, msg, desc=None):
        Exception.__init__(self, msg)
        self.msg = msg
        self.desc = desc

    def __str__(self):
        class_name = self.__class__.__name__
        return f"{class_name}: {self.msg}\nDESCRIPTION: {self.desc}"

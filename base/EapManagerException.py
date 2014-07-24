__author_ = "Samuele Dell'Angelo (Red Hat)"

class EapManagerException(Exception):

    def __init__(self, message):
        self.message = message

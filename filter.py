import re


class Filter:
    def __init__(self, pattern):
        self.pattern = pattern

    def apply(self, expression):
        return re.compile(self.pattern, re.DOTALL).findall(expression.decode())
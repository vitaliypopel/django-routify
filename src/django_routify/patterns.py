

class BasePattern:
    def parse(self):
        pass


class ColonPattern(BasePattern):
    REGEX = r':(\w+)'


class CurlyPattern(BasePattern):
    REGEX = r'\{(\w+)\}'


class AnglePattern(BasePattern):
    REGEX = r'<(\w+)>'

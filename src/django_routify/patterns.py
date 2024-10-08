from ._abstraction import BasePattern


class Pattern(BasePattern):
    def normalize(self, custom_url: str) -> str:
        pass


class ColonPattern(Pattern):
    REGEX = r':(\w+)'


class CurlyPattern(Pattern):
    REGEX = r'\{(\w+)\}'


class AnglePattern(Pattern):
    REGEX = r'<(\w+)>'

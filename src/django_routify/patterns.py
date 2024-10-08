from ._abstraction import BasePattern


class Pattern(BasePattern):
    def normalize(self, custom_url: str) -> str:
        pass


class ColonPattern(BasePattern):
    REGEX = r':(\w+)'


class CurlyPattern(BasePattern):
    REGEX = r'\{(\w+)\}'


class AnglePattern(BasePattern):
    REGEX = r'<(\w+)>'

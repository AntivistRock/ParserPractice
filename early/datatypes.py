from dataclasses import dataclass


@dataclass
class Scene:
    """
    Правило вывода с текущей позицией.
    nonterm - нетерминал правила.
    layout - во что раскрывается нетерминал.
    sep - индекс в layout, после которого стоит точка, -1, если стоит перед всем
    layout.
    """
    nonterm: str
    layout: list
    sep: int


@dataclass
class Situation:
    """
    Хранит ситуацию.
    scene - см. Scene.__doc__
    terms_above: - сколько терминалов прочитали в текущем поддереве разбора.
    """
    scene: Scene
    terms_above: int

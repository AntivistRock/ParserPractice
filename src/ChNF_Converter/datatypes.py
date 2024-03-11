from dataclasses import dataclass


@dataclass
class CYKGrammarAPI:
    grammar_rules: list
    start_nonterm: str


@dataclass(eq=True, frozen=True)
class ReducedRule:
    nonterm: str
    layout: tuple

    def __repr__(self):
        return f'{self.nonterm} -> {self.layout}'


@dataclass(eq=True, frozen=True)
class Rule:
    nonterm: str
    layout: list
    right_nonterms_generative: set
    right_nonterms_eps: set

    def __repr__(self):
        return f'{self.nonterm} -> {self.layout} | ' \
               f'layout nont: {self.right_nonterms_eps}'

    def is_right_nonterms_empty(self, step: str):
        """
        Checks if set of layout nonterms is empty
        If step == generative: non-generative nonterm delete step
        If step == eps: eps-generative nonterm delete step
        """
        if step == 'generative':
            return not bool(self.right_nonterms_generative)
        if step == 'eps':
            return not bool(self.right_nonterms_eps)

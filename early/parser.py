from early.datatypes import Situation, Scene


class EarlyParser:
    def __init__(self, grammar_path):
        self._grammar_path = grammar_path
        self._grammar_rules = {}
        self._parsing_list = None
        self._word = None
        self._start_nonterm = None
        self._build_grammar()

    def _extract_rules(self, line):
        line = line.strip('\n')
        nonterm, layouts = line.split('::=')
        nonterm = nonterm.strip(' ')

        if self._start_nonterm is None:
            self._start_nonterm = nonterm

        self._grammar_rules[nonterm] = list()
        for layout in layouts.split('|'):
            self._grammar_rules[nonterm].append(
                list(layout.strip(' ').split(' ')))

    def _build_grammar(self):
        grammar = open(self._grammar_path, 'r')
        for line in grammar:
            if line == '\n':
                continue
            self._extract_rules(line)

    def get_grammar(self):
        bnf_grammar = ''
        for nonterm, layouts in self._grammar_rules.items():
            bnf_grammar += nonterm + ' ::= '
            bnf_grammar += ' | '.join(
                [' '.join(layout) for layout in layouts]) + '\n\n'
        return bnf_grammar

    def _init_parsing_list(self):
        zero_sit = Situation(
            Scene(self._start_nonterm[:-1] + '`>', [self._start_nonterm], -1),
            0)
        self._parsing_list = list(range(len(self._word) + 1))
        self._parsing_list[0] = list([zero_sit])
        for i in range(1, len(self._word) + 1):
            self._parsing_list[i] = list()

    @staticmethod
    def _is_terminal(str_):
        return str_[-1] == str_[0] == '"'

    def _is_nonterminal(self, str_):
        return not self._is_terminal(str_)

    def _predict(self, j):
        for sit in self._parsing_list[j]:
            layout = sit.scene.layout
            sep = sit.scene.sep
            nonterm = layout[sep + 1]
            if self._is_terminal(nonterm):
                continue
            for rule in self._grammar_rules[nonterm]:
                new_sit = Situation(Scene(nonterm, rule, -1), j)
                self._parsing_list[j].append(new_sit)

    def _scan(self, j):
        for sit in self._parsing_list[j]:
            layout = sit.scene.layout
            sep = sit.scene.sep
            if len(layout) == sep + 1:
                continue
            next_ = layout[sep + 1]
            if self._is_nonterminal(next_):
                continue
            nonterm = sit.scene.nonterm
            if next_ == self._word[j]:
                new_sit = Situation(Scene(nonterm, layout, sep + 1),
                                    sit.terms_above)
                self._parsing_list[j + 1].append(new_sit)

    def _complete(self, j):
        for sit_j in self._parsing_list[j]:
            layout_j = sit_j.scene.layout
            sep_j = sit_j.scene.sep
            if sep_j + 1 != len(layout_j) and layout_j != ['""']:
                continue
            nonterm_j = sit_j.scene.nonterm
            for sit_k in self._parsing_list[sit_j.terms_above]:
                layout_k = sit_k.scene.layout
                sep_k = sit_k.scene.sep
                if len(layout_k) == sep_k + 1 or nonterm_j != layout_k[
                    sep_k + 1]:
                    continue
                nonterm_k = sit_k.scene.nonterm
                new_sit = Situation(Scene(nonterm_k, layout_k, sep_k + 1),
                                    sit_k.terms_above)
                self._parsing_list[j].append(new_sit)

    def parse(self, word):
        self._word = word
        self._init_parsing_list()

        while True:
            set_before = self._parsing_list[0]
            self._predict(0)
            self._complete(0)
            set_after = self._parsing_list[0]
            if set_before == set_after:
                break
            set_before = set_after

        for j in range(1, len(word) + 1):
            self._scan(j - 1)

            while True:
                set_before = self._parsing_list[j]
                self._predict(j)
                self._complete(j)
                set_after = self._parsing_list[j]
                if set_before == set_after:
                    break
                set_before = set_after

        return Situation(
            Scene(self._start_nonterm[:-1] + '`>', [self._start_nonterm], 0),
            0) in \
            self._parsing_list[0 if word == '""' else len(word)]

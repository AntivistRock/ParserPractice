from src.ChNF_Converter.datatypes import ReducedRule
from src.ChNF_Converter.converter import Converter


class CYKParser:
    def __init__(self, grammar_path, is_in_ch_nf=True):
        self._grammar_path = grammar_path
        self._grammar_rules = list()
        self._d = {}
        self._word = None
        self._start_nonterm = None
        if grammar_path is is_in_ch_nf:
            self._build_grammar()
        else:
            conv = Converter(self._grammar_path)
            conv.convert_to_ch_nf()
            grammar_info = conv.GetGrammarToCYK()
            self._grammar_rules, self._start_nonterm = grammar_info.grammar_rules, grammar_info.start_nonterm

    def _extract_rules(self, line):
        line = line.strip('\n')
        nonterm, layouts = line.split('::=')
        nonterm = nonterm.strip(' ')

        if self._start_nonterm is None:
            self._start_nonterm = nonterm

        for layout in layouts.split('|'):
            layout = tuple(layout.strip(' ').split(' '))
            self._grammar_rules.append(ReducedRule(nonterm, layout))

    def _build_grammar(self):
        grammar = open(self._grammar_path, 'r')
        for line in grammar:
            if line == '\n':
                continue
            self._extract_rules(line)

    def _init_one_letters(self):
        for idx, letter in enumerate(self._word):
            for rule in self._grammar_rules:
                if rule.layout[0][0] != '"':
                    continue
                if letter == rule.layout[0]:
                    self._d[rule.nonterm][idx][idx + 1] = True

    def _process_words(self, word_length):
        for start in range(len(self._word)):
            end = word_length + start
            if end > len(self._word):
                break
            for rule in self._grammar_rules:
                if rule.layout[0][0] == '"':
                    continue
                for mid_position in range(start + 1, end):
                    self._d[rule.nonterm][start][end] |= \
                        self._d[rule.layout[0]][start][mid_position] and \
                        self._d[rule.layout[1]][mid_position][end]

    def check_word(self, word):
        self._word = word

        for rule in self._grammar_rules:
            self._d[rule.nonterm] = [[False] * (len(self._word) + 1) for i in
                                     range(len(self._word))]

        if word == ['""']:
            return ReducedRule(self._start_nonterm,
                               tuple(['""'])) in self._grammar_rules

        self._init_one_letters()

        for word_len in range(2, len(self._word) + 1):
            self._process_words(word_len)

        return self._d[self._start_nonterm][0][len(self._word)]

from queue import Queue

from src.ChNF_Converter.datatypes import Rule, ReducedRule, CYKGrammarAPI


class Converter:
    def __init__(self, grammar_path):
        self._grammar_path = grammar_path
        self._grammar_rules = list()
        self._start_nonterm = None
        self._nonterms = set()
        self._build_grammar()

    def _extract_rules(self, line):
        line = line.strip('\n')
        nonterm, layouts = line.split('::=')
        nonterm = nonterm.strip(' ')

        if self._start_nonterm is None:
            self._start_nonterm = nonterm

        self._nonterms.add(nonterm)

        for layout in layouts.split('|'):
            layout = layout.strip(' ').split(' ')

            nonterms_in_layout = set(
                [symbol for symbol in layout if
                 symbol[0] == '<' and symbol[-1] == '>']
            )

            self._nonterms.union(nonterms_in_layout)

            self._grammar_rules.append(
                Rule(nonterm, layout, nonterms_in_layout,
                     nonterms_in_layout.copy())
            )

    def _build_grammar(self):
        grammar = open(self._grammar_path, 'r')
        for line in grammar:
            if line == '\n':
                continue
            self._extract_rules(line)

    def _del_non_generative(self):
        non_generative = Queue()
        new_grammar_rules = list()
        used = [False] * len(self._grammar_rules)
        for idx, rule in enumerate(self._grammar_rules):
            if rule.is_right_nonterms_empty('generative'):
                non_generative.put(rule)
                new_grammar_rules.append(rule)
                used[idx] = True

        while not non_generative.empty():
            generative_rule = non_generative.get()
            for idx, rule in enumerate(self._grammar_rules):
                if used[idx]:
                    continue
                rule.right_nonterms_generative.discard(generative_rule.nonterm)

                if rule.is_right_nonterms_empty('generative'):
                    non_generative.put(rule)
                    new_grammar_rules.append(rule)
                    used[idx] = True

        self._grammar_rules = new_grammar_rules

    def _del_unattainable(self):
        is_attainable_keys = list(self._nonterms)
        is_attainable_vals = [False] * len(self._nonterms)

        is_attainable = dict(zip(is_attainable_keys, is_attainable_vals))

        def dfs(nonterm):
            is_attainable[nonterm] = True
            for rule in self._grammar_rules:
                if rule.nonterm != nonterm:
                    continue

                for new_nonterm in rule.right_nonterms_eps:
                    if not is_attainable[new_nonterm]:
                        dfs(new_nonterm)

        dfs(self._start_nonterm)

        new_grammar_rules = list()
        for rule in self._grammar_rules:
            if not is_attainable[rule.nonterm]:
                continue

            for nonterm in rule.right_nonterms_eps:
                if not is_attainable[nonterm]:
                    continue
            new_grammar_rules.append(rule)

        self._grammar_rules = new_grammar_rules

    def _del_mixed_rules(self):

        def is_term(symbol):
            return symbol[0] == '"' and symbol[-1] == '"'

        def is_nonterm(symbol):
            return not is_term(symbol)

        new_grammar_rules = list()
        new_nonterm_idx = 1
        for rule in self._grammar_rules:
            if any(map(is_term, rule.layout)) and \
                    any(map(is_nonterm, rule.layout)):
                for idx, symbol in enumerate(rule.layout):
                    if is_term(symbol):
                        new_grammar_rules.append(
                            Rule(f'<{new_nonterm_idx}>', [symbol], set(),
                                 set()))
                        rule.layout[idx] = f'<{new_nonterm_idx}>'
                        rule.right_nonterms_eps.add(f'<{new_nonterm_idx}>')
                        new_nonterm_idx += 1
            new_grammar_rules.append(rule)
        self._grammar_rules = new_grammar_rules

    def _del_long_rules(self):
        new_grammar_rules = list()
        new_nonterm_idx = 1
        for rule in self._grammar_rules:
            if len(rule.layout) > 2:
                for idx, _ in enumerate(rule.layout):
                    if idx == 0:
                        continue
                    if idx == 1:
                        nonterm = rule.nonterm
                    else:
                        nonterm = new_grammar_rules[-1].layout[-1]
                    layout_fst_nonterm = rule.layout[idx - 1]
                    connection_nonterm = f'<_{new_nonterm_idx}>'
                    new_layout = [layout_fst_nonterm, connection_nonterm]

                    new_grammar_rules.append(
                        Rule(nonterm, new_layout, set(new_layout),
                             set(new_layout)))

                    if idx == len(rule.layout) - 1:
                        new_grammar_rules.append(
                            Rule(connection_nonterm, [rule.layout[-1]],
                                 {rule.layout[-1]},
                                 {rule.layout[-1]}))

                    new_nonterm_idx += 1
            else:
                new_grammar_rules.append(rule)
        self._grammar_rules = new_grammar_rules

    def _del_eps_generative(self):
        eps_generative_nonterms = set()

        def find_eps_generative():
            eps_generative = Queue()
            used = [False] * len(self._grammar_rules)
            for idx, rule in enumerate(self._grammar_rules):
                if rule.layout[0] == '""':
                    eps_generative.put(rule)
                    eps_generative_nonterms.add(rule.nonterm)
                    used[idx] = True

            while not eps_generative.empty():
                generative_rule = eps_generative.get()
                for idx, rule in enumerate(self._grammar_rules):
                    if used[idx]:
                        continue
                    rule.right_nonterms_eps.discard(
                        generative_rule.nonterm)

                    if rule.is_right_nonterms_empty('eps') and rule.layout[0][
                        0] != '"':
                        eps_generative.put(rule)
                        eps_generative_nonterms.add(rule.nonterm)
                        used[idx] = True

        find_eps_generative()
        new_grammar_rules = list()
        eps_generative_nonterms = list(eps_generative_nonterms)
        """Selects non eps-generative rules and create necessary rules."""
        for rule in self._grammar_rules:
            if rule.layout[0] == '""':
                continue

            if rule.layout[0][0] == '"':
                new_grammar_rules.append(rule)
                continue

            if rule.layout[0] in eps_generative_nonterms:
                new_grammar_rules.append(
                    Rule(rule.nonterm, [rule.layout[-1]],
                         {rule.layout[-1]},
                         {rule.layout[-1]}))

            if rule.layout[-1] in eps_generative_nonterms:
                new_grammar_rules.append(
                    Rule(rule.nonterm, [rule.layout[0]], {rule.layout[0]},
                         {rule.layout[0]}))

            new_grammar_rules.append(rule)

        new_start_nonterm = '<_' + self._start_nonterm[1:-1] + '>'
        new_grammar_rules.append(
            Rule(new_start_nonterm, [self._start_nonterm],
                 {self._start_nonterm},
                 {self._start_nonterm}))

        """Add S' -> S and S' -> eps (if necessary)"""
        if self._start_nonterm in eps_generative_nonterms:
            new_grammar_rules.append(
                Rule(new_start_nonterm, ['""'], set(), set()))
        self._start_nonterm = new_start_nonterm

        self._grammar_rules = new_grammar_rules

    def _transitive_closure(self):
        reduced_grammar_rules = list()
        for rule in self._grammar_rules:
            reduced_grammar_rules.append(
                ReducedRule(rule.nonterm, tuple(rule.layout)))
        self._grammar_rules = set(reduced_grammar_rules)
        new_grammar_rules = set()
        while True:
            for fst_rule in self._grammar_rules:
                if len(fst_rule.layout) == 1 and fst_rule.layout[0][0] == '<':
                    for snd_rule in self._grammar_rules:
                        if fst_rule.layout[0] == snd_rule.nonterm:
                            new_grammar_rules.add(
                                ReducedRule(fst_rule.nonterm, snd_rule.layout))

                new_grammar_rules.add(fst_rule)
            if new_grammar_rules == self._grammar_rules:
                break
            self._grammar_rules = new_grammar_rules.copy()
            new_grammar_rules.clear()
        new_grammar_rules.clear()
        for rule in self._grammar_rules:
            if len(rule.layout) != 1 or rule.layout[0][0] != '<':
                new_grammar_rules.add(rule)
        self._grammar_rules = new_grammar_rules

    def convert_to_ch_nf(self):
        self._del_non_generative()
        self._del_unattainable()
        self._del_mixed_rules()
        self._del_long_rules()
        self._del_eps_generative()
        self._transitive_closure()

        return self._grammar_rules

    def print_rules(self):
        for rule in self._grammar_rules:
            print(rule)

    def GetGrammarToCYK(self):
        return CYKGrammarAPI(self._grammar_rules, self._start_nonterm)

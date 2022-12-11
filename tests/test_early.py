import pytest
from pathlib import Path

from early.parser import EarlyParser

TEST_DATA_DIR = Path(__file__).resolve().parent / 'data'


def test_early_parser():
    parser = EarlyParser(TEST_DATA_DIR / 'BNF_example.txt')

    assert (True == parser.parse('""'))

    assert (True == parser.parse(['"a"', '"b"']))
    assert (True == parser.parse(['"a"', '"b"', '"a"', '"b"']))
    assert (True == parser.parse(['"a"', '"b"', '"a"', '"b"', '"a"', '"b"']))

    assert (True == parser.parse(['"a"', '"a"', '"b"', '"b"']))
    assert (True == parser.parse(['"a"', '"a"', '"a"', '"b"', '"b"', '"b"']))
    assert (True == parser.parse(
        ['"a"', '"a"', '"a"', '"b"', '"b"', '"b"', '"a"', '"b"']))
    assert (True == parser.parse(
        ['"a"', '"a"', '"a"', '"b"', '"b"', '"b"', '"a"', '"a"', '"b"', '"b"']))

    assert (False == parser.parse(['"a"', '"a"']))
    assert (False == parser.parse(['"b"', '"b"']))
    assert (False == parser.parse(['"a"', '"a"', '"a"']))
    assert (False == parser.parse(['"a"', '"b"', '"a"']))
    assert (False == parser.parse(['"a"', '"b"', '"b"', '"a"']))

    assert ( '<S> ::= "a" <S> "b" <S> | ""\n\n' == parser.get_grammar())

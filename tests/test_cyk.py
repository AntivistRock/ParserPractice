import pytest
from pathlib import Path

from src.CYK.CYK import CYKParser

TEST_DATA_DIR = Path(__file__).resolve().parent / 'data'


def test_cyk_parser():
    parser = CYKParser(TEST_DATA_DIR / 'BNF_example.txt', is_in_ch_nf=False)

    assert (True == parser.check_word(['""']))

    assert (True == parser.check_word(['"a"', '"b"']))
    assert (True == parser.check_word(['"a"', '"b"', '"a"', '"b"']))
    assert (True == parser.check_word(['"a"', '"b"', '"a"', '"b"', '"a"', '"b"']))

    assert (True == parser.check_word(['"a"', '"a"', '"b"', '"b"']))
    assert (True == parser.check_word(['"a"', '"a"', '"a"', '"b"', '"b"', '"b"']))
    assert (True == parser.check_word(
        ['"a"', '"a"', '"a"', '"b"', '"b"', '"b"', '"a"', '"b"']))
    assert (True == parser.check_word(
        ['"a"', '"a"', '"a"', '"b"', '"b"', '"b"', '"a"', '"a"', '"b"', '"b"']))

    assert (False == parser.check_word(['"a"', '"a"']))
    assert (False == parser.check_word(['"b"', '"b"']))
    assert (False == parser.check_word(['"a"', '"a"', '"a"']))
    assert (False == parser.check_word(['"a"', '"b"', '"a"']))
    assert (False == parser.check_word(['"a"', '"b"', '"b"', '"a"']))

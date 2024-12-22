import pytest
from filter_bazhar import is_preposition


@pytest.mark.parametrize("word,expected", [
    ("и", True),  # conjunction
    ("в", True),  # preposition
    ("не", True),  # particle
    ("ах", False),  # interjection
    ("дом", False),  # noun
    ("бежать", False),  # verb
    ("красивый", False),  # adjective
    ("быстро", False),  # adverb
])
def test_is_preposition(word, expected):
    assert is_preposition(word) == expected

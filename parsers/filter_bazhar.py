import pymorphy3


def is_preposition(word):
    """Определяет, является ли слово предлогом."""
    morph = pymorphy3.MorphAnalyzer()
    parsed_word = morph.parse(word)[0]
    return parsed_word.tag.POS in {'PREP', 'CONJ', 'PRCL', 'INTJ'}

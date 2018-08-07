import re
import unicodedata
import os


def remove_num(phrase):
    numRE = re.compile("[0-9]+")
    return numRE.sub(" ", phrase)


def remove_unicode_spaces(phrase):
    spacesRE = re.compile(u"[\u2000-\u200F\u00A0\u2028-\u202F]")
    return spacesRE.sub(" ", phrase)


def normalize_quotes(phrase):
    quotesRE = re.compile(u"[`\u2019]")
    return quotesRE.sub("'", phrase)


def remove_symbols(phrase):
    """Remove ascii symbols"""
    latinRE = re.compile("[\ -/:-@\[-`{-~]")
    return latinRE.sub(" ", phrase)


def remove_unicode_symbols(phrase):
    latinOneRE = re.compile(u"[\u00A1-\u00BF]")
    unicodeRE = re.compile(u"[\u2010-\u2027\u2030-\u203A]")
    currencyRE = re.compile(u"[\u20A0-\u20BF]")
    blockRE = re.compile(u"[\u2580-\u259F]")
    othersRE = re.compile(u"[\ufeff]")
    return latinOneRE.sub(" ", unicodeRE.sub(" ",
                    currencyRE.sub(" ", blockRE.sub(" ",
                    othersRE.sub(" ", phrase)))))


def remove_accents(phrase):
    """Remove accents from characters and
    return their ascii equivalent
    """
    nkfd_form = unicodedata.normalize('NFKD', phrase)
    # more about normalized forms
    # https://www.unicode.org/reports/tr15/
    return nkfd_form.encode('ASCII', 'ignore').decode('ASCII')


def one_line_doc(file_path):
    """Merge all lines of a file into one"""
    lines = []
    with open(file_path, "r") as input_file:
        for line in input_file:
            lines.append(line.strip())
    return " ".join(lines)


def load_stop_words():
    french_stop_words = []
    stop_word_path = os.path.join(os.path.dirname(__file__), "french_stop.txt")
    with open(stop_word_path, 'r') as stop_list:
        for word in stop_list:
            french_stop_words.append(word.strip())
    return french_stop_words

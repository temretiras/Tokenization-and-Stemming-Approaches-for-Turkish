import re

TR_LETTERS_LOWER = r"a-zçğıöşüâîû"
TR_LETTERS_UPPER = r"A-ZÇĞİÖŞÜÂÎÛ"
TR_LETTERS_ALL = TR_LETTERS_LOWER + TR_LETTERS_UPPER
TR_ALPHANUMERIC = r"0-9" + TR_LETTERS_ALL
TR_ALPHANUMERIC_UNDERSCORE = TR_ALPHANUMERIC + r"_"
APOSTROPHE = r"['`´‘’]"
APOS_AND_SUFFIX_PATTERN = rf"{APOSTROPHE}[{TR_LETTERS_ALL}]+"

REGEX_PUNCTUATION_MULTI = r"\.{3}|\…"
REGEX_URL = r"https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+|www\.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
REGEX_EMAIL = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"

REGEX_DATE = r"\b(?:[0-3]?\d(?:[./\-])(?:0?[1-9]|1[0-2])(?:[./\-])(?:(?:1[7-9]|20)\d{2}|\d{2}))\b"
REGEX_TIME = r"\b[0-2]?\d[:.][0-5]\d(?:[:.][0-5]\d)?\b"
REGEX_PERCENT_NUM = r"%\d+(?:[.,]\d+)?(?:[Ee][+\-]?\d+)?|%\d{1,3}(?:\.\d{3})*(?:,\d+)?|%\d+"
REGEX_NUMBER_FULL = r"[+\-]?\d{1,3}(?:\.\d{3})+(?:,\d+)?\b"
REGEX_NUMBER_DECIMAL_COMMA = r"[+\-]?\d+,\d+\b"
REGEX_NUMBER_SIMPLE = r"[+\-]?\d+\b"

REGEX_ABBREVIATION_DOTS = r"(?:[A-ZÇĞİÖŞÜ]\.){2,}"
REGEX_SHORT_ABBR = r"\b(?:[A-ZÇĞİÖŞÜ][a-zçğıöşü]{1,3}\.|[a-zçğıöşü]{2,3}\.)\b"
REGEX_WORD_WITH_SYMBOL = rf"[{TR_ALPHANUMERIC}]+(?:[-/][{TR_ALPHANUMERIC}]+)+"

REGEX_HASHTAG = rf"#[{TR_ALPHANUMERIC_UNDERSCORE}]+"
REGEX_MENTION = rf"@[{TR_ALPHANUMERIC_UNDERSCORE}]+"

REGEX_WORD_ALPHANUMERIC = rf"\b[{TR_LETTERS_ALL}\d]+\b"
REGEX_APOSTROPHE_SUFFIX = rf"{APOSTROPHE}[{TR_LETTERS_ALL}]+"
REGEX_PUNCTUATION = r"""[.,!?%$&*+;:(){}\[\]\"'`´‘’«»<>^=/|\\\-–—]"""

TOKEN_PATTERN = re.compile(
    "|".join([
        REGEX_PUNCTUATION_MULTI,
        REGEX_URL, REGEX_EMAIL,
        REGEX_DATE, REGEX_TIME, REGEX_PERCENT_NUM,
        REGEX_NUMBER_FULL, REGEX_NUMBER_DECIMAL_COMMA, REGEX_NUMBER_SIMPLE,
        REGEX_ABBREVIATION_DOTS, REGEX_SHORT_ABBR,
        REGEX_WORD_WITH_SYMBOL,
        REGEX_HASHTAG, REGEX_MENTION,
        REGEX_WORD_ALPHANUMERIC,
        REGEX_APOSTROPHE_SUFFIX,
        REGEX_PUNCTUATION
    ]),
    re.UNICODE
)

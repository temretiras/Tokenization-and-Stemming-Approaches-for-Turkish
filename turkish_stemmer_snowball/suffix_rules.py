INFLECTIONAL_SUFFIXES = [
    "lar", "ler",
    "yı", "yi", "yu", "yü",
    "ya", "ye",
    "yda", "yde", "ydan", "yden",
    "de", "te", "da", "nda", "ta", "den", "ten", "dan", "tan",
    "m", "n", "miz", "niz", "leri", "si", "sı", "su", "sü",
    "sin", "sın", "siniz", "sınız", "ımız", "uz", "sınız",
    "di", "dı", "du", "dü", "ti", "tı", "tu", "tü",
    "yor", "acak", "ecek", "mış", "miş", "muş", "müş",
    "dir", "dır", "dur", "dür", "tir", "tır", "tur", "tür",
    "abilir", "ebilir", "yabilir", "yebilir", "bil", "ebil",
    "le", "la", "yla", "yle",
    "ne", "na", "e", "a", "i", "ı", "u", "ü",
    "dik", "ur", "ul", "il", "r", "mez", "maz",
    "iyor", "üyor", "ıyor", "uyor", "sın", "sin", "sun", "sün", "ız", "iz", "uz", "üz", "yse", "sa", "se", "ysa"
]


DERIVATIONAL_SUFFIXES = [
    "ci", "cı", "cu", "cü", "siz", "sız", "suz", "süz",
    "laş", "leş", "laştır", "leştir", "tir", "tır", "tur", "tür",
    "ce", "ca",
    "mak", "mek",
    "c", "ç",
    "ecek", "acak", "yacak", "yip", "up", "er", "ul",
    "dık", "dik", "dük", "duk", "mez", "maz",
    "ış", "üp", "ıp", "ip", "erek", "arak", "yarak", "yerek",
    "dur", "ıl", "abil", "ebil", "ma", "me", "inci", "iş"
]


def normalize_word(word: str) -> str:
    if not isinstance(word, str):
        return word
    return word.strip().lower()


def normalize_suffix_lists():
    """Ensure suffix lists are unique and ordered by length (mak/mek prioritized)."""
    global INFLECTIONAL_SUFFIXES, DERIVATIONAL_SUFFIXES
    priority = {"mak", "mek"}
    INFLECTIONAL_SUFFIXES = sorted(set(INFLECTIONAL_SUFFIXES), key=len, reverse=True)
    DERIVATIONAL_SUFFIXES = (
        ["mak", "mek"]
        + [s for s in sorted(set(DERIVATIONAL_SUFFIXES), key=len, reverse=True) if s not in priority]
    )


normalize_suffix_lists()

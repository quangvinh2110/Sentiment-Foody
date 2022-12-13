import re
import sys
import unicodedata
from string import ascii_lowercase, digits, whitespace, punctuation


CURRENCIES = {
    "$": "USD",
    "zł": "PLN",
    "£": "GBP",
    "¥": "JPY",
    "฿": "THB",
    "₡": "CRC",
    "₦": "NGN",
    "₩": "KRW",
    "₪": "ILS",
    "₫": "VND",
    "€": "EUR",
    "₱": "PHP",
    "₲": "PYG",
    "₴": "UAH",
    "₹": "INR",
}
CURRENCY_REGEX = re.compile(
    "({})+".format("|".join(re.escape(c) for c in CURRENCIES.keys()))
)

PUNCT_TRANSLATE_UNICODE = dict.fromkeys(
    (i for i in range(sys.maxunicode) if unicodedata.category(chr(i)).startswith("P")),
    "",
)

ACRONYM_REGEX = re.compile(
    r"(?:^|(?<=\W))(?:(?:(?:(?:[A-Z]\.?)+[a-z0-9&/-]?)+(?:[A-Z][s.]?|[0-9]s?))|(?:[0-9](?:\-?[A-Z])+))(?:$|(?=\W))",
    flags=re.UNICODE,
)

# taken hostname, domainname, tld from URL regex below
EMAIL_REGEX = re.compile(
    r"(?:^|(?<=[^\w@.)]))([\w+-](\.(?!\.))?)*?[\w+-](@|[(<{\[]at[)>}\]])(?:(?:[a-z\\u00a1-\\uffff0-9]-?)*[a-z\\u00a1-\\uffff0-9]+)(?:\.(?:[a-z\\u00a1-\\uffff0-9]-?)*[a-z\\u00a1-\\uffff0-9]+)*(?:\.(?:[a-z\\u00a1-\\uffff]{2,}))",
    flags=re.IGNORECASE | re.UNICODE,
)

REGEX_WEIGHT_KG = re.compile(r'(?<=[{}{}])\d+kg(?=[{}{}])'.format(punctuation, whitespace, punctuation, whitespace), flags=re.I)
REGEX_WEIGHT_G = re.compile(r'(?<=[{}{}])\d+g(?=[{}{}])'.format(punctuation, whitespace, punctuation, whitespace), flags=re.I)
# regex_currency_d = [r'[0-9]{3,}d', r'[0-9]{3,}đ', r'[0-9]{3,}₫', r'[0-9]{3,}vnd']
REGEX_CURRENCY_D = re.compile(r'(?<=[{}{}])\d+(d|đ|₫|vnd)(?=[{}{}])'.format(punctuation, whitespace, punctuation, whitespace), flags=re.I)
# regex_currency_k = re.compile(r'[0-9]{1,}k')
REGEX_CURRENCY_K = re.compile(r'(?<=[{}{}])\d+k(?=[{}{}])'.format(punctuation, whitespace, punctuation, whitespace), flags=re.I)
REGEX_CURRENCY_TR = re.compile(r'(?<=[{}{}])\d+tr(?=[{}{}])'.format(punctuation, whitespace, punctuation, whitespace), flags=re.I)
REGEX_HOUR = re.compile(r'(?<=[{}{}])\d+h(?=[{}{}])'.format(punctuation, whitespace, punctuation, whitespace), flags=re.I)

# for more information: https://github.com/jfilter/clean-text/issues/10
PHONE_REGEX = re.compile(
    r"0[0-9\s.-]{9,13}"
)

NUMBERS_REGEX = re.compile(
    r"(?:^|(?<=[^\w,.]))[+–-]?(([1-9]\d{0,2}(,\d{3})+(\.\d*)?)|([1-9]\d{0,2}([ .]\d{3})+(,\d*)?)|(\d*?[.,]\d+)|\d+)(?:$|(?=\b))"
)

LINEBREAK_REGEX = re.compile(r"((\r\n)|[\n\v])+")
TWO_LINEBREAK_REGEX = re.compile(r"((\r\n)|[\n\v])+((\r\n)|[\n\v])+")
MULTI_WHITESPACE_REGEX = re.compile(r"\s+")
MULTI_SPACE_REGEX = re.compile(r" {2,}")
NONBREAKING_SPACE_REGEX = re.compile(r"(?!\n)\s+")

# source: https://gist.github.com/dperini/729294
# @jfilter: I guess it was changed
URL_REGEX = re.compile(
    r"(?:^|(?<![\w\/\.]))"
    # protocol identifier
    # r"(?:(?:https?|ftp)://)"  <-- alt?
    r"(?:(?:https?:\/\/|ftp:\/\/|www\d{0,3}\.))"
    # user:pass authentication
    r"(?:\S+(?::\S*)?@)?" r"(?:"
    # IP address exclusion
    # private & local networks
    r"(?!(?:10|127)(?:\.\d{1,3}){3})"
    r"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
    r"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"
    # IP address dotted notation octets
    # excludes loopback network 0.0.0.0
    # excludes reserved space >= 224.0.0.0
    # excludes network & broadcast addresses
    # (first & last IP address of each class)
    r"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
    r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
    r"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
    r"|"
    # host name
    r"(?:(?:[a-z\\u00a1-\\uffff0-9]-?)*[a-z\\u00a1-\\uffff0-9]+)"
    # domain name
    r"(?:\.(?:[a-z\\u00a1-\\uffff0-9]-?)*[a-z\\u00a1-\\uffff0-9]+)*"
    # TLD identifier
    r"(?:\.(?:[a-z\\u00a1-\\uffff]{2,}))" r"|" r"(?:(localhost))" r")"
    # port number
    r"(?::\d{2,5})?"
    # resource path
    r"(?:\/[^\)\]\}\s]*)?",
    # r"(?:$|(?![\w?!+&\/\)]))",
    # @jfilter: I removed the line above from the regex because I don't understand what it is used for, maybe it was useful?
    # But I made sure that it does not include ), ] and } in the URL.
    flags=re.UNICODE | re.IGNORECASE,
)

VIETNAMESE_CHARS = r"àảãáạằẳẵắặăầẩẫấậâđèẻẽéẹềểễếệêìỉĩíịòỏõóọồổỗốộôờởỡớợơùủũúụừửữứựưỳỷỹýỵ{}".format(
    ascii_lowercase)

VIETNAMESE_CHARS_AND_DIGITS = r"àảãáạằẳẵắặăầẩẫấậâđèẻẽéẹềểễếệêìỉĩíịòỏõóọồổỗốộôờởỡớợơùủũúụừửữứựưỳỷỹýỵ{}{}".format(
    ascii_lowercase, digits)

strange_double_quotes = [
    "«",
    "‹",
    "»",
    "›",
    "„",
    "“",
    "‟",
    "”",
    "❝",
    "❞",
    "❮",
    "❯",
    "〝",
    "〞",
    "〟",
    "＂",
]
strange_single_quotes = ["‘", "‛", "’", "❛", "❜", "`", "´", "‘", "’"]

DOUBLE_QUOTE_REGEX = re.compile("|".join(strange_double_quotes))
SINGLE_QUOTE_REGEX = re.compile("|".join(strange_single_quotes))


# regex_weight_kg = re.compile(r'[0-9]{1,}kg')
# regex_weight_g = re.compile(r'[0-9]{1,}g')
# regex_currency_d = [r'[0-9]{3,}d', r'[0-9]{3,}đ', r'[0-9]{3,}₫', r'[0-9]{3,}vnd']
# regex_currency_k = re.compile(r'[0-9]{1,}k')
# regex_currency_tr = re.compile(r'[0-9]{1,}tr')
# regex_hours = re.compile(r'[0-9]{1,}h')
# regex_speed_traffict = [r'[0-9]{1,}mbps', r'[0-9]{1,}gb']


TONENORMALIZE_DICT = (
    ("òa", "oà"),
    ("Òa", "Oà"),
    ("ÒA", "OÀ"),
    ("óa", "oá"),
    ("Óa", "Oá"),
    ("ÓA", "OÁ"),
    ("ỏa", "oả"),
    ("Ỏa", "Oả"),
    ("ỎA", "OẢ"),
    ("õa", "oã"),
    ("Õa", "Oã"),
    ("ÕA", "OÃ"),
    ("ọa", "oạ"),
    ("Ọa", "Oạ"),
    ("ỌA", "OẠ"),
    ("òe", "oè"),
    ("Òe", "Oè"),
    ("ÒE", "OÈ"),
    ("óe", "oé"),
    ("Óe", "Oé"),
    ("ÓE", "OÉ"),
    ("ỏe", "oẻ"),
    ("Ỏe", "Oẻ"),
    ("ỎE", "OẺ"),
    ("õe", "oẽ"),
    ("Õe", "Oẽ"),
    ("ÕE", "OẼ"),
    ("ọe", "oẹ"),
    ("Ọe", "Oẹ"),
    ("ỌE", "OẸ"),
    ("ùy", "uỳ"),
    ("Ùy", "Uỳ"),
    ("ÙY", "UỲ"),
    ("úy", "uý"),
    ("Úy", "Uý"),
    ("ÚY", "UÝ"),
    ("ủy", "uỷ"),
    ("Ủy", "Uỷ"),
    ("ỦY", "UỶ"),
    ("ũy", "uỹ"),
    ("Ũy", "Uỹ"),
    ("ŨY", "UỸ"),
    ("ụy", "uỵ"),
    ("Ụy", "Uỵ"),
    ("ỤY", "UỴ"),
)

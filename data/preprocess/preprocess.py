from typing import Optional
import emoji
import json
from .constants import *
from string import punctuation, whitespace
import re
import unicodedata
import os

with open(os.path.dirname(os.path.realpath(__file__)) + '/teencode.json', 'r') as f:
    teencode = json.load(f)


def normalize_text_to_nfc_standard(text: str) -> str:
    return unicodedata.normalize('NFC', text)

def normalize_text_to_nfkc_standard(text: str) -> str:
    return unicodedata.normalize('NFKC', text)

def normalize_tone(text: str) -> str:
    for tone, tone_replace in TONENORMALIZE_DICT:
        text = text.replace(tone, tone_replace)
    return text


def handle_phone_numbers(text: str, replace_with: str = " <PN>") -> str:
    return PHONE_REGEX.sub(replace_with, text)


def handle_emails(text: str, replace_with: str = " <EMAIL> ") -> str:
    return EMAIL_REGEX.sub(replace_with, text)


def handle_urls(text: str, replace_with: str = " <URL> ") -> str:
    return URL_REGEX.sub(replace_with, text)


def handle_currency(text: str) -> str:

    text = REGEX_WEIGHT_KG.sub('N kilogam', text)
    text = REGEX_WEIGHT_G.sub('N gam', text)
    text = REGEX_CURRENCY_D.sub('N vnd', text)
    text = REGEX_CURRENCY_K.sub('N nghìn vnd', text)
    text = REGEX_CURRENCY_TR.sub('N triệu vnd', text)
    text = REGEX_HOUR.sub('N giờ', text)

    # for match in REGEX_WEIGHT_G.findall(text):
    #     text = text.replace(match, match[0] + 'N gam' + match[-1])
    # for match in REGEX_WEIGHT_KG.findall(text):
    #     text = text.replace(match, match[0] + 'N kilogam' + match[-1])
    # for match in REGEX_CURRENCY_D.findall(text):
    #     text = text.replace(match, match[0] + 'N vnd' + match[-1])
    # for match in REGEX_CURRENCY_K.findall(text):
    #     text = text.replace(match, match[0] + 'N nghìn vnd' + match[-1])
    # for match in REGEX_CURRENCY_TR.findall(text):
    #     text = text.replace(match, match[0] + 'N triệu vnd' + match[-1])
    # for match in REGEX_HOUR.findall(text):
    #     text = text.replace(match, match[0] + 'N giờ' + match[-1])

    return text

# def replace_speed_traffic(text):
#     list_speed_traffict = []
#     for e_regex in regex_speed_traffict:
#         list_speed_traffict += re.findall(e_regex, text)
#     for e_match_k in list_speed_traffict:
#         text = text.replace(e_match_k, " số tốc độ mạng ")

#     text = text.replace(" 3g.", " ba g.")
#     text = text.replace(" 3g ", " ba g ")
#     text = text.replace(" 3g,", " ba g,")
#     text = text.replace(" 4g ", " bốn g ")
#     text = text.replace(" 4g.", "bốn g.")
#     text = text.replace(" 4g,", "bốn g,")
#     return text

def handle_punctuation(text: str) -> str:
    # return text.translate(str.maketrans('', '', punctuation))
    return text.translate(str.maketrans(punctuation, ' '*len(punctuation)))


def handle_multispace(text: str) -> str:
    # text = re.sub('\s+', ' ', text)
    text = re.sub(' {2,}', ' ', text)
    # handle exception when line just all of punctuation
    if len(text) == 0:
        return text

    if text[0] == " ":
        return text[1:]

    return text


def handle_whitespace(text: str) -> str:
    return text.translate(str.maketrans(whitespace, ' '*len(whitespace)))


def join_punctuation(seq, characters='.,;?!'):
    characters = set(characters)
    seq = iter(seq)
    current = next(seq)

    for nxt in seq:
        if nxt in characters:
            current += nxt
        else:
            yield current
            current = nxt

    yield current


def handle_teencode(text: str) -> str:
    parts = re.findall(
        r"[{}]+|[^{}]+".format(VIETNAMESE_CHARS_AND_DIGITS, VIETNAMESE_CHARS_AND_DIGITS), text, flags=re.I)
    return "".join(teencode.get(part, part) for part in parts)


def remove_multi_space_and_replace_teencode(text: str) -> str:
    # _pattern = r"[\w']+|[{}]".format(punctuation)
    # return " ".join(join_punctuation(teencode.get(word, word) for word in re.findall(_pattern, text, flags=re.I)))
    return " ".join(teencode.get(word, word) for word in text.split())


def handle_foody_data(text: str,
                      normalize: bool = True,
                      lowercase: bool = True,
                      tone_normalize: bool = True,
                      remove_punctuation: bool = True,
                      replace_currency: bool = True,
                      replace_teencode: bool = True,
                      phone_number: Optional[str] = None,
                      url: Optional[str] = None,
                      email: Optional[str] = None,
                      emoji_mode: Optional[str] = None,
                      remove_special_characters: bool = False,
                      remove_whitespace: bool = True,
                      remove_multispace: bool = True,
                      ) -> str:

    # normalize text to NFC standard
    if normalize:
        text = normalize_text_to_nfkc_standard(text)
    # convert text to lowercase
    if lowercase:
        text = text.lower()
    # normalize tone for vietnamese data
    if tone_normalize:
        text = normalize_tone(text)
    # remove punctuation
    if remove_punctuation:
        text = handle_punctuation(text)
    # replace currency
    if replace_currency:
        text = handle_currency(text)
    # replace some teencode
    if replace_teencode:
        text = handle_teencode(text)
    # handle phone number
    if phone_number:
        text = handle_phone_numbers(text, phone_number)
    # handle url
    if url:
        text = handle_urls(text, url)
    # handle email
    if email:
        text = handle_emails(text, email)
    # handle emoji
    if not emoji_mode:
        text = emoji.demojize(text, delimiters=(" !@#", "!@# "))
        text = emoji.emojize(text, delimiters=("!@#", "!@#"))
    elif emoji_mode == "demojize":
        text = emoji.demojize(text, delimiters=(" ", " "))
        text = text.replace("_", " ")
    elif emoji_mode == "remove":
        text = emoji.replace_emoji(text, replace=' ')
    else:
        raise Exception("ERROR!!!!!")
    # remove all character except vietnamese characters, digits and punctuation
    if remove_special_characters:
        if not emoji_mode:
            text = emoji.demojize(text)
            text = re.sub(r'[^{}{}]+'.format(punctuation,
                                            VIETNAMESE_CHARS_AND_DIGITS),
                        ' ', text, flags=re.I)
            text = emoji.emojize(text)
        else:
            text = re.sub(r'[^{}{}]+'.format(punctuation,
                                         VIETNAMESE_CHARS_AND_DIGITS),
                      ' ', text, flags=re.I)
    # remove tab, newline,...
    if remove_whitespace:
        text = handle_whitespace(text)
    # remove multispace
    if remove_multispace:
        text = handle_multispace(text)

    return text


if __name__ == '__main__':
    test_string_1 = """
    ❖▬▬▬▬▬▬▬▬▬ஜ۩۞۩ஜ▬▬▬▬▬▬▬▬▬❖
    ➤  NHẤN ĐĂNG KÝ & THEO DÕI KÊNH  Barina TV để nhận thông báo khi có Video mới nhé cả nhà ơi !!!
    ➤ Chúc cả nhà có thật nhiều sức khỏe, nhiều niềm vui trong cuộc sống...! 

    ➤ Đăng ký kênh ""Barina TV"" ủng hộ tinh thần tại đây: http://www.youtube.com/c/BarinaTV
    """
    test_string_2 = """
    😍CÀ PHÊ SỮA TRẦN QUANG GOOD MORNING😍
    💥Giá 50.000đ /1 gói 24 túi pha milako
    ☕️ Đây là sản phẩm cà phê mang hương vị nhẹ nhàng, ngọt thanh khiết kết hợp với vị kem sữa đặc biệt làm lên một dòng sản phẩm tuyệt hảo.
    ☕Chào buổi sáng đặc biệt thích hợp với những ai thích vị kem sữa, ngọt và ít cà phê hoặc những ai có lựa chọn có thể uống cà phê nhiêu hơn một 1 lần trong ngày.
    ☕Bạn muốn uống cà phê nhưng không có thời gian pha phin. Muốn tiện lợi, tiết kiệm thời gian.Bạn muốn an tâm về sức khỏe với nguồn gốc, xuất xứ cà phê rõ ràng. Dùng nóng trong những ngày se lạnh hoặc dùng lạnh trong những ngày oi bức.
    ☕Với cà phê sữa Good Morning bạn sẽ yên tâm về chất lượng, an toàn vệ sinh thực phẩm cũng như tính tiện lợi vô cùng của sản phẩm. 
    ☕️Mùa dịch này thèm thì tự pha, hạn chế đi lại, hạn chế tiếp xúc, cố gắng lên mọi người nhé. 
    😘khách có nhu cầu chọn món ⤵️
    🛒 𝑯𝒂̃𝒚 𝒍𝒊𝒆̂𝒏 𝒉𝒆̣̂ đ𝒂̣̆𝒕 𝒉𝒂̀𝒏𝒈 𝒏𝒈𝒂𝒚 𝒒𝒖𝒂 : 𝑰𝒏𝒃𝒐𝒙 𝑭𝒂𝒏𝒑𝒂𝒈𝒆 bảo bảo shop, 𝒁𝒂𝒍𝒐 ( 0902654056 ) đ𝒆̂̉ đ𝒖̛𝒐̛̣𝒄 𝒕𝒖̛ 𝒗𝒂̂́𝒏 𝒕𝒓𝒖̛̣𝒄 𝒕𝒊𝒆̂́𝒑 𝒗𝒂̀ 𝒈𝒊𝒂𝒐 𝒉𝒂̀𝒏𝒈 𝒕𝒂̣̂𝒏 𝒏𝒐̛𝒊. 
    🚚 Ship ngoại thành GHTK - GHN 
    🛵 Ship nội thành GRAB- AHA- NOW 
    ( Phí ship tính từ Phường 11 Quận 6 ) 
    💳 Thanh Toán - Ck - Momo - Zalo pay 
    ----------------❤️❤️❤️-----------------
    🙇 Cửa hàng xin trân trọng cảm ơn quý khách ❤
    ---------------------------------------------------
    🛵 NHẬN SHIPCOD TOÀN QUỐC !!!
    ---------------------------------------------------
    📲 Hotline đặt hàng:0393144464
    🏠 Cửa Hàng : 729 Hậu Giang Phường 11 Quận 6
    """
    with open("output.txt", "w") as text_file:
        print(handle_foody_data(test_string_2, phone_number=" <PN> ", url=" <URL> ", email=" <MAIL> "), file=text_file)

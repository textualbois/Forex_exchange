def format_currency_location(location, lang):
    if location == "NAL":
        return in_cash[lang]
    elif location == "RU":
        return on_russian_account[lang]
    elif location == "TR":
        return on_turkish_account[lang]


in_cash = {"RUS": "наличными", "ENG": "in cash"}
on_russian_account = {"RUS": "на Российской карте", "ENG": "on Russian account"}
on_turkish_account = {"RUS": "на Турецкой карте", "ENG": "on Turkish account"}


def format_currency_name(currency_name, lang):
    rubles = {"RUS": "Российских Рублях", "ENG": "Russian Rubles"}
    trl = {"RUS": "Турецких Лирах", "ENG": "Turkish Liras"}
    usd = {"RUS": "Долларах", "ENG": "US Dollars"}
    if currency_name == "RUB":
        return rubles[lang]
    elif currency_name == "TRL":
        return trl[lang]
    elif currency_name == "USD":
        return usd[lang]




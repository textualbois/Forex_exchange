from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup



def markup_menu_start(chatId):
    markup = InlineKeyboardMarkup()
    markup.width = 2
    markup.add(
        InlineKeyboardButton("Оставить заявку", callback_data="NEWBID__")
    )
    markup.add(
        InlineKeyboardButton("Посмотреть свои заявки", callback_data="MYBIDS__")
    )
    markup.add(
        InlineKeyboardButton("Входящие запросы", callback_data="INCOMINGBIDS__")
    )
    markup.add(
        InlineKeyboardButton("Посмотреть подходящие обмены", callback_data="OTHERSBIDS__")
    )
    markup.add(
        InlineKeyboardButton("Мои данные", callback_data="CONTACTSMENU__")
    )
    markup.add(
        InlineKeyboardButton("не работает Обратная связь. Ошибки в боте", callback_data="FEEDBACK__")
    )
    return markup


def markup_my_contacts(chatId):
    markup = InlineKeyboardMarkup()
    markup.width = 2
    markup.add(
        InlineKeyboardButton("Посмотреть свои данные", callback_data="VIEWCONTACTS__")
    )
    markup.add(
        InlineKeyboardButton("Добавить свои данные", callback_data="ADDCONTACTS__")
    )
    return markup


def markup_my_bids(chatId):
    markup = InlineKeyboardMarkup()
    markup.width = 2
    markup.add(
        InlineKeyboardButton("Активные заявки", callback_data="WHATBIDS_ACTIVE__")
    )
    markup.add(
        InlineKeyboardButton("Исполненные заявки", callback_data="WHATBIDS_FULFILLED__")
    )
    markup.add(
        InlineKeyboardButton("Удаленные заявки", callback_data="WHATBIDS_CANCELLED__")
    )
    return markup


def markup_my_active(chatId, bid_id_list, offset, show_more):
    print(bid_id_list)
    markup = InlineKeyboardMarkup()
    markup.width = 2
    if show_more:
        markup.add(
            InlineKeyboardButton("Показать ещё заявки", callback_data="MYACTIVEBIDS_SHOWMORE__")
        )
    markup.add(
        InlineKeyboardButton("Выйти в основное меню", callback_data="MAINMENU__")
    )
    for i in range(len(bid_id_list)):
        markup.add(
            InlineKeyboardButton(f"🛑 Удалить №{offset + i + 1}",
                                 callback_data=f"DELETEBID_{bid_id_list[i]}__"),
            InlineKeyboardButton(f"💱 Подобрать №{offset + i + 1}",
                                 callback_data=f"MATCHTHISBID_{bid_id_list[i]}__")
        )
    return markup


# TODO
def markup_my_cancelled(chatId, bid_id_list, offset, show_more):
    markup = InlineKeyboardMarkup()
    markup.width = 2
    if show_more:
        markup.add(
            InlineKeyboardButton("Показать ещё заявки", callback_data="MYСANCELLEDBIDS_SHOWMORE__")
        )
    markup.add(
        InlineKeyboardButton("Выйти в основное меню", callback_data="MAINMENU__")
    )
    for i in range(len(bid_id_list)):
        markup.add(
            InlineKeyboardButton(f"Восстановить копию заявки №{offset + i + 1}",
                                 callback_data=f"RESTOREBID_{bid_id_list[i]}__")
        )
    return markup


def markup_search_range(chatId):
    markup = InlineKeyboardMarkup()
    markup.width = 2
    markup.add(
        InlineKeyboardButton("2 Km", callback_data="SEARCHRANGE_2__"),
        InlineKeyboardButton("5 Km", callback_data="SEARCHRANGE_5__"),
        InlineKeyboardButton("10 Km", callback_data="SEARCHRANGE_10__")
    )
    markup.add(
        InlineKeyboardButton("15 Km", callback_data="SEARCHRANGE_15__"),
        InlineKeyboardButton("20 Km", callback_data="SEARCHRANGE_20__"),
        InlineKeyboardButton("25 Km", callback_data="SEARCHRANGE_25__")
    )
    markup.add(
        InlineKeyboardButton("50 Km", callback_data="SEARCHRANGE_50__"),
        InlineKeyboardButton("75 Km", callback_data="SEARCHRANGE_75__"),
        InlineKeyboardButton("100 Km", callback_data="SEARCHRANGE_100__")
    )
    markup.add(
        InlineKeyboardButton("150 Km", callback_data="SEARCHRANGE_150__"),
        InlineKeyboardButton("250 Km", callback_data="SEARCHRANGE_250__"),
        InlineKeyboardButton("500 Km", callback_data="SEARCHRANGE_500__")
    )
    return markup


# todo
def markup_matching_bids(chatId, bid_id_list, offset, show_more):
    markup = InlineKeyboardMarkup()
    markup.width = 2
    if show_more:
        markup.add(
            InlineKeyboardButton("Показать ещё заявки", callback_data="MYBIDMATCHES_SHOWMORE__")
        )
    markup.add(
        InlineKeyboardButton("Выйти в основное меню", callback_data="MAINMENU__")
    )
    for i in range(len(bid_id_list)):
        markup.add(
            InlineKeyboardButton(f"Запросить обмен с №{offset + i + 1}",
                                 callback_data=f"SENDEXCHANGEREQUEST_{bid_id_list[i]}__")
        )
    return markup


def markup_need_currency(chatId):
    markup = InlineKeyboardMarkup()
    markup.width = 2
    markup.add(
        InlineKeyboardButton("Рубли/RUB", callback_data="GET_RUB__"),
        InlineKeyboardButton("Лиры/TRL", callback_data="GET_TRL__")
    )
    return markup


def markup_receive(chatId):
    markup = InlineKeyboardMarkup()
    markup.width = 2
    markup.add(
        InlineKeyboardButton("На Рус. карту", callback_data="REC_RU__")
    )
    markup.add(
        InlineKeyboardButton("На Тур. карту", callback_data="REC_TR__")
    )
    markup.add(
        InlineKeyboardButton("Наличными", callback_data="REC_NAL__")
    )
    return markup


def markup_how_u_send(chatId):
    markup = InlineKeyboardMarkup()
    markup.width = 2
    markup.add(
        InlineKeyboardButton("Перевод с Рус. карты", callback_data="FROM_RU__")
    )
    markup.add(
        InlineKeyboardButton("Перевод с Тур. карты", callback_data="FROM_TR__")
    )
    markup.add(
        InlineKeyboardButton("Передам Наличными", callback_data="FROM_NAL__")
    )
    return markup


def markup_what_u_got(chatId):
    markup = InlineKeyboardMarkup()
    markup.width = 2
    markup.add(
        InlineKeyboardButton("Рубли/RUB", callback_data="HAS_RUB__"),
        InlineKeyboardButton("Лиры/TRL", callback_data="HAS_TRL__")
    )
    return markup


def markup_will_you_fulfill_request(chatId, bidder_id):
    markup = InlineKeyboardMarkup()
    markup.width = 2
    markup.add(
        InlineKeyboardButton("Готов к обмену", callback_data="REPLYTOREQUEST_YES__" + str(bidder_id)),
        InlineKeyboardButton("Не готов", callback_data="REPLYTOREQUEST_NO__" + str(bidder_id))
    )
    return markup


def markup_check_input(chatId):
    markup = InlineKeyboardMarkup()
    markup.width = 2
    markup.add(
        InlineKeyboardButton("Все верно", callback_data="CHECK_OK__")
    )
    markup.add(
        InlineKeyboardButton("Я неверно ввел", callback_data="CHECK_USERBAD__")
    )
    markup.add(
        InlineKeyboardButton("Бот неверно записал", callback_data="CHECK_BOTBAD__")
    )
    return markup


def markup_offer_terms_initial(chatId):
    markup = InlineKeyboardMarkup()
    markup.width = 2
    markup.add(
        InlineKeyboardButton("Согласен на условия пользователя", callback_data="MAKINGOFFER_HIS__")
    )
    markup.add(
        InlineKeyboardButton("Предложить условия своей заявки", callback_data="MAKINGOFFER_MINE__")
    )
    markup.add(
        InlineKeyboardButton("Предложить третий вариант", callback_data="MAKINGOFFER_OTHER__")
    )
    markup.add(
        InlineKeyboardButton("Отказаться", callback_data="MAKINGOFFER_OTHER__")
    )
    return markup
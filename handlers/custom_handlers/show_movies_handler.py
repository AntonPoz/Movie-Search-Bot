from loader import bot
from telegram_bot_pagination import InlineKeyboardPaginator
from database.custom_models import WatchedMovie
from telebot.types import InlineKeyboardButton

chat_info = {}


class PaginatorData:
    def __init__(self, description: str, watched_movie: WatchedMovie):
        self.description = description
        self.watched_movie = watched_movie


class Paginator:
    def __init__(self, message, data_list):
        self.message = message
        self.data_list = data_list
        chat_info[self.message.chat.id] = self

    @bot.callback_query_handler(
        func=lambda call: call.data.split('#')[0] == 'show_movie'
    )
    async def characters_page_callback(call):
        paginator = chat_info[call.message.chat.id]
        page = int(call.data.split('#')[1]) - 1
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await paginator.show_page(page)
        print(page)

    @bot.callback_query_handler(
        func=lambda call: call.data.split('#')[0] == 'watched'
    )
    async def characters_watched_callback(call):
        paginator = chat_info[call.message.chat.id]
        page = int(call.data.split('#')[1])
        watched_movie = paginator.data_list[page].watched_movie
        watched_movie.is_watched = not watched_movie.is_watched
        await watched_movie.save()
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await paginator.show_page(page)

    async def show(self):
        self.paginator = InlineKeyboardPaginator(
            len(self.data_list),
            current_page=1,
            data_pattern='show_movie#{page}'
        )

        button_label = 'Просмотрен' \
            if self.data_list[0].watched_movie.is_watched \
            else 'Не просмотрен'
        self.paginator.add_before(
            InlineKeyboardButton(
                f'{button_label}', callback_data=f'watched#{0}'
            )
        )

        await bot.send_message(
            self.message.chat.id,
            self.data_list[0].description,
            reply_markup=self.paginator.markup,
            parse_mode='Markdown'
        )

    async def show_page(self, page):
        self.paginator = InlineKeyboardPaginator(
            len(self.data_list),
            current_page=page + 1,
            data_pattern='show_movie#{page}'
        )
        button_label = 'Просмотрен' \
            if self.data_list[page].watched_movie.is_watched \
            else 'Не просмотрен'
        self.paginator.add_before(
            InlineKeyboardButton(
                f'{button_label}', callback_data=f'watched#{page}'
            )
        )

        await bot.send_message(
            self.message.chat.id,
            self.data_list[page].description,
            reply_markup=self.paginator.markup,
            parse_mode='Markdown'
        )

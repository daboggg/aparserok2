import hashlib
import os

from youtube_search import YoutubeSearch

from aiogram import Bot, Dispatcher, types, utils, executor
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle
from dotenv import load_dotenv

TOKEN = ''

load_dotenv('.env')
token = os.getenv('TOKEN_API')
bot = Bot(token=token)
dp = Dispatcher(bot=bot)


def search(text):
    return  YoutubeSearch(text, max_results=1).to_dict()


@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
    text = query.query or 'echo'
    links = search(text)

    articles = [
        InlineQueryResultArticle(
            id = hashlib.md5(f'{link["id"]}'.encode()).hexdigest(),
            title = f'{link["title"]}',
            url = f'https://www.youtube.com/watch?v={link["id"]}',
            thumb_url = f'{link["thumbnails"][0]}',
            input_message_content=types.InputTextMessageContent(
                message_text=f'https://www.youtube.com/watch?v={link["id"]}'
            )
        ) for link in links
    ]
    await query.answer(articles, cache_time=10,is_personal=True)


executor.start_polling(dp, skip_updates=True)
import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.types import Message, ChatType, ContentType, AllowedUpdates
from aiogram.utils.exceptions import RetryAfter, MessageCantBeDeleted

log = logging.getLogger(__name__)
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(ChatTypeFilter((ChatType.SUPERGROUP, ChatType.GROUP)), content_types=ContentType.NEW_CHAT_MEMBERS)
async def delete_new_chat_member_message(msg: Message):
    try:
        await msg.delete()
    except RetryAfter as e:
        log.exception(f'Retry after {e.timeout}')
        await asyncio.sleep(e.timeout)
        await delete_new_chat_member_message(msg)
    except MessageCantBeDeleted:
        log.exception(f'Message {msg.message_id} can\'t be deleted')
    except Exception as e:
        log.exception(e)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
    )

    allowed_updates = AllowedUpdates.MESSAGE
    log.info('Starting bot!')
    await dp.start_polling(allowed_updates=allowed_updates)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log.warning('Bot stopped!')


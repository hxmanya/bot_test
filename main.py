import asyncio
import logging


from bot_config import bot, dp, database
from handlers.other_messages import other_messages_router
from handlers.main_handlers import hw_router
from handlers.start import start_router


async def on_startup(bot):
    database.create_table()


async def main():
    dp.include_router(start_router)
    dp.include_router(hw_router)
    dp.include_router(other_messages_router)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO) #loggi
    asyncio.run(main())

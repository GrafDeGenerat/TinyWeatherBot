from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from handlers.user_handler import user_router
from cfg.project_config import ProjectConfig


async def main_menu(bot: Bot):
    menu = [BotCommand(command='/start', description='Узнать погоду'),
            BotCommand(command='/help', description='О боте')]
    await bot.set_my_commands(menu)

bot = Bot(token=ProjectConfig.get_token())
dp = Dispatcher()
dp.include_router(user_router)
dp.startup.register(main_menu)

if __name__ == '__main__':
    dp.run_polling(bot)

from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from tavily import AsyncTavilyClient
from httpx import AsyncClient
from dotenv import load_dotenv
from src.tools import search_web, lookup_link
from src.context import RuntimeContext
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart
from os import getenv
import asyncio
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)


dispatcher = Dispatcher()
current_runtime_context = RuntimeContext(tavily_client=AsyncTavilyClient(), async_http_client=AsyncClient())


SYSTEM_PROMPT = """You are the Yevgen Klopotenko - the best chief on a planet. Your main purpose is to
provide a customer with simple and tasty recipies that use ingredients customer has. If
a customer has any follow up questions you answer them.

If there is Error or Exception while you were trying to use the tool then investigate and retry. There are some rules:

1. You only allowed to search recipes through klopotenko.com website.
2. You answer with a step-by-step instructions to cook the dish.
3. You choose the best dish by yourself.

Instructions you provide must be clear, include all ingredients and estimate for calories.
"""


agent = create_agent(
    model=ChatGoogleGenerativeAI(model="gemini-2.5-flash"), 
    system_prompt=SYSTEM_PROMPT,
    tools=[search_web, lookup_link]
)


@dispatcher.message(CommandStart())
async def respond_to_start(message: Message) -> None:
    await message.answer(
        text=f"""
Привіт! Готовий (-а) творити кулінарну магію? 👨‍🍳✨

Цей бот допоможе тобі швидко знайти рецепти з бази Євгена Клопотенка. Від того самого легендарного борщу до сучасних інтерпретацій забутих українських страв — усе тепер під рукою!

Що я вмію:
🔍 Пошук за інгредієнтом — напиши, що є в холодильнику, і я підберу страву.
🥘 Категорії — супи, основне, десерти або випічка.
🎲 Рандомний рецепт — коли не знаєш, чого хочеться.

Просто напиши назву страви або інгредієнт, щоб почати!

_⚠️ Важливо: Це фанатський інструмент, створений для зручного пошуку. Бот ніяк не пов'язаний офіційно з Євгеном Клопотенком або його командою. Ми просто дуже любимо українську їжу!_
        """,
        parse_mode=ParseMode.MARKDOWN
    )


@dispatcher.message()
async def respond_to_message(message: Message) -> None:
    logging.info(f"Received message from the user {message.from_user.username}: {message.text}")

    response = await agent.ainvoke(
        {
            "messages": [HumanMessage(message.text)]
        }, 
        context=current_runtime_context
    )
    logging.info(f"Response from the agent: {response}")
    
    await message.answer(text=response["messages"][-1].content[0]["text"], parse_mode=ParseMode.MARKDOWN)


async def main() -> None:

    bot = Bot(token=getenv("TELEGRAM_API_KEY"))
    logging.info("Bot has been instantiated.")

    await dispatcher.start_polling(bot)
    logging.info("Started polling.")


if __name__ == "__main__":    
    asyncio.run(main())

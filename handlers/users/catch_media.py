from loader import dp, bot
from aiogram.types import ContentType, Message


@dp.message_handler()
async def catch_text(message: Message):
    await message.reply("Вы прислали текст")


@dp.message_handler(content_types=ContentType.DOCUMENT)
async def catch_doc(message: Message):
    await message.document.download()
    await message.reply("Документ скачан\n"
                        f"<pre>FILE ID = {message.document.file_id}</pre>",
                        parse_mode="HTML")


@dp.message_handler(content_types=ContentType.AUDIO)
async def catch_audio(message: Message):
    await message.audio.download()
    await message.reply(
        "Аудиозапись скачана\n"
        f"<pre>FILE ID = {message.audio.file_id}</pre>")


@dp.message_handler(content_types=ContentType.VIDEO)
async def catch_video(message: Message):
    await message.video.download()
    await message.reply(
        "Видеозапись скачана\n"
        f"<pre>FILE ID = {message.video.file_id}</pre>")


@dp.message_handler(content_types=ContentType.PHOTO)
async def catch_photo(message: Message):
    await message.photo[-1].download()
    await message.reply(
        "Фотография скачана\n"
        "<pre>FILE ID = {message.photo[-1].file_id}</pre>")


@dp.message_handler(content_types=ContentType.ANY)
async def catch_else(message: Message):
    await message.reply(f"Вы прислали... {message.content_type}")

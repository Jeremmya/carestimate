from aiogram import Bot, Dispatcher, executor, types
import config
import main
import excel_edit
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.utils.markdown import hlink
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from aiogram.types import InputFile
import time
import avtoelon



import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)

#API_TOKEN = Bot(config.TOKEN)


bot = Bot(config.TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# States
class Form(StatesGroup):
	
	starter = State()
	car_model = State()
	car_mileage = State()
	car_transmition = State()
	made_year = State()
	car_fuel_type = State()


	
	
	


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
	"""
	Conversation's entry point
	"""
	# Set state
	await Form.starter.set()
	
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add("Сформировать письмо", "Оценить машину")
	markup.add("Создать отчет", "Быстрая оценка")

	await message.reply("*Привет. Я бот-помощник для составления отчетов, писем и оценки машин. "
		"Знаю все о наших заказчиках и храню в себе все доступные шаблоны.* \n"
		"\n Мои команды:"
		"\n /letter — составить письм"
		"\n /report — составить отчет"
		"\n /estimate — начать оценку машины", reply_markup = markup, parse_mode="Markdown")

@dp.message_handler(commands='estimate')
async def download(message: types.Message):

	await Form.starter.set()

	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add("NEXIA 2", "SPARK")
	markup.add("MALIBU 2", "LACETTI")
	markup.add("COBALT", "LABO")
	markup.add("EQUINOX", "DAMAS")
	markup.add("NEXIA 3", "MALIBU")
	markup.add("CAPTIVA", "MATIZ")
	markup.add("TRACKER", "ORLANDO")

	await Form.next()
	return await message.reply("Выберите Модель." , reply_markup = markup)



@dp.message_handler(lambda message: message.text in ["Сформировать письмо", "Создать отчет"], state=Form.starter)
async def process_estimate_invalid(message: types.Message):
	"""
	In this example gender has to be one of: Male, Female, Other.
	"""
	return await message.reply("Кнопки в режиме разработки.В скором времени вы сможете ими воспользоваться.")


@dp.message_handler(lambda message: message.text in ["Оценить машину", "Быстрая оценка"], state=Form.starter)
async def process_estimate(message: types.Message):
	
	"""
	In this example gender has to be one of: Male, Female, Other.

	"""
	
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
	markup.add("NEXIA 2", "SPARK")
	markup.add("MALIBU 2", "LACETTI")
	markup.add("COBALT", "LABO")
	markup.add("EQUINOX", "DAMAS")
	markup.add("NEXIA 3", "MALIBU")
	markup.add("CAPTIVA", "MATIZ")
	markup.add("TRACKER", "ORLANDO")

	await Form.next()
	return await message.reply("Выберите Модель." , reply_markup = markup)


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Отменено.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.car_model)
async def process_model(message: types.Message, state: FSMContext):
    """
    Process user name
    """
    #print(message.text)
    async with state.proxy() as data:
        data['car_model'] = message.text

    await Form.next()
    markup_remove = types.ReplyKeyboardRemove(selective=False)
    await message.reply("*Отправьте пробег ТС в формате: 77890. Имеется ввиду, просто цифры, без лишних пробелов, точек и запятых.: *" ,parse_mode="Markdown", reply_markup = markup_remove)


# Check age. Age gotta be digit
@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.car_mileage)
async def process_mileage_invalid(message: types.Message):
    """
    If age is invalid
    """
    return await message.reply("*Пробег должен быть номером.\nКакой у вас пробег? (только номера)*",parse_mode="Markdown")


@dp.message_handler(lambda message: message.text.isdigit(), state=Form.car_mileage)
async def process_mileage(message: types.Message, state: FSMContext):
    # Update state and data
    await Form.next()
    await state.update_data(car_mileage=int(message.text))

    # Configure ReplyKeyboardMarkup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Автомат", "Механика")

    await message.reply("Выберите коробку передач", reply_markup=markup)


@dp.message_handler(lambda message: message.text not in ["Автомат", "Механика"], state=Form.car_transmition)
async def process_transmition_invalid(message: types.Message):
    """
    In this example gender has to be one of: Male, Female, Other.
    """
    return await message.reply("Нажмите одну из кнопок!")

@dp.message_handler(lambda message: message.text in ["Автомат", "Механика"], state=Form.car_transmition)
async def process_transmition(message: types.Message,state: FSMContext):
    """
    In this example gender has to be one of: Male, Female, Other.
    """
    async with state.proxy() as data:
        data['car_transmition'] = message.text

    await Form.next()

    return await message.reply("*Отправьте год выпуска машины в формате: 2016.*",parse_mode="Markdown", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.text.isdigit(), state=Form.made_year)
async def process_age(message: types.Message, state: FSMContext):
    # Update state and data
    await Form.next()
    await state.update_data(made_year=int(message.text))

    # Configure ReplyKeyboardMarkup
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add("Бензин", "Газ/Бензин")

    await message.reply("Выберите вид топлива", reply_markup=markup)


@dp.message_handler(state=Form.car_fuel_type)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['car_fuel_type'] = message.text

        # Remove keyboard
        markup = types.ReplyKeyboardRemove()

        # And send message
        await bot.send_message(message.chat.id, 'Идет поиск...',reply_markup=markup)
            #md.text(
            #    md.text('Модель:', md.bold(data['car_model'])),
            #    md.text('Одометр:', md.code(data['car_mileage']), 'км'),
            #    md.text('Коробка:', data['car_transmition']),
            #    md.text('Год выпуска:', md.code(data['made_year'])),
            #    md.text('Вид топлива:', data['car_fuel_type']),
            #    sep='\n',
           # ),
        #    reply_markup=markup,
        #    parse_mode=ParseMode.MARKDOWN,
        #)

    # Finish conversation
    myTuple = avtoelon.web_scraping(data['made_year'], data['car_mileage'], data['car_transmition'], data['car_fuel_type'], data['car_model'])
    print(myTuple)
    if myTuple is not None:
    	first = myTuple[0]
    	second = myTuple[1]
    	third = myTuple[2]
    	link = myTuple[3]
    	#print(first[2][1])

    	await bot.send_message(message.chat.id, f'1️⃣{first[1]}\n'
    		f'Пробег: {first[4]} км \n'
    		f'Цена: {first[2]} у.е.\n'
    		'\n'
            f'ID: {first[0]}'
    		'\n'
            '\n'
    		f'2️⃣{second[1]}\n'
    		f'Пробег: {second[4]} км \n'
    		f'Цена: {second[2]} у.е.\n'
    		'\n'
            f'ID: {second[0]}'
    		'\n'
            '\n'
    		f'3️⃣{third[1]}\n'
    		f'Пробег: {third[4]} км \n'
    		f'Цена: {third[2]} у.е.\n'
    		'\n'
            f'ID: {third[0]}'
    		'\n'
            '\n'
            f'{link}'
            '\n'
            '\n'
            ,parse_mode="HTML")
    	#excel_edit.excel_editor(first[2], second[2], third[2],data['car_model'], data['car_mileage'],data['made_year'],first[4], first[3], second[4],second[3],third[4], third[3])
    	#time.sleep(3)
    	#await message.answer_document(open('/Users/mike13/Downloads/output.xlsx', 'rb'))

    	
    if not myTuple:
    	await bot.send_message(message.chat.id, "По вашему запросу ничего не найдено")

    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
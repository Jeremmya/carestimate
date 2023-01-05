from aiogram import Bot, Dispatcher, executor, types
import config
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

bot = Bot(config.TOKEN)
dp = Dispatcher(bot)

#@dp.message_handler()
#async def echo(message: types.Message):
#	await message.answer(text=message.text)  #otvetit na soobshenie

@dp.message_handler(commands = ['start'])
async def start(message: types.Message):
	markup_begining = types.ReplyKeyboardMarkup(row_width = 2)
	Letter = types.KeyboardButton('Сформировать письмо')
	Estimate = types.KeyboardButton('Оценить машину')
	Report = types.KeyboardButton('Создать отчет')
	Fast_Estimate = types.KeyboardButton('Быстрая оценка')

	markup_begining.add(Letter,Estimate,Report,Fast_Estimate)
	await bot.send_message(message.chat.id, '*Привет. Я бот-помощник для составления отчетов, писем и оценки машин. '
		'Знаю все о наших заказчиках и храню в себе все доступные шаблоны.* \n'
		'\n Мои команды:'
		'\n /letter — составить письмо'
		'\n /report — составить отчет'
		'\n /estimate — начать оценку машины', reply_markup = markup_begining,parse_mode="Markdown")

@dp.message_handler(text_contains = "Оценить машину")
async def estimate(message: types.Message):
	print(message.text)
	markup_reply = types.ReplyKeyboardMarkup(row_width = 2)
	NEXIA_2 = types.KeyboardButton('NEXIA 2')
	SPARK = types.KeyboardButton('SPARK')
	LACETTI = types.KeyboardButton('LACETTI')
	MALIBU_2 = types.KeyboardButton('MALIBU 2')
	COBALT = types.KeyboardButton('COBALT')
	LABO = types.KeyboardButton('LABO')
	EQUINOX = types.KeyboardButton('EQUINOX')
	DAMAS = types.KeyboardButton('DAMAS')
	MALIBU = types.KeyboardButton('MALIBU')
	NEXIA_3 = types.KeyboardButton('NEXIA 3')
	CAPTIVA = types.KeyboardButton('CAPTIVA')
	MATIZ = types.KeyboardButton('MATIZ')
	TRACKER = types.KeyboardButton('TRACKER')
	ORLANDO = types.KeyboardButton('ORLANDO')
	markup_reply.add(NEXIA_2, SPARK, LACETTI, MALIBU_2, COBALT, LABO, EQUINOX, DAMAS, MALIBU, NEXIA_3,
	CAPTIVA, MATIZ, TRACKER, ORLANDO)
	await bot.send_message(message.chat.id, 'Выберите Модель', reply_markup = markup_reply)

@dp.message_handler(text_contains = "Сформировать письмо")
async def estimate(message: types.Message):
	print(message.text)

@dp.message_handler(text_contains = "Создать отчет")
async def estimate(message: types.Message):
	print(message.text)

@dp.message_handler(text_contains = "Быстрая оценка")
async def fast_estimate(message: types.Message):
	print(message.text)
	markup_reply = types.ReplyKeyboardMarkup(row_width = 2)
	NEXIA_2 = types.KeyboardButton('NEXIA 2')
	SPARK = types.KeyboardButton('SPARK')
	LACETTI = types.KeyboardButton('LACETTI')
	MALIBU_2 = types.KeyboardButton('MALIBU 2')
	COBALT = types.KeyboardButton('COBALT')
	LABO = types.KeyboardButton('LABO')
	EQUINOX = types.KeyboardButton('EQUINOX')
	DAMAS = types.KeyboardButton('DAMAS')
	MALIBU = types.KeyboardButton('MALIBU')
	NEXIA_3 = types.KeyboardButton('NEXIA 3')
	CAPTIVA = types.KeyboardButton('CAPTIVA')
	MATIZ = types.KeyboardButton('MATIZ')
	TRACKER = types.KeyboardButton('TRACKER')
	ORLANDO = types.KeyboardButton('ORLANDO')
	markup_reply.add(NEXIA_2, SPARK, LACETTI, MALIBU_2, COBALT, LABO, EQUINOX, DAMAS, MALIBU, NEXIA_3,
	CAPTIVA, MATIZ, TRACKER, ORLANDO)
	await bot.send_message(message.chat.id, 'Выберите Модель', reply_markup = markup_reply)
	if message.text == "NEXIA 2":
		markup_remove = types.ReplyKeyboardRemove(selective=False)
		await bot.send_message(message.chat.id, "*Отправьте пробег ТС в формате: 77890. Имеется ввиду, просто цифры, без лишних пробелов, точек и запятых.: *" ,parse_mode="Markdown", reply_markup = markup_remove)
		print("message.text")
		car_milege = int(message.text)
		if car_milege > 1 :
			print("message.text")
			markup_reply = types.ReplyKeyboardMarkup(resize = True)
		    Benzin = types.KeyboardButton('Бензин')
		    Gaz = types.KeyboardButton('Газ-бензин')
		    markup_reply.add(Benzin, Gaz)
		    print("message.text")
		    await bot.send_message(message.chat.id, '*Выберите тип топлива машины.*', reply_markup = markup_reply, parse_mode="Markdown")
		    if message.text == "Бензин":
		    	markup_reply = types.ReplyKeyboardMarkup(resize = True)
		    	print("message.text")
			    Avtomat = types.KeyboardButton('Автомат')
			    Mexanika = types.KeyboardButton('Механика')
			    markup_reply.add(Benzin, Gaz)
			    await bot.send_message(message.chat.id, '*Выберите тип коробки передач машины.*', reply_markup = markup_reply, parse_mode="Markdown")
		    	pass
	else:
		print("ERROR")

@dp.message_handler()
async def get_milege(message):
    print(message.text) ##
    car_milege = message.text
    await bot.send_message(message.chat.id, "*Отправьте год выпуска машины в формате: 2016.*",parse_mode="Markdown")

@dp.message_handler()
async def get_year(message: types.Message):
    print(message.text)
    car_year = message.text
    markup_reply = types.ReplyKeyboardMarkup(resize = True)
    Benzin = types.KeyboardButton('Бензин')
    Gaz = types.KeyboardButton('Газ-бензин')
    markup_reply.add(Benzin, Gaz)
    await bot.send_message(message.chat.id, '*Выберите тип топлива машины.*', reply_markup = markup_reply, parse_mode="Markdown")

@dp.message_handler(text_contains = "Бензин")
async def fuel_type(message):
    markup_reply = types.ReplyKeyboardMarkup(resize = True)
    Avtomat = types.KeyboardButton('Автомат')
    Mexanika = types.KeyboardButton('Механика')
    markup_reply.add(Benzin, Gaz)
    await bot.send_message(message.chat.id, '*Выберите тип коробки передач машины.*', reply_markup = markup_reply, parse_mode="Markdown")

#@dp.message_handler(func=lambda message: True)
#def get_milege(message):
#	print("on milege")
#	print(message.text)
#	if message.text == '1234':
#		bot.send_message(message.chat.id, '12341234')



if __name__ == '__main__':
	executor.start_polling(dp)
	

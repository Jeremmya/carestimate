import requests
from bs4 import BeautifulSoup
import bot
import statistics



automatic = 546
mechanic = 545
gasoline = 542
metanWithGasoline = 545
image_number = 0


made_year_from = int(2021)
made_year_to = int(2021)
car_made = "chevrolet"
car_model = "malibu"
mileage_from = 12000 
mileage_to = 15000
car_transmition = automatic
car_fuel_type = gasoline
begining_link = f"https://www.olx.uz/"
cars = []
median_calc = []



def kurs_valyut():
	bank_link = "https://bank.uz/currency"
	responces = requests.get(bank_link).text
	bank_soup = BeautifulSoup(responces, 'lxml')
	first_block = bank_soup.find('div', class_ = 'tab-pane fade in show active')
	needed_info = first_block.find('div', class_ = 'tab-content')
	final = needed_info.find('div', class_ = 'bc-inner-blocks-left')
	last = final.find('span', class_ = 'medium-text green-date')
	kurs = last.text
	kursc = kurs.replace('сум', '')
	kursv = kursc.replace(' ', '')
	valyuta = int(kursv)
	print(valyuta)
	return valyuta




def web_scraping(a,b,c,e,f):
	car_full_info = []
	first_car = []
	second_car = []
	third_car = []
	count = int(0)

	made_year_b = a
	mileage_b = b
	car_transmition_b = c
	car_fuel_type_b = e
	car_model_b = f

	#print(made_year_b)
	#print(mileage_b)
	#print(car_transmition_b)
	#print(car_fuel_type_b)
	#print(car_model_b)

	if car_transmition_b == "Автомат":
		car_transmition = 546
	else:
		car_transmition = 545

	if car_fuel_type_b == "Бензин":
		car_fuel_type = 542
	else:
		car_fuel_type = 545


	made_year_to = int(made_year_b)
	made_year_from = int(made_year_b)
	mileage_from = int(mileage_b)
	mileage_to = int(mileage_b) + 30000
	car_model = car_model_b.lower()



	link = f"https://www.olx.uz/d/transport/legkovye-avtomobili/chevrolet/?currency=UZS&search%5Bfilter_float_motor_year:from%5D={made_year_from}&search%5Bfilter_float_motor_year:to%5D={made_year_to}&search%5Bfilter_float_motor_mileage:from%5D={mileage_from}&search%5Bfilter_float_motor_mileage:to%5D={mileage_to}&search%5Bfilter_enum_transmission_type%5D%5B0%5D={car_transmition}&search%5Bfilter_enum_fuel_type%5D%5B0%5D={car_fuel_type}&search%5Bfilter_enum_model%5D%5B0%5D={car_model}"
	responce = requests.get(link).text
	print(mileage_from)
	print(mileage_to)
	#with open("1.html", "w", encoding="utf-8") as file:
		#file.write(responce)x
	soup = BeautifulSoup(responce, 'lxml')
	block = soup.find('div', class_ = 'css-pband8')
	all_info = block.find_all('div', class_ = 'css-1sw7q4x')

	runer = 'a'
	car_count = 0
	runers = int(0)
	

	for info in all_info:
		car_count = car_count + 1
		cares = []
		checker = int(0)
		count = count + 1
		info_link = info.find('a').get('href') #silka kajdogo avto bez nachalo
		download_link = requests.get(f'{begining_link}{info_link}').text # glavnaya ssilka kajdogo avto
		download_soup = BeautifulSoup(download_link, 'lxml') # ssilka dlya raboti

		#название обявления
		for download_name in download_soup.find_all('h1'):
			print(download_name.text)

		# work to get photo link
		download_block = download_soup.find('div', class_ = 'swiper-zoom-container')
		if download_block is None:
			break
		result_link = download_block.find('img').get('src') # image link get
		
		


		#price parsing
		download_block_price = download_soup.find('div', class_ = 'css-dcwlyx')
		car_pri = download_block_price.find('h3').text
		separate_car_link = f"https://www.olx.uz{info_link}"
		car_pric = car_pri.replace('у.е.', '')
		car_price = car_pric.replace(' ', '')
		print(car_price)
		median_calc.append(int(car_price))

		#
		
		download_block_mileage = download_soup.find('ul', class_ = 'css-sfcl1s')
		for car_mileage in download_block_mileage.find_all('p'):
			if 'Пробег:' in car_mileage.text:
				milea = car_mileage.text
				mil_num = milea.replace('Пробег:', '')
				milea = mil_num.replace('км', '')
				mil_num = milea.replace(' ', '')
				cares.append(int(mil_num))
				print(mil_num)
			else:
				print(checker)
				if checker == 0:
					cares.insert(0, car_price)
				elif checker == 1:
					cares.insert(1, separate_car_link)
				elif checker == 2:
					cares.insert(2, download_name.text)
				cares.append(car_mileage.text)
				checker = checker + 1
		cars.insert(runers,cares)
		runers = runers + 1	
	print(cars)	
	swapped = False
	for i in range(count-1):
		for j in range(0, count-i-1):
			if cars[j][7] > cars[j+1][7]:
				swapped = True
				cars[j], cars[j+1] = cars[j+1], cars[j]
		if not swapped:
			break

	
	print(statistics.median(median_calc))
	print("AFTER SORT")
	print(cars)

	print(car_count)


	return cars[0], cars[1], cars[2], link

# download image to desktop
	#image_bytes = requests.get(f'{result_link}').content
	#with open(f'{image_number}.jpg', 'wb') as file:
#		file.write(image_bytes)
#	image_number += 1

	#print(result_link)


if __name__ == '__main__':
	web_scraping()




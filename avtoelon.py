import requests
import lxml
import cchardet
from bs4 import BeautifulSoup
import bot
import statistics
import re


#data['made_year'], data['car_mileage'], data['car_transmition'], data['car_fuel_type'], data['car_model']
def web_scraping(a,b,c,d,e):
	cars = []
	cares = []
	idis = []
	#a = 2020
	#b = 64000
	#c = "Автомат"
	#d = "Бензин"
	#e = "spark"
	e_changed = e.replace(' ', '')
	model = e_changed.lower()
	if d == "Бензин":
		fuel_type = 1
	else:
		fuel_type = 3
	if c == "Автомат":
		transmition = 2
	else:
		transmition = 1
	mile = int(b)
	year = a
	counter = 0
	page_num = 0

	if model == 'labo':
		link_for_labo = f'https://avtoelon.uz/avto/body-pickup/chevrolet/{model}/?year[from]={year}&year[to]={year}&auto-fuel={fuel_type}&auto-car-transm={transmition}'
	else:
		link = f'https://avtoelon.uz/avto/chevrolet/{model}/?year[from]={year}&year[to]={year}&auto-fuel={fuel_type}&auto-car-transm={transmition}'
	
	responce = requests.get(link).text
	soup = BeautifulSoup(responce, 'lxml')
	block = soup.find('div', class_ = 'result-block col-sm-8')
	page_info = block.find('div', class_ = 'col-sm-12 col-md-12 col-lg-12')
	if page_info is None:
		return None
	page_count = page_info.find('ul')
	for li in page_count.find_all('span'):
		page_num = page_num + 1
		#print(page_num)
	#print("here")


	for page in range(1,page_num):
		if model == 'labo':
			link_for_labo = f'https://avtoelon.uz/avto/body-pickup/chevrolet/{model}/?year[from]={year}&year[to]={year}&auto-fuel={fuel_type}&auto-car-transm={transmition}&page={page}'
		else:
			link = f'https://avtoelon.uz/avto/chevrolet/{model}/?year[from]={year}&year[to]={year}&auto-fuel={fuel_type}&auto-car-transm={transmition}&page={page}'
		responce = requests.get(link).text
		soup = BeautifulSoup(responce, 'lxml')
		block = soup.find('div', class_ = 'result-block col-sm-8')
		information = block.find('div', class_ = 'finded').text
		#print(information)
		if block is None:
			return None
		download_names = block.find_all('div', class_ = 'row list-item a-elem')

		for info in download_names:
			

			ids = info.get('data-id')

			name = info.find('a').text

			pri = info.find('span', class_ = 'price').text
			price_num = ''
			for c in pri:
				if c.isdigit():
					price_num = price_num + c

			mileage_without_filtr = info.find('div', class_ = 'desc').text
			milege_filtr = mileage_without_filtr.replace(' ', '')
			milege_fltr = milege_filtr.replace('Торгесть', '')
			milege_flt = milege_fltr.replace('\n', '')
			chunks = milege_flt.split(',')
			yeard = ''
			for f in chunks[0]:
				if f.isdigit():
					yeard = yeard + f
			if ids not in idis:
				idis.append(ids)
				if 'км' in chunks[3]:
					milege_int = ''
					for m in chunks[3]:
						if m.isdigit():
							milege_int = milege_int + m
					milege_int = int(milege_int)
					if milege_int >= (mile):
						counter = counter +1
						cars.insert(counter,[ids,name,price_num,yeard,milege_int])
	swapped = False
	for i in range(counter-1):
		for j in range(0, counter-i-1):
			if cars[j][4] > cars[j+1][4]:
				swapped = True
				cars[j], cars[j+1] = cars[j+1], cars[j]
		if not swapped:
			break
	#print(cares)
	return cars[0], cars[1], cars[2], information.strip()







if __name__ == '__main__':
	web_scraping()
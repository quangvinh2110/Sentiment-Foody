import time
import csv
from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

def crawl_restaurant_list():

	path = "https://www.foody.vn/ha-noi/o-dau"
	driver = webdriver.Chrome()
	driver.get(path)
	driver.implicitly_wait(20)

	infinite_scroll_down(driver)
	load_more_click(driver=driver,
					load_more_css=".btn-load-more > a",
					n=1000,
					get_data="restaurant_name")


def load_more_click(driver, 
					load_more_css: str = ".fd-btn-more", 
					n: int = 100,
					get_data: Optional[str] = None):

	# last_height = driver.execute_script("return document.body.scrollHeight")
	LOADING_TIME = 1
	count = 0
	actions = ActionChains(driver)

	for i in range(n):

		# while True:
		try: 
			element = driver.find_element(By.CSS_SELECTOR, load_more_css)
			# break
		except:
			element = None
			# break

		# new_height = driver.execute_script("return document.body.scrollHeight")

		# start_time = time.time()
		# while new_height == last_height:
		# 	print("wait for 1s")
		# 	time.sleep(LOADING_TIME)
		# 	if time.time()-start_time > 3:
		# 		print("TIME OUT!!!")
		# 		break
		# 	new_height = driver.execute_script("return document.body.scrollHeight")
			
		# print(i)
		if element:
			actions.click(on_element = element)
			actions.perform()

		if get_data == "cmt_and_score":
			count = get_comment_and_score(driver, count)
		elif get_data == "restaurant_name":
			count = get_restaurant_name(driver, count)

		if not element:
			break


def get_restaurant_name(driver, count: int):
	
	restaurant_names = list()

	while True:

		css_restaurant = f".ldc-item:nth-child({count+1}) > .ldc-item-header a"

		try:
			restaurant_name = driver.find_element(By.CSS_SELECTOR, css_restaurant)
			restaurant_name = restaurant_name.get_attribute('ng-href')
		except:
			print(f"Cant find {count+1}th restaurant name!!")
			break

		restaurant_names.append(restaurant_name)
		count = count+1

	with open('name.txt', 'a', encoding='utf-8') as f:
		for item in restaurant_names:
			f.write(f"{item}\n")

	return count


def get_comment_and_score(driver, count: int):

	cmts = list()
	scores = list()

	while True:
		cmt_flag = False
		score_flag = False

		css_cmt = f".review-item:nth-child({count+1}) .rd-des > .ng-binding"
		css_score = f".review-item:nth-child({count+1}) .review-points > .ng-binding"
		try:
			cmt = driver.find_element(By.CSS_SELECTOR, css_cmt)
			cmt = cmt.text
		except:
			print(f"Cant find {count+1}th comment element!!")
			cmt = None
			cmt_flag = True
		try:
			score = driver.find_element(By.CSS_SELECTOR, css_score)
			score = score.text
		except:
			print(f"Cant find {count+1}th score element!!")
			score = None
			score_flag = True

		if cmt_flag and score_flag:
			break

		cmts.append(cmt)
		scores.append(score)
		count = count+1

	data = list(zip(cmts, scores))
	with open('data.csv', 'a', encoding='utf-8') as f:
		writer = csv.writer(f, delimiter=",", skipinitialspace=True)
		for tup in data:
			writer.writerow(tup)

	return count


def infinite_scroll_down(driver):

	# Get scroll height and pause time
	last_height = driver.execute_script("return document.body.scrollHeight")
	SCROLL_PAUSE_TIME = 0.5

	while True:
		# Scroll down to bottom
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		# Wait to load page
		time.sleep(SCROLL_PAUSE_TIME)

		# Calculate new scroll height and compare with last scroll height
		new_height = driver.execute_script("return document.body.scrollHeight")
		
		if new_height == last_height:
			break

		last_height = new_height


def crawl_comment_by_restaurant(dish_url: str):

	# options = webdriver.ChromeOptions()
	# options.add_argument("headless")
	# # Create a driver to perform actions in website as: crawl,event
	# driver = webdriver.Chrome(options=options)
	# options = Options()
	# options.headless = True
	driver = webdriver.Chrome()
	#
	path = "https://www.foody.vn"
	# dish_path = "/ho-chi-minh/mi-goi-xao-bo"
	# Go to the site https:https://www.foody.vn/dish_url
	driver.get(path + dish_url + "/binh-luan")
	driver.implicitly_wait(20)
	# actions = webdriver.ActionChains(driver)

	# Scroll down and get comment and score
	infinite_scroll_down(driver)
	load_more_click(driver=driver)
	get_comment_and_score(driver=driver, count=0)


def crawl_comment():

	driver = webdriver.Chrome()
	path = "https://www.foody.vn/ha-noi/binh-luan"
	driver.get(path)
	driver.implicitly_wait(20)
	actions = webdriver.ActionChains(driver)

	infinite_scroll_down(driver)

	load_more_click(driver=driver)

	get_comment_and_score(driver, 0)





if __name__ == "__main__":

	with open('name.txt', mode='r') as file:
		lines = [line.rstrip() for line in file]
	
	for line in lines:
		if line == "None" or line is None:
			continue
		crawl_comment_by_restaurant(line)

	# crawl_comment()

	# crawl_restaurant_list()



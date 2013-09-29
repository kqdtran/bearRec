import requests
import re
from bs4 import BeautifulSoup

def main():
	department_list = scrape()
	department_scrape(department_list)

def scrape():
	
	
	# Set up pull requests and soup object
	front_html = requests.get("http://general-catalog.berkeley.edu/catalog/gcc_search_menu")
	soup = BeautifulSoup(front_html.content, from_encoding="utf-8")
	
	# variable for info
	text = []

	
	# extract department list and write it in a file
	with open("list.txt", "w") as f:
		#solving the ascii problem
		problem_str = u'This is not all ascii\xf8 man'
		safe_str = problem_str.encode('ascii', 'ignore')
		for sp in soup.find_all('option'):
			text.append(sp.string)
			#print(type(sp.string))
			safe_str = sp.string.encode('ascii','ignore')
			f.write(safe_str +"\n")

	return text


#(TEST) testing Biology deparment 
def department_scrape(d_list):
	# set up post url
	url = "http://general-catalog.berkeley.edu/catalog/gcc_search_sends_request"
	# set up post parameter
	

	for department in d_list:


		payload = {'p_dept_name': department}
		# posting website and constructing soup object
	 	r = requests.post(url, params=payload)
	 	soup = BeautifulSoup(r.content, from_encoding="utf-8")
	 	# variable for scrap object
	 	text = []



		# iterate the table row element
		for sp in soup.find_all("tr"):
		 	text.append(sp.text.strip())




		# formatting text array
		format_text = []
		class_name = []
		i = 0
		title_indicator = False
		after_format_indicator = False
		while i < len(text):

			if ("Course Format" in text[i]) and title_indicator == False:
				i = i - 1
				title_indicator = True
				after_format_indicator = False
			elif "Course Format" in text[i]:
				format_text.append(text[i])
				title_indicator = False
				after_format_indicator = True

			if "Prerequisites" in text[i]:
				format_text.append(text[i])

			if "Description" in text[i]:
				format_text.append(text[i])

			if title_indicator == True:
				class_name.append(text[i])
				format_text.append(text[i])

			i = i + 1


		#### List of spliter
		s1 = "Course Format:"
		s2 = "Prerequisites:"
		s3 = "Credit option"
		s4 = "Description:"

		save_indicator = False

		for element in class_name:

			name = element + ".txt"
			name = name.replace("/", "     ")
			safe_name = name.encode('ascii', 'ignore')
			for info in format_text:

				if element in info:
					save_indicator = True

				if save_indicator == True:
					if s4 in info:
						save_indicator = False

					with open("data/" + safe_name, "w") as f:
						problem_str = u'This is not all ascii\xf8 man'
						safe_str = info.encode('ascii', 'ignore')
						safe_element = element.encode('ascii', 'ignore')
						f.write(safe_element + "\n")
						f.write(safe_str + "\n")





if __name__ == "__main__":
	main()





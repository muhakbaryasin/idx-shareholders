from requests import Request, Session

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
# from redis import Redis
import uuid
import pickle

class Scraper(object):
	def __init__(self, url, id=None):
		self.session = None
		self.setUrl(url)
		self.red = None#Redis()
		self.key = 'scrapper_session'
		
		if id is not None:
			self.setId(id)
			self.loadSession()
		else:
			self.setId(str(uuid.uuid4()))
		
	def setUrl(self, url):
		if url is None:
			return
			
		if type(url) is not str:
			raise Exception("Url must be a string.")

		self.url = url

	def setId(self, id):
		if type(id) is not str:
			raise Exception("Id must be a string.")

		self.id = id
	
	def saveSession():
		pass
		#self.red.hset( self.key, self.id, pickle.dumps(self.session) )
	
	def loadSession():
		if id is None:
			raise Exception('Please specify session id')
		
		#self.session = pickle.loads(self.red.hget(self.key, self.id) )
	

class WebDriver(Scraper):
	def __init__(self, url=None, id=None):
		Scraper.__init__(self, url, id=id)
		options = Options()
		options.set_headless(headless=False)
		
		if id is None:
			self.session = webdriver.Firefox(firefox_options=options, executable_path='geckodriver')
			#self.session = webdriver.Chrome(executable_path='chromedriver.exe')
		
		if url is not None:
			self.goto(url)
			
	
	def selectOptionByValue(self, select_elmt, value):
		for option in select_elmt[0].find_elements_by_tag_name('option'):
			if option.get_attribute('value') == value:
				option.click()
	
	def findElementsById(self, id_name):
		return self.session.find_elements_by_id(id_name)
	
	def findElementByClass(self, class_name):
		return self.session.find_elements_by_class(class_name)
	
	def findElementByTag(self, tag_name):
		return self.session.find_elements_by_tag_name(tag_name)
	
	def sendKeys(self, element, value):
		element[0].send_keys(value)
	
	def clickElement(self, element):
		element[0].click()
	
	def executeScript(self, script):
		self.session.execute_script(script)
	
	def goto(self, url):
		print("get url -> {}".format(url))
		self.session.get(url)
	
	def quit(self):
		self.session.quit()
		

class Rest(Scraper):
	def __init__(self, url, method='GET', id=None, headers=None):
		Scraper.__init__(self, url, id=id)
		self.setMethod(method)
		self.setParams( {} )
		self.session = Session()
		
		self.headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3;, Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
		
		if headers is not None:
			self.updateHeaders(headers)
	
	def setMethod(self, method):
		if type(method) is not str and (method != 'GET' or method != 'POST' or method != 'GET_JSON' or method != 'POST_JSON'):
			raise Exception("Method must be a string GET/POST/GET_JSON/POST_JSON")

		self.method = method

	def updateHeaders(self, headers):
		if type(headers) is not dict:
			raise Exception("Headers must be a dict.")
		
		self.headers.update(headers)
	
	def setParams(self, params):
		if type(params) is not dict:
			raise Exception("Params must be a dict.")
	
		self.params = params
	
	def updateParams(self, params):
		if type(params) is not dict:
			raise Exception("Params must be a dict.")
	
		self.params.update(params)
	
	def getParams(self):
		return self.params
	
	def getHeaders(self):
		return self.headers
	
	def getMethod(self):
		return self.method
	
	def execute(self):
		kwargs = {}
		args = []
		
		if self.getMethod() == "GET" or self.getMethod() == "POST":
			args.append(self.getMethod())
			kwargs['data'] = self.getParams()
		elif self.getMethod() == "GET_JSON":
			args.append("GET")
			kwargs['json'] = self.getParams()
		elif self.getMethod() == "POST_JSON":
			args.append("POST")
			kwargs['json'] = self.getParams()
			
		args.append(self.url)
		kwargs['headers'] = self.headers
		
		req = Request(*args, **kwargs)
		
		response = self.session.head(self.url)
		content_type = response.headers['content-type']
		
		prepared = self.session.prepare_request(req)
		print('Request url -> {}'.format(req.url))
		print('Request headers : {}'.format(req.headers))
		print('Request body : {}'.format(prepared.body))
		res = self.session.send(prepared)
		
		return (content_type, res)

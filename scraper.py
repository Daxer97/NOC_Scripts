from dotenv import load_dotenv
import requests
import random
import misc
from  os import environ
from os.path import exists	
import json
import xmltodict
import regex
from prettyprinter import pprint
from requests_ntlm import HttpNtlmAuth
import ast
import re

# Load all oteh variable fromthe .env file
load_dotenv(".env")

# This class is used to take data form the nmt.
class NetworkManagementTool():
	def __init__(self, subclass):

		# Initialize the subclass network monitoring tool of reference
		# A grubber will be initalized in order to access mre specifc function when needed
		subclas = getattr(globals()["NetworkManagementTool"], subclass)
		if subclas:
			# Grubber for nested class methods (monitoring tool specifc)
			self.specs = subclas()
		else:
			raise ValueError("Not a valid class name")

		# Initialize the Router informations streamed from the NMT
		# This ATTRIBUTES are summarizations of the information taken from a specific subclass webinterface
		if exists(f"{subclass}_Routers.py"):
			self.routers = ast.literal_eval(open(f"{subclass}_Routers.py", 'r').read())
		else:
			self.routers = self.specs.pops(self.specs.devlist)
			# Stream the neatd information form the scainemo web interface
			with open(f"{subclass}_Routers.py", 'w') as out:
				pprint(self.routers, stream=out)

		# Validation data returned by the subclasses
		def validate_data_structure(data):
		    raise ValueError("Some Error")

	class SCAI:
		def __init__(self):
			# Contiene lista link raccordi(JSON)
			with open("linkdata.py", "r") as file:
				dic = file.read()
				self.linkdata = eval(dic)

			# Contiene Allarmi& GeodataAllarm (JSON)
			self.geodataAllarm = self.sso().get(f"https://.it/scainemo/tabAddon.php?addon=spracc&action=getgeodata", stream=True).json()
			
			# Contiene tutti dispositivi Router (XML)
			self.devlist = self.sso().get(f"https://.it/scainemo/tabDevice.php?action=getlist", stream=True).content
			
			# Contiene la lista di tutti i subnet e le relative interfaccie (JSON)
			try:
				self.subnet_link = self.sso().get(f"https://.it/scainemo/tabAddrMgr.php?action=getlist", stream=True).json()
			except:
				self.subnet_link = misc.format_file(self.sso().get(f"https://.it/scainemo/tabAddrMgr.php?action=getlist").text)
			# Trash List
			self.trashlist = self.sso().get("https://.it/scainemo/tabAlarms.php?action=getth").json()['data']

			# POP need to be the short of the router
			self.pop = None

			#------------------------------------------------------------------

			if isinstance(self.geodataAllarm, dict):
				with open('geodataAllarm.py', 'w') as out:
					pprint("Printing")
					pprint(self.geodataAllarm, stream=out)
			else:
				raise ValueError("Not an instance of dict")
			if isinstance(self.subnet_link, dict):
				with open('subnet_link.py', 'w') as out:
					pprint("Printing")
					pprint(self.subnet_link, stream=out, depth=None)
			else:
				raise ValueError("Not an instance of dict")
			if isinstance(xmltodict.parse(self.devlist, process_namespaces=True), dict):
				with open('devlist.py', 'w') as out:
					pprint("Printing")
					pprint(xmltodict.parse(self.devlist, process_namespaces=True), stream=out)
			else:
				raise ValueError("Not an instance of dict")

		#------------------------------------------------------------------


		def sso(self):
			# URL del file PAC
			pac_url = 'http://tnavigation.telecomitalia.local:8080/tpac.pac'

			# Imposta le credenziali del proxy
			username = 'x1073377'
			password = 'Retail.5'
			domain = '\\'
			data = {"username": "x1073377", "password": "Retail.5"}
			headers = requests.utils.default_headers()
			# Update the default headers to provide spoofing of user agent
			headers.update(
		    	{
		    	    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
		    	}
			)

			# Ottieni le impostazioni del proxy dal file PAC
			session = requests.Session()
			session.headers = headers

			# pprint(session.cookies.get_dict())

			# Prova a fare una richiesta per prendere IAM
			session.get('https://.it/scainemo', verify=False)
			session.post("https://.it/oam/server/auth_cred_submit", data=self.sex_cookie(session.cookies, data), verify=False)

			return session

		#------------------------------------------------------------------

		def sex_cookie(self, cok, data):
			for k, v in reversed(cok.items()):
				if str(k).find("OAM_REQ_ID_") != -1:
					data["request_id"] = str(k).split("_")[3]
					data["login"] = "login"
					# print(data)
					break
			return data

		#------------------------------------------------------------------

		# Return
		def rev_byID(self, _id):
			rev = self.sso().get(f'https://.it/scainemo/subtabDevice.php?action=loadcfghist&page=0&devid={_id}', verify=False).json()

			# Return a int defining thr revsion number of the configuration
			return rev['data'][0]['revision'] if (type(rev['data'][0]['revision']) is str) and len(rev['data'][0]['revision']) > 0 else ValueError(f'The revision number is not a number: {type(rev['data'][0]['revision'])}')

		#------------------------------------------------------------------
		
		# Return config of a specific router SHORT

		def router_config(self, short):
			self.pop = short
			_id = self.ID_router
			# Define the credential for the log into the website 
			data = {"username": "x1073377", "password": "Retail.5"}


			d = self.sso().get(f'https://.it/scainemo/subtabDevice.php?action=deviceCfgDownload&id={_id}&rev={self.rev_byID(_id)}', verify=False, stream=True, allow_redirects=False)

			# Sometime the req does not go thorugh so refresh of the session is needed
			if d.status_code != 200:
				print(d.status_code)
				session = requests.Session()
				session.get('https://.it/scainemo', verify=False)
				session.post("https://.it/oam/server/auth_cred_submit", data=self.sex_cookie(session.cookies, data), verify=False)
				session.get(f'https://.it/scainemo/subtabDevice.php?action=deviceCfgDownload&id={_id}&rev={self.rev_byID(_id)}', verify=False, stream=True)
				d = session.post("https://.it/oam/server/auth_cred_submit", data=self.sex_cookie(session.cookies, data), verify=False).text
			elif d.status_code == 200:
				d = d.text
			else:
				ValueError(f'The response for getting condiguration is again 302:\n\n{d.text}\n\n')


			# Return textbundle of a specified router
			return d if type(d) == "<classe 'str'>" else ValueError(f'The outputted configuration is or another data type has been sourced:\n\n{d}')
 

		#------------------------------------------------------------------


		@property
		# Return a list of string containing description and related interfaces of deivice
		def devint(self, x=None):

			if not self.pop:
				raise ValueError("self.pop nit defined please define a POP name")

			self._devint = self.sso().get(f"https://.it/scainemo/subtabDevice.php?action=discovery&devid={self.ID_router}&item=Interfaces&xml=1").content
			# Reeturn the interfaces associated to a POP ID
			return [l["cell"][2] for l in xmltodict.parse(self._devint, process_namespaces=True)['rows']['row'] if l["cell"][2]]

		#------------------------------------------------------------------

		@property
		# Find the ID router of reference from a POP name in short

		def ID_router(self):

			if not self.pop:
				raise ValueError("self.pop not defined please define a POP name")

			# Loop threough the devlist xml response to find the ID router from a given POP Short
			for index,elements in enumerate(xmltodict.parse(self.devlist, process_namespaces=True)['rows']['row']):
				if elements['cell'][10] and elements['cell'][10].upper() ==  self.pop.upper():
					self._ID_router =  elements['cell'][1]
					# pprint(self._ID_router)

			return self._ID_router

		#------------------------------------------------------------------
		
		# Find the loopback of the router
		# self.POP must be a short

		def loop_router(self):
			if not self.pop:
				raise ValueError("self.pop nit defined please define a POP name")

			for item in self.devint:
				if ('Lo0' in item or 'Loopback0'in item or 'lo0' in item or 'lo0.0' in item or 'LoopBack0' in item) and re.search(r"\[(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\]", item):
					self._loop_router = re.search(r"\[(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\]", item).group(1)
					return self._loop_router
			else:
				# Debug the router that does not list loopback
				pprint(f"No loopback Found in:\n{pprint(self.pop)}")

				return None

		#------------------------------------------------------------------

		# Return a list of dict containing "ALIAS":"Description"
		# Where the description is the one associated with the interface where the TIS circuit is configurated
		# If no match has been found we will return handle it with a pp statement of the XML content of the resonse self.sso.get(resurce).contet

		def find_pop(self, tis):
			data = self.sso().get(f"https://.it/scainemo/nemoajax/xmlGetSuggest.php?pos=0&mask={tis}&a_dhx_rSeed=1704668783457").content
			pops = xmltodict.parse(data, process_namespaces=True)['complete']['option']

			pprint(pops)
			self._pop = []

			if isinstance(pops, dict):
				raise ValueError('TIS not found:\n{pops}') # Debug
			else:
				for items in pops[1:]:
					if 'Traffic' in items['#text']:
						self._pop.append({items['#text'].split()[0]: list(items.values())[1].split(" -", 1)[1]})
						# pprint(self._pop) # Debug
						return self._pop

				# Return the list of POP
				return self._pop if self.pop else ValueError("Check logic of te function find_pop() empty list has been returned")

		#------------------------------------------------------------------

		# Find te latitude and longitude of the POP

		def find_geo(self, name):
			a = []
			# For loop through the dict to find the POP and the relative geodataAllarm to append
			for items in self.geodataAllarm['routers']:
				if items['title'] == name:
					a.append(items['lat'])
					a.append(items['lng'])

					return a

			return print(f"Name of Router: {name} not found")

		#------------------------------------------------------------------

		# Find all possible links (written in shorts) for a given pop short
		# The string that is passed as a short will match the list returned by the function filter_strings()
		def find_xconn(self, name):

			# print(name)
			# Cretate an array that will be iterated in order to match possible links
			arr = misc.filter_strings(self.linkdata['rows'])
			arr1 = []

			for index,shorts in enumerate(arr):
				if name in shorts.split('-'):
					if shorts.split('-')[0] == name:
						arr1.append(
							{shorts.split('-')[1]:{
								'NET':[l for l in misc.find_IP_band(self.subnet_link[' rows'], shorts.lower())],
								'BANDWIDTH': misc.find_bw(self.linkdata['rows'], shorts) / 1000000000,
								'LINKS':[l for l in misc.find_links_leg(self.linkdata['rows'], shorts)]
								}
							}
						)

					else:
						arr1.append(
							{shorts.split('-')[0]: {
								'NET_BAND':[l for l in misc.find_IP_band(self.subnet_link[' rows'], shorts.lower())],
								'BANDWIDTH': misc.find_bw(self.linkdata['rows'], shorts) / 1000000000,
								'LINKS':[l for l in misc.find_links_leg(self.linkdata['rows'], shorts)]
								}
							}
						)
			#print(arr1)
			return arr1 if len(arr1) != 0 else None

		#------------------------------------------------------------------

		# Create a dict with all pop info and initialize a diff var that keep track of updates
		# The returning dict will need to be stored in the .env file with the name of the network
		# Local variable need to bed a list dictioanry

		def pops(self, x, local=None):

			pop_dict = []

			print(f'ITERATING SCAI().devlist TO GET ROUTERS DATA\n\n-------------------------------------------------------------------------------\n\n')

			for index,elements in enumerate(xmltodict.parse(x, process_namespaces=True)['rows']['row']):
				if elements['cell'][2].find('Customer') != -1 or elements['cell'][2].find('Peerings') != -1 or elements['cell'][2].find('Raccordi') != -1 or elements['cell'][2].find('scainemo') != -1 or elements['cell'][2].find('Scai') != -1 or elements['cell'][2].find('shad') != -1 or elements['cell'][2].find('TIS') != -1:
					pass
				elif self.find_xconn(elements['cell'][10]) == None:
					pass
				else:
					pop_dict.append({elements['cell'][10]:{
						'id': elements['cell'][1],
						'Loopback': [l if l else elements['cell'][3] for l in [self.loop_router(elements['cell'][10])]][0],
						'alias': elements['cell'][2],
						'Model': elements['cell'][4],
						'iOS_Version': elements['cell'][5],
						'Role': elements['cell'][8],
						'xconn': self.find_xconn(elements['cell'][10]),
						'geodata': self.find_geo(elements['cell'][10])
					}})

					pprint(pop_dict[len(pop_dict) - 1])

			print(f'FILE ITERATED\n\n-------------------------------------------------------------------------------\n\n')

			return pop_dict

		#-------------------------------------------------------------

		def find_links_SMF(self):

			arr = []
			racc = self.linkdata['rows']

			for items in racc:
				for i in items.keys():
					# print(item.keys())
					if i == 'parent':
						#print(items[i])
						arr.append(items[i])

			result = misc.find_links(arr)

			print(result)
			misc.find_dsc(racc, result)

			return

		#-------------------------------------------------------------

		# Find specifci information based POP and informations needed
		def pop_map(self, name, routers):
			# Return the dict with the specification of the router short passed as parameter
			a = next((d for d in routers if d.get(name.upper()) != None), None)

			return a if a != None else f'Router {name.upper()} not in table'

		#-------------------------------------------------------------

		# Fin the correlated allarms from a defined allarm type and a POP invloved

		def find_allarm(self, pop, typ):
			return next((item['alarm_desc'] for items in self.geodataAllarm['routers'] if items['title'] == pop and items['alarms'] and items['alarms'] != 0), None) #list of allarms

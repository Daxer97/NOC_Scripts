import json

def find_links_SMF():

	arr = []

	# Open the file containing all json links in sparkle
	with open('RACCORDI.json', 'r') as file:
		racc = json.load(file)
		racc = racc['rows'] # List of dictionary
		# print(racc)

		for items in racc:
			for i in items.keys():
				# print(item.keys())
				if i == 'parent':
					#print(items[i])
					arr.append(items[i])

		result = find_links(arr)

		print(result)
		find_dsc(racc,result)
	return

#-------------------------------------------------------------------------------------

# Return parent values of LINKS at risk SMF

def find_links(x):
	y = []
	# For loop to check if the value is 0 
	# Than check the x.index(0) +3 == 0
		# recursion with  index value to next occurence of 0

	for index, items in enumerate(x):
	    if items == '0':
	    	# print(index)
	    	#print(len(x) - index)
	    	if ((len(x) - 1) - index) > 3:
	    		# print('enr')
	    		if x[index + 3] == '0':
	    			#print('HERE')
	    			y.append(x[index + 1])
	    			y.append(x[index + 2])
	return y

#-------------------------------------------------------------------------------------

# Find the description of LINKS at risk SMF

def find_dsc(x, lis):
	a = []

	for index, items in enumerate(x):
		for y in lis:
			if items['parent'] == y:
				print(items['name'])
				a.append(items['name'])

	return

#-------------------------------------------------------------------------------------
if __name__ == "__main__":

	find_links_SMF()

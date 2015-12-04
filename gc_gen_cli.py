import requests, random
from time import sleep
from ConfigParser import SafeConfigParser

# suppress urllib3 errors
requests.packages.urllib3.disable_warnings()

# -- read login credentials  --
creds = SafeConfigParser()
creds.read('credentials.ini')

account = creds.get('main', 'account')
key = creds.get('main', 'key') 
pwd = creds.get('main', 'pwd') 
# -- end login creds section --

# -- begin functions section --
def ran_char():
  a_z = list(range(65,91))        # create a list with all values from 65 to 91
  random.shuffle(a_z)             # shuffle the list
  l = random.randint(0, 25)       # pick a random position in the randomized array
  y = a_z[l]                      # select the value
  return(y)

def ran_part(r_len):
	i = 0
	r_p= ''                       # initialise string variable
	while i < r_len:              
		r_p += chr(ran_char())    # fill up the string with random charcters 
		i += 1
	return(r_p)

def seq_part(c_len,r_len,nr):
	s_len = c_len - r_len         # determine length of seq part
	s_p = str(nr).zfill(s_len)    # pad seq part with zeroes
	return(s_p)

def code(cod_len,num):
	r_part = gc_len - (len(str(gc_codes))+1) 					 # determine the length for the random part
	gc_code = ran_part(r_part) + seq_part(cod_len,r_part,num)    # put code together 
	return(gc_code)

def get_input(question):
    numeric = False                         # initialise flag
    while numeric != True:                  # while flag not set, repeat
      try:                                  # try
     	 raw_in = raw_input(question)       # get raw input
     	 numeric = raw_in.isdigit()         # check ig input is numeric
     	 value = int(raw_in)                # change int to string
      except ValueError:                    # catch
         print("That's not a number.")      # warn if failed
    return(value)

def send_to_store(store,payload,apikey,apipwd):
	s = requests.post(store, json=payload,  auth=(apikey,apipwd))
	if s.status_code != 201:
		print s.status_code
	sleep(0.05)
	return()

def code_list(c_len,nr_codes):
	i = 1
	gc_list = []
	while i <= nr_codes:
		g_code = code(c_len,i)
		gc_list.append(g_code)
		print g_code
		i += 1
	return(gc_list)	
# -- end functions section --

# -- main --
# get info from user
gc_codes = get_input("How many gift cards would you like to create: ")
gc_len = get_input("How long should the gift card code be: ")
gc_value = get_input("What is the gift card $ value: ")

# process info
q = 0										# initialise counter
x = code_list(gc_len,gc_codes)				# create list with codes
f = open('gc_code_list.txt','w')			# open file in current directory
while q < gc_codes:							# loop through the list of codes 
	line = str(x[q]) + '\n'					# create string to write to file
	f.write(line)							# write line to file
	gc_note = 'Employee giftcard nr:' + str(q+1)  # create note to add to code
	# create JSON payload
	gc_data = { 							
		       "gift_card": { "note": gc_note,      
	                          "initial_value": gc_value, 
	                          "code": x[q] 
	                        } 
	          }
	print gc_data
	send_to_store(account,gc_data,key,pwd)                    
	q += 1
print 'Codes created.'	
f.close	
# -- end main --


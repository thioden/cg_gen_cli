import requests, random, sys
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
def header():
	print '################################################################################'
	print '#                   GIFTCARD API COMMAND LINE INTERFACE                        #'
	print '################################################################################'
	print '\n'
	return()

def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor


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
	# send POST request to the account
	s = requests.post(store, json=payload,  auth=(apikey,apipwd))
	if s.status_code != 201:				# if POST failed
		print s.status_code					# print error code
	sleep(0.05)								# sleep to prevent filling the bucket
	return()

def code_list(c_len,nr_codes):
	i = 1									# initialise counter
	gc_list = []							# initialise list
	print 'Creating code list'				
	while i <= nr_codes:					# loop through list
		g_code = code(c_len,i)				# create code
		gc_list.append(g_code)				# add code to list
		i += 1								# increment counter
	return(gc_list)				
# -- end functions section --

# -- main --
# get info from user
header()
gc_codes = get_input("How many gift cards would you like to create: ")
gc_len = get_input("How long should the gift card code be: ")
gc_value = get_input("What is the gift card $ value: ")

# process info
q = 0										# initialise counter
x = code_list(gc_len,gc_codes)				# create list with codes
f = open('gc_code_list.txt','w')			# open file in current directory
print 'File opened'
print 'Writing codes...'
spinner = spinning_cursor()
while q < gc_codes:							# loop through the list of codes 
	line = str(x[q]) + '\n'					# create string to write to file
	f.write(line)							# write line to file
	gc_note = 'Employee giftcard nr:' + str(q+1)  # create note to add to code
	# create JSON payload - 
	gc_data = { 							
		       "gift_card": { "note": gc_note,      
	                          "initial_value": gc_value, 
	                          "code": x[q] 
	                        } 
	          }
	send_to_store(account,gc_data,key,pwd)  # POST to account                  
	sys.stdout.write(spinner.next())        # show busy indicator
	sys.stdout.flush()						# show busy indicator
	sleep(0.1)								# show busy indicator
	sys.stdout.write('\b')					# show busy indicator
	q += 1									# increment counter
print 'Codes created'	
f.close	
print 'File closed'
# -- end main --


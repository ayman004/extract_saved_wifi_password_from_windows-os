import subprocess,sys
import pprint
def getssids():
	com = subprocess.Popen(['netsh', 'wlan', 'show', 'profiles', '*', 'key=clear','|', 'findstr', 'SSID'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
	(output, error) = com.communicate()


	clean = []
	final = []

	data = output.decode().split('\n')
	for d in data:
		if 'Number of SSIDs' not in d :
			clean.append(d)

	for i in range(len(clean)- 1):
		final.append(clean[i].split(':')[1])

	return final
def print_ssid():
	ssids = getssids()
	my_ssid =[]
	for ssid in ssids:
		ssid = ssid.strip('\r')
		clean = ssid.strip()[1:len(ssid)-2]
		my_ssid.append(clean)
	print('*'*7,str(len(my_ssid))+' Wifi(s) found','*'*7)
	print('*'*31)
	print(my_ssid)
	
def connected_wifi():
	com = subprocess.Popen(['netsh', 'wlan', 'show', 'interfaces', '|', 'findstr', 'SSID'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
	(output, error) = com.communicate() 
	if  str(output.decode()) == "":
			print("""Sorry, it seems you are currently not connected to a wifi\nPossible Reasons:\n\t1)You have disabled wifi or you are using ethernet.\n\t2)You are running a VM.\n\t3)You are mising wireless drivers.""")
	else:
		ssid = output.decode().split('\n')
		bssid = ssid[0].split(':')[1].strip()
		arg = "Content"
		com1 = subprocess.Popen(['netsh', 'wlan', 'show', 'profile','name=',bssid, 'key=clear', '|', 'findstr', arg ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
		(output1, error1) = com1.communicate()
		passwd = output1.decode().split(':')[1]
		print('*'*25)
		print('*'*25)
		print('Wifi Name:',bssid)
		print('Password:',passwd)
	
	
def getpass():
	final = getssids()
	clean_wifi = []
	for ssid in final:
		ssid = ssid.strip('\r')
		clean = ssid.strip()[1:len(ssid)-2]
		clean_wifi.append(clean)
	print('*'*40)
	print('*'*40)
	

	number = 1
	
	for i in range(len(clean_wifi)):
		wifi_name = str(final[i]).lstrip().rstrip()
	
		print(number, '.', 'Wifi Name\t\t:', wifi_name.strip('"'))
		
		
		arg = "Content"
		com1 = subprocess.Popen(['netsh', 'wlan', 'show', 'profiles','name=',wifi_name.strip('"'), 'key=clear','|', 'findstr', arg], stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
		(output1, error1) = com1.communicate()
		print(str(output1.decode()).replace('Key Content', 'Password'))
		print('  '*5, '*'*3,'  '*5)
		number += 1
		
def get_pass_by_name():
	print('*'*15)
	print('*'*15)
	q = str(input('Enter a wifi name or hit enter to get back to main menu: '))
	final = getssids()
	clean_wifi = []
	for ssid in final:
		ssid = ssid.strip('\r')
		clean = ssid.strip()[1:len(ssid)-2]
		clean_wifi.append(clean)
	
	if q == "":
		print('Going back to main menu')
		main()
	
	else:
		existing_wifi = [wifi.strip() for wifi in clean_wifi]
		if q in str(existing_wifi):
			arg = "Content"
			com1 = subprocess.Popen(['netsh', 'wlan', 'show', 'profile','name=',q, 'key=clear', '|', 'findstr', arg ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
			(output1, error1) = com1.communicate()
			if output1:
				passwd = output1.decode().split(':')[1]
				print('*** Details for',q, '***')
				#print('________________________')
				print('Wifi Name:',q)
				print('Password:',passwd)
			else:
				print('No password found for',q)
		else:
			print('Sorry, that wifi name,is not found in the system')
#Display the options the user has
def options():
	print("""
	CHOICES
	-------
	[1] Get Password of currently connected wifi
	[2] Get Passwords of All Wifi
	[3] Get All saved wifi's names
	[4] Get Password of a given wifi
	[5] Display options
	[99] exit

	""")		
	
#Display the wellcome message as
#well as name of the program		
print()
print("                     _  __ _                 ")
print("                    (_)/ _(_)               ")
print("  ((.))    __      ___| |_ _ _              ")
print(r"    |      \ \ /\ / / |  _| |  SAVED PASSWORD            ")
print(r"   /_\      \ V  V /| | | | |   EXTRACTOR           ")
print(r"  /___\      \_/\_/ |_|_| |_|              ")
print(r" /     \                    by ayman_safi           	   ")
print("                                                             ")
print("                                                             ")
print('\t\t A tool that extracts saved wifi password from the system')
print()
options()
#Main function
def main():
	while True:
		try:
			choice = int(input("Choice: "))
		except ValueError:
			print("That was an integer,try again")
			main()
		
		if choice == 99:
			sys.exit()
		elif choice == 1:
			connected_wifi()	
		elif choice == 2:
			getpass()
		elif choice == 3:
			print_ssid()
		elif choice == 4:
			get_pass_by_name()
		elif choice == 5:
			options()
		else:
			print('Wrong option,try again')
			
		
		
	
if __name__ == '__main__':
	
	main()

import os
import re
from time import sleep


def refresh():
	print(">>> Refreshing connections...")
	os.system(".\\resources\\wlanrefresh.exe")
	print("\tStatus : Done")


def get_saved_profiles():
	resp = os.popen('netsh wlan show profiles').read()
	rx = r'All User Profile     : ([\w]+)'
	return re.findall(rx, resp)


def get_available_profiles():
	rx = r'SSID \d+ : ([\w]+)'
	resp = os.popen('netsh wlan show networks').read()
	return re.findall(rx, resp)


class WiFi:
	def __init__(self):
		self.saved_profiles = get_saved_profiles()
		self.available = get_available_profiles()
		self.preferred_ssid = 'wow_momo'

	def disconnect(self):
		resp = os.popen("netsh wlan disconnect").read()
		if resp:
			if 'completed successfully' in resp:
				return True
			else:
				return False
		else:
			return True

	def check(self):
		if self.preferred_ssid not in self.saved_profiles:
			print(f">>> Profile for {self.preferred_ssid} is not saved in system")
			sleep(1)
			quit()
	
	def wait_till_available(self):
		print(">>> Waiting for WiFi.....")
		while True:
			avail = get_available_profiles()
			if self.preferred_ssid in avail:
				print('\tStatus : Found')
				break
			else:
				refresh()

	def connect(self):
		print('>>> Connecting')
		resp = os.popen(f'netsh wlan connect name={self.preferred_ssid}').read()
		print("\tStatus : " + resp)


def main():
	print("")
	refresh()
	driver = WiFi()
	driver.preferred_ssid = 'wow_momo'
	driver.disconnect()
	driver.check()
	driver.wait_till_available()
	driver.connect()
	sleep(1)


if __name__ == "__main__":
	main()

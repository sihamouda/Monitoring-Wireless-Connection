import re
import subprocess
import time
import platform 
import matplotlib.pyplot as plt 
# import numpy as np

def read_data_from_cmd():
	p = subprocess.Popen("netsh wlan show interfaces", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out = p.stdout.read().decode('unicode_escape').strip()
	# print(out)
	if platform.system() == 'Linux':
		m = re.findall('(wlan[0-9]+).*?Signal level=(-[0-9]+) dBm', out, re.DOTALL)
	elif platform.system() == 'Windows':
		m = re.findall('Nom.*?:.*?([A-z0-9 ]*).*?Signal.*?:.*?([0-9]*)%', out, re.DOTALL)
	else:
		raise Exception('reached else of if statement')

	p.communicate()
	return str(m[0])

puissance=read_data_from_cmd()

def plot_puissance(puissance):
	now=time.time()
	puissance_label=[]
	time_label=[]
	timer=0
	while timer != 10:
		time_label.append(timer)
		puissance_label.append(int(puissance.lstrip('(').rstrip(')').split(',')[1].replace("\'","")))
		end=time.time()
		timer=round(end-now)
	plt.plot(time_label,puissance_label)
	plt.ylabel('Puissance du signal')
	plt.xlabel('Temps en secondes')
	plt.show()

def show_networks():
	networks={}
	p = subprocess.Popen("netsh wlan show networks", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out = p.stdout.read().decode('unicode_escape').strip()
	print(out)
	m = re.findall('SSID.*?:.*?([A-z-0-9 ]*)', out, re.DOTALL)
	print(m)
	for network in m:
		p = subprocess.Popen("netsh wlan connect name="+network.strip() , stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		res = p.stdout.read().decode('unicode_escape').strip()
		if "La demande de connexion a" in res:
			time.sleep(10)
			p = subprocess.Popen("netsh wlan show interfaces", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			out = p.stdout.read().decode('unicode_escape').strip()
			# print(out)
			if platform.system() == 'Linux':
				signal = re.findall('(wlan[0-9]+).*?Signal level=(-[0-9]+) dBm', out, re.DOTALL)
			elif platform.system() == 'Windows':
				signal = re.findall('Nom.*?:.*?([A-z0-9 ]*).*?Signal.*?:.*?([0-9]*)%', out, re.DOTALL)
			else:
				raise Exception('reached else of if statement')
			print(signal)
			networks[network]=int(str(signal[0]).lstrip('(').rstrip(')').split(',')[1].replace("\'", ""))
			# networks[network]=int(str(signal[0]).lstrip('(').rstrip(')').split(',')[1].replace("\'",""))
		else:
			print("Pas de mdp pour"+network)
	print(networks)
	best=max(networks, key=networks.get)
	p = subprocess.Popen("netsh wlan connect name="+best.strip() , stdout=subprocess.PIPE, stderr=subprocess.PIPE)

show_networks()
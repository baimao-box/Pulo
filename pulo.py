#!/bin/python3
import threading
import os
import sys
import argparse
import json
import re
import subprocess
try:
	def add_http_prefix(input_string):
		if "http://" not in input_string:
			input_string = "http://" + input_string
		return input_string

	def remove_http_prefix(input_string):
		if "http://" in input_string:
			input_string = input_string.replace("http://", "")
		if "https://" in input_string:
			input_string = input_string.replace("https://", "")
		return input_string

	def delete_last_line(file_path):
		with open(file_path, 'r+') as file:
			lines = file.readlines()
			if len(lines) > 0:
				lines = lines[:-1]
				file.seek(0)
				file.truncate()
				file.writelines(lines)

	def extract_service_version(scan_output, service_name):
		pattern = r"\d+\/tcp\s+open\s+{}\s+(.*?)\n".format(service_name)
		match = re.search(pattern, scan_output)
		if match:
			return match.group(1)
		return None

	def replace_special_characters_with_space(text):
		pattern = r"[\(\);-]"
		cleaned_text = re.sub(pattern, " ", text)
		return cleaned_text

	def search_exploits(service_name, version):
		command = ["searchsploit", "{} {}".format(service_name, version)]
		result = subprocess.run(command, capture_output=True, text=True)
		return result.stdout

	def nmap_scan(ip_hosts):
		os.system("nmap -sV -sC " + str(ip_hosts) + " > nmap_scan.txt ")

	def ffuf_scan(url):
		os.system("ffuf -w /usr/share/seclists/Discovery/Web-Content/raft-medium-directories-lowercase.txt -t 100 -mc 200,301 -u " + url +"/FUZZ -o fuff_scan.json")

	def nikto_scan(ip_hosts):
		os.system("nikto -h " + ip_hosts + " > nikto_scan.txt")

	def subdomains_scan(new_url):
		os.system("/home/kali/gobuster-linux-386/gobuster vhost -w /usr/share/seclists/Discovery/DNS/bitquark-subdomains-top100000.txt -t 50 -u " + new_url + " -o subdomains_scan.txt")
		
	def nuclei_scan(url):
		os.system("nuclei -u " + url + " -o nuclei_scan.txt")

	def search_vuln(service_name):
		if(service_name == 'http' or service_name == 'https'):
			service_name = ""
			return
		cmd = "searchsploit " + service_name
		os.system(cmd)

	if __name__ == '__main__':
		parser = argparse.ArgumentParser(description="My program description")
		parser.add_argument('-t', '--target', type=str, help='')
		parser.add_argument('-u', '--url', type=str, help='')
		args = parser.parse_args()
		
		if args.target:
			ip_hosts = args.target
			print("\033[1;31;40mTarget ip :\033[0m " + ip_hosts)
		else:
			ip_hosts = args.url
			ip_hosts = remove_http_prefix(ip_hosts)
			print("\033[1;31;40mTarget ip :\033[0m " + ip_hosts)
		
		if args.url:
			url = args.url
			url = add_http_prefix(url)
			print("\033[1;31;40mTarget url :\033[0m " + url)
		else:
			url = ip_hosts
			url = add_http_prefix(url)
			print("\033[1;31;40mTarget url :\033[0m " + url)
			
		
		threads = []

		t = threading.Thread(target=nmap_scan, args=(ip_hosts,))
		threads.append(t)


		t = threading.Thread(target=ffuf_scan, args=(url,))
		threads.append(t)
		
		new_url = remove_http_prefix(url)
		t = threading.Thread(target=subdomains_scan, args=(new_url,))
		threads.append(t)
		
		t = threading.Thread(target=nuclei_scan, args=(url,))
		threads.append(t)
		

		for t in threads:
			t.start()

		for t in threads:
			t.join()
			
		with open('nmap_scan.txt', 'r') as file:
			lines = file.readlines()
		lines = lines[4:-2]
		with open('nmap_scan.txt', 'w') as f:
			f.write(''.join(lines))
		file_path = 'nmap_scan.txt'
		delete_last_line(file_path)
		
		with open('fuff_scan.json', 'r') as f:
			data = json.load(f)
			
		with open('newfile.txt', 'w') as f:
			for result in data['results']:
				url_params = result['input']
				url = result['url']
				if 'FUZZ' in url_params.keys():
					f.write(url_params['FUZZ'] + '\n')
		with open("newfile.txt", "r") as f:
			with open("fuff_scan.txt", "w") as f_out:
				for line in f:
					line = line.strip()
					line_with_http = url + line
					f_out.write(line_with_http + "\n")
					
		os.system("clear")
		
		print("\033[1;31;40mPort scanning:\033[0m")
		with open('nmap_scan.txt', 'r') as f:
			content = f.read()
			print(content)
			
		print("\033[1;31;40mWebsite Directory:\033[0m")
		with open('fuff_scan.txt', 'r') as f:
			content = f.read()
			print(content)
		
		print("\033[1;31;40mWebsite Subdomains:\033[0m")
		with open('subdomains_scan.txt', 'r') as f:
			content = f.read()
			print(content)
			
		print("\033[1;31;40mNuclei scan:\033[0m")
		with open('nuclei_scan.txt', 'r') as f:
			content = f.read()
			print(content)
		
		print("\033[1;31;40mSearchsploit:\033[0m")
		with open("nmap_scan.txt", "r") as file:
			scan_output = file.read()
		
		ssh_version = extract_service_version(scan_output, "ssh")
		if ssh_version:
			print("")
			print("\033[1;33;40mSSH Version:\033[0m", ssh_version)
			cleaned_text = replace_special_characters_with_space(ssh_version)
			os.system("searchsploit " + cleaned_text)


		http_version = extract_service_version(scan_output, "http")
		if http_version:
			print("")
			print("\033[1;33;40mHTTP Version:\033[0m", http_version)
			cleaned_text = replace_special_characters_with_space(http_version)
			os.system("searchsploit " + cleaned_text)
		
		smb_version = extract_service_version(scan_output, "smb")
		if smb_version:
			print("")
			print("\033[1;33;40msmb Version:\033[0m", smb_version)
			os.system("searchsploit " + smb_version)
		
		ftp_version = extract_service_version(scan_output, "ftp")
		if ftp_version:
			print("")
			print("\033[1;33;40mftp Version:\033[0m", ftp_version)
			os.system("searchsploit " + ftp_version)

		telnet_version = extract_service_version(scan_output, "telnet")
		if telnet_version:
			print("")
			print("\033[1;33;40mtelnet Version:\033[0m", telnet_version)
			os.system("searchsploit " + telnet_version)

		smtp_version = extract_service_version(scan_output, "smtp")
		if smtp_version:
			print("")
			print("\033[1;33;40msmtp Version:\033[0m", smtp_version)
			os.system("searchsploit " + smtp_version)

		mysql_version = extract_service_version(scan_output, "mysql")
		if mysql_version:
			print("")
			print("\033[1;33;40mmysql Version:\033[0m", mysql_version)
			os.system("searchsploit " + mysql_version)

		mssql_version = extract_service_version(scan_output, "mssql")
		if mssql_version:
			print("")
			print("\033[1;33;40mmssql Version:\033[0m", mssql_version)
			os.system("searchsploit " + mssql_version)



		print("")
		print("\033[1;31;40mDone\033[0m")
except:
	print("help:")
	print("    pulo -u [url]")
	print("example:")
	print("    pulo -u http://www.exploit.com")

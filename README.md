# Pulo v1.0

This is an automated information collection tool for penetration testing. You only need to enter the domain name or ip to get the template's open port information, web directory, subdomain name, and plug-in vulnerabilities.

This tool can also automatically search for related vulnerabilities in the vulnerability database based on the scanned port service version and output
## Install
```
chmod +x setup.py
python3 setup.py
```
## Run
```
help:
pilo -u [url]
pilo -t [ip]
pilo -t [ip] -u [url]
example:
pilo -u http://www.exploit.com
pilo -t 127.0.0.1
pilo -t 127.0.0.1 -u http://www.exploit.com
```
It will take some time for the tool to run, you need to wait for about 5 minutes

![image](https://github.com/baimao-box/Pulo/assets/52622597/325843a4-fbcc-4917-bc57-31edc3e89a60)

![image](https://github.com/baimao-box/Pulo/assets/52622597/a031ded2-61e6-425c-92b6-7707cab500b8)

![image](https://github.com/baimao-box/Pulo/assets/52622597/b6e39f3e-0dc6-43c9-bbc9-5026827c9f6a)

Only need to enter a domain name, you can get the open port and service version, web directory, sub-domain name, plug-in vulnerability information

It can also automatically search for related vulnerabilities in Kali's exploit-db vulnerability database according to the scanned service version

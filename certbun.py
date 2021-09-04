import json
import requests
import sys
import os

def getSSL(domain): #grab all the records so we know which ones to delete to make room for our record. Also checks to make sure we've got the right domain
	allRecords=json.loads(requests.post(apiConfig["endpoint"] + '/ssl/retrieve/' + domain, data = json.dumps(apiConfig)).text)
	if allRecords["status"]=="ERROR":
		print('Error getting domain. Check to make sure you specified the correct domain, and that API access has been switched on for this domain.');
		sys.exit();
	return(allRecords)

if len(sys.argv)>1: #at least the config and root domain is specified
	apiConfig = json.load(open(sys.argv[1])) #load the config file into a variable
	rootDomain=apiConfig["domain"]
	print("Downloading certs for " + rootDomain + "\n");
	certJSON=getSSL(rootDomain)

	f = open(apiConfig["domainCertLocation"], "w")
	print("Installing " + apiConfig["domainCertLocation"])
	f.write(certJSON["certificatechain"])
	f.close()

	f = open(apiConfig["privateKeyLocation"], "w")
	print("Installing " + apiConfig["privateKeyLocation"])
	f.write(certJSON["privatekey"])
	f.close()

	f = open(apiConfig["publicKeyLocation"], "w")
	print("Installing " + apiConfig["publicKeyLocation"])
	f.write(certJSON["publickey"])
	f.close()

	f = open(apiConfig["intermediateCertLocation"], "w")
	print("Installing " + apiConfig["intermediateCertLocation"])
	f.write(certJSON["intermediatecertificate"])
	f.close()
	
	print("\nExecuting system command:\n" + apiConfig["commandToReloadWebserver"] + "\n")
		
	commandOutput=os.popen(apiConfig["commandToReloadWebserver"]).read()		
	print(commandOutput + "\n")	
	
else:
	print("certbun, a simpler way to keep your web server's SSL certificates current.\n\nError: not enough arguments. Example:\npython certbun.py /path/to/config.json \n\nThe config file contains your Porkbun API keys as well as the \ndomain in question, the location on your file system to copy\nthe keys, and the command to restart/reload the web server.\n")

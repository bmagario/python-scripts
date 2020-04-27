import json
import os
import urllib.request
import uuid
from MyMail import MyMail

# configure parameters and send the email.
# to: "example@exampledomain.com"
def sendEmail(body, to):
	email_data = {
		"from": "myemail@mydomain.com",
		"to": to,
		"subject": "EOP URLs e IPs verification",
		"body": body,
		"server": "myserver.mydomain.com"
	}
	myMail = MyMail(email_data)
	myMail.sendEmail()

# helper to call the webservice and parse the response
def webApiGet(methodName, instanceName, clientRequestId):
	ws = "https://endpoints.office.com"
	requestPath = ws + '/' + methodName + '/' + instanceName + '?clientRequestId=' + clientRequestId
	request = urllib.request.Request(requestPath)
	with urllib.request.urlopen(request) as response:
		return json.loads(response.read().decode())

def checkVersion():
    # path where client ID and latest version number will be stored
    datapath = 'C:\Scripts\Python\Logs\endpoints_clientid_latestversion.txt'
    body = ""

    # fetch client ID and version if data exists; otherwise create new file
    if os.path.exists(datapath):
        with open(datapath, 'r') as fin:
            clientRequestId = fin.readline().strip()
            latestVersion = fin.readline().strip()
    else:
        clientRequestId = str(uuid.uuid4())
        latestVersion = '0000000000'
        with open(datapath, 'w') as fout:
            fout.write(clientRequestId + '\n' + latestVersion)

    # call version method to check the latest version, and pull new data if version number is different
    version = webApiGet('version', 'Worldwide', clientRequestId)
    if version['latest'] > latestVersion:
        # write the new version number to the data file
        with open(datapath, 'w') as fout:
            fout.write(clientRequestId + '\n' + version['latest'])

        body = 'New version of Office 365 worldwide commercial service instance endpoints detected\n\n'
    else:
        body = 'Office 365 worldwide commercial service instance endpoints are up-to-date\n\n'

    # Invoke endpoints method to get the new data
    endpointSets = webApiGet('endpoints', 'Worldwide', clientRequestId)

    # Filter dict to get de id=9
    endpointSet = [x for x in endpointSets if int(x['id']) == 9][0]

    # Transform these into tuples with port and category
    flatUrls = []
    category = endpointSet['category']
    urls = endpointSet['urls'] if 'urls' in endpointSet else []
    tcpPorts = endpointSet['tcpPorts'] if 'tcpPorts' in endpointSet else ''
    udpPorts = endpointSet['udpPorts'] if 'udpPorts' in endpointSet else ''
    flatUrls.extend([(category, url, tcpPorts, udpPorts) for url in urls])

    flatIps = []
    ips = endpointSet['ips'] if 'ips' in endpointSet else []
    category = endpointSet['category']

    # IPv4 strings have dots while IPv6 strings have colons
    ip4s = [ip for ip in ips if '.' in ip]
    tcpPorts = endpointSet['tcpPorts'] if 'tcpPorts' in endpointSet else ''
    udpPorts = endpointSet['udpPorts'] if 'udpPorts' in endpointSet else ''
    flatIps.extend([(category, ip, tcpPorts, udpPorts) for ip in ip4s])	
    
    return body, flatIps, flatUrls


# Generates the body message and send with the verification of EOP.
body, flatIps, flatUrls = checkVersion()
body += 'IPv4 Firewall IP Address Ranges\n'
body += ','.join(sorted(set([ip for (category, ip, tcpPorts, udpPorts) in flatIps])))
body += '\nURLs for Proxy Server\n'
body += ','.join(sorted(set([url for (category, url, tcpPorts, udpPorts) in flatUrls])))

sendEmail(body)	
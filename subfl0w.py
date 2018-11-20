import requests, sys
from random import randint
from colorama import Fore, Back, Style


def logo():
	print(Fore.GREEN+"""
            ___.    _____.__  _______          
  ________ _\\_ |___/ ____\\  | \\   _  \\__  _  __
 /  ___/  |  \\ __ \\   __\\|  | /  /_\\  \\ \\/ \\/ /
 \\___ \\|  |  / \\_\\ \\  |  |  |_\\  \\_/   \\     / 
/____  >____/|___  /__|  |____/\\_____  /\\/\\_/  
     \\/          \\/                  \\/        
   # Coded By Mohamed Sayed - @flex0geek	\n"""+Style.RESET_ALL)

try:
	file = open(sys.argv[1], 'r+')
	file2 = open(sys.argv[1], 'r+')
	numOfSubdomains = len(file2.readlines())
except IndexError:
	logo()
	print("[+] python "+sys.argv[0]+" <subdomains-list>\n")
	exit()
except IOError:
	logo()
	print("[+] File "+sys.argv[1]+" Not Found.")
	exit()

error = {
"AWS/S3":"The specified bucket does not exist",
"Bitbucket":"Repository not found",
"Cargo or Collective":"404 Not Found",
"Cloudfront":"Bad Request: ERROR: The request could not be satisfied",
"Desk":"Please try again or try Desk.com free for 14 days.",
"Fastly":"Fastly error: unknown domain:",
"Feedpress":"The feed has not been found.",
"Ghost":"The thing you were looking for is no longer here, or never was",
"Github":"There isn't a Github Pages site here.",
"Help Juice":"We could not find what you're looking for.",
"Help Scout":"No settings were found for this company:",
"Heroku":"No such app",
"JetBrains":"is not a registered InCloud YouTrack",
"Mashery":"Unrecognized domain",
"Readme.io":"Project doesnt exist... yet!",
"Shopify":"Sorry, this shop is currently unavailable.",
"Statuspage":"You are being redirected",
"Surge.sh":"project not found",
"Tumblr":"Whatever you were looking for doesn't currently exist at this address",
"Tilda":"Please renew your subscription",
"Unbounce":"The requested URL was not found on this server.",
"UserVoice":"This UserVoice subdomain is currently available!",
"Wordpress":"Do you want to register *.wordpress.com?",
"Zendesk":"Help Center Closed",
}

USER_AGENTS = [
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Crazy Browser 1.0.5)",
"curl/7.7.2 (powerpc-apple-darwin6.0) libcurl 7.7.2 (OpenSSL 0.9.6b)",
"Mozilla/5.0 (X11; U; Linux amd64; en-US; rv:5.0) Gecko/20110619 Firefox/5.0",
"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b8pre) Gecko/20101213 Firefox/4.0b8pre",
"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0) chromeframe/10.0.648.205",
"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727)",
"Opera/9.80 (Windows NT 6.1; U; sv) Presto/2.7.62 Version/11.01",
"Opera/9.80 (Windows NT 6.1; U; pl) Presto/2.7.62 Version/11.00",
"Opera/9.80 (X11; Linux i686; U; pl) Presto/2.6.30 Version/10.61",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.861.0 Safari/535.2",
"Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.872.0 Safari/535.2",
"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.812.0 Safari/535.1",
"Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
]


def gotVulnLink(vulnerableLinks, key):
	print("\n\n-------------------------------\n[+] Count of Vulnerable Subdomains: "+ str(len(vulnerableLinks)))
	print("[+] Vulnerable Links: ")
	for links in vulnerableLinks:
		print("==> "+ links)

def main():
	logo()
	print("[+] Number of Subdomains is: "+str(numOfSubdomains)+"\n-------------------------------" + Style.RESET_ALL)
	num = 1
	vulnerableLinks = []
	vulnerableKey = ""
	try:
		for domain in file:
			url = "http://" + domain.strip()
			headers = {"User-Agent" : USER_AGENTS[randint(0, len(USER_AGENTS)-1)]}

			try:
				req = requests.get(url, headers=headers)
			except requests.exceptions.ConnectionError:
				pass
			except requests.exceptions.InvalidSchema:
				pass
			except requests.exceptions.InvalidURL:
				pass
			except requests.exceptions.TooManyRedirects:
				pass
				
			sys.stdout.write(Fore.CYAN + "\n["+str(num)+":"+str(numOfSubdomains)+"][+] Testing [ " + domain.strip() + " ] "+Style.RESET_ALL)
			num = num + 1
			for key in error:
				try:
					if error[key] in req.text:
						sys.stdout.write(Fore.RED+"==> This Subdomain maybe Vulnerable on [ "+key+" ]"+Style.RESET_ALL)
						vulnerableKey = key
						if key not in vulnerableLinks:
							vulnerableLinks.append(url+" on [ "+key+" ]")
				except UnboundLocalError:
					pass

		if len(vulnerableLinks) != 0 and len(vulnerableKey) != 0:
			gotVulnLink(vulnerableLinks, vulnerableKey)

	except KeyboardInterrupt:
		if len(vulnerableLinks) != 0 and len(vulnerableKey) != 0:
			gotVulnLink(vulnerableLinks, vulnerableKey)
		else:
			print("\n\n[-] Script closed ....")


main()

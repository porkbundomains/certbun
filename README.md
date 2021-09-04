# certbun

Porkbun's minimalist Certbot alternative leaves the certificate generation to Porkbun and simply downloads certs to the location of your choosing, then reloads your web server with the command of your choosing.

## Before you install
We recommend [manually downloading the certificate bundle](https://kb.porkbun.com/article/71-how-your-free-ssl-certificate-works) and getting it working with your web server first, before trying to automate the process via certbun. Once your web server is reliably serving HTTPS traffic with no issue, you can automate the renewal process with certbun.

## Installation 

 1. Install Python if it's not already installed. This client is Python 2-compatible so it should run out of the box on MacOS and many Linux distributions. If you're running Windows, you should download the most recent production Python version.
 2. Download and uncompress certbun to the folder of your choice
 3. Install the *requests* library:
 	`pip install requests`
 4. Rename config.json.example to config.json and paste in your generated API and Secret keys. Save the config file. If you haven't yet generated the keys, check out our [Getting Started Guide.](https://kb.porkbun.com/article/190-getting-started-with-the-porkbun-dns-api) 
 5. Configure the config file's **domain**
field with the domain you wish to pull certs from.
6. Configure the config file's  **domainCertLocation**, **privateKeyLocation**, **intermediateCertLocation**, and **publicKeyLocation** fields with where you want the retrieved certificates to be saved. If your web server doesn't need the intermediate cert and public key, you can specify /dev/null as the filename.
7. Configure the config file's **commandToReloadWebserver** field with the command you typically execute to get your web server to load the new certificate bundle. I usually use `/sbin/service nginx reload` on Amazon Linux VPS instances I administer, but the command will vary depending on your web server and operating system.


## Running the client

    python certbun.py /path/to/config.json 

### Add it to cron
Since this client works in a fairly non-sophisticated way, you probably just want to download certs every week or so and restart your web server. 

Edit your crontab with:

		crontab -e

If you've never done this before, you may want to read a guide on how to do it. 

Assuming you wanted certbun to run once per week, you'd do something like:

	23 1 * * 1 python /path/to/certbun.py /path/to/config.json | logger

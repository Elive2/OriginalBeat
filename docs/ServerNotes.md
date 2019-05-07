```
"""
File: ServerNotes.md

Description: This file documents and instructions for theoriginalbeat.com prod server

Author: Eli Yale
"""
```

# Github:
The repo can be found at https://github.com/Elive2/OriginalBeat.git

# Description
We use digital ocean droplet for hosting

# To deploy a new release

1. start ssh session
```
ssh root@138.197.199.250
```

2. swithc to eyale user
```
su - eyale
```

3. activate the virtual environment
```
source venv/bin/activate
```

4. cd into the OriginalBeat Repository
```
cd OriginalBeat
```

5. Pull the latest changes
```
git pull origin master
```

6. Install any new python modules
```
pip3 install -r requirements.txt
```

Note: this step is rarely necessary

7. change to the web directory
```
cd web
```

8. migrate the databases
```
python3 manage.py migrate
```

8. Build the frontend for production if you haven't already
```
cd OriginalBeat/frontend && npm run prod
```

9. Restart suprvisor
```
sudo supervisorctl restart OriginalBeat
```

10. Done! http://theoriginalbeat.com


# Notes for when things go wrong

* To restart nginx you may use:
```
sudo service nginx restart
```

* To test all nginx files for syntax erros use
```
sudo nginx -t
```

* All log files are located in
```
/home/eyale/venv/logs
```

* The nginx config file is located at
```
/etc/nginx/sites-available/OriginalBeat
```

* The overall nginx config file is ad:
```
/etc/nginx/nginx.conf 
```

* To see nginx users and process
```
ps -eo "%U %G %a" | grep nginx
```
* The supervisor config is located at:
```
/etc/supervisor/conf.d/OriginalBeat.conf
```
This config is read when you restart supervisor with step 9

* The gunicorn start script is located at:
```
/home/eyale/venv/bin/gunicorn_start
```
This script is invoked by supervisor automatically

* The certbot ssl certificate is located at:
```
/etc/letsencrypt/live/theoriginalbeat.com/fullchain.pem
```

* The certbot keyfile is located at:
```
/etc/letsencrypt/live/theoriginalbeat.com/privkey.pem
```

*  Your cert will expire on 2019-07-30. To obtain a new or tweaked
   version of this certificate in the future, simply run certbot again
   with the "certonly" option. To non-interactively renew *all* of
   your certificates, run "certbot renew"

* certbot account credentials are at
```
/etc/letsencrypt
```

* useful tutorials:
	* Full Deploy: https://simpleisbetterthancomplex.com/tutorial/2016/10/14/how-to-deploy-to-digital-ocean.html
	* Certbot: https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-18-04
	* UFW: https://www.digitalocean.com/community/tutorials/how-to-set-up-a-firewall-with-ufw-on-ubuntu-18-04
	* UFW commands: https://www.digitalocean.com/community/tutorials/ufw-essentials-common-firewall-rules-and-commands

Problems:

error logs seems to be writing
Midi.js.map error seems to be gone
now there is a handshake error with ssl






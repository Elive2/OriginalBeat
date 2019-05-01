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

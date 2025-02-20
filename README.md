# Django Gunicorn
This repository and README file describe basic python and django setup and deploy from local to cloud using Ubuntu 20.04 LTS, Nginx Web Server, Apache Web Server, Sqlite3 Database and Let's Encrypt SSL.

**Usage Note:** This documentation is for both local and remote machine (Local & Cloud flagged). If the local machine is already configured then just setup the cloud according to the below guidelines.

## Python, Pipenv and Virtual Environment Intro
In this repo described the fully optimized way to install Python using **pyenv** so that we can install and manage different versions of Python in the both local and remote machine. Then described the optimized way to install python virtual environment for isolating individual python application and managing package dependencies using pipenv.

**Important:** Using python virtual environment is very useful for developing any kind of python applications (ex: this django application). It is because we can use different version and dependencies for each appliccation running in the same machine. Moreover, as the virtual environment is installed right inside the project folder so that the envrionment for the application remains same for local and remote machine when it is subject to deploy from local to remote server. So that, the dependencies never conflict.

## Django, Gunicorn & Nginx Intro
**Django** is a full stack web framework written in python for developing web applications and web API.

**Gunicorn** is a python application server that helps to run python application (in this case django application) also can be run flask application as well.

**Nginx** is a high end web application server for serving static and dynamic content. In this repo nginx is used with gunicorn for running our django aplication.

## Ubuntu 24.04 Setup (Local & Cloud)
We will not use root user alwyas. That's why we will create a new user with the sudo privilege.

1. On the local machine just create the user.
2. On remote machine first connect the machine using ssh.
3. Use a non-root sudo user for all the below operations.
**Hints:** To connect via SSH, add your local machine's public key (~/.ssh/id_rsa.pub) to the cloud SSH portion and then access the remote via $ ssh root@your_server_ip or use a .pem private key file for corresponding added public key on the machine (ex: EC2) by $ ssh -i 'key.pem' user@server-ip.

## Creating user account (Local & Remote)
1. `$ sudo adduser lina` Then enter password and info to create user.
2. `$ usermod -aG sudo lina` to add lina to sudo
3. `$ sudo ufw app list` to see all the firewall list
4. `$ sudo ufw allow OpenSSH`
5. `$ sudo ufw allow 22` to allow port 22
6. and then `$ sudo ufw enable` to enable the firewall
7. `$ sudo ufw status` to check status.
8. `$ su - lina` switch to lina from root or any other user.

## Installing pyenv (Local & Remote)
Pyenv is a python package manager that can be used to manage multiple versions of python on a single OS. Let's install pyenv latest version.

1. `$ sudo apt update -y` to update the system.
2. `$ sudo apt install -y build-essential` install the build dependencies.
4. `$ sudo apt install zlib1g-dev libssl-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python3-openssl python3-dev libpq-dev gcc`
5. `$ curl https://pyenv.run | bash` to clone the latest version of pyenv for managigng pyenv (Python Virsion control package)
6. Now need to open the `.bashrc` file by typeing `$ nano ~/.bashrc`. In this file go to the bottom of this file and add the following three lines.
    ```
    export PATH="$HOME/.pyenv/bin:$PATH"
    eval "$(pyenv init --path)"
    eval "$(pyenv virtualenv-init -)"
    ```
    Then the file by `Ctrl+X the Y then Enter`
7. `$ exec "$SHELL"` Then run this command to take effect in CMD.
8. `$ pyenv --version`. Now pyenv is installed successfully.
8. `$ pyenv update` to update the pyenv anytime.

**Learn more about pyenv:** https://realpython.com/intro-to-pyenv/

##  Installing Python (Local & Remote)
**Note:** The python version to be installed depends on the version that require the application. We can install multiple version of python and switch back to specific verion for our specific python version.

0. `$ pyenv install --list` to see all the available python version.
1. `$ pyenv install x.x.x` (3.6.9 in this project) to install the needed version. We can install multiple versions. We can activate specific version when we need to create a virtual environment for a specific application.
2. `$ pyenv versions` to see installed/available version to activate.
3. `$ pyenv global x.x.x` to activate a specific python version globally.
4. `$ pyenv global system` switch back to system version.

**Note:** In this deployment we will use python 3.6.9


## Virtual Environment

### Using Virtualenv
NB: If you don't setup the project folder yet, then come back to here to create and activate the virtualenv after project folder created.

1. To install virtualenv `$ pip install virtualenv`
2. Open the Project directory and run `$ virtualenv .venv` (Where the .venv is the virtualenv location inside the current folder, But you can name it as you want)
3. To activate the virtualenv run `$ source .venv/bin/activate` (The current directory must be in the project directory where .venv folder exisits)
4. To install dependencies from requirements.txt (if available) Run: `$ pip install -r requirements.txt`


### Using Pipenv (Python package manager) - (Local & Remote):
Pipenv is a python package manager intend to replace the pip tool. It is an integrated tool to work with virtual environment as well. Let's install Pipenv and then see its function:

1. Before installing Pipenv make sure python and pip is already installed (`$ python -V, python3 -V` and `$ pip --version, pip3 --version`).
2. If you are using multiple versions of python using pyenv then switch to the version of python that you want to work with Pipenv first (`$ pyenv global x.x.x`).
3. `$ pip install --user pipenv` to install pipenv.
4. `$ pipenv --version` to check the version.
5. If pipenv command does not work then, `$ pip uninstall pipenv` and then run `$ pip install pipenv` now it should work.
6. `$ pip install --user --upgrade pipenv` to upgrade Pipenv anytime.

Learn more about Pipenv: https://github.com/mohuls/pipenv

### Creating Virtual Environments using Pipenv (Local & Remote)

**Important:** Before creating any virtual environment, switch to the desired python version using `$ pyenv global x.x.x`.

Now as the Pipenv package is installed, now go to the project directory where your Django project resides. And the follow the below commands:

1. `$ pipenv install` to install virtual environment for the project directory under current user account and Generate Pipfile and Pipfile.lock that is actually the dependency file.
2. `$ pipenv shell` to activate the virtual environment for the project dir. Now the project, python version and python packages are isolated. Now it is time to develop.
3. `$ pipenv install <pkg-name==x.x.x>` to install a package specific version or `$ pipenv install <pkg-name>` to install latest version. It will install the specified packages and will add to Pipfile for keep tracking the dependencies for the project including Python version.

NB: Use either pipenv or virtualenv (One of anyone)

# Deplyment Local to Remote
**Developed locally:** https://github.com/mohuls/django-gunicorn

**Note:** Make sure the app that was developed locally used python version is same as the virtual env.

### Develop Django Application (Local)
Now develop the django application locally. Make sure the version of virtual environment of development environment is same as the remote environment we just created.

### Pushing to GitHub (Local)

1. Upload the source file to a GitHub repo.
2. If the application uses databases rather than sqlite3. Then backup the database and put in source file (better keep that db file in db folder).
3. `$ git init` then `$ git add .` the `$ git commit -m 'test deploy'`
4. `$ git remote add origin git@github.com:mohuls/django-gunicorn.git` the GitHub repo we just created on GitHub.
5. `$ git push -u origin master` to push the full project to GitHub repo.

### Deploying to Live Server (Remote)
0. If the github repo is Private then the server must be authenticated with SSH Key. To connect with the SSH key of the server with GitHub, Follow the below insturtions:
    1. Generate a SSH key suing `$ ssh-keygen` and hit enter.
    2. Show the SSH key using `$ cat ~/.ssh/id_rsa.pub`, It will reveal the SSH public key of the server.
    3. Copy the SSH key and go to the GitHub -> Setings -> SSH & GPG Keys -> Add New Keys -> Give the Server Name, and Paste the SSH key -> Save

1. Clone the github repo `$ git clone https://github.com/mohuls/django-gunicorn` in user home directory.

If you use virtualenv instead of pipenv then Go to the the virtualenv installation above.

Or continue here...
1. `$ cd django-gunicorn` and then `$ pipenv install` to install all the dependencies from Pipfile and Pipfile.lock.
2. `$ pipenv shell` to activate the virtual environment.
3. `$ nano stocks/settings.py` and add the server IP or domain in the allowed hosts list. The line will looks like `ALLOWED_HOSTS = ['192.46.213.168', 'example.com']`. Now go to bottom of the file and add `STATIC_ROOT = os.path.join(BASE_DIR, 'static/')` for static file location. import the os modue at the top if it is not imported already.
4. `$ python manage.py makemigrations` and `$ python manage.py migrate` to migrate the database.
5. `$ python manage.py collectstatic` to compile static file in the static dir.
6. `$ sudo ufw allow 8000` to allow the development port.
7. `$ python manage.py runserver 0.0.0.0:8000` to run the development server.
8. Now Browse the server IP with port 8000 (http://server-ip:8000)to see if the app is running. (It should be running actually).


# Starting project on Remote Server (Remote)
1. In VS Code, Install the SSH Remote Explorer Package
2. Then access the VPS using IP, username and password: (example: ssh username@id-address)
3. Giving above command will ask for password, Enter the server password it will open the folder now create a folder in the server from terminal using `mkdir` command
4. Then open the folder by clicking the open folder from file menu.
5. Once the folder is opened then start creating project from the terminal or manage files form file explorer.



## Installing PostgreSQL (if needed)
### Installing PostgreSQL 17 on Ubuntu 24.04

### Step 1: Add PostgreSQL Repository

PostgreSQL maintains an official repository. Add it to your system:

```bash
sudo apt install -y wget curl ca-certificates
wget -qO - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo tee /etc/apt/trusted.gpg.d/postgresql.asc
echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list
```

### Step 2: Install PostgreSQL 17

Update the package list and install PostgreSQL 17:

```bash
sudo apt update
sudo apt install -y postgresql-17
```

### Step 3: Start and Enable PostgreSQL Service

Ensure PostgreSQL is running and starts on boot:

```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

Check the status:

```bash
sudo systemctl status postgresql
```

### Step 4: Verify PostgreSQL Installation

Check the installed version:

```bash
psql --version
```

Switch to the PostgreSQL user and open the PostgreSQL prompt:

```bash
sudo -i -u postgres
psql
```

Exit the PostgreSQL shell:

```sql
\q
```

### Step 6: Set a Password for PostgreSQL User

Run:

```bash
sudo -u postgres psql
```

Inside the prompt, set a password:

```sql
ALTER USER postgres WITH PASSWORD 'your_secure_password';
\q
```

### Create Database
```bash
CREATE DATABASE database_name;
```

### Step 7: Firewall Configuration (Optional)

If you have UFW enabled, allow PostgreSQL:

```bash
sudo ufw allow 5432/tcp
```


# Nginx Web Server (Remote)
### Run using gunicorn server (Remote)

1. cd to project dir then make sure the virtual environment is active (`$ pipenv shell` if you use pipenv) or (`$ source .venv/bin/activate` if you use virtualenv)
2. `$ pipenv install gunicorn or pip install gunicorn` to install gunicorn application server.
3. `$ gunicorn --bind 0.0.0.0:8000 project_name.wsgi` to start the application using gunicorn server.


### Configuring Gunicorn Startup service (Remote)

1. Cd to project dir.
2. `$ exit` to deactivate the virtual environment.
3. `$ sudo nano /etc/systemd/system/django-gunicorn.service` here **django-gunicorn** is the gunicorn service name. Change according to your choice. Conventionally use the name of the app. Paste the following:

```conf
[Unit]
Description=gunicorn service for serving a django app
After=network.target

[Service]
User=lina
Group=www-data
WorkingDirectory=/home/lina/django-gunicorn
ExecStart=/home/lina/.local/share/virtualenvs/django-gunicorn-3Op5-KvH/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/lina/django-gunicorn/django-gunicorn.sock project_name.wsgi:application

[Install]
WantedBy=multi-user.target
```

**Note:** Here define the current username, path of virtual env bin and gunicorn service path and here `django-gunicorn` is the app name. `stocks` is the project name.

5. `$ sudo systemctl start django-gunicorn` to start the gunicorn server.
6. `$ sudo systemctl enable django-gunicorn` to enable the gunicorn server on system startup.
7. `$ sudo systemctl status django-gunicorn` to check the status.
8. `$ sudo systemctl stop django-gunicorn` to stop the service.

### Configuring Nginx (Remote)
1. `$ sudo apt install nginx` to install nginx server.
2. `$ sudo nano /etc/nginx/sites-available/django-gunicorn` create a nginx server configaration.
```conf
server {
    listen 80;
    server_name server_domain_or_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/lina/django-gunicorn;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/lina/django-gunicorn/django-gunicorn.sock;
    }
}
``` 
3. `$ sudo ln -s /etc/nginx/sites-available/django-gunicorn /etc/nginx/sites-enabled` to enable the conf file.
4. `$ sudo unlink /etc/nginx/sites-enabled/default` to disable the default site.

5. `$ sudo nginx -t` to check the configaration file.
6. `$ sudo systemctl restart nginx` to restart the server.
7. `$ sudo ufw delete allow 8000` to delete the development port.
8. `$ sudo ufw allow 'Nginx Full'` to allow nginx traffic.
9. Now browse the server IP again. Now it should serve the application using Nginx web server by piping to gunicorn server.

### Configuring Domain (Remote)

0. Edit the `$ nano stocks/settings.py` file and add the domain name in the `ALLOWED_HOSTS` list.
1. `$ sudo nano /etc/nginx/sites-available/django-gunicorn` edit the server block file. Replace the domain name you want to configure with the server IP.
2. Make sure you have added the IP address in the domain's DNS.
3. `$ sudo systemctl restart nginx` to restart the server.
4. Wait for propagrating the domain wordwide (can take upto 48 hours)
5. Now the app sould be accessed by the domain name.

## Nginx Permission and Restart Commands

### Change Permissions for the Project Directory (If the domain not wroks due to Permission error)

```bash
sudo chmod -R a+x /home/username/projectfolder
sudo chmod -R 755 /home/username/projectfolder
sudo chmod -R 777 /home/username/projectfolder
```

### Restart Nginx Service

```bash
sudo service nginx restart
```

### Set Ownership and Permissions for Nginx Logs

```bash
sudo chown -R www-data:www-data /var/log/nginx
sudo chmod -R 755 /var/log/nginx
sudo chmod -R u+X /var/log/nginx
```

### Add User to Groups

```bash
sudo usermod -aG www-data
sudo usermod -aG sudo www-data
sudo usermod -aG username www-data
```


### Configuring Let's Encrypt SSL (Remote)
1. `$ sudo apt install python3-certbot-nginx` to install certbot.
2. `$ sudo ufw allow 'Nginx Full'` allow Nginx in http and htpps.
3. `$ sudo nano /etc/nginx/sites-available/django-gunicorn` and add the host name as the domain name that is configured with the server ip: server_name mohuls.com www.mohuls.com;
4. `$ sudo systemctl restart nginx` restarts nginx.
5. `$ sudo certbot --nginx -d mohuls.com -d www.mohuls.com` starts the installation process. Answer appropriate to the asked questions to complete.
6. `$ sudo systemctl status certbot.timer` to check status.
7. `$ sudo certbot renew --dry-run` tests renewal process. Now the site should serve in https.

### Disable Debug Mode

1. When you are on production the disable the Debug mode in the settings.py.
2. `$ nano stocks/settings.py` and change `DEBUG = True` to `DEBUG = False`.

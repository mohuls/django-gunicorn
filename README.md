# Django Gunicorn
This repository and README file describe basic python and django setup and deploy from local to cloud using Ubuntu 20.04 LTS, Nginx Web Server, Apache Web Server, Sqlite Database and Let's Encrypt SSL.

**Usage Note:** This documentation is for both local and remote machine (Local & Cloud flagged). If the local machine is already configured then just setup the cloud according to the below guidelines.

## Python and Virtual Environment Intro
In this repo described the fully optimized way to install Python using **pyenv** so that we can install and manage different versions of Python in the both local and remote machine. Then described the optimized way to install python virtual environment for isolating individual python application.

**Important:** Using python virtual environment is very useful for developing any kind of python applications (ex: this django application). It is because we can use different version and dependencies for each appliccation running in the same machine. Moreover, as the virtual environment is installed right inside the project folder so that the envrionment for the application remains same for local and remote machine when it is subject to deploy from local to remote server. So that, the dependencies never conflict.

## Django, Gunicorn & Nginx Intro
Django is a full stack web framework written in python for developing web applications and web API.

Gunicorn is a python application server that helps to run python application (in this case django application) also can be run flask application as well.

Nginx is a high end web application server for serving static and dynamic content. In this repo nginx is used with gunicorn for running our django aplication.

## Ubuntu 20.04 Setup (Local & Cloud)
We will not use root user alwyas. That's why we will create a new user with the sudo privilege.

1. On the local machine just create the user.
2. On remote machine first connect the machine using ssh.
3. Use a non-root sudo user for all the below operations.
**Hints:** To connect via SSH, add your local machine's public key (~/.ssh/id_rsa.pub) to the cloud SSH portion and then access the remote via $ ssh root@your_server_ip or use a .pem private key file for corresponding added public key on the machine (ex: EC2) by $ ssh -i 'key.pem' user@server-ip.

## Creating user account
1. `$ sudo adduser lina` Then enter password and info to create user.
2. `$ usermod -aG sudo lina` to add lina to sudo
3. `$ sudo ufw app list` to see all the firewall list
4. `$ sudo ufw allow OpenSSH` and then `$ sudo ufw enable` to allow OpenSSH
5. `$ sudo ufw status` to check status.
6. `$ su - lina` switch to lina from root or any other user.

## Installing pyenv (Local & Remote)
Pyenv is a python package manager that can be used to manage multiple versions of python on a single OS. Let's install pyenv latest version.

1. `$ sudo apt update -y` to update the system.
2. `$ sudo apt install -y build-essential` install the build dependencies.
3. `$ sudo apt install zlib1g-dev libssl-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl`
3. `$ git clone https://github.com/pyenv/pyenv.git ~/.pyenv` to clone the latest version of git.
4. `$ sudo echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc`
5. `$ sudo echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc`
6. `$ sudo echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -)"\nfi' >> ~/.bashrc`
7. `$ exec "$SHELL"`
8. `$ pyenv --version`. Now pyenv is installed successfully.

**Learn more about pyenv:** https://realpython.com/intro-to-pyenv/

##  Installing Python (Local & Remote)
**Note:** The python version to be installed depend on the version that require the application. We can install multiple version of python and switch back to specific verion for our specific python version.

0. `$ pyenv install --list` to see all the available python version.
1. `$ pyenv install x.x.x` to install the needed version. We can install multiple versions. We can activate specific version when we need to create a virtual environment for a specific application.
2. `$ pyenv versions` to see installed/available version to activate.
3. `$ pyenv global x.x.x` to activate a specific python version locally.
4. `$ pyenv global system` switch back to system version.

**Note:** In this deployment we will use python 3.6.9

## Creating Virtual Environments (Local & Remote)

**Important:** Before creating any virtual environment, switch to the desired python version using `$ pyenv global x.x.x`.

1. `$ pip install --user virtualenv` to install virtual environment.
2. `$ mkdir ~/django-gunicorn`  `$ cd ~/django-gunicorn` to project directory. Now to create a virtual env goto your project directory and type `$ python -m virtualenv env` it will create a virtual environment in the env folder.
3. `$ source env/bin/activate` to active the virtual env. Now you are isolated in the project directory with your own python version and packages.
4. To check the python and pip location type `$ which python` and `$ which pip`. Check if the installation location indicating the env folder or not. If indicates the env folder then the environment working fine (Environment activation is needed before checking).

**Note:** Make sure the app that was developed locally used python version is same as the virtual env.

## Develop Django Application (Locally)
Now develop the django application locally. Make sure the version of virtual environment of development environment is same as the remote environment we just created.

1. After development `$ pip freeze > requirements.txt` to store required packages.

## Pushing to GitHub (Local)

1. Upload the source file to a GitHub repo. Keep env folder in the .gitignore file. So that env folder will not be uploaded. Because it is created in the remote server by following above instructions.
2. If the application uses databases rather than sqlite3. Then backup the database and put in source file (better keep that db file in db folder).
3. `$ git init` then `$ git add .` the `$ git commit -m 'test deploy'`
4. `$ git remote add origin git@github.com:mohuls/django-gunicorn.git` the GitHub repo we just created on GitHub.
5. `$ git push -u origin master` to push the full project to GitHub repo.
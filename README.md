# ConnectMe
### Billionaires Boys Club<img src="https://ballzbeatz.com/wp-content/uploads/2018/01/Billionaire-Boys-Club-Logo-Decal-Sticker.jpg" height="60" style="margin-top:=-20px">
#### Project Manager: [Robin Han](https://www.github.com/robinhanstuy/) | Members: [Sajed Nahian](https://github.com/SajedNahian), [Jerry Ye](https://github.com/jerry1ye10), [Bill Ni](https://www.github.com/bnidevs/)
Software Development Second Term Project 

Overview:  
Tinder meets linkedin. A swipe based website that allows individuals to meet each other in a professional manner whether it be for a job interview or a mentor/mentee relationship. Our website will pair every mentee with a mentor and vice versa once per day. If the two both decide that it’s worth it to contact each other, a chat box will be created with the two of them. Matches will be based off similar professional interests and location. For example, if a mentee is interested in connecting with a software engineer and a mentor has developed at google for 5 years, they could be matched. 

### Install and run on localhost
1. Clone the repo via ssh or https
   - SSH: ```git clone git@github.com:robinhanstuy/ConnectMe.git```
   - HTTPS: ```git clone https://github.com/robinhanstuy/ConnectMe.git```
2. **(Optional)** Make and activate virtual environment
```
python3 -m venv <venv_name>
. <path-to-venv>/bin/activate
```
3. Enter the repo directory
```
cd <path-to-repo>
```
4. Install requirements
   - Python 3.7: ```pip3 install -r requirements.txt```
   - If in virtual environment with Python 3.7: ```pip install -r requirements.txt```
5. Run app.py
   - Python 3.7: ```python3 app.py```
   - If in virtual environment with Python 3.7: ```python app.py```
6. Go to http://127.0.0.1:5000/ on any browser

### Install and run on Apache2
1. SSH into your droplet:
```ssh <user>@<ip address>```
2. Move to the www directory:
```cd ../../var/www```
3. Create a new directory named after your app and cd into it
```
mkdir <appname>
cd <appname>
```
4. Get root access:
```sudo su```
5. Create a wsgi file named \<appname\>.wsgi
6. Clone the repo via https:
```git clone https://github.com/robinhanstuy/ConnectMe.git <appname>```
7. Add write permisssions:
```
chgrp -R www-data <appname>
chmod -R g+w <appname>
```
8. Move into the repo, rename app.py, and install requirements
```
cd <appname>
mv app.py __init__.py
pip3 install -r requirements.txt
```
9. Move to the sites-enabled directory:
```cd ~/../../etc/apache2/sites-enabled/```
10. Create a conf file named \<appname\>.conf
11. Enable the site:
```a2ensite <appname>```
12. Reload and restart the server
```
service apache2 reload
service apache2 restart
```
13. Go to your ip address on any browser

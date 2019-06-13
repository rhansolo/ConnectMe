# ConnectMe
### Billionaires Boys Club<img src="https://ballzbeatz.com/wp-content/uploads/2018/01/Billionaire-Boys-Club-Logo-Decal-Sticker.jpg" height="60" style="margin-top:=-20px">
#### Project Manager: [Robin Han](https://www.github.com/robinhanstuy/) | Members: [Sajed Nahian](https://github.com/SajedNahian), [Jerry Ye](https://github.com/jerry1ye10), [Bill Ni](https://www.github.com/bnidevs/)
Software Development Second Term Project 

Overview:  
Tinder meets linkedin. A swipe based website that allows individuals to meet each other in a professional manner whether it be for a job interview or a mentor/mentee relationship. Our website will pair every mentee with a mentor and vice versa once per day. If the two both decide that it’s worth it to contact each other, a chat box will be created with the two of them. Matches will be based off similar professional interests and location. For example, if a mentee is interested in connecting with a software engineer and a mentor has developed at google for 5 years, they could be matched. 

## Video
* [Watch our video demo here](https://youtu.be/NQfPFLINlhY)

### Install and run on localhost
1. Clone the repo via ssh or https
   - SSH: ```git clone git@github.com:robinhanstuy/ConnectMe.git```
   - HTTPS: ```git clone https://github.com/robinhanstuy/ConnectMe.git```
2. **(Optional)** Make and activate virtual environment
```
python3 -m venv <venv_name>
. <path-to-venv>/bin/activate
```
3. Move into the repo
```
cd <path-to-repo>
```
4. Install requirements
   - Python 3.7: ```pip3 install -r requirements.txt```
   - If in virtual environment with Python 3.7: ```pip install -r requirements.txt```
5. Move into the ConnectMe directory:
```cd ConnectMe```
6. Run \_\_init\_\_.py
   - Python 3.7: ```python3 __init__.py```
   - If in virtual environment with Python 3.7: ```python __init__.py```
7. Go to http://127.0.0.1:5000/ on any browser

### Install and run on Apache2
1. SSH into your droplet:
```ssh <user>@<ip address>```
2. Move to the www directory:
```cd ../../var/www```
3. Get root access:
```sudo su```
4. Clone the repo via https:
```git clone https://github.com/robinhanstuy/ConnectMe.git```
5. Move into the repo, add write permisssions, and install requirements:
```
cd ConnectMe
sudo chmod -R 777 data/
sudo chmod -R 777 static/
pip3 install -r requirements.txt
```
6. Open the conf file and change the server name to your ip address:
```nano connectme.conf```
7. Move the conf file to the sites-available directory:
```mv ConnectMe.conf ~/../../etc/apache2/sites-available/```
8. Move to the sites-available directory
```cd ~/../../etc/apache2/sites-available/```
9. Enable the site:
```a2ensite ConnectMe```
10. Restart the apache server:
```service apache2 restart```
11. Go to your ip address on any browser

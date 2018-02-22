# fishtankmonitor
This project holds all the information to make your own Fish Tank Monitor!

Login to the Pi using a HDMI cable and plugged in Keyboard and Mouse 

# Enable SSH by typing:
sudo raspi-config

sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
Add

network={
    ssid="Your Wifi Name"
    psk="Your Wifi Password"
}

# Update and set the login password to the "pi" account
passwd

# Setup Samba Share
 - This allows you to transfer files to the Pi ! You need to find out the pi's IP address and then you can browse to it using \\192.168.x.x   (or whetever your home network would have setup the Pi's address as)
 in terminal run 
 ```
 sudo ifconfig
```
and then just look for the inet addr: line for the relevant interface e.g. the Wifi Adapter
  
sudo apt-get install samba samba-common-bin
sudo nano /etc/samba/smb.conf 

Add this:
```
[Pi Home]
 comment= Pi Home
 path=/home/pi
 browseable=Yes
 writeable=Yes
 only guest=no
 create mask=0777
 directory mask=0777
 public=no
 valid users=pi

[Apache]
 comment= Apache
 path=/var/www
 browseable=Yes
 writeable=Yes
 only guest=no
 create mask=0777
 directory mask=0777
 public=no
 valid users=pi
```
sudo smbpasswd -a pi

# Setup Temp Sensing
sudo nano /boot/config.txt 

add

dtoverlay=w1-gpio
 to bottom and reboot


# Setup MySql
sudo apt-get install mysql-server --fix-missing
sudo apt-get install mysql-client php5-mysql
sudo apt-get install python-mysqldb

# Copy the TemperatureSensor folder your Pi home drive 

# Restore the database
Cd TemperatureSensor
Gunzip mysqldump.gz
mysql -u root -p < mysqldump

# Update the sql permissions 
Mysql -u root -p
Use mysql;
update user set Password=PASSWORD("password") where User='mysql-read';
update user set Password=PASSWORD("password") where User='mysql-all';
flush privileges;

# Install services for InstaPush  YEAAA IT ALERTS YOUR PHONE :D
http://videos.cctvcamerapros.com/digital-io-alarm-in-out/send-push-notifications-from-raspberry-pi.html

sudo apt-get install python-pycurl 
sudo apt-get install python-requests

# Install Apache and PHP
sudo apt-get install apache2 -y
sudo apt-get install php5 libapache2-mod-php5 -y
sudo apt-get install python-mysqldb


# Copy backup files from the Apache folder into the /var/www/html folder
run ```sudo chown -R pi /var/www/html ```

# Install LIRC for Aircon
sudo apt-get install lirc

# Update  this file
sudo nano /etc/lirc/hardware.conf
With 
```#Try to load appropriate kernel modules
LOAD_MODULES=true

# Run "lircd --driver=help" for a list of supported drivers.
DRIVER="default"
# usually /dev/lirc0 is the correct setting for systems using udev
DEVICE="/dev/lirc0"
MODULES="lirc_rpi"

# Default configuration files for your hardware if any
LIRCD_CONF=""
LIRCMD_CONF=""
```

# Update this file 
sudo nano /boot/config.txt

Update the dtoverlay lirc section to this:
dtoverlay=lirc-rpi,gpio_out_pin=17


# Password Protect Apache
sudo htpasswd -c /etc/apache2/.htpasswd userName
sudo htpasswd /etc/apache2/.htpasswd userName


sudo nano /etc/apache2/sites-enabled/000-default.conf
```
<VirtualHost *:80>
  ServerAdmin webmaster@localhost
  DocumentRoot /var/www/html
  ErrorLog ${APACHE_LOG_DIR}/error.log
  CustomLog ${APACHE_LOG_DIR}/access.log combined
<Directory "/var/www/html/aircon">
      AuthType Basic
      AuthName "Restricted Content"
      AuthUserFile /etc/apache2/.htpasswd
      Require valid-user
  </Directory>
</VirtualHost>
```


# reboot

# Install No-IP

Mkdir /home/pi/noip
cd noip
wget http://www.no-ip.com/client/linux/noip-duc-linux.tar.gz
tar vzxf noip-duc-linux.tar.gz
Next navigate to the directory you created to locate the downloaded files.
cd noip-2.1.9-1
Now install the program.
sudo make
sudo make install
Login when prompted


# Lights
sudo apt-get install pigpio
sudo apt-get install python-pigpio

# Setup Cron
sudo crontab -e 

@reboot sudo python /home/pi/TemperatureSensor/temperaturelogger.py >> /home/pi/TemperatureSensor/log.txt
@reboot sudo pigpiod
@reboot sudo python /home/pi/Lights/autolights.py reboot >> /home/pi/Lights/log.txt
@reboot sudo /usr/local/bin/noip2
#0 7 * * * sudo python /home/pi/Lights/autolights.py dawn
#0 12 * * * sudo python /home/pi/Lights/autolights.py off
#55 18 * * * sudo python /home/pi/Lights/autolights.py dusk
#30 21 * * * sudo python /home/pi/Lights/autolights.py dawnlow
#0 0 * * *  sudo python /home/pi/Lights/autolights.py night
0 1 * * * sudo sh /home/pi/TemperatureSensor/backupDB.sh


Job done 

import libcamera
from picamera2 import Picamera2, Preview
import smtplib
from datetime import datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import RPi.GPIO as GPIO
import time

# Adjust the below constants to your requirements!!
# You can generate an app password by visiting this link: https://myaccount.google.com/apppasswords

SMTP_USERNAME = '<Google account address>'
SMTP_PASSWORD = '<app password>'

SUBJECT = 'Security alert!'
FROM_ADDRESS = '<Google account address, same as SMTP_USERNAME>'
TO_ADDRESS = '<Email address to send the alert to>'

GPIO.setmode(GPIO.BCM)

picam = Picamera2()
picam.resolution = (4608,2592)
picam.start_preview()

config = picam.create_preview_configuration(main={"size": (4608,2592)})
picam.configure(config)
picam.start()
   
GPIO.setup(23, GPIO.IN)
while True:
    if GPIO.input(23):
        current_date_temp = datetime.now()
        current_date = current_date_temp.strftime("%d-%m-%Y-%H-%M-%S")
        filename = f"motion-image-{current_date}.jpg"
        print("Motion detected!")
        #camera warm-up time
        picam.start()
        time.sleep(2)
        picam.capture_file(filename)
        time.sleep(10)
        msg = MIMEMultipart()
        msg['Subject'] = SUBJECT
        msg['From'] = FROM_ADDRESS
        msg['To'] = TO_ADDRESS
       
        fp = open(filename,'rb')
        img = MIMEImage(fp.read())
        fp.close()
        msg.attach(img)

        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(user=SMTP_USERNAME, password=SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        picam.close()
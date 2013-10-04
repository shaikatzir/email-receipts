
from time import strftime
from time import sleep
import time
import oauth2 as oauth
import oauth2.clients.imap as imaplib
import oauth2.clients.smtp as smtplib
#user_mail = "donde.test@gmail.com"
#user_token = 
#user_pwd = 

def getInbox(user_mail,user_token,user_pwd,connType = "IMAP",retries=5, delay=3):
   while True:
        try:
        
          # Set up your Consumer and Token as per usual. Just like any other
          # three-legged OAuth request.
          consumer = oauth.Consumer('anonymous', 'anonymous')
          token = oauth.Token(user_token, user_pwd)

          # Setup the URL according to Google's XOAUTH implementation. Be sure
          # to replace the email here with the appropriate email address that
          # you wish to access.
          url = "https://mail.google.com/mail/b/"+user_mail+"/imap/"

          if (connType == "IMAP"):
              conn = imaplib.IMAP4_SSL('imap.googlemail.com')
              conn.debug = 0 
          else:
              conn = smtplib.SMTP('smtp.googlemail.com', 587)
              conn.set_debuglevel(True)
              conn.ehlo('test')
              conn.starttls()
              conn.ehlo()
          # This is the only thing in the API for impaplib.IMAP4_SSL that has 
          # changed. You now authenticate with the URL, consumer, and token.
          conn.authenticate(url, consumer, token)

          
    
          return conn
#        except imaplib.IMAP4_SSL.abort:
        except:
            if retries > 0:
                retries -= 1
                time.sleep(delay)
            else:
                raise
                


import email , email.errors, email.header, email.message, email.utils
import getpass, imaplib, smtplib, os , sys, time, getopt
from time import strftime
from time import sleep
import datetime
import sys, os, re,  io
from io import StringIO
import email, mimetypes
from email.utils import parseaddr

from lxml import etree, html
import connect_mail

detach_dir = '.' # directory where to save attachments (default: current)
# if using user input :
#EXAMPLE CODE :user = raw_input("Enter your GMail username:")
#EXAMPLE CODE :pwd = getpass.getpass("Enter your password: ")
username = "donde.test@gmail.com"
password = "dondetest123"

#imap_host = 'imap.gmail.com'
imap_host =  'imap.googlemail.com'
smtp_host = "smtp.gmail.com"
smtp_port = 587
to_addr = "donde.test@gmail.com"

#Frequency - frequency of checking server in seconds
Frequency = 10

import urllib, re, datetime, json, string, sys, time #, urllib.request, urllib.error

DBG = 1


user_mail = "try.new.shai@gmail.com"
user_token = "1/oYVRk7YiY_nWRD0LlOnfjNEVvKDVGLQ2moPxqaqKewQ"
user_pwd = "m-sGj5UcLcN5Zb0m-xdbGXKb"



            
def fetch_mail():
    # connecting to the user gmail imap server
    m= connect_mail.getInbox(user_mail,user_token,user_pwd)
    
    # open authenticated SMTP to our application gmail and send message with
    # specified envelope from and to addresses
#    smtp = smtplib.SMTP(smtp_host, smtp_port)
#    smtp.set_debuglevel(0)
#    smtp.ehlo()
#    smtp.starttls()
#    smtp.ehlo
#    smtp.login(username,password)
#    smtp = connect_mail.getInbox(user_mail,user_token,user_pwd,"SMTP")
    conn = imaplib.IMAP4_SSL('imap.gmail.com', port = 993)
    conn.login(username, password)
    conn.select("INBOX")
    

    #EXAMPLE CODE :m.select("[Gmail]/All Mail") # here you a can choose a mail box like INBOX instead
    # use m.list() to get all the mailboxes, "INBOX" to get only inbox
    m.select("INBOX")
    #resp, items = m.search(None, '(UNSEEN)') # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
    
    first_time = True

    datestr = (datetime.date.today() - datetime.timedelta(20)).strftime("%d-%b-%Y")
    #print "date is " + datestr 
    
    queryBrands = '(OR (SUBJECT "castro") (SUBJECT "J.Crew"))'
    queryDate =  '(SINCE "{date}")'.format(date=datestr) #'((FROM "castro") OR (SUBJECT "castro"))'
    #search in the user mail for eReceipts .
    if (first_time):
        #if new user search all mail
        resp, items = m.search(None, queryBrands)
    else :
        #if no new, search mails since last search
        resp, items = m.search(None, queryBrands, queryDate)
        
    items = items[0].split() # getting the mails id

    for emailid in items:
        if (DBG):
             print ("===========EMAIL============================")
        resp, data = m.fetch(emailid, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
        #resp2, data2 = m.fetch('fetch', uid, '(BODY[HEADER.FIELDS (DATE SUBJECT)]])')
        #email_header = data2[0][1]
        #msg2 = email.message_from_string(email_header)
        
        if resp != 'OK':
            error(data[-1])
        #print (data[0])
        #EXAMPLE CODE :email_body = data[0][1] # getting the mail content
        email_body = data[0][1]
        #print ("email_body is :" + email_body)
        #print(email_body)
        #msg = email.message_from_string(email_body)
        conn.append("INBOX", '', imaplib.Time2Internaldate(time.time()), str(email.message_from_string(data[0][1])))
#        #SUBJECT
#        if (DBG):
#              print("subject :")
#              print(msg['Subject'])

#        #FROM
#        email_From = parseaddr(msg['From'])[1]
#        if (DBG) :
#              print("email from :")
#              print(email_From)
#        

#        #DATE
#        if (DBG):
#            print("date :")
#            print(msg['date'])



#        #to
#        if (DBG):
#            print("to :")
#            print(msg['to'])
        

        #header = 'To:' + to_addr + '\n' + 'From: ' + user_mail + '\n' + 'Subject:test\n'#+ msg['Subject'] +'\n'
        #print header
        #bodytext=msg.get_payload()[0].get_payload();
        #msg = header + bodytext
        # replace headers (could do other processing here)
        #msg.add_header("From", user_mail)
        #msg.add_header("To", to_addr)
        #print msg
        #try :
        #msg=header + email_body
        #print msg
        #smtp.sendmail(user_mail, [to_addr], msg.as_string())
        #except:
        #  print "errorororororor" 



        sleep(0.1)
        
#       IF WANT TO FLAG AS UNREAD : resp, data = m.store(emailid,'-FLAGS','\\Seen')


    conn.expunge()
    conn.close()
    conn.logout()
    m.expunge()
    m.close()
    m.logout()

def main():
        
#	file_or_server = args()
#	print "\n"
#	print "Monitoring the Mail server  " + file_or_server + "  for account  " + User
#        while 1:
#            process_server(file_or_server)
             fetch_mail()
             printfre = str(Frequency)
             print ("Sleeping for  " + printfre + "  seconds...")
#             sleep(Frequency)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		pass

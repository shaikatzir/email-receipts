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

username = "donde.test@gmail.com"
password = "dondetest123"

imap_host =  'imap.googlemail.com'
to_addr = "donde.test@gmail.com"

import urllib, re, datetime, json, string, sys, time 

DBG = 1


#user_mail = "try.new.shai@gmail.com"
#user_token = "1/oYVRk7YiY_nWRD0LlOnfjNEVvKDVGLQ2moPxqaqKewQ"
#user_pwd = "m-sGj5UcLcN5Zb0m-xdbGXKb"


Brands_List = ["castro","tt", "J.Crew"]

queryBrands = ""
for br in Brands_List[:-1] :
   queryBrands += '(OR (SUBJECT "' + br +'") '
queryBrands += '(SUBJECT "' + Brands_List[-1] + '")'
for i in range(1,len(Brands_List)):
   queryBrands += ')' 
print   queryBrands
            
def fetch_mail():
    
    if len(sys.argv) > 1 :
       user_mail = sys.argv[1]
       user_token = sys.argv[2]
       user_pwd = sys.argv[3]
       
    # connecting to the user gmail imap server
    m= connect_mail.getInbox(user_mail,user_token,user_pwd)
    
    conn = imaplib.IMAP4_SSL(imap_host)#('imap.gmail.com', port = 993)
    conn.login(username, password)
    conn.select("INBOX")

    m.select("INBOX")
    
    first_time = True

    datestr = (datetime.date.today() - datetime.timedelta(20)).strftime("%d-%b-%Y")
    #print "date is " + datestr 
    
    
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
        
        if resp != 'OK':
            error(data[-1])
        #print (data[0])
        conn.append("INBOX", '', imaplib.Time2Internaldate(time.time()), str(email.message_from_string(data[0][1])))


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
#             printfre = str(Frequency)
#             print ("Sleeping for  " + printfre + "  seconds...")
#             sleep(Frequency)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		pass

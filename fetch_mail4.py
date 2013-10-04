import email , email.errors, email.header, email.message, email.utils
import getpass, imaplib, os , sys, time, getopt
from time import strftime
from time import sleep
import sys, os, re,  io
from io import StringIO
import email, mimetypes
# Import the email modules we'll need
from email.parser import Parser
from email.mime.multipart import MIMEMultipart      # Message subclasses
from email.mime.text import MIMEText 
#import BeautifulSoup
#from dist import BeautifulSoup as bs
from bs4 import BeautifulSoup as bs
from email.utils import parseaddr
import unicodedata
from bs4 import UnicodeDammit
from lxml import etree, html

detach_dir = '.' # directory where to save attachments (default: current)
# if using user input :
#EXAMPLE CODE :user = raw_input("Enter your GMail username:")
#EXAMPLE CODE :pwd = getpass.getpass("Enter your password: ")

# Constant mail
user = "donde.test"
pwd = "dondetest123"

#Frequency - frequency of checking server in seconds
Frequency = 5

import urllib, re, datetime, json, string, sys, time #, urllib.request, urllib.error

server='donde-app.com'
port='2222'
checksum='323232'
ver='0.1'
DBG = 1

def searchItemBySKU(clientID,SKU):
    url = 'http://'+server+':'+port+'/'+ver+'/API/searchItemBySKU/'+checksum+'/SKU='+SKU+'&clientID='+str(clientID)
    if (DBG):
        print("URL Request 1 :" + url)
    try:
#         open_url = urllib.request.urlopen(url)
         open_url = urllib.urlopen(url)
         ans = open_url.read()
#         ans = ans.decode('utf8')
    except :
         print(sys.exc_info()[0])
         return 0
    if (DBG):
         print("URL Answer")
         print(ans)
    data = json.loads(ans)
    if (data['success']):
        if (data['profile']):
             if (data['profile'][0]):
                  if (data['profile'][0]['itemID']):
                       print(str(data['profile'][0]['itemID'])+" "+ str(data['profile'][0]['desc']) +" "+ str(data['profile'][0]['color']) +" "+ str(data['profile'][0]['type']))
                       return(str(data['profile'][0]['itemID']))
                  else:
                       print("ERROR " + str(data['error']))
                       return 0
             else:
                  return 0
        else:
             return 0
    else:
         return 0
def addItemToClient(clientID,itemID):
    url = 'http://'+server+':'+port+'/'+ver+'/API/addToClientItemCon/'+checksum+'/clientID='+str(clientID)+'&itemID='+str(itemID)
#         open_url = urllib.request.urlopen(url)
    open_url = urllib.urlopen(url)
    ans = open_url.read()
#         ans = ans.decode('utf8')
    if (DBG):
         print("URL Answer 2")
         print(ans)
    data = json.loads(ans)
    if (data['success']):
         if (data['error']==""):
              print("clientID "+clientID+ " added item "+ itemID+ " successfully")
         else:
              print("ERROR " + str(data['error']))

def userByEmail(email):
    url = 'http://'+server+':'+port+'/'+ver+'/API/userByEmail/'+checksum+'/email='+email
#         open_url = urllib.request.urlopen(url)
    while True:
        try:
            open_url = urllib.urlopen(url)
            ans = open_url.read()
            break
        except:    
            print 'failed read url: ' + url
            pass
        
    if (DBG):
         print("URL Answer3")
         print(ans)
    data = json.loads(ans)
    if (data['success']):
        #print(email+ " login successfully clientID : "+data['profile']['clientID'])
        return data['profile'][0]['_id']
    else:
        print("ERROR " + email+" "+str(data['error']))



def find_SKU(text) :

    #EXAMPLE HTML for test
    #text2= "<table width=100% border=1 cellpadding=0 cellspacing=0 bgcolor=#e0e0cc><tr><td width=12% height=1 align=center valign=middle  bgcolor=#e0e0cc bordercolorlight=#000000 bordercolordark=white> <b><font face='Verdana' size=1><a href='http://www.dailystocks.com/' alt='DailyStocks.com' title=\"Home\">Home</a></font></b></td></tr></table><table width='100%' border='0' cellpadding='1' cellspacing='1'> <tr class='odd'><td class='left'><a href='whatever'>ABX</a></td><td class='left'>Barrick Gold Corp.</td><td>55.95</td><td>55.18</td><td class='up'>+0.70</td><td>11040601</td><td>70.28%</td><td><center>&nbsp;<a href='whatever' class='bcQLink'>&nbsp;Q&nbsp;</a>&nbsp;<a href='chart.asp?sym=ABX&code=XDAILY' class='bcQLink'>&nbsp;C&nbsp;</a>&nbsp;<a href='texpert.asp?sym=ABX&code=XDAILY' class='bcQLink'>&nbsp;O&nbsp;</a>&nbsp;</center></td></tr></table>"
    #text=text2

    #print(text.decode('utf-8'));
    #dammit = UnicodeDammit(text);
    #dammit =dammit.unicode_markup;
    #dammit=text.decode('utf-8');
    #html = lxml.html.fromstring(text);
    #dammit = lxml.html.tostring(html);
    #parse into HTML tree
    try :
        soup = bs(text, "lxml")
        if (DBG) :
            print("using lxml parser")
    except :
        try :
            soup = bs(text,"html5lib")
            if (DBG) :
                 print("using html5lib parser")
        except:
            soup = bs(text)
            if (DBG) :
                 print("using default parser")
        

    #print(soup.prettify())
   
    #locate the table containing a cell with the given text
    owner = re.compile('sku',re.I) #re.I - don't be case sensitive
    cells = soup.findAll(text=owner)
    items = []
    if (DBG) : 
        print("found SKUs :")
        print (cells)
    for cell in cells:

        #find the row
        cell = cell.find_parent("tr")
        tr_table = cell
        #print("parent")
        #print(cell)
        if not cell :
             return 0   #should add function to deal SKU outside table

        #search which column is "SKU"
        column = 0
          
        #take all td or th
        col = cell.findAll(["td", "th"]);
        #iterate inside first row to find "sku" column
        while not col[column].findAll(text=owner) :
             column = column +1

        if (DBG):
             print ("which column is SKU :" + str(column))

        #search every row (except for the first one) for the sku number
        rows = tr_table.find_parent("table").findAll("tr")
        print("rows")
        print(rows)
        
        for row in rows[1:]:
            print("row")
            print(row)
            ob = row.findAll(["td", "th"])[column]
            print("ob")
            for s in ob.text.split():
               if s.isdigit() and len(s) > 6:
                   print("SKU :" + str(s))
                   item = searchItemBySKU("51ab7e778638fa9f2100002a",s)
                   print(item)
                   if item:
                        print("returning "+item)
                        items.append(item)
                        #addItemToClient("51ab7e778638fa9f2100002a",item)

    
    return items



def connect(retries=5, delay=3):
    while True:
        try:
            imap_host = 'imap.gmail.com'
            mail = imaplib.IMAP4_SSL(imap_host)
            mail.login(user,pwd)
            return mail
        except imaplib.IMAP4_SSL.abort:
            if retries > 0:
                retries -= 1
                time.sleep(delay)
            else:
                raise

            
def fetch_mail():
    # connecting to the gmail imap server
    m = connect()

    #m = imaplib.IMAP4_SSL("imap.gmail.com")
    #m.login(user,pwd)
    #EXAMPLE CODE :m.select("[Gmail]/All Mail") # here you a can choose a mail box like INBOX instead
    # use m.list() to get all the mailboxes, "INBOX" to get only inbox
    m.select("INBOX")
    resp, items = m.search(None, '(UNSEEN)') # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
    items = items[0].split() # getting the mails id

    for emailid in items:
        if (DBG):
             print ("===========EMAIL============================")
        resp, data = m.fetch(emailid, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
        if resp != 'OK':
            error(data[-1])
        #print (data[0])
        #EXAMPLE CODE :email_body = data[0][1] # getting the mail content
        email_body = data[0][1]
        #print ("email_body is :" + email_body)
        #print(email_body)
        msg = email.message_from_string(email_body)

        #SUBJECT
        if (DBG):
              print("subject :")
              print(msg['Subject'])

        #FROM
        email_From = parseaddr(msg['From'])[1]
        if (DBG) :
              print("email from :")
              print(email_From)
        clientID = 0
        if (email_From):
            clientID = userByEmail(email_From)
            if (DBG):
                print("clientID from :")
                print(clientID)
        

        #DATE
        if (DBG):
            print("date :")
            print(msg['date'])



        #to
        if (DBG):
            print("to :")
            print(msg['to'])


        #body

        count = 0
        for part in msg.walk():
            #print ("=================================" + str(count))
            count = count +1
            #print (part.get_content_type())
            #print (part)
            if part.get_content_type() == "text/html":
                text = str(part)
            
            
        
        
        

        #resp, data = m.fetch(emailid, '(UID BODY[TEXT])')
        #print("body :")
        #print(data[0][1])
        #text = str(data[0][1])
        #text= text[text.find("<table"):]
        

        #text = "<body>" + text + "</body>"
        #print("text is : " + text)
        #print("done text")
        
        items = find_SKU(text)
        print("items")
        print(items)
        if clientID:
            if items:
               for item in items:
                    addItemToClient(clientID,item)

        sleep(0.1)
        
        #addItemToClient("51ab7e778638fa9f2100002a",item)
#       IF WANT TO FLAG AS UNREAD : resp, data = m.store(emailid,'-FLAGS','\\Seen')



    m.expunge()
    m.close()
    m.logout()

def main():
        
#	file_or_server = args()
#	print "\n"
#	print "Monitoring the Mail server  " + file_or_server + "  for account  " + User
        while 1:
#            process_server(file_or_server)
             fetch_mail()
             printfre = str(Frequency)
             print ("Sleeping for  " + printfre + "  seconds...")
             sleep(Frequency)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		pass

import json                               
import time
from urllib.request import urlopen         
from urllib.parse import quote, unquote 

# request format: https://api.telegram.org/bot<your-bot-token>/<command>
def aux_dec2utf8(resp):                     # a function for decoding HTML content to utf-8 format
    decoded = ''
    for line in resp:
        decoded += line.decode('utf-8')
    return decoded

TOKEN = '1883360322:AAFDrnxMJ1eaNEfUDwtYOGyhwMcteRA-dRs'
URL   = 'https://api.telegram.org/bot{}/'.format(TOKEN)

cmd   = 'getme'                      # Auxiliary variable for defining commands


resp  = urlopen(URL + cmd)                                     # reading the url
line  = aux_dec2utf8(resp)                                     # converting the content to utf-8
gtm   = json.loads(line)                                       # converting the content to JSON


status = True                                                  # define a status variable for the while loop
while status:                                                  # interring the while loop

    cmd = 'getUpdates'                                         # Auxiliary variable for defining commands

    resp = urlopen(URL + cmd)                                  # reading the url to get the current updates
    line = aux_dec2utf8(resp)                                  # converting the content to utf-8
    upds = json.loads(line)                                    # converting the content to JSON

    NoM  = len(upds['result'])                                 # Number of New Messages Received

    if NoM != 0:                                               # if updates are available

        msg  = upds['result'][0]['message']                    # make the current message ready for processing
        chid = str(msg['chat']['id'])                          # read the chat id

        if 'text' in msg:
            txt  = quote(msg['text'].encode('utf-8'))              # encoding the text to utf-8 then quoting it to url

            cmd  = 'sendMessage'                                   # Auxiliary variable for defining commands

            resp = urlopen(URL + cmd +
                 '?chat_id={}&text={}'.format(chid, txt))          # Parameter, Value pair for chat id and the text
            line = aux_dec2utf8(resp)                              # converting the content to utf-8
            chck = json.loads(line)                                # converting the content to JSON


            if chck['ok']:                                         # If sending was successfull

                uid = upds['result'][0]['update_id']               # Read the update id
                cmd = 'getUpdates'                                 # Auxilary variable for defining commands
                urlopen(URL + cmd + '?offset={}'.format(uid + 1))  # Giving the offset Telegram forgets all those messages before this update id
        else:
            uid = upds['result'][0]['update_id']                   # Read the update id
            cmd = 'getUpdates'                                     # Auxilary variable for defining commands
            urlopen(URL + cmd + '?offset={}'.format(uid + 1))      # Giving the offset Telegram forgets all those messages before this update id
    print('Waiting!')
    time.sleep(5)
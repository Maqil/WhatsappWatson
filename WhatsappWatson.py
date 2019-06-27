from selenium import webdriver
from ibm_watson import AssistantV1
from bs4 import BeautifulSoup
import json
import time
import threading

# Chrome driver
driverLocation = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(driverLocation)
driver.get('https://web.whatsapp.com/')

# Connect to Watson assistant
assistant = AssistantV1(
    version ='2019-02-28',
    iam_apikey ='DJgF-bLxDLiWlxVCebmLsonwEokj26QQdn4QQ4z2nKhc',
    url ='https://gateway-lon.watsonplatform.net/assistant/api'
)

# Get response from Watson Assistant
def askChatbot(userMessage, assistant):        
    response = assistant.message(
    workspace_id='29d60f54-68af-4df1-8f40-4d5687a2a80f',
    input={
        'text': userMessage
    }
    ).get_result()
    
    # Get response as JSON 
    chatbotRes = json.dumps(response.get(
        "output", "none").get("text", "none")[0], indent=4)    
    return chatbotRes

def chatbotResponse():
    conversation = driver.find_elements_by_class_name('message-in')

    list = []   
    for msgs in conversation:
        list.append(msgs.text)
    
    userMessageTime = list[-1]
    # Receive the last message without time
    userMessage = userMessageTime.splitlines()[0]
    print(userMessage)

    chatbotMsg = askChatbot(userMessage,assistant).replace('"', '')    
    print(chatbotMsg)

    # # Find message box
    msg_box = driver.find_element_by_class_name('_3u328')
    # Find the send button
    msg_box.send_keys(chatbotMsg)
    button = driver.find_element_by_class_name('_3M-N-')
    button.click()

def clientHandler():
    while True:
        # Count message tabs
        clients = driver.find_elements_by_class_name('_1ZMSM')    
        clientsList = []
    
        for clt in clients:
            clientsList.append(clt.text)
            print(clt.text)
            clt.click()
            chatbotResponse()
    
        clientCounter = len(clientsList)
        print("Client counter : " + str(clientCounter))
        time.sleep(3)

time.sleep(5)

# Takes receiver's name
name = input('Receiver name : ')

# Find receiver by name
receiver = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
receiver.click()
    
# Get all received messages
conversation = driver.find_elements_by_class_name('message-in')

list = []
for msgs in conversation:
    list.append(msgs.text)

chatbotResponse()

msgsCount = len(list)

threading.Thread(target=clientHandler).start()

while True:
    while msgsCount == len(list):
    
        time.sleep(2)
    
        conversation = driver.find_elements_by_class_name('message-in')
        list = []
        for msgs in conversation:
            list.append(msgs.text)
    
    	# Handle one message
        if (msgsCount + 1) == len(list):
            chatbotResponse()
            msgsCount = len(list)

        # Handle multiple msgs
        if (msgsCount + 2) == len(list):
        	# Find message box
            msg_box = driver.find_element_by_class_name('_3u328')       
            # Find the send button
            msg_box.send_keys("Please enter just one message")
            button = driver.find_element_by_class_name('_3M-N-')
            button.click()
            msgsCount = len(list)
import wiotp.sdk.device
import time
import random
import requests

wt = 2000
f1 = [0]
f2 = [0]
f3 = [0]
f4 = [0]
due = [0,0,0,0]
billed = [0,0,0,0]
total = [0,0,0,0]

myConfig = { 
    "identity": {
        "orgId": "udbkdj",
        "typeId": "project_device",
        "deviceId":"Ziggyp"
    },
    "auth": {
        "token": "919347495679"
    }
}

client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)
client.connect()

def publish():
    global f1, f2, f3, f4, wt
    
    myData={'Tank_level': wt, 'House_A':f1[-1], 'House_B':f2[-1], 'House_C':f3[-1], 'House_D':f4[-1]}
    client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
    print("Published data Successfully: %s", myData)

def empty_alert():
    url = "https://www.fast2sms.com/dev/bulkV2?authorization=RMnNiWhwprVQPFd4BTzGuCbeH2EAvfJOcUqKDxY6LjsSla9y3txN2psik6Am04wL75gIzt9fQTSYavhB&route=v3&sender_id=TXTIND&message=The%20water%20tank%20has%20emptied%20and%20being%20refilled!&language=english&flash=0&numbers=9030435887"
    sen = requests.get(url)
    print(sen.text)
    
def full_alert():
    url = "https://www.fast2sms.com/dev/bulkV2?authorization=RMnNiWhwprVQPFd4BTzGuCbeH2EAvfJOcUqKDxY6LjsSla9y3txN2psik6Am04wL75gIzt9fQTSYavhB&route=v3&sender_id=TXTIND&message=The%20water%20tank%20is%20refilled!%20The%20current%20capacity%20is%202000L&language=english&flash=0&numbers=9030435887"
    sen = requests.get(url)
    print(sen.text)

def billnotif(house, summ, quantity, loan, pnum):
    base_url = "https://www.fast2sms.com/dev/bulkV2?authorization=RMnNiWhwprVQPFd4BTzGuCbeH2EAvfJOcUqKDxY6LjsSla9y3txN2psik6Am04wL75gIzt9fQTSYavhB&route=q&message=Smart%20Water%20System-%20Dear%20House_A%20owner,%20The%20water%20bill%20of%20summ_%20is%20generated%20against%20your%20quantity_%20Litres%20of%20water%20usage%20in%20this%20term%20and%20loan_%20rupees%20of%20past%20dues.%20you%20can%20check%20out%20our%20website%20for%20more%20information%0AThank%20You%20for%20using%20our%20services&language=english&flash=0&numbers=9347495679"
    url = base_url.replace("House_A", house)
    url = url.replace("summ_", str(summ))
    url = url.replace("quantity_", str(quantity))
    url = url.replace("loan_", str(loan))
    url = url.replace("9347495679", str(pnum))
    
    sen = requests.get(url)
    print(sen.text) 

def publishbills():
    global f1, f2, f3, f4, due, billed, total
    
    billed[0] = billed[0]+sum(f1)
    billed[1] = billed[1]+sum(f2)
    billed[2] = billed[2]+sum(f3)
    billed[3] = billed[3]+sum(f4)

    due[0] = (billed[0]-sum(f1))*3
    due[1] = (billed[1]-sum(f2))*3
    due[2] = (billed[2]-sum(f3))*3
    due[3] = (billed[3]-sum(f4))*3

    total[0] = sum(f1)*3+due[0]
    total[1] = sum(f2)*3+due[1]
    total[2] = sum(f3)*3+due[2]
    total[3] = sum(f4)*3+due[3]
    
    myData={'Quan_A':sum(f1), 'Quan_B':sum(f2), 'Quan_C':sum(f3), 'Quan_D':sum(f4),
            'Due_A': due[0], 'Due_B': due[1], 'Due_C': due[2], 'Due_D': due[3], 
            'Cur_A': sum(f1)*3, 'Cur_B': sum(f2)*3, 'Cur_C': sum(f3)*3, 'Cur_D': sum(f4)*3, 
            'Total_A': total[0], 'Total_B': total[1], 'Total_C': total[2], 'Total_D': total[3]}
    
    client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
    print("Published data Successfully: %s", myData)
    billnotif("House_A", total[0], sum(f1), due[0], 9347495679)
    billnotif("House_B", total[1], sum(f2), due[1], 7903051892)
    billnotif("House_C", total[2], sum(f3), due[2], 9338971111)
    billnotif("House_D", total[3], sum(f4), due[3], 9290444031)
    
def consume(fa):
    global f1, f2, f3, f4, wt
    a = random.randint(0,30)
    if wt<a:
        if(fa == "f1"):
            f1.append(wt)
        if(fa == "f2"):
            f2.append(wt)
        if(fa == "f3"):
            f3.append(wt)
        if(fa == "f4"):
            f4.append(wt) 
        publishbills()
        f1 = [0]
        f2 = [0]
        f3 = [0]
        f4 = [0]
        fa = [0]      
        wt = 0
        publish()
        empty_alert()     
        for i in range(0, 2001, 200):
            wt = i
            publish() 
            time.sleep(0.5)           
        full_alert()            
              
    else:
        if(fa == "f1"):
            f1.append(a)
        if(fa == "f2"):
            f2.append(a)
        if(fa == "f3"):
            f3.append(a)
        if(fa == "f4"):
            f4.append(a)
        wt = wt-a

def paynotif(hs, tt,pn):
    base_url = "https://www.fast2sms.com/dev/bulkV2?authorization=RMnNiWhwprVQPFd4BTzGuCbeH2EAvfJOcUqKDxY6LjsSla9y3txN2psik6Am04wL75gIzt9fQTSYavhB&route=q&message=Smart%20Water%20System-%20Dear%20House_A%20owner,%20Payment%20of%20Total_%20has%20been%20received%20against%20your%20water%20bill.%20You%20are%20clear%20for%20this%20term%20of%20dues.%20you%20can%20check%20out%20our%20website%20for%20more%20information%0AThank%20You%20for%20using%20our%20services&language=english&flash=0&numbers=9347495679"
    url = base_url.replace("House_A", hs)
    url = url.replace("Total_", str(tt))
    url = url.replace("9347495679", str(pn))
    sen = requests.get(url)
    print(sen.text)
    
def paybills(m):
    global due, billed, f1, f2, f3, f4, total
    if m == "Pay_A":
        paynotif("House_A", total[0], 9347495679)
        billed[0] = 0
        due[0] = 0
        total[0] = 0
        myData={'Total_A': "Paid", 'Cur_A': "Paid", 'Due_A': due[0]}
        client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
        print("Published data Successfully: %s", myData)     
    elif m == "Pay_B":
        paynotif("House_B", total[1], 7903051892)
        billed[1] = 0
        due [1] = 0
        total[1] = 0
        myData={'Total_B': "Paid", 'Cur_B': "Paid", 'Due_B': due[1]}
        client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
        print("Published data Successfully: %s", myData)
    elif m == "Pay_C":
        paynotif("House_C", total[2], 9338971111)
        billed[2] = 0
        due[2] = 0
        total[2] = 0
        myData={'Total_C': "Paid", 'Cur_C': "Paid", 'Due_C': due[2]}
        client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
        print("Published data Successfully: %s", myData)
    elif m == "Pay_D":
        paynotif("House_D", total[3], 8978715993)
        billed[3] = 0       
        due[3] = 0
        total[3] = 0
        myData={'Total_D': "Paid", 'Cur_D': "Paid", 'Due_D': due[3]}
        client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
        print("Published data Successfully: %s", myData)

    
def myCommandCallback(cmd):
    print("\nMessage received from IBM IoT Platform: %s" % cmd.data['command'])
    m = cmd.data['command']
    print(m)
    if "Pay" in str(m):
        paybills(m)
    
    
while True:
    consume("f1")
    consume("f2")
    consume("f3")
    consume("f4")
    publish()
    client.commandCallback = myCommandCallback
    time.sleep(2)
client.disconnect()

import io
from tkinter import *
import csv
import requests
from style import text1,text2,colors
import os
from dotenv import load_dotenv
from contants import IDLE,LOAD,DONE,WRONG

load_dotenv()

API_KEY = os.getenv('API_KEY')
placeholder_text="Type Something ..."

win = Tk()
win.title("Chatbot by Meganova")

def getWeather(city):
    
    statusLabel.config(text=f"Status : {LOAD}")
    win.update()

    res=requests.get(f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no")

    if res.status_code==200:
        statusLabel.config(text=f"Status : {DONE}")
        win.update()
        
        res_body=res.json()
        
        weather_body=f"""
                    \n----------- Weather Report -------------
                    \n>> City : {res_body['location']['name']} 
                    \n>> Country : {res_body['location']['country']}
                    \n>> Temperature : {res_body['current']['temp_c']} ℃
                    \n>> Sky : {res_body['current']['condition']['text']}
                    \n>> Wind Speed : {res_body['current']['wind_kph']} Km/hr
                    \n>> Wind Degree : {res_body['current']['wind_degree']} Degree
                    \n>> Humadity : {res_body['current']['humidity']}
                    """
    
        label = Label(label_frame, 
                      text=f"Chatbot : {weather_body}",
                      bg=colors[0],fg=colors[1],font=text1, 
                      justify='left')

        
        label.pack(anchor=W)
        # print(res.json())
    else:
        statusLabel.config(text=f"Status : {WRONG}")
        win.update()

        label = Label(label_frame, text=f"Chatbot : This City doesn't exist !",bg=colors[0],fg=colors[3],font=text1)
        label.pack(anchor=W)
        print(res.json())

def getMessage():
    userMessage=messageBox.get("1.0","end-1c").capitalize()
    messageBox.delete("1.0",END)

    if(userMessage!=""):
        label = Label(label_frame, text=f"You : {userMessage}",bg=colors[0],fg=colors[2],font=text1)
        label.pack(anchor=W)
    
        if weatherCmd(userMessage):
            userMessage = userMessage[len('/weather'):].strip()
            getWeather(userMessage)
        else:
            getLocalResponse(userMessage)
            print(userMessage)
        
    canvas.config(scrollregion=canvas.bbox("all"))

def weatherCmd(message):
    if message.lower().startswith('/weather'):
        message = message[len('/weather'):]

        message = message.strip()

        return True
    else:
        return False


res=""
def getLocalResponse(message):

    with open("greeting.csv") as f:
        csv_data=csv.reader(f)
        
        for greetingMsg in csv_data:
            if(greetingMsg[0]==message.strip()):
                print(greetingMsg[1])  
                global res
                res=greetingMsg[1]
                break

    if(res!=""):
        label = Label(label_frame, text=f"Chatbot : {res}",bg=colors[0],fg=colors[1],font=text1)
        label.pack(anchor=W)
        res=""
    else:
        label = Label(label_frame, text=f"Chatbot : Invalid question",bg=colors[0],fg=colors[3],font=text1)
        label.pack(anchor=W)
    
    canvas.config(scrollregion=canvas.bbox("all"))


def focus_in(event):
    if messageBox.get("1.0", "end-1c") == placeholder_text:
        messageBox.delete("1.0", END)

def focus_out(event):
    if messageBox.get("1.0", "end-1c") == "":
        messageBox.insert(END, placeholder_text)

chatframe=Frame(win)
chatframe.grid(row=0,column=0,columnspan=2)

scrollbar = Scrollbar(chatframe, orient=VERTICAL)

canvas = Canvas(chatframe, yscrollcommand=scrollbar.set, height=400, width=520,bg=colors[0])
canvas.pack(side=LEFT, fill=BOTH, expand=True)

label_frame = Frame(canvas,bg=colors[0],padx=10,pady=15)

canvas.create_window((0, 0), window=label_frame, anchor=NW)

scrollbar.config(command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)


statusLabel=Label(win,text=f"Status : {IDLE}",font=text1,width=53,bg=colors[1],fg=colors[0])
statusLabel.grid(row=1,column=0,columnspan=2)

messageBox=Text(win,height=1,width=44,padx=10,pady=10,font=text1,bg=colors[0],fg=colors[1])
messageBox.insert(END, placeholder_text)

messageBox.bind("<FocusIn>", focus_in)
messageBox.bind("<FocusOut>", focus_out)

messageBox.grid(row=2,column=0)

sendBtn=Button(win,text="Send",font=text2,width=10,bg=colors[0],fg=colors[1],command=getMessage)
sendBtn.grid(row=2,column=1)

win.resizable(height=False,width=False)
win.mainloop()
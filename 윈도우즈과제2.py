# 컴퓨터학부 2021218019 김지나 윈도우즈 과제

import tkinter as tk
from datetime import datetime
from threading import Thread
from tkinter import ttk
import wx
import random
from multiprocessing import Queue
from tkinter import messagebox

# 전역 선언
surverQueue = Queue()
dataQueue = False


# 클래스 GUI
class GUI(wx.Panel):
    def __init__(self, parent, user):
        wx.Panel.__init__(self, parent)
        self.user = user
        self.color = random_color()
        text.tag_configure(self.user, foreground=self.color)
        userListBox.tag_configure(self.user, foreground=self.color)

        parent.CreateStatusBar()
        menuBar = wx.MenuBar()
        menu1 = wx.Menu()
        menu2 = wx.Menu()


        backcolor_red = menu1.Append(wx.ID_ANY, "빨간색")
        backcolor_yellow = menu1.Append(wx.ID_ANY, "노란색")
        backcolor_blue = menu1.Append(wx.ID_ANY, "파란색")

        menu1.Bind(wx.EVT_MENU, lambda event, color=wx.Colour(255, 0, 0): self.on_button_click(event, color),
                   backcolor_red)
        menu1.Bind(wx.EVT_MENU, lambda event, color=wx.Colour(255, 255, 0): self.on_button_click(event, color),
                   backcolor_yellow)
        menu1.Bind(wx.EVT_MENU, lambda event, color=wx.Colour(0, 0, 255): self.on_button_click(event, color),
                   backcolor_blue)

        fontcolor_red = menu2.Append(wx.ID_ANY, "빨간색")
        fontcolor_yellow = menu2.Append(wx.ID_ANY, "노란색")
        fontcolor_blue = menu2.Append(wx.ID_ANY, "파란색")


        menu2.Bind(wx.EVT_MENU, lambda event, color=wx.Colour(255, 0, 0): self.on_change_color(event, color),
                   fontcolor_red)
        menu2.Bind(wx.EVT_MENU, lambda event, color=wx.Colour(255, 255, 0): self.on_change_color(event, color),
                   fontcolor_yellow)
        menu2.Bind(wx.EVT_MENU, lambda event, color=wx.Colour(0, 0, 255): self.on_change_color(event, color),
                   fontcolor_blue)

        menuBar.Append(menu1, "배경화면 색 설정")
        menuBar.Append(menu2, "글자 색 설정")
        parent.SetMenuBar(menuBar)




        button = wx.Button(self, label="입력", size=(30, 30), pos=(250, 320))

        self.Bind(wx.EVT_BUTTON, self.write_Queue, button)
        self.chatlog = wx.TextCtrl(self, size=(280, 320), style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL | wx.VSCROLL)

        self.textBox = wx.TextCtrl(self, size=(250, 30), style=wx.TE_MULTILINE, pos=(0, 320))



        join_message = f"{self.user}님이 채팅에 참여했습니다.\n"
        putDataIntoQueue(join_message)
        self.chatlog.AppendText(join_message)


    def on_button_click(self, event, color):
        self.chatlog.SetBackgroundColour(color)
        self.chatlog.Refresh()

    def initTextBox(self):
        self.textBox.Clear()

    def syncChat(self):
        for user_id in id_list:
            user_id.chatlog.SetValue(text.get("0.0", tk.END))

    def print_chat(self):
        if dataQueue:
            data = read_Queue()
            text.insert("1.0", data)
            text.tag_add(self.user, "1.0", "1.end")
            self.syncChat()

        self.initTextBox()

    def write_Queue(self, event):
        text_value = self.textBox.GetValue()
        timestamp_full = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

        putDataIntoQueue(timestamp_full + " " + self.user + ":" + text_value + "\n")
        self.print_chat()

    def on_change_color(self, event, color):
        self.chatlog.SetForegroundColour(wx.Colour(color))
        self.chatlog.Refresh()




def wxPythonApp():
    user = name.get()
    app = wx.App()
    frame = wx.Frame(
        None, title=f"{user}", size=(300, 440))
    user_id = GUI(frame, user)
    id_list.append(user_id)
    frame.Show()
    runT = Thread(target=app.MainLoop)
    runT.daemon = True
    runT.start()
    update_user_listbox()


def random_color():
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)

    color = "#{:02x}{:02x}{:02x}".format(red, green, blue)
    return color


def update_user_listbox():
    userListBox.delete(1.0, tk.END)
    for user_id in id_list:
        user_text = f"{user_id.user}\n"
        userListBox.insert("1.0", user_text)
        userListBox.tag_add(user_id.user, "1.0", "1.end")


def putDataIntoQueue(data):
    global dataQueue
    dataQueue = True
    surverQueue.put(data)


def read_Queue():
    global dataQueue
    dataQueue = False
    return surverQueue.get()

def on_closing():
    if messagebox.askokcancel("프로그램 종료", "정말로 채팅 프로그램을 종료하시겠습니까?"):
        win.destroy()




win = tk.Tk()
win.title("컴퓨터학부 2021218019 김지나 윈도우즈과제-채팅프로그램_서버")
win.geometry("300x500")
win.iconbitmap("cpu_setting_icon_257310.ico")

id_list = []
name = tk.StringVar()
nameEntered = ttk.Entry(win, width=12, textvariable=name)
nameEntered.grid(column=1, row=3)
nameEntered.focus()

text = tk.Text(win, height=20, width=40, borderwidth=2, wrap='word')
text.grid(column=0, sticky='WE', columnspan=3)

ttk.Label(win, text="닉네임을 입력하세요:").grid(column=0, row=3)
ttk.Label(win, text="<서버 컴퓨터>").grid(column=0, row=0, sticky='WE')

ttk.Label(win, text="접속한 유저 목록").grid(column=0, row=1, sticky='WE')
userListBox = tk.Text(win, height=10, width=20)
userListBox.grid(column=0, row=2, sticky='WE', columnspan=3)

action = ttk.Button(win, text="닉네임 입력", command=wxPythonApp)
action.grid(column=2, row=3)

win.protocol("WM_DELETE_WINDOW", on_closing)
win.mainloop()
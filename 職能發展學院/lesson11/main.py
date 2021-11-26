import tkinter as tk
import dataSource
from tkinter import messagebox
import tkinter.ttk as ttk
from datetime import datetime,timedelta

class Window(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("全省空氣品質指標")

        #--------------取得資料start-------------------#
        try:
            self.downloadTime = datetime.now()
            citylist = dataSource.getAirData()
            self.cities = {cityObject.county:cityObject for cityObject in citylist} #包存現在要顯示的資料,轉成dict,key=城市名,value=CityWeather的實體
        except ValueError as e:
            messagebox.showwarning("連線錯誤",e)
            self.destroy()

        currentTimeString = citylist[0].time #取得json內顯示的時間字串

        self.currentDateTime = datetime.strptime(currentTimeString,"%Y-%m-%d %H:%M:%S.%f") #將字串轉為datetime物件,保存目前顯示資料的datetime物件

        print(self.currentDateTime)
        print(self.cities)
        # --------------取得資料end-------------------#



        # --------------建立視窗start-------------------#
        mainFrame = tk.Frame(self,width=500,height=600,borderwidth=1,relief=tk.GROOVE,padx=20,pady=20)

        #建立上方的topFrame
        topFrame = tk.Frame(mainFrame)
        tk.Label(topFrame,text="台灣各地空氣品質指標",font=("arial",22,"bold"),fg="#555555").pack()
        self.currentTimeLabel = tk.Label(topFrame,text="觀測時間:xxxxxxxxx",font=("arial",16),fg="#555555")
        self.currentTimeLabel.pack(pady=(30,10))
        self.nextTimeLabel = tk.Label(topFrame,text="下次更新時間:xxxxxxxxx",font=("arial",16),fg="#555555")
        self.nextTimeLabel.pack()
        self.leftTimeLabel = tk.Label(topFrame, text="20:15", font=("arial", 16), fg="#555555")
        self.leftTimeLabel.pack()
        topFrame.pack()

        #建立中間的middleFrame
        middleFrame = tk.Frame(mainFrame)
        tk.Label(middleFrame,text="請選擇監測站:",font=("arial",20),fg="#555555").pack(side=tk.LEFT)
        self.comboBox = ttk.Combobox(middleFrame,font=("arial",20))
        self.comboBox.pack(side=tk.LEFT)
        self.comboBox.bind('<<ComboboxSelected>>', self.combobox_selected)
        middleFrame.pack(pady=20)

        #建立下方的bottomFrame
        bottomFrame = tk.Frame(mainFrame)
        tk.Label(bottomFrame,text="監測點:",font=("Arial",14)).grid(row=0,column=0,sticky=tk.E,padx=10,pady=10)
        self.siteNameLabel = tk.Label(bottomFrame,text="監測點",font=("Arial",16)).grid(row=0,column=1,sticky=tk.E,padx=10,pady=10)
        tk.Label(bottomFrame, text="城市:", font=("Arial", 14)).grid(row=1, column=0, sticky=tk.E, padx=10, pady=10)
        self.cityNameLabel = tk.Label(bottomFrame, text="城市", font=("Arial", 16)).grid(row=1, column=1, sticky=tk.E,
                                                                                        padx=10, pady=10)
        tk.Label(bottomFrame, text="AQI:", font=("Arial", 14)).grid(row=2, column=0, sticky=tk.E, padx=10, pady=10)
        self.aqiLabel = tk.Label(bottomFrame, text="AQI", font=("Arial", 16)).grid(row=2, column=1, sticky=tk.E,
                                                                                       padx=10, pady=10)
        tk.Label(bottomFrame, text="PM2.5:", font=("Arial", 14)).grid(row=3, column=0, sticky=tk.E, padx=10, pady=10)
        self.pm25Label = tk.Label(bottomFrame, text="PM2.5", font=("Arial", 16)).grid(row=3, column=1, sticky=tk.E,
                                                                                   padx=10, pady=10)
        tk.Label(bottomFrame, text="狀態:", font=("Arial", 14)).grid(row=4, column=0, sticky=tk.E, padx=10, pady=10)
        self.stateLabel = tk.Label(bottomFrame, text="狀態", font=("Arial", 16)).grid(row=4, column=1, sticky=tk.E,
                                                                                      padx=10, pady=10)

        bottomFrame.pack(pady=20)


        mainFrame.pack_propagate(0)
        mainFrame.pack(padx=50,pady=50)
        # --------------建立視窗end-------------------#

        #-------------更新標題start---------#
        self.updateWindowContent(self.currentDateTime,self.downloadTime,list(self.cities.keys()))
        # -------------更新標題end---------#

    def updateWindowContent(self,displayCurrent,downloadTime,cityNames):
        '''
        更新畫面的內容
        :param displayCurrent: 觀測的時間(datetime物件)
        :param downloadTime: 現在下載的時間(datetime物件)
        :param cityNames:目前所有城市名程(list,包含城市名稱字串)
        :return:
        '''
        self.currentTimeLabel.config(text=displayCurrent.strftime("觀測時間:%Y年%m月%d日--%H時%M分%S秒"))
        updateTime = downloadTime + timedelta(minutes=30);
        self.nextTimeLabel.config(text=updateTime.strftime("下次更新時間:%Y年%m月%d日--%H時%M分%S秒"))
        self.comboBox.config(values=cityNames)
        self.comboBox.current(0) #預設選擇第一位


    def combobox_selected(self,event):
        widget = event.widget
        comboBoxIndex = widget.current()
        print(comboBoxIndex)

if __name__ == "__main__":
    window = Window()
    window.mainloop()
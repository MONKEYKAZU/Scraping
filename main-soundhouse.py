# amazon@p1-com.com
import os,sys
import time
import pandas as pd
from selenium import webdriver
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

def Exit():
    sys.exit()

class clicked:
    # ファイル指定の関数
    def filedialog_clicked(self):#iFilePath1
        fTyp = [("アプリケーション", "*.exe")]
        iFile = os.path.abspath(os.path.dirname(__file__))
        #ファイルダイアログを表示
        iFilePath1 = filedialog.askopenfilename(filetype = fTyp, initialdir = iFile)
        entry1.set(iFilePath1)

def go():
    webdriverfile = entry1.get()
    driver = webdriver.Chrome(executable_path=webdriverfile)
    type(driver)

    #URLを直で貼る。browser.getでwebのURLを取得する。
    driver.get('https://www.soundhouse.co.jp/')
    time.sleep(5)

    #ログイン
    login_btn = driver.find_element_by_class_name('login')
    login_btn.click()
    time.sleep(5)

    """
    ログイン入力部
    """
    #id名はinput id="~~"みたいな所の~~の部分
    usr_name_el = driver.find_element_by_name('user_id')
    #ユーザー名を入力する
    usr_name_el.send_keys('e-mail入力')
    time.sleep(1)
    #id名はinput id="~~"みたいな所の~~の部分
    usr_name_el = driver.find_element_by_name('password')
    #ユーザー名を入力する
    usr_name_el.send_keys('パスワード入力')
    #ボタンのクリック
    Clicklog = driver.find_element_by_xpath('//*[@id="globalContents"]/div/div[3]/form/input[3]')
    Clicklog.click()
    time.sleep(5)

    """
    半年間の購入履歴を取得する
    """
    dates = []
    sums = []
    links = []
    names =[]
    #マイページを押下
    mypage_btn = driver.find_element_by_class_name('mypage')
    mypage_btn.click()
    time.sleep(3)
    #購入履歴を押下
    buy = driver.find_element_by_xpath('//*[@id="mypageMenu"]/li[1]/a')
    buy.click()
    time.sleep(5)
    while True:
        try:
            # すべてのページの購入履歴を取得するプログラムを書く
            count = 0
            Invoices = driver.find_elements_by_class_name('orderBox')
            print(len(Invoices))
            for invoice in range(len(Invoices)):
                INvo = driver.find_elements_by_class_name('orderBox')
                voice = INvo[count]
                #日付けを取得
                year_link = voice.find_element_by_class_name('date')
                month = year_link.find_element_by_tag_name('span')
                print(month.text)
                dates.append(month.text)
                print(dates)
                #合計値を取得
                sum_link = voice.find_element_by_class_name('total')
                goukei = sum_link.find_element_by_tag_name('span')
                print(goukei.text)
                sums.append(goukei.text)
                print(sums)
                #請求書を取得
                http = 'https://www.soundhouse.co.jp/customers/order_history/invoice/?ono='
                link = voice.find_element_by_class_name('number')
                aTag = link.find_element_by_tag_name('span')
                print(aTag.text)
                url_find = http + aTag.text
                print(url_find)
                links.append(url_find)
                print(links)
                #商品名を取得
                Name = voice.find_element_by_class_name('name')
                Tag = Name.find_element_by_tag_name("a")
                print(Tag.text)
                names.append(Tag.text)
                print(names)
                count+=1
                
            driver.find_element_by_link_text('»').click()

        except:
            info = {'日付':dates,'金額':sums,'請求書URL':links,'商品名':names}
            print(info)
            df = pd.DataFrame(info)
            df.to_csv('soundhouse.csv',index=False,encoding='utf-8')
            break

    driver.close()


"""
メイン
"""
clickedclass = clicked()
# rootの作成
root = Tk()
root.title("実行選択")
# Frame1の作成
frame1 = ttk.Frame(root, padding=5)
frame1.grid(row=0, column=0, sticky=E)
# 「ファイル参照」ラベルの作成
IFileLabel = ttk.Label(frame1, text="webdriver選択")
IFileLabel.pack(side='top')
# 「ファイル参照」エントリーの作成
entry1 = StringVar()
IFileEntry = ttk.Entry(frame1, textvariable=entry1, width=30)
IFileEntry.pack(fill = 'x',side=LEFT)
# 「ファイル参照」ボタンの作成
IFileButton = ttk.Button(frame1, text="参照", command=clickedclass.filedialog_clicked)
IFileButton.pack(side=LEFT)

# Frame3の作成
frame3 = ttk.Frame(root, padding=10)
frame3.grid(row=12,column=0,sticky=W+E)

# 実行ボタンの設置
start_button = ttk.Button(frame3, text="実行", command=lambda:go())
start_button.pack(side=LEFT)

#実行ボタン
close_button = ttk.Button(frame3, text='閉じる', command = lambda:Exit())
close_button.pack(side=RIGHT)

root.mainloop()
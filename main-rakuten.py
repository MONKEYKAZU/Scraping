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
    driver.get('https://www.rakuten.co.jp/')
    time.sleep(5)

    #ログイン
    login_btn = driver.find_element_by_xpath('//*[@id="wrapper"]/div[7]/div/ul[2]/li[2]/button')
    login_btn.click()
    time.sleep(5)

    """
    ログイン入力部
    """
    #id名はinput id="~~"みたいな所の~~の部分
    usr_name_el = driver.find_element_by_name('u')
    #ユーザー名を入力する
    usr_name_el.send_keys('e-mail入力')
    time.sleep(1)
    #id名はinput id="~~"みたいな所の~~の部分
    usr_name_el = driver.find_element_by_name('p')
    #ユーザー名を入力する
    usr_name_el.send_keys('パスワード入力')
    #ボタンのクリック
    Clicklog = driver.find_element_by_name('submit')
    Clicklog.click()
    time.sleep(5)
    """
    購入履歴
    """
    #日付け
    dates = []
    #合計値
    sums = []
    #送料
    sents = []
    #金額
    prices = []
    #請求書リンク
    links = []
    #商品名
    names =[]

    buy_btn = driver.find_element_by_xpath('//*[@id="wrapper"]/div[5]/div/div/div/div[3]/div[3]/a')
    buy_btn.click()
    time.sleep(5)

    # すべてのページの購入履歴を取得するプログラムを書く
    pagecount = 1
    count = 0
    Invoices = driver.find_elements_by_class_name('oDrListGrid')
    print(len(Invoices))
    for invoice in range(len(Invoices)):
        time.sleep(3)
        voice = driver.find_elements_by_class_name('oDrDetailList')
        url_link = voice[count].find_element_by_tag_name('a').get_attribute("href")
        #新しいタブを作成
        driver.execute_script("window.open()")
        #新しいタブに切り替える
        driver.switch_to.window(driver.window_handles[pagecount])
        driver.get(url_link)
        time.sleep(3)
        print(count)

        #日付けを取得
        year_link = driver.find_element_by_class_name('orderDate')
        print(year_link.text)
        dates.append(year_link.text)
        print(dates)
        #商品名を取得
        Name = driver.find_element_by_class_name('prodName')
        Tag = Name.find_element_by_tag_name("a")
        print(Tag.text)
        names.append(Tag.text)
        print(names)

        #値段を取得
        prices_link = driver.find_element_by_class_name('subTot')
        print(prices_link.text)
        prices.append(prices_link.text)
        print(prices)
        
        sents_link = driver.find_element_by_class_name('ship')
        print(sents_link.text)
        sents.append(sents_link.text)
        print(sents)

        sums_link = driver.find_element_by_class_name('netTot')
        print(sums_link.text)
        sums.append(sums_link.text)
        print(sums)

        #請求書を取得
        link = driver.find_element_by_class_name('orderReceiptLink')
        aTag = link.find_element_by_tag_name('a')
        url_find = aTag.get_attribute("href")
        print(url_find)
        links.append(url_find)
        print(links)
        count+=1
        pagecount+=1
        #前のタブに切り替え
        driver.switch_to.window(driver.window_handles[0])
        driver.execute_script('window.scroll(0,1000000);')

    info = {'日付':dates,'合計金額':sums,'商品金額':prices,'送料':sents,'請求書URL':links,'商品名':names}
    print(info)
    df = pd.DataFrame(info)
    df.to_csv('rakuten.csv',index=False,encoding='utf-8')

    driver.quit()

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
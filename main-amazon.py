import 
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

#pythonファイルがある場所にダウンロードするとpythonファイルはPATHが通っているので下の"executable"を使わなくていい
#executable_path="フルパス"
driver = webdriver.Chrome()
type(driver)

#URLを直で貼る。browser.getでwebのURLを取得する。
driver.get('https://www.amazon.co.jp/')

#ログイン
login_btn = driver.find_element_by_id('nav-link-accountList')
login_btn.click()
time.sleep(1)
"""
email入力部
"""
#id名はinput id="~~"みたいな所の~~の部分
usr_name_el = driver.find_element_by_id('ap_email')
#ユーザー名を入力する
usr_name_el.send_keys('e-mail入力')
#ボタンのクリック
driver.find_element_by_id('continue').click()

"""
パスワード入力部
"""
#5秒待機
time.sleep(1)
#id名はinput id="~~"みたいな所の~~の部分
usr_name_el = driver.find_element_by_id('ap_password')
#ユーザー名を入力する
usr_name_el.send_keys('パスワード入力')
#ボタンのクリック
# url_name_el.submit()
driver.find_element_by_id('signInSubmit').click()

"""
注文履歴まで飛ぶ
"""
#5秒待機
time.sleep(1)
#id名はinput id="~~"みたいな所の~~の部分
usr_name_el = driver.find_element_by_id('nav-link-accountList')
driver.find_element_by_id('nav-link-accountList').click()
# #注文履歴を押す
usr_name_el = driver.find_element_by_class_name('a-box-inner')
driver.find_element_by_class_name('a-box-inner').click()


#年度のドロップダウンリストを探す
year = driver.find_element_by_class_name('a-dropdown-container')
time.sleep(5)
year.click()
time.sleep(2)

# 選択したい年を選ぶ
year_link=driver.find_element_by_link_text('2020年')
year_link.click()
time.sleep(2)
"""
一つ一つの領収書を別画面に表示
"""
# すべてのページで行う
while True:
    main_handle = driver.current_window_handle
    receipt_url = []
    try:
        count = 0
        #ページ内の領収書の数を数える
        receipt_links = driver.find_elements_by_link_text('領収書等')
        receipt = len(receipt_links)
        print(receipt)
        for receipt_link in range(receipt):
            #textはlistで値が返ってくるのでclickの対称では無かった。
            #find_elements_by_link_textはダメ！！クリックできない
            receipt_links = driver.find_elements_by_link_text('領収書等')
            print(count)
            #countでクリックする領収書をかぶらないようにる。
            #これがないとずっと最初の領収書をクリックし続ける
            receipt_links[count].click()
            #タッチしてウィンドウが開くタイプのやつは、画面上にないとクリックできないのでタッチするところまで見えるようにスクロールする
            driver.execute_script('window.scroll(0,1000000);')
            time.sleep(1)
            #hrefのurlを取得する
            receipt_purchase_link = driver.find_element_by_link_text('領収書／購入明細書')
            receipt_link_element2 = receipt_purchase_link.get_attribute("href")
            print(receipt_link_element2)
            receipt_url.append(receipt_link_element2)

            # # クリック前のハンドルリスト
            handles_before = driver.window_handles

            # 新しいタブで開く
            actions = ActionChains(driver)
            actions.key_down(Keys.CONTROL)
            actions.click(receipt_purchase_link)
            actions.perform()

            # 新しいタブが開くまで最大30秒待機
            WebDriverWait(driver, 30).until(lambda a: len(driver.window_handles) > len(handles_before))

            # クリック後のハンドルリスト
            handles_after = driver.window_handles
            print("完了",count)
            count+=1

        # 次へのボタンが押せなくなった時点で終了
        driver.find_element_by_class_name('a-last').find_element_by_tag_name('a')
        driver.find_element_by_class_name('a-last').click()
        # driver.switch_to.window(driver.window_handles[-1])
    except:
        df = pd.DataFrame({'領収書のurl':[receipt_url]})
        print(df)
        breakpy




"""
終わったら閉じる
"""
driver.close()
driver.quit()
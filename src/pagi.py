from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from config import CHROME_PROFILE_PATH
import pyperclip
import sys
import time

try:
    if sys.argv[1]:
        with open(sys.argv[1], 'r', encoding='utf8') as f:
            kontaks = [kontak.strip() for kontak in f.readlines()]
except IndexError:
    print('Sertakan daftar kontak.')

options = webdriver.ChromeOptions()
options.add_argument(CHROME_PROFILE_PATH)

# Starting chrome as warming up so it will not slow when the broadcast starts
s = Service('/Users/asyaky/chromedriver/chromedriver')
browser = webdriver.Chrome(service=s, options=options)
browser.maximize_window()
browser.get('https://web.whatsapp.com/')
search_xpath = '//div[@contenteditable="true"][@data-testid="chat-list-search"]'
search_box = WebDriverWait(browser, 500).until(
    EC.presence_of_element_located((By.XPATH, search_xpath))
)
time.sleep(3)
browser.quit()
time.sleep(15)

s = Service('/Users/asyaky/chromedriver/chromedriver')
browser = webdriver.Chrome(service=s, options=options)
browser.maximize_window()
browser.get('https://web.whatsapp.com/')

jumlah = 0
admin = "Muhammad Sidik Asyaky"

for kontak in kontaks:
    t = time.localtime()
    waktu = time.strftime("%H:%M", t)

    msg = "Mohon izin, Bapak/Ibu " + kontak + ". \n*Saat ini sudah pukul " + waktu +" WIB.* Mohon *segera* melaksanakan *presensi masuk kerja*. Jika masih dalam perjalanan dan kemungkinan akan *terlambat* silahkan ajukan *izin terlambat* masuk kerja. \n\n*Pesan ini merupakan pesan broadcast yang dikirim ke seluruh pegawai demi meningkatkan disiplin PNS Disperkim. Abaikan jika sudah melaksanakan presensi. Hatur nuhun."

    search_xpath = '//div[@contenteditable="true"][@data-testid="chat-list-search"]'

    search_box = WebDriverWait(browser, 500).until(
        EC.presence_of_element_located((By.XPATH, search_xpath))
    )

    search_box.clear()

    pyperclip.copy(kontak)

    search_box.send_keys(Keys.SHIFT, Keys.INSERT)  # Keys.CONTROL + "v"

    time.sleep(1)

    try:
        kontak_xpath = f'//span[@title="{kontak}"]'
        kontak_title = browser.find_element(By.XPATH, kontak_xpath)

        kontak_title.click()

    except NoSuchElementException:
        # Kirim kontak yang tidak terdaftar ke admin
        search_xpath = '//div[@contenteditable="true"][@data-testid="chat-list-search"]'

        search_box = WebDriverWait(browser, 500).until(
            EC.presence_of_element_located((By.XPATH, search_xpath))
        )

        search_box.clear()

        pyperclip.copy(admin)

        search_box.send_keys(Keys.SHIFT, Keys.INSERT)

        time.sleep(1)

        kontak_xpath = f'//span[@title="{admin}"]'
        kontak_title = browser.find_element(By.XPATH, kontak_xpath)

        kontak_title.click()

        time.sleep(1)

        input_xpath = '//div[@contenteditable="true"][@data-testid="conversation-compose-box-input"]'
        input_box = browser.find_element(By.XPATH, input_xpath)

        msgTidakDitemukan = "Kontak " + kontak + " tidak ditemukan"

        pyperclip.copy(msgTidakDitemukan)
        input_box.send_keys(Keys.SHIFT, Keys.INSERT)
        input_box.send_keys(Keys.ENTER)

        time.sleep(1)

        continue

    time.sleep(1)

    input_xpath = '//div[@contenteditable="true"][@data-testid="conversation-compose-box-input"]'
    input_box = browser.find_element(By.XPATH, input_xpath)

    pyperclip.copy(msg)
    input_box.send_keys(Keys.SHIFT, Keys.INSERT)
    input_box.send_keys(Keys.ENTER)

    jumlah = jumlah + 1

    time.sleep(1)

# Kirim jumlah ke admin
search_xpath = '//div[@contenteditable="true"][@data-testid="chat-list-search"]'

search_box = WebDriverWait(browser, 500).until(
    EC.presence_of_element_located((By.XPATH, search_xpath))
)

search_box.clear()

pyperclip.copy(admin)

search_box.send_keys(Keys.SHIFT, Keys.INSERT)  # Keys.CONTROL + "v"

time.sleep(1)

kontak_xpath = f'//span[@title="{admin}"]'
kontak_title = browser.find_element(By.XPATH, kontak_xpath)

kontak_title.click()

time.sleep(1)

input_xpath = '//div[@contenteditable="true"][@data-testid="conversation-compose-box-input"]'
input_box = browser.find_element(By.XPATH, input_xpath)

total = jumlah-1
msgAkhir = "Total pegawai " + str(total)

pyperclip.copy(msgAkhir)
input_box.send_keys(Keys.SHIFT, Keys.INSERT)  # Keys.CONTROL + "v"
input_box.send_keys(Keys.ENTER)

time.sleep(2)
browser.quit()
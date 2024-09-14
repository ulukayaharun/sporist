from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def run(tc_kimlik:str, sifre:str, tesis:str, saha:str):
    driver = webdriver.Chrome()
    driver.maximize_window()

    login_to_website(driver, tc_kimlik, sifre)
    select_tesis_and_saha(driver, tesis, saha)
    make_reservations(driver)
    
    sleep(100)
    driver.quit()

def login_to_website(driver, tc_kimlik, sifre):
    driver.get("https://online.spor.istanbul/uyegiris")
    sleep(0.5)
    driver.find_element(By.ID, "txtTCPasaport").send_keys(tc_kimlik)
    driver.find_element(By.ID, "txtSifre").send_keys(sifre)
    driver.find_element(By.ID, "txtSifre").send_keys(Keys.ENTER)

def close_modal_if_exists(driver):
    try:
        close_modal = driver.find_element(By.ID, "closeModal")
        if close_modal.is_displayed():
            close_modal.click()
        else:
            pass
    except Exception as e:
        print(f"Modal kapatılamadı: {e}")

def select_tesis_and_saha(driver, tesis, saha):
    close_modal_if_exists(driver)

    driver.find_element(By.ID , "rblKiralik").click()


    find_and_click(driver, "/html/body/form/section[1]/div/div/div/div/div/div/div/div[1]/div/div[2]/div[1]/div/div/div/span/span[1]/span")
    enter_text_and_submit(driver, "/html/body/span/span/span[1]/input", "FUTBOL")

    find_and_click(driver, "/html/body/form/section[1]/div/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/div/div/div/span/span[1]/span")
    enter_text_and_submit(driver, "/html/body/span/span/span[1]/input", tesis)

    driver.find_element(By.ID, "pageContent_ucUrunArama_lbtnSKAra").click()

    close_modal_if_exists(driver)

    #burda sorun çekiyorum sahayı bazen seçmiyor zorlama kullanmış oldum.

    find_and_click(driver, "/html/body/form/div[3]/div[3]/div[1]/div/div/div/div/div[3]/span[2]/span[1]/span")
    enter_text_and_submit(driver, "/html/body/span/span/span[1]/input", saha)
    
    close_modal_if_exists(driver)

    find_and_click(driver, "/html/body/form/div[3]/div[3]/div[1]/div/div/div/div/div[3]/span[2]/span[1]/span")
    enter_text_and_submit(driver, "/html/body/span/span/span[1]/input", saha)

    close_modal_if_exists(driver)

def find_and_click(driver, xpath):
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    element.click()
    

def enter_text_and_submit(driver, xpath, text):
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    element.send_keys(text)
    element.send_keys(Keys.ENTER)
    

def make_reservations(driver):
    found = False
    sleep(0.5)
    days = driver.find_elements(By.XPATH, "//*[@id='pageContent_Div1']")
    days.reverse()
    
    for day in days:
        if found:
            break

        time_slots = day.find_elements(By.XPATH, ".//span[contains(text(), '22:') or contains(text(), '21:') or contains(text(), '20:') or contains(text(), '19:')]")

        
        for slot in time_slots:
            if found:
                break

            try:
                reservation_button = slot.find_element(By.XPATH, ".//following-sibling::a[contains(@title, 'Rezervasyon')]")
                if reservation_button:
                    reservation_button.click()
                    reservation_button.send_keys(Keys.ENTER)

                    found = True
                    sleep(0.5)
                    
            except Exception as e:
                print(f"Rezervasyon yapılamadı: {e}")
                continue

# Kodunuzu çalıştırmak için:
run("14099433250", "59214860", "MALTEPE SAHİL SPOR TESİSİ", "HALI SAHA 2")


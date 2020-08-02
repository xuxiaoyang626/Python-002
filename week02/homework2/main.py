from selenium import webdriver
import time

try:
    browser = webdriver.Chrome()
    
    browser.get('https://shimo.im/login?from=home')
    time.sleep(1)

    browser.find_element_by_name('mobileOrEmail').send_keys('15055495@qq.com')
    browser.find_element_by_name('password').send_keys('test123test456')
    time.sleep(1)

    browser.find_element_by_xpath('//button[text()="立即登录"]').click()

    cookies = browser.get_cookies()
    print(cookies)
    time.sleep(3)

except Exception as e:
    print(e)
finally:
    browser.close()
    
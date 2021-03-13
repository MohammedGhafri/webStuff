from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
# driver = webdriver.Chrome(ChromeDriverManager().install())
# driver = webdriver.Firefox()
# print (driver.current_url)
#####
# driver_2 = webdriver.Chrome()

driver_3 = webdriver.Chrome('facebook.com')
print (driver_3.current_url)
# print(webdriver.__dict__)
# print(webdriver.__dict__)


# import win32ui

# def WindowExists(classname):
#     try:
#         win32ui.FindWindow(classname, None)
#     except win32ui.error:
#         return False
#     else:
#         return True

# if WindowExists("DropboxTrayIcon"):
#     print "Dropbox is running, sir."
# else:
#     print "Dropbox is running..... not."
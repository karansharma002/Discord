from bs4 import BeautifulSoup as bs4
import requests
from alive_progress import alive_bar
from tkinter.filedialog import askopenfilename
from tkinter import *
def scraper():
    root = Tk()
    root.withdraw()
    filename = askopenfilename()
    with_captcha = []
    without_captcha = []
    file = open(filename, "r")

    line_count = 0

    for line in file:

        if line != "\n":

            line_count += 1

    file.close()
    print('---------- ANALYZING THE URLS ---------')
    with open(filename) as f:
        with alive_bar(line_count) as bar:
            for line in f:
                response = requests.get(line)
                soup = bs4(response.content,'html.parser')
                is_captcha_on_page = soup.find("div", id="recaptcha") is not None
                if is_captcha_on_page == True:
                    with_captcha.append(line)
                else:
                    without_captcha.append(line)
                bar()
    
    print('------------------- EXPORTING THE DATA ------------------')
    if not with_captcha == []:
        with open('Captcha_Detected_Sites.txt', 'w') as f:
            for item in with_captcha:
                f.write("%s\n" % item)
            
    
    if not without_captcha == []:
        with open('Normal Sites.txt', 'w') as f:
            for item in without_captcha:
                f.write("%s\n" % item)
    
    print('------------------- DATA SAVED ----------------------')


scraper()
        


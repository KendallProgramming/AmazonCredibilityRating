from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json, ast, os, sys, chardet


def stripUrl(url:str) -> str:
    lastSlash = url.rfind("/")
    if lastSlash == -1:
        return False
    else:
        parse = urlparse(url)
        if parse.scheme != "https":
            return False
        else:
            webnoslash = parse.netloc
            index = webnoslash.find(".")
            webnoslash = webnoslash[index+1:]
    return webnoslash

def checkUrl(url: str) -> bool:
    websiteList = ["amazon.com", "Target.com"]
    lastSlash = url.rfind("/")
    if lastSlash == -1:
        return False
    else:
        parse = urlparse(url)
        if parse.scheme != "https":
            return False
        else:
            webnoslash = parse.netloc
            index = webnoslash.find(".")
            webnoslash = webnoslash[index+1:]
            if webnoslash not in websiteList:
                return [False, None]
            elif webnoslash in websiteList[0]:
                return [True, "Amazon"]
            else:
                return [True, "Target"]
        
def checkProductName(url: str, soup: BeautifulSoup, product:str) -> bool:
    global alreadyChecked
    if alreadyChecked:
        return product
    
    check = input(f"Is your product {product}? (Y/N) \n")
    check = check.capitalize()
    while check != "Y" and check != "N":
        print("Invalid")
        check = input(f"Is your product {product}? (Y/N) \n")
    if check == "Y":
        alreadyChecked = True
        check = True
    else:
        alreadyChecked = True
        check = False
    return check 

def getActualDate(date: str, form:str) -> str:
    monthDict={"01":'Jan', "02":'Feb', "03":'Mar', "04":'Apr', "05":'May', "06":'Jun', "07":'Jul', "08":'Aug', "09":'Sep', "10":'Oct', "11":'Nov', "12":'Dec'}
    nums = [0,1,2,3,4,5,6,7,8,9]
    fstr = ""
    months = list(monthDict.values())
    monthDict = {y: x for x, y in monthDict.items()}
    for item in months:
        if item in date:
            monthNum = monthDict[item]

    day = date.split(" ")[1].strip(",")
    if len(day) != 2:
        day = "0" + str(day)
    else:
        day = str(day)
    year = date.split(" ")[2]
    year = str(year)
    
    if form == "MMDDYYYY":
        fstr = str(monthNum) + day + str(year)
    elif form == "DDMMYYYY":
        fstr = str(day) + str(monthNum) + str(year)
    else:
        raise "Error: Form not in possible forms"
    return fstr


def getReview(data:list,ind:int=0) -> dict:
    return data[ind]


def stripSpecials(string:str) -> str:
    retString = "".join(ch for ch in string if ch.isalnum())
    return retString
            
            
def fixBody(string:str) -> str:
    ind = string.find("review_body")+11
    string = string[ind:]
    ind2 = string.find(', "amount_')
    string = string[:ind]
    string = string.strip("'")
    string = string.strip('"')
    return string

def getDataFromLogging(name:str) -> dict | str: #FINALLY WORKNIG AKL FJDSOIFAHDSOIF UADSHFDSIFJDS FHNKDLFDASJLKF AL FDJSAKFLDAFJWOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    with open("Logging.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            data = ast.literal_eval(line)
            prod:str = data[0]["review_product"]
            if prod == name:
                return data
            else:
                continue
        
    return "Unknown product " + name
    

#test body
#mac uses "os.system("clear")" to clear the screen, windows uses "os.system("cls")" to clear the screen. get if user is on mac or windows and decide which to use
def clearTerminal() -> None:
    mow = str(sys.platform)
    if "win" in mow[:3]:
        mow = "windows"
    else:
        #TODO: make a check for mac as well
        mow = "mac"

    if mow == "mac":
        os.system("clear")
    elif  mow  == "windows":
        os.system("cls")
    else:
        return None

def getCurLine() -> int:
    with open("Logging.txt", "r") as f:
        return len(f.readlines())
            
            
def detectEncoding() -> str:
    with open('Logging.txt', 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        return encoding


def fixEncoding() -> None:
    encoding = detectEncoding()
    if str(encoding) != "utf-8":
        try:
            with open("Logging.txt", 'r', encoding=detectEncoding()) as ascii_file:
                content = ascii_file.read()

            # Write the content back to the same file with UTF-8 encoding
            with open("Logging.txt", 'w', encoding='utf-8') as utf8_file:
                utf8_file.write(content)
        except FileNotFoundError:
            return "Failed"
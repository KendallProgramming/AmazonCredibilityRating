import  requests, ast
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
import re
from BaseFunctions import getActualDate, checkProductName, stripUrl, checkUrl, clearTerminal, getCurLine, fixEncoding
#credit: https://stackoverflow.com/questions/77549293/python-beatifulsoup-only-scrapes-the-1st-page-of-amazon-reviews-someone-knows-h


#This class doesn't work, kept in here for future expansion
class AmazonSearchFail:
    def __init__(self, url):
        self.url = url
        
    
        
    
    def getReviewDataAmazon(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")
        

        
        product = findProduct(self.url)
        check = checkProductName(self.url, soup, product)
        if check:
            amountReviews = amntReviews(soup)
            if amountReviews > 100:
                titles = []
                texts = []
                dates = []
                stars = []
                lengths = []

                revSection = review_section(soup)
                totalAvgstars = avgStars(soup)
                
                revStars = review_stars(soup)        
                for st in revStars:
                    stars.append(addListStars(st))

                revText = review_texts(soup)
                for t in revText:
                    texts.append(addListText(t))
                    for i in texts:
                        if i == None:
                            texts.remove(i)
                    
                revHeader = review_headers(soup)
                for row in revHeader:
                    titles.append(addListTitle(row))
       
                revDates = review_dates(soup)
                for date in revDates:
                    dates.append(addListDate(date, "MMDDYYYY"))
                    
                revLens = review_lens(soup, texts)
                for len in revLens:
                    lengths.append(addListLength(len))
            
            # print(revSection)
            # print(product)
            else:
                print("Invalid")
                #raise error, too few reviews

        else:
            # URL = input("Paste web name: ")
            pass
        # print(revHeader)

        
            

        print(f"titles = {titles} \n")
        print(f"Texts = {texts} \n")
        print(f"dates = {dates} \n")
        print(f"stars = {stars}\n")
        print(f"Lens = {lengths}")
        

def amntReviews(soup: BeautifulSoup):
    line =  str(soup.find(
        "span", {"id": "acrCustomerReviewText",
                 "class": "a-size-base"}
    ))
    ind = line.find('">')
    line = line[ind+2:]
    ind2 = line.find("ratings")
    retVal = int(line[:ind2-1].replace(",", ""))
    return retVal

def review_stars(soup: BeautifulSoup):
    return soup.find_all(
        "i", {
            "data-hook": "review-star-rating"
              }
    )

def review_dates(soup: BeautifulSoup):
    return soup.find_all(
        "span", {"class": "a-size-base a-color-secondary review-date"},
        )

def review_headers(soup: BeautifulSoup):
    return soup.find_all(
            "a",
            {
                "class": "a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold"
            },
        )

def review_texts(soup: BeautifulSoup): 
        return soup.find_all(
        "span", {"class": "a-size-base review-text"}
    )

def findProduct(url:str) -> str:
    webName = stripUrl(url)
    web2 = url.split("/")
    index = 0
    ret_val = ""
    for item in web2:
        if item == "www.amazon.com":
            prod = web2[index+1]
            prod = prod.split("-")
            if type(prod) == list:
                for w in prod:
                    ret_val = "{} {}".format(ret_val, w)
            
        index +=1
    return ret_val[1:]

def avgStars(soup: BeautifulSoup):
    return soup.find("span", {"class": "a-icon-alt"}).get_text()         

def formatReview(revDate:str, revTitle:str,revProd:str, revLen:int, revStars:int, revBody:str, amntReviews:int):
    return {
        "review_product": revProd,
        "review_title": revTitle,
        "review_stars": revStars,
        "review_date": revDate,
        "review_length": revLen,
        "review_body": revBody,
        "amount_reviews": amntReviews
    }

def review_lens(revTexts:list) -> list:
    lis = []
    for i in revTexts:
        lis.append(i)
    return lis
        
def review_section(soup: BeautifulSoup):
    return soup.find_all("div", {
            "class": "a-section celwidget"
        })

def addListTitle(row):
    row = str(row)
    row = row.split("\n")
    for item in row:
    # print(f"item = {item}") 
        if "<span>" in item:
            # print(f"This works {item}")
            item = item.strip("<span>")
            item = item.strip("</span>")
            # print(f"test {item}")
            return item

def addListText(t):
    texts = str(t)
    retVal = ""
    texts = texts.split("\n")
    for text in texts:
        if "<span>" in text:
            text = text.replace("<span>", "")
            text = text.replace("</span>", "")
            if len(text) <= 1:
                retVal = None
            else:
                retVal = text
    # print(f"ret = {retVal}\t len = {len(retVal)}")
    if "<br" in retVal or "/br" in retVal:
        retVal = retVal.replace("<br", "")
        retVal = retVal.replace("</", "")
        retVal = retVal.replace("/>", "")
    # print(f"ret = {retVal}\t len = {len(retVal)}")
    return retVal

def addListDate(date, form:str):
    dates = str(date)
    dates = dates.split("\n")
    for date in dates:
        if "<span" in date:
            date = date.strip("<span")
            date = date.replace("</span>", "")
            index1 = date.find("Reviewed")
            date = date[index1:]
            index2 = date.find("on")
            date = date[index2+3:]
            date = getActualDate(date, form)
            return date[:len(date)-1]

def addListStars(star):
    stars = str(star)
    stars = stars.split("\n")
    for star in stars:
        if "a-star-" in star:
            # print(star)
            ind1 = star.find("a-s")
            star = star[ind1:]
            ind2 = star.find("rev")
            star = star[:ind2]
            star = star[-2]
            if int(star) == 5:
                return 5
            if int(star) == 4:
                return 4
            if int(star) == 3:
                return 3
            if int(star) == 2:
                return 2
            if int(star) == 1:
                return 1

def addListLength(txt):
    lens = str(txt)
    lens = lens.split("\n")
    for txt in lens:
        return len(txt)
      
def addListName(txt) -> str:
    text = str(txt)
    ind = text.find('name">') + 6
    text = text[ind:]
    ind = text.find('<')
    text = text[:ind]
    return text
    
def findAsin(url:str) -> str:
    ind1 = url.find("/dp")
    if ind1 == -1:
        ind1 = url.find("product-reviews")
        if ind1 == -1:
            return "Invalid"
        url = url[ind1+16]
    else:
        url = url[ind1+4:]
    ind = url.find("/")
    url = url[:ind]
    return url

def addListStar(txt) -> str:
    text = str(txt)
    ind = text.find('a-icon-alt') + 11
    text = text[ind:]
    ind = text.find('s<')
    text = text[1:ind]
    star = float(text[:3])
    return star

# def findPrice(soup: BeautifulSoup, url):
#     txt = str(soup.find("span", {"class": "a-price aok-align-center reinventPricePriceToPayMargin priceToPay"}))
#     print(f" txt = {txt}")
#     wholeind = re.findall('\<span class\="a-price-whole"\>', txt)
#     print(wholeind)
#     decind = re.findall('\<span class\="a-price-fraction"\>', txt)
#     wholeindd = txt.find(wholeind[0])
#     txt = txt[wholeindd:]
#     whole = txt[len(wholeind)+27:]
#     inddd = whole.find("<")
#     whole = int(whole[:inddd])
    
#     decimal = txt[len(decind):]
#     decimalInd = decimal.find("<")+76
#     decimal = decimal[decimalInd:]
#     decimalIndd = decimal.find("<")
#     decimal = decimal[:decimalIndd]

#     retVal = "{}.{}".format(whole, decimal)
#     return float(retVal)
    
#a-price-whole
    

class AmazonSearch:
    def __init__(self, product):
        self.url = "https://www.amazon.com/hz/reviews-render/ajax/reviews/get/ref=cm_cr_arp_d_paging_btm_next_2"
        self.productUrl = product
        self.productName = findProduct(self.productUrl)
        self.asin = findAsin(product)
        self.avgStars = avgStars(soup=BeautifulSoup(requests.get(self.productUrl).content, "html.parser"))
        self.amntReviews = amntReviews(soup=BeautifulSoup(requests.get(self.productUrl).content, "html.parser"))
        # self.price = findPrice(soup=BeautifulSoup(requests.get(self.productUrl).content, "html.parser"),url=self.productUrl)
        self.bodies = []
        self.headers = []
        self.dates = []
        self.ratings = []
        self.reviewers = []
        self.lenBodies = []
        self.retList = []
        self.titles = []
        self.mainRan = False
        
    def main(self):
        headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"
        }       

        payload = {
            "sortBy": "",
            "reviewerType": "all_reviews",
            "formatType": "",
            "mediaType": "",
            "filterByStar": "",
            "filterByAge": "",
            "pageNumber": "1",
            "filterByLanguage": "",
            "filterByKeyword": "",
            "shouldAppend": "undefined",
            "deviceType": "desktop",
            "canShowIntHeader": "undefined",
            "reftag": "cm_cr_arp_d_paging_btm_next_2",
            "pageSize": "10",
            "asin": self.asin,  # <--- change product asin here
            "scope": "reviewsAjax0",
        }


        for page in range(1, 4):  # <--- change number of pages here
            payload["pageNumber"] = page

            t = requests.post(self.url, data=payload, headers=headers).text
            self.check = t

            soup = BeautifulSoup(
                "\n".join(map(ast.literal_eval, re.findall(r'"<div id=.*?</div>"', t))),
                "html.parser",
            )
            
            for r in soup.select('[data-hook="review"]'):
                revName = r.find_all("span", {"class": "a-profile-name"}) 
                revText = r.find_all("span", {"class": "a-size-base review-text review-text-content"}) 
                revStar = r.find_all("a", {"class": "a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold"}) #temporarily remove, fix later TODO: fix
                revDates = r.find_all("span", {"class": "a-size-base a-color-secondary review-date"})
                revTitles = r.find_all("a", {"class": "a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold"})

                
                self.reviewers.append(revName)
                self.bodies.append(revText)
                self.ratings.append(revStar)
                self.dates.append(revDates)
                self.titles.append(revTitles)
                
        for i in range(len(self.reviewers)):
            self.reviewers[i] = addListName(self.reviewers[i])
            
        for i in range(len(self.bodies)):
            self.bodies[i] = addListText(self.bodies[i])
            
        for i in range(len(self.ratings)):
            self.ratings[i] = addListStar(self.ratings[i])
        
        for i in range(len(self.dates)):
            self.dates[i] = addListDate(self.dates[i], "MMDDYYYY")
        
        for i in range(len(self.bodies)):
            self.lenBodies.append(len(self.bodies[i]))
        
        for i in range(len(self.titles)):
            self.titles[i] = addListTitle(self.titles[i])
        
    def retData(self):
        self.mainRan = True
        """gets all the data from main function and appends it to a list. 

        Returns:
            list: formatted data, price as a string to be used to check other websites for similar prices. 
        """
        self.retList = ["" for x in range(len(self.bodies))]
        for i,thing in enumerate(self.bodies):
            self.retList[i] = formatReview(self.dates[i], self.titles[i], self.productName,
                                           self.lenBodies[i], self.ratings[i], self.bodies[i], self.amntReviews)
        
        return self.retList    
    
    def getProductName(self):
        return str(self.productName)        
        

    def logData(self):
        if self.mainRan:
            try:
                with open("Logging.txt", "r") as f1:
                    lines = f1.readlines()
                    for line in lines:
                        if line[-1] != "\n":
                            with open("Logging.txt", "a+") as f2:
                                f2.write("\n")
                        
                with open("Logging.txt" ,"a+") as f:
                    for i,thing in enumerate(self.bodies):
                        # print(f"currently logging {self.retlist[i]}")
                        if i == 0: f.write(f"[{self.retList[i]}, ")
                        elif not len(self.bodies)-1 == i: f.write(f"{self.retList[i]}, ") 
                        else: f.write(f"{self.retList[i]}]")
            except FileNotFoundError as e:
                with open("Logging.txt" ,"w+") as f:
                    for i,thing in enumerate(self.bodies):
                        # print(f"currently logging {self.retlist[i]}")
                        if i == 0: f.write(f"[{self.retList[i]}, ")
                        elif not len(self.bodies)-1 == i: f.write(f"{self.retList[i]}, ") 
                        else: f.write(f"{self.retList[i]}]")
                
    
        
    def checkProductInLogging(self):
        check = fixEncoding()
        if check != "Failed":
            try:
                with open("Logging.txt", "r") as f1:
                    lines = f1.readlines()
                if lines == []:return False
                else:
                    with open("Logging.txt", "r") as f:
                        lines = f.readlines()
                        
                        for line in lines:
                            data:list = ast.literal_eval(line)
                            prod:str = data[1]["review_product"]
                            if prod == self.productName:return True
                            else:continue
                        return False
            except FileNotFoundError as e:
                return False
        else:
                return "Error too big"


#LOTS OF TESTING BELOW

# tempUrl = "https://www.amazon.com/Kerastase-Absolu-Overnight-Recovery-Cicanuit/dp/B08L5Q6K5T/?_encoding=UTF8&pd_rd_w=mNrTP&content-id=amzn1.sym.a725c7b8-b047-4210-9584-5391d2d91b93%3Aamzn1.symc.d10b1e54-47e4-4b2a-b42d-92fe6ebbe579&pf_rd_p=a725c7b8-b047-4210-9584-5391d2d91b93&pf_rd_r=CJKDQJPW6H3CWVHY5DE0&pd_rd_wg=az9cm&pd_rd_r=89c5e0ea-5e70-4323-a924-3f54ded0827a&ref_=pd_hp_d_atf_ci_mcx_mr_hp_atf_m"
# temp = "https://www.amazon.com/Kerastase-Absolu-Overnight-Recovery-Cicanuit/product-reviews/B08L5Q6K5T/?_encoding=UTF8&pd_rd_w=mNrTP&content-id=amzn1.sym.a725c7b8-b047-4210-9584-5391d2d91b93%3Aamzn1.symc.d10b1e54-47e4-4b2a-b42d-92fe6ebbe579&pf_rd_p=a725c7b8-b047-4210-9584-5391d2d91b93&pf_rd_r=CJKDQJPW6H3CWVHY5DE0&pd_rd_wg=az9cm&pd_rd_r=89c5e0ea-5e70-4323-a924-3f54ded0827a&ref_=pd_hp_d_atf_ci_mcx_mr_hp_atf_m"
# URL = input("Paste web name: \n")

# if not checkUrl:
#     print("Invalid URL")
# else:
#     # clearTerminal()
# Amazon = AmazonSearch(URL)
# Amazon.main()
# data = Amazon.retData()
# Amazon.logData()





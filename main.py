import urllib3, requests, html, os
import tkinter as tk
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
from ast import literal_eval
import re
from datetime import date

from searchAmazon import AmazonSearch
from BaseFunctions import checkUrl, getReview,getDataFromLogging, clearTerminal

class credible:
    

    def __init__(self, data):
        self.data = data
        self.credibilityScore = 0.0
        self.tempData = None
        self.isCredible = None #True or false 
        self.credList = []
        self.amntReviews = data[len(data)-1]["amount_reviews"]
        self.reviewCheck = str
        self.productName = str
    
    def getCredScore(self,maxRange):
        """Key
        year: 0 if year diff > 10, otheriwse 10
        length: 0 if below 100 chars, 5 if below 300 chars, 10(max value) if above 300 chars
        stars: if review length <200 and star > 4, 0. Otherwise 10
        
        Args:
            maxRange (int): maxrange based on length of data
        """
        if self.amntReviews > 500:
            self.reviewCheck = "Good amount of reviews"
            temp = 0
            Invalids = 0
            for index in range(maxRange-1):
                
                self.tempData = getReview(self.data, index)
                year = int(self.tempData["review_date"][4:])
                curYear = int(date.today().strftime("%Y"))
                
                self.productName = self.tempData["review_product"]
                
                if abs(year-curYear)>10:
                    temp=0
                    self.credList.append(temp)
                else:
                    temp = 10
                    self.credList.append(temp)
                
                if self.tempData["review_length"] < 100:
                    temp = 0
                    self.credList.append(temp)
                elif self.tempData["review_length"]<300:
                    temp = 5
                    self.credList.append(temp)
                else:
                    temp = 10
                    self.credList.append(temp)
                
                if self.tempData["review_stars"] >=4.0 and self.tempData["review_length"] <=200:
                    temp = 0
                    self.credList.append(temp)
                elif self.tempData["review_stars"] >= 4.0 and self.tempData["review_length"] <=400:
                    temp = 5
                    self.credList.append(temp)
                else:
                    temp = 10
                    self.credList.append(temp)
            
            avg = sum(self.credList) / len(self.credList)
            avg = avg if avg>10 else avg+1
            self.credibilityScore = avg
        else:
            self.credibilityScore = 0.0
            self.reviewCheck = "Too few reviews"
        
        if self.reviewCheck != "Too few reviews":
            self.credibilityScore = str(round(self.credibilityScore, 2))
            
        else:
            return "Too few reviews to calculate"
        
    def returnCred(self) -> str:
        return f"\nProduct {self.productName}'s credibility score is {self.credibilityScore} out of 10"
        
    def checkUnit(self):
        print(self.data)
        

        
URL = input("Please paste your URL to your product (Amazon only as of now) below.\n")
c = checkUrl(URL)
if c[0]:
    Amazon = AmazonSearch(URL)
    if Amazon.checkProductInLogging():
        data = getDataFromLogging(Amazon.getProductName())
        # print(data)

    else:
        Amazon.main()
        Amazon.logData()
        data = Amazon.retData()
    # clearTerminal()
    new = credible(data)
    new.getCredScore(len(data))
    print(new.returnCred())
else:
    print("failure useless")
#TODO: create explanation for credibility scores 


# #!/usr/bin/env python
# # coding: utf-8

# # In[122]:


from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

class shoeScraper:
    def __init__(self):
        self.gender=""
        self.dataSet=list()

    def getPageData(self,baseUrl,page):
        params={"page":page}
        url=baseUrl
        html=requests.get(url,params=params).text
        soup=bs(html,"html.parser")
        master_list=soup.find_all("div",{"class":"bucket bucket-product-with-details bucket-product-with-attributes"})
        for element in master_list:
            self.getShoeInfo(element.select_one("a")["href"])
            
    def getShoeInfo(self,url):
        self.gender=url.split("/")[1]
        temp_dic={}
        html=requests.get("https://superbalist.com"+url).text
        soup=bs(html,"html.parser")
        temp_dic["Model"]=soup.find("h1",{"class":"headline-tight"}).text.strip()
        temp_list=soup.find_all("div",{"class":"layout-halfling"})
        temp_list.reverse()
        del temp_list[0]
        del temp_list[-1]
        for element in temp_list:
            temp_dic[element.select_one("div",{"class":"product-key"}).text.strip().replace("\n","").split()[0]]=" ".join(element.select_one("div",{"class":"product-value"}).text.strip().replace("\n","").split()[1:])
        temp_dic["Price"]=soup.find("span",{"class":"price"}).text.strip()
        temp_dic["Picture"]=soup.find("img",{"class":"bucket-img"})['src']
        temp_dic["Age"]=self.gender
        stri=""
        for size in soup.find_all("div",{"class":"sku--item"}):
            if size['class'][1]!="solOut":
                stri+=size.text.strip()+", "
        temp_dic["size"]=stri
        if temp_dic.get("Material"):
            del temp_dic["Material"]
        if temp_dic.get("Flatform"):
            del temp_dic["Flatform"]
        self.dataSet.append(temp_dic)
        
    def getCsvFile(self):
        df=pd.DataFrame(self.dataSet)
        df.to_csv("Output_1.csv",index=True)


# In[123]:

# provide the baseUrl and pageNo the scrape data from

scraper=shoeScraper()
# for i in range(10):
scraper.getPageData("https://superbalist.com/browse/women/shoes/sneakers",3)


# In[ ]:


scraper.getCsvFile()


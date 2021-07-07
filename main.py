# #!/usr/bin/env python
# # coding: utf-8

# # In[122]:


from bs4 import BeautifulSoup as bs
import time
import requests
import pandas as pd

class shoeScraper:
    def __init__(self):
        self.gender=""
        self.dataSet=list()


    def getPageData(self,baseUrl):
        params={"page":"1"}
        url=baseUrl
        html=requests.get(url,params=params).text
        soup=bs(html,"html.parser")
        totalPages=soup.find("li",{"class":"last"}).text
        totalPages=int(totalPages)
        for i in range(totalPages+1):
            params['page']=str(i+1)
            print(params['page'])
            html=requests.get(url,params=params).text
            soup=bs(html,"html.parser")
            master_list=soup.find_all("div",{"class":"bucket bucket-product-with-details bucket-product-with-attributes"})
            for j,element in enumerate(master_list):
                # time.sleep(0.5)
                print(j)
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
        placeHolders=["Colour","Style","Fabrication"]
        temp_dic["Brand"]=soup.find("a",{"class":"loud-light sub-head dampen pdp-brand"}).text.strip()
        for element in temp_list:
            if element.select_one("div",{"class":"product-key"}).text.strip().replace("\n","").split()[0] in placeHolders:
                temp_dic[element.select_one("div",{"class":"product-key"}).text.strip().replace("\n","").split()[0]]=" ".join(element.select_one("div",{"class":"product-value"}).text.strip().replace("\n","").split()[1:])
        temp_dic["Price"]=soup.find("span",{"class":"price"}).text.strip()[1:]
        temp_dic["Picture"]=soup.find("img",{"class":"bucket-img"})['src'].replace("142x206","500x720")
        temp_dic["Age"]=self.gender
        stri=""
        for size in soup.find_all("div",{"class":"sku--item"}):
            if size['class'][1]!="solOut":
                stri+=size.text.strip()+", "
        temp_dic["size"]=stri
        temp_dic["Product url"]="https://superbalist.com"+url
        if temp_dic.get("Material"):
            del temp_dic["Material"]
        if temp_dic.get("Flatform"):
            del temp_dic["Flatform"]
        self.dataSet.append(temp_dic)
        
    def getCsvFile(self):
        df=pd.DataFrame(self.dataSet)
        df.to_csv("Output_women_3.csv",index=True)


# In[123]:

# provide the baseUrl and pageNo the scrape data from

scraper=shoeScraper()
scraper.getPageData("https://superbalist.com/browse/women/shoes/sneakers")


# In[ ]:


scraper.getCsvFile()



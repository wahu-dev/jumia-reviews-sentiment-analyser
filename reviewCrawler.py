from bs4 import BeautifulSoup as soup
import requests as req
import math

class Scraper:
    def __init__(self,link):
        self.link=link
        self.connect()
        self.parse_page()
        self.get_product_details()
        self.get_feedback_section()
        self.get_ratings()
        self.get_reviews()
    def connect(self):
        self.res=req.get(self.link)
        self.status=self.res.status_code

    def parse_page(self):
        self.page=soup(self.res.content,"lxml")

    def get_product_details(self):
        self.prod_name=self.page.find("h1").text.strip()

    def get_feedback_section(self):
        for x in self.page.find_all("section"):
            try:
                if x.div["id"]=="feedback":
                    self.feed=x
                    if "product has no ratings yet" in self.feed.text:
                        self.feed_sect=False
                    else:
                        self.feed_sect=True
                else:
                    pass
            except KeyError:
                pass


    def get_ratings(self):
        if self.feed_sect:
            stars=[{i:int(x.p.text.strip("(").strip(")"))} for i,x in zip(list(reversed(range(1,6))),self.feed.find("ul").find_all("li"))]
            ratings_count=sum([list(x.values())[0] for x in stars ])
            ave_rating=sum([list(x.values())[0]*list(x.keys())[0] for x in stars ])/ratings_count
            self.rating_dict={
                "stars":stars,
                "ratings":ratings_count,
                "ave_rating":ave_rating
            }

    def get_reviews(self):
        if self.feed_sect:
            self.r_url="https://www.jumia.co.ke"+self.feed.find("header").a["href"]
            self.sku=self.r_url.strip("/").split("sku/")[1]
            r_page=soup(req.get(self.r_url).content,"lxml")
            rev_count=int(r_page.find("div",{"class":"cola"}).find("h2").text.split(" ")[-1].strip("(").strip(")"))
            page_len=math.ceil(rev_count/10)
            self.rev_list=[]
            for j in range(1,page_len+1):
                pr_url=self.r_url+f"?page={j}"
                r_page=soup(req.get(pr_url).content,"lxml")
                containers=r_page.find_all("article",{"class","-pvs"})
                for i in range(len(containers)):
                    p_stars=containers[i].find("div",{"class":"stars"}).text.split(" ")[0]
                    p_heading=containers[i].find("h3").text
                    p_rev=containers[i].find('p').text
                    p_date=containers[i].find("span",{"class","-prs"}).text
                    self.rev_list.append(
                        {
                            "Date":p_date,
                            "Stars":p_stars,
                            "Heading":p_heading,
                            "Review":p_rev
                        }
                    )




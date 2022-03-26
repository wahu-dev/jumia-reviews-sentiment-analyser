from transformers import pipeline
import pandas as pd
from reviewCrawler import Scraper
from time import time

global nlp
nlp = pipeline(
            "sentiment-analysis"
        )

class Sentiment:
    def __init__(self,X):
        self.sdf=pd.DataFrame(X.rev_list)
        self.nlp_sent= nlp
        self.wrangler()
        self.get_meandf()
        self.get_corrdf()   
    def get_sentiment(self,text): 
        resp=self.nlp_sent(text)[0]
        if resp['label']=='NEGATIVE':
            score=1-resp['score']
        else:
            score=resp['score']
        return score
    def wrangler(self):
        self.sdf.Stars=pd.to_numeric(self.sdf.Stars)
        start=time()
        self.sdf["Headings Sentiment"]=[self.get_sentiment(x) for x in self.sdf.Heading]
        print(f"headings took {time()-start} seconds")
        start=time()
        self.sdf["Reviews Sentiment"]=[self.get_sentiment(x) for x in self.sdf.Review]
        print(f"reviews took {time()-start} seconds")
        start=time()
        self.sdf['Combined Sentiment']=[self.get_sentiment(" ".join([x,y])) for x,y in zip(self.sdf.Heading,self.sdf.Review)]
        print(f"combined took {time()-start} seconds")
    def get_meandf(self):
        dfs=[]
        for i in range(1,6):
            mdf=self.sdf[self.sdf.Stars==i][['Headings Sentiment','Reviews Sentiment', 'Combined Sentiment']].mean()
            dfs.append(mdf)
        self.mean_df=pd.DataFrame(dfs)
        self.mean_df["Stars"]=[x for x in range(1,6)]
    def get_corrdf(self):
        self.corrdf=self.sdf[["Stars",'Headings Sentiment','Reviews Sentiment', 'Combined Sentiment']].corr()


import threading
from transformers import pipeline

nlp_sent=pipeline(
            "sentiment-analysis"
        )
def get_sentiment(text): 
    resp=nlp_sent(text)[0]
    if resp['label']=='NEGATIVE':
        score=1-resp['score']
    else:
        score=resp['score']
    return score

def df_wrangler(sdf,colname,):
    sdf["Headings Sentiment"]=[get_sentiment(x) for x in sdf.Heading]
    sdf["Reviews Sentiment"]=[get_sentiment(x) for x in sdf.Review]
    sdf['Combined Sentiment']=[get_sentiment(" ".join([x,y])) for x,y in zip(sdf.Heading,sdf.Review)]


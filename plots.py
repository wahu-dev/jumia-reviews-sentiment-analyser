from plotly import graph_objects as go
import pandas as pd
from reviewCrawler import Scraper
import plotly.express as px
import io
import base64
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def get_corrplot(corr):
    fig = px.imshow(corr,
                    labels=dict(
                        color="Correlation Coefficient"
                    ),
                    x=corr.columns,y=corr.columns)
    return fig


def get_wordcloud(df,star):
    try:
        wordcloud=WordCloud(max_font_size=50, max_words=100, background_color="white").generate(" ".join([x for x in df[df.Stars==star].Review]).lower())
        buf = io.BytesIO() # in-memory files
        wordcloud.to_image().save(buf,format="png")
        data = base64.b64encode(buf.getbuffer()).decode("utf8") # encode to html elements
        plt.close()
        return "data:image/png;base64,{}".format(data)
    except ValueError:
        return "data:image/png;base64,"




def get_dailyplot(df):
    df["Date"]=pd.to_datetime(df.Date,format="%d-%m-%Y")
    ddf=pd. DataFrame(df.Date.value_counts()).sort_index()
    ddf['MA5'] = ddf.Date.rolling(5).mean()
    ddf['MA20'] = ddf.Date.rolling(20).mean()

    fig=go.Figure()
    fig.add_trace(
        go.Bar(
            x=ddf.index,
            y=ddf.Date,
            name="Daily Reviews"
        )
    )
    fig.add_trace(
        go.Scatter(
            x=ddf.index,
            y=ddf.MA5,
            mode="lines+markers+text",
            line_shape='spline',
            name="Moving Average with a 5 day lag"
        )
    )
    fig.add_trace(
        go.Scatter(
            x=ddf.index,
            y=ddf.MA20,
            mode="lines+markers+text",
            line_shape='spline',
            name="Moving Average with a 20 day lag"
        )
    )
    return fig



def get_starplot(rd):
    rdf=pd.DataFrame(data={
        "Stars":[list(a.keys())[0] for a in rd["stars"]],
        "Count":[list(a.values())[0] for a in rd["stars"]]
    })
    fig=go.Figure()
    fig.add_trace(
        go.Pie(
            labels=[f"{'⭐'*x}" for x in rdf.Stars],
            values=rdf.Count
        )
    )
    fig.update_traces(hole=.4, hoverinfo="label+percent+name")
    return fig


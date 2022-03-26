from urllib.parse import quote_plus as urlquote
def link_builder(link):
    url="https://www.jumia.co.ke/brown-mens-leather-loafer-shoes-fashion-mpg247191.html"
    link=f'https://c.jumia.io/?a=65472&c=9&p=r&E=kkYNyk2M4sk%3D&ckmrdr={urlquote(url,encoding="utf-8")}&utm_campaign=65472'
    return link






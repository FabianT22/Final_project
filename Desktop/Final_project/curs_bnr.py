def curs(moneda):
    import requests,datetime
    root_url="http://www.infovalutar.ro/bnr"
    year=datetime.datetime.now().year
    month=datetime.datetime.now().month
    day=datetime.datetime.now().day
    currency = moneda
    url = root_url + "/" + str(year)+ "/" + str(month) + "/" + str(day) + "/" + currency
    curs_actual = requests.get(url).text
    return curs_actual

print(curs("GBP"))
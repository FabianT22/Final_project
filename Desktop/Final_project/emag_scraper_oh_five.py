import requests
import datetime
import product_class_obj
import db_repository
from bs4 import BeautifulSoup

def emag_scraper(search_term):
    search_DT = datetime.datetime.now()

    # url - the etailer website where the search is going to take place
    url = "https://www.emag.ro/"
    # search_term - search term, this will come as an input from the end user

    # correct_term = adapted term to be used to integrate into the final search url
    correct_term = search_term.replace(" ", "%")

    # search_url - correct URL in which the search will happen
    search_url = url + "search/" + correct_term + "?ref=effective_search"

    site = requests.get(search_url)
    soup = BeautifulSoup(site.text, "html5lib")

    # product_page = soup object that contains all the products
    product_page = soup.find("div", {"id": "card_grid"})
    # all products
    product_cards = product_page.findAll("div", {"class": "card-item"})
    st = search_term.replace(' ', '')
    prime_prod = []
    # extracts all relevant information from the soup object
    for product in product_cards:
        # pn variable stands for Product Name
        # product name formatting (string formatting)
        # pp variable stands for Product Price
        pp = str(product.find('p', {'class': 'product-new-price'}).contents[0])
        pn = str(product.find('a', {'data-zone': 'title'}).string)
        pn = pn.replace('\n', '')
        pn = pn.lstrip()
        pn = pn.rstrip()
        if "." in pp:
            pp = pp.replace('.', '')
            pp = int(pp)
        elif pp.isnumeric() == False:
            pp = 0
        # p_href link to the product
        p_href = str(product.find("h2", {'class': 'card-body'}).find("a", href=True).get('href'))
        # prime_prod is a product_class_object
        prodi = product_class_obj.Product(pp, p_href, search_DT.strftime('%Y-%m-%d %H:%M:%S'), search_DT.strftime('%Y-%m-%d %H:%M:%S'), 11, pn)
        # repo is the list of products, each list item is a product_class_object
        # this list will be passed to the repo object
        prime_prod.append(prodi)
    return prime_prod


# the build_interface function gathers information about the products in question
# TODO resolve the build_interface
def build_interface(prime_prod):
    spec_table = []
    if len(prime_prod) > 10:
        for i in range(0, 10):
            spec_page = requests.get(prime_prod[i].product_href, 'html5lib').text
            spec_soup = BeautifulSoup(spec_page, "html5lib")
            # spec_table.append(spec_soup.find("div",{'class':'container pad-btm-lg'}).get)
            # spec_table.append(spec_soup.find("div", {'class': 'col-md-12'}).text)
            # st = spec_soup.find("div", {'class': 'col-md-12'}).get
            st = spec_soup.findall("div", {'class': 'pad-top-sm'})
            for item in st:
                spec_part = item.text
                spec_table.append(spec_part)
            # spec_table.append(st)
        return spec_table

# what_to_track: chooses an item to track based on list index


def what_to_track(prime_prod):
    cn = 0
    t_i = []
    for item in prime_prod:
        print("[ " + str(cn) + " ]"+" "+str(item)+"\n")
        cn += 1
    trck = input("What do you want to track: ")
    l_track = trck.split(",")
    for i in l_track:
        temp = prime_prod.pop(int(i))
        t_i.append(temp)
    return t_i

# price_check() - checks the prices for all the items that are tracked in the DB


def price_check(items_to_check):
    import time
    print("\n")
    for item in items_to_check:
        url = item.product_href
        site = requests.get(url)
        product_page_soup = BeautifulSoup(site.text, "html5lib")
        product_new_price = product_page_soup.find("p", {"class": "product-new-price"}).contents[0]
        product_new_price = product_new_price.strip()
        time.sleep(120)
        if float(item.product_price) < float(product_new_price):
            item.product_price = product_new_price
            item.start_date = datetime.datetime.now()
    return items_to_check


# Working
# db_repository = db_repository.DBRepository()
# db_repository.add_new_item_from_scraper(what_to_track(emag_scraper()))
# print(db_repository.list_of_products)



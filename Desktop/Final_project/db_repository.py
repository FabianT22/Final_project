# this class creates a repository of the database in memory for easy and fast access
# it makes changes to the database based on the findings
class DBRepository():
    def __init__(self):
        # initialization with of the object with an empty list
        self.list_of_products = []

    # object representation
    def __repr__(self, list_of_products):
        return str(self.list_of_products)

    def add_new_item_from_scraper(self, list_of_products):
        for item in list_of_products:
            self.list_of_products.append(item)

    # get_data method: fetches the information related to the searched for item(product)
    # def get_data(self, search_term):
      #  import connection_sgtn
       # sql = """SELECT *
        #        FROM product
         #       WHERE product_name=(%s)
          #      """
        # data=(str(search_term))
        # connection_sgtn.DBConnection.getInstance().connection_do(sql, search_term)

    def get_data(self, search_term):
        import connection_sgtn
        return connection_sgtn.DBConnection.connection_do_select(search_term)


    # the ischanged method receives a "new price" for the product and compares it with the price it already has from the database
    # if the price changes, a new product price is added and both the start date and end date of the product are changed to be the same.
    # if the price remains the same only the end date gets changed, thus having continuity
    def ischanged(self, new_price):
        current_price = self.product_price
        import datetime
        sdt = datetime.datetime.now()
        if current_price != new_price:
            self.product_price = new_price
            self.start_date = sdt.strftime('%Y-%m-%d %H:%M:%S')
            self.end_date = sdt.strftime('%Y-%m-%d %H:%M:%S')
            return True
        else:
            self.end_date = sdt.strftime('%Y-%m-%d %H:%M:%S')
            return False

    # commit_change method: commits changes to the database.
    # if there was a search for the item, and price of the item changes, the cursor will receive the sql command on the if branch
    # if there was no change in price, the else branch's sql command is given: moves the end date of certain price, by the new end date, thus marking the continuity
    # def commit_change(self):
        # import psycopg2
        # if self.ischanged(new_price) == True:
            # sql = """UPDATE price
                    # SET
                    # start_date = (%s)
                    # end_date = (%s)
                    # price =(%s)
                    # WHERE
                    # id_product = self.id_product"""
            # to_update = (str(self.start_date), str(self.end_date), int(self.product_price))

        # else:
            # sql = """UPDATE price
                    # SET
                    # end_date = (%s)
                    # WHERE
                    # id_product = self.id_product"""
            # to_update = (str(self.end_date))

        # has to be changed to use the "connection singleton class later on"
        # conn = None
        # prm = 'dbname=e_db user=postgres password=admin'
        # conn = psycopg2.connect(prm)
        # cur = conn.cursor()
        # cur.execute(sql, to_update)



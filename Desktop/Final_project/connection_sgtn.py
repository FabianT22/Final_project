# Singleton class for connection to the DB
class DBConnection:
    __instance = None
    @staticmethod
    def getInstance():
        """ Static access method. """
        if DBConnection.__instance == None:
            DBConnection()
        return DBConnection.__instance

    def __init__(self):
       """ Private constructor. """
       if DBConnection.__instance != None:
           raise Exception("This is the DBConnection!")
       else:
           DBConnection.__instance = self


    # selects all items currently tracked in the database
    def connection_do_select(self):
        import psycopg2
        import product_class_obj
        prm = 'dbname=e_db user=postgres password=admin'
        sql_get_etailer = "SELECT name, site_href FROM etailer"
        sql_get_price = "SELECT start_date, end_date, price FROM price"
        sql_get_product = "SELECT product_name, product_image, product_link_href, id_product FROM product"
        conn = psycopg2.connect(prm)
        cur = conn.cursor()
        cur.execute(sql_get_product)
        products = cur.fetchall()
        cur.execute(sql_get_etailer)
        cur.execute(sql_get_price)
        prices = cur.fetchall()
        # pl - product list
        pl = []
        for item in range(0, len(products)):
            p_l = product_class_obj.Product(prices[item][2], products[item][2], prices[item][0], prices[item][1], products[item][3], products[item][0])
            pl.append(p_l)

        if len(pl) != 0:
            return pl
        else:
            return 'No data exists for your query.'
        conn.close()

    # commits items to be tracked to the DB
    # t_i - tracking item received from emag_scraper.what_to_track()
    def track_commit_to_db(self, t_i):
        import psycopg2
        prm = 'dbname=e_db user=postgres password=admin'
        conn = psycopg2.connect(prm)
        cur = conn.cursor()
        sql_insert_etailer = "INSERT INTO etailer(name, site_href) VALUES(%s,%s)"
        sql_insert_price = "INSERT INTO price(start_date, end_date, price, id_product) VALUES (%s, %s, %s, %s)"
        sql_insert_product = "INSERT INTO product(product_name, product_image, product_link_href) VALUES (%s,%s,%s) RETURNING id_product"

        for i in range(0, len(t_i)):
            data_etailer = ["emag.ro", "https://www.emag.ro"]
            cur.execute(sql_insert_etailer, data_etailer)
            data_product = [str(t_i[i].product_name), "product_image_placeholder", str(t_i[i].product_href)]
            cur.execute(sql_insert_product, data_product)
            prod_id = cur.fetchone()[0]
            data_price = [str(t_i[i].start_date), str(t_i[i].end_date), str(t_i[i].product_price), prod_id]
            cur.execute(sql_insert_price, data_price)
            conn.commit()
        cur.close()
        conn.close()

    # update_prices updates all the prices in the DB
    # this is the method that would need to be scheduled along with the emag_scraper_oh_five.price_to_check()
    def update_prices(self, updated_items):
        import psycopg2
        import datetime
        prm = 'dbname=e_db user=postgres password=admin'
        conn = psycopg2.connect(prm)
        cur = conn.cursor()
        sql_update_price = "UPDATE price SET price = (%s), start_date = (%s)"
        for item in updated_items:
            data_new_price = [item.product_price, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
            cur.execute(sql_update_price, data_new_price)


    # deletes a tracked item
    def delete_item(self):
        items = DBConnection.getInstance().connection_do_select()
        import psycopg2
        data = []
        td = []
        for i in range(0, len(items)):
            print('\n')
            print('[ ' + str(i) + ' ] ' + str(items[i]))
        what_to_delete = input("Which item would you like to delete: ")
        what_to_delete = what_to_delete.split(",")
        for i in what_to_delete:
            temp = items.pop(int(i))
            td.append(temp)
        prm = 'dbname=e_db user=postgres password=admin'
        conn = psycopg2.connect(prm)
        cur = conn.cursor()
        sql_delete = """
                    DELETE 
                    FROM product 
                    WHERE id_product = (%s)"""
        for item in td:
            print(item.id_product)
            data.append(int(item.id_product))
            cur.execute(sql_delete, data)
            conn.commit()
        cur.close()
# below: correct syntax for calling a singleton class
# conn = DBConnection.getInstance().connection_do(sql,search_term)

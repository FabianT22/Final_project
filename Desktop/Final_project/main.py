# TO DO: Make a .py file that does the scheduled tracking from the DB
import emag_scraper_oh_five
# import db_repository
# import product_class_obj
import connection_sgtn
print("Welcome to emag_scraper CLI!" + "\n")
print('\n' + 'What would you like to do today?' + '\n')


def schedule_events():
    import sched
    import time
    schedule = sched.scheduler.enterabs()

# menu_items is a function that creates the command line interface


def menu_items():
        print('Tasks:' + '\n')
        print('To track new items, press 1')
        print('To view current selection, press 2')
        print('To delete items, press 3')
        print('To close this session, press 4')

# creates infinite loop with an exit clause
# used for interaction with the program
answer = 0
while answer != 4:
    menu_items()
    answer = int(input("Press the button corresponding to the command you wish to execute: "))
    if int(answer) == 1:
        search_item = input('What items would you like to track: ' + '\n')
        t_i = emag_scraper_oh_five.what_to_track(emag_scraper_oh_five.emag_scraper(search_item))
        connection_sgtn.DBConnection.getInstance().track_commit_to_db(t_i)

    if int(answer) == 2:
        print(connection_sgtn.DBConnection.getInstance().connection_do_select())

    if int(answer) == 3:
        connection_sgtn.DBConnection.getInstance().delete_item()

# t_i = emag_scraper_oh_five.what_to_track(emag_scraper_oh_five.emag_scraper(search_item))
# db_repository = db_repository.DBRepository()
# connection_sgtn.DBConnection.getInstance().track_commit_to_db(t_i)
# connection_sgtn.DBConnection.getInstance().update_prices(emag_scraper_oh_five.price_check(pc))
# pc = emag_scraper_oh_five.price_check(connection_sgtn.DBConnection.getInstance().connection_do_select())
# connection_sgtn.DBConnection.getInstance().delete_item()
# print(connection_sgtn.DBConnection.getInstance().connection_do_select())
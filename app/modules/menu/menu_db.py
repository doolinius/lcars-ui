import sqlite3
from datetime import date

class MenuDB:

    def __init__(self):
        self.db_file = "modules/menu/doolin_menu.db"

    def connect(self):
        self.db = sqlite3.connect(self.db_file,
                detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES)
        self.db.row_factory = sqlite3.Row

    def close(self):
        self.db.close()

    def set_made(self, menu_id, dinner_id, made):
        self.connect()
        print("SET MADE")
        self.db.execute("UPDATE menu_items set made={} WHERE menu_id = {} and dinner_id = {}".format(made, menu_id, dinner_id))
        self.db.commit()
        self.db.close()

    def get_current(self):
        self.connect()
        result = self.db.execute("SELECT * from menus where start_date <= DATE('now') and DATE('now') <= end_date").fetchall()

        if len(result) == 0:
            self.db.close()
            return(None)
        else:
            row = result[0]
            menu_id = row[0]
            start_date = row[1]
            end_date = row[2]
            #made = row[3]
            result = self.db.execute("SELECT * from menu_items INNER JOIN dinners ON menu_items.dinner_id = dinners.id WHERE menu_items.menu_id = " + str(menu_id));
            dinners = []
            for item in result:
                dinners.append({k: item[k] for k in item.keys()})

            current_menu = {
                    'menu_id': menu_id,
                    'start_date': start_date,
                    'end_date': end_date,
                    'dinners': dinners
                    }

            self.db.close()
            return(current_menu)

if __name__ == "__main__":
    db = MenuDB()
    #db.connect()
    menu = db.get_current()
    print(dinners)
    #db.close()

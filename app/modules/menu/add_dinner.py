#!/usr/bin/env python3

import sqlite3

def toBool(answer):
    if answer.lower() in ["y", "yes"]:
        return True
    else:
        return False

con = sqlite3.connect('doolin_menu.db')
cur = con.cursor()

another = "yes"

while another.lower() in ["y", "yes"]:
    name = input("Dinner Name: ")
    main_ingredient = input("Main Ingredient: ")
    ethnicity = input("Ethnicity: ")
    season = input("Season ['None' if not seasonal]: ").lower()
    dietary_class = input("Dietary class ('vegetarian' or 'flexitarian'): ").lower()
    comfort = toBool(input("Is it comfort food (y/N): "))
    litman_friendly = toBool(input("Litman Friendly (y/N): "))

    #query = "INSERT into dinners (name, main_ingredient, ethnicity, season, dietary_class, comfort, litman_friendly) VALUES ('{}', '{}', '{}', '{}', '{}', {}, {})".format(name, main_ingredient, ethnicity, season, dietary_class, comfort, litman_friendly)

    cur.execute("INSERT into dinners (name, main_ingredient, ethnicity, season, dietary_class, comfort, litman_friendly) VALUES (?, ?, ?, ?, ?, ?, ?)", (name, main_ingredient, ethnicity, season, dietary_class, comfort, litman_friendly))

    con.commit()
    another = input("Enter another? ")

con.close()

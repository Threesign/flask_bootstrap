import sqlite3 as lite
import sys

sales = (
    ('riemer.kerkstra', 6),
    ('taeker', 5),
    ('andre_roukema', 3),
    ('ot8', 2)
)


con = lite.connect('sales.db')

with con:

    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS reps")
    cur.execute("CREATE TABLE reps(rep_name Text, amount INT)")
    cur.executemany("INSERT INTO reps VALUES(?, ?)", sales)
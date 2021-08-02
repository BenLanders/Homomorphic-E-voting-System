import sqlite3
conn = sqlite3.connect('e_voting_user_data.db')

c = conn.cursor()

c.execute('''CREATE TABLE users
             (userName, password)''')

c.execute('''CREATE TABLE encryptedVotes
             (userName, encryptedVote)''')

c.execute('''CREATE TABLE admin
             (userName, password)''')

c.execute("INSERT INTO admin VALUES ('Admin','e3afed0047b08059d0fada10f400c1e5')")

conn.commit()

conn.close()

import sqlite3

conn = sqlite3.connect(r"C:\Users\spook\OneDrive\Desktop\testDBsql\UserDataBase")

# Create a cursor to execute SQL commands
cur = conn.cursor()

# Create a table
cur.execute(f'''
CREATE TABLE IF NOT EXISTS users
(id INT, username TEXT, password TEXT)
''')

# Insert data into the table
users = [
    (1, "0", "5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9"),
    (2, "ben", "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"),
    (3, "koolkid", "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"),
    (4, "1", "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b"),
    (5, "5", "ef2d127de37b942baad06145e54b0c619a1f22327b2ebbcfbec78f5564afe39d")
]
cur.executemany('''
INSERT INTO users VALUES (?,?,?)
''', users)

# Commit the transaction
conn.commit()

# Select and print the data from the table
cur.execute('SELECT * FROM users')
for row in cur.fetchall():
    print(row)

# Close the connection
conn.close()

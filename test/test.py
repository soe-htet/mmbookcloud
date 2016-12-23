# import sqlite3
#
# connection = sqlite3.connect('data.db')
#
# cursor = connection.cursor()
#
# create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
# cursor.execute(create_table)
# #
# # user = (1, "Soe", "asdf")
# #
# # insert_query = "INSERT INTO users VALUES (?,?,?)"
# # #cursor.execute(insert_query, user)
# #
# # users = [(2, "soe2","asdf"), (3, "soe3","asdf")]
# #
# # cursor.executemany(insert_query,users)
# #
# # select_query = "SELECT * FROM users"
# # for row in cursor.execute(select_query):
# #     print(row)
#
# # drop_query = "DROP TABLE IF EXISTS users"
# # cursor.execute(drop_query)
# # print("droppped")
#
# connection.commit()
# connection.close()

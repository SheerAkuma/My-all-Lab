import sqlite3
from sqlite3 import Error

def create_connection(Messengers_file):
    conn = None
    try:
        conn = sqlite3.connect('Messengers.db')
    except Error as e:
        print(e)
    return conn

#db = sqlite3.connect('Messengers.db')
#c = db.cursor()

def select_all_message(conn):
    sql = 'SELECT m.mes_id, m.user_id, m.chat_id, m.mes_text FROM Message m JOIN Chats ch ON m.chat_id = ch.chat_id'
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print(row)


# Вибрати повідомлення з чату Друзі
def select_mes_chat_friends(conn):
    sql = 'SELECT m.mes_id, m.user_id, m.chat_id, m.mes_text FROM Message m JOIN Chats ch ON m.chat_id = ch.chat_id WHERE ch.chat_id = 11'
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print(row)

# Створення нового повідомлення
def create_mes(conn, text):
    sql = ''' INSERT INTO Message(mes_id, user_id, chat_id, mes_text)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, text)

# Оновлення повідомлення чаті
def update_mes_text(conn, mes_text):
    sql = ''' UPDATE Message
              SET mes_text = ?
              WHERE mes_id = ?'''
    cur = conn.cursor()
    cur.execute(sql, mes_text)
    conn.commit()

# Видалення повідомлення
def remove_mes(conn, remove_mes):
    sql = ''' DELETE FROM Message WHERE mes_text = ? '''
    cur = conn.cursor()
    cur.execute(sql, remove_mes)
    conn.commit()


def main():

    # Шлях до БД
    database = r"Messeger.db" 
 
    # Встановлення з'єднання
    conn = create_connection(database)

    # Використовууючи встановлене з'єднання виконуються операції над БД
    with conn:
        print("\nВсі повідомлення з чатів (id-повідомлення, id-юзера, id-чату, текст чату)")
        select_all_message(conn)
        print("\nВивести чат з друзями (завдання, дата, приорітет)")
        select_mes_chat_friends(conn)
        print("\nВставка нового повідомлення...")
        create_mes(conn,(27, 15, 11,'Hello guys, i hack you chat'))
        print("\nВсі повідомлення з чатів (id-повідомлення, id-юзера, id-чату, текст чату)")
        select_all_message(conn)
        print("\nЗміна повідомлення...")
        update_mes_text(conn, ('Noooooo', 2))
        print("\nВсі повідомлення з чатів (id-повідомлення, id-юзера, id-чату, текст чату)")
        select_all_message(conn)        
        print("\nВидалення повідомлення")
        remove_mes(conn, ('Hello guys, i hack you chat',))
        print("\nВсі повідомлення з чатів (id-повідомлення, id-юзера, id-чату, текст чату)")
        select_all_message(conn)
        
 
if __name__ == '__main__':
    main()

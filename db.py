import sqlite3

def user_exists(id):
    conn = sqlite3.connect('user.db')
    command = conn.cursor()
    command.execute(f"SELECT Count(*) from USER where id='{id}';")   
    result = command.fetchone()[0]
    conn.commit()
    conn.close()   

    if result == 1:
        return True

    return False


def get_lottery_people_num():
    conn = sqlite3.connect('user.db')
    command = conn.cursor()
    command.execute(f"SELECT Count(*) from USER where status='lottery';")   
    result = command.fetchone()[0]
    conn.commit()
    conn.close()   

    return result


def add_user(id, type):
    conn = sqlite3.connect('user.db')
    command = conn.cursor()
    command.execute(f"insert into user (id, status) values ('{id}', '{type}');")   
    conn.commit()
    conn.close()   


def delete_user(id):
    conn = sqlite3.connect('user.db')
    command = conn.cursor()
    command.execute(f"delete from USER where id='{id}'")   
    conn.commit()
    conn.close()   

def get_user_status(id):
    conn = sqlite3.connect('user.db')
    command = conn.cursor()
    command.execute(f"select status from USER where id='{id}';")   
    result = command.fetchone()[0]
    conn.commit()
    conn.close()   
    return result
    


if __name__ == '__main__':
    conn = sqlite3.connect('user.db')
    command = conn.cursor()
    command.execute("SELECT Count(*) from USER where id='test';")   
    result = command.fetchone()

    print(user_exists('lalalaa'))

    # command.execute('''create table user
    #    (id char(50) primary key     not null,
    #    status       char(20));''')

    # command.execute("insert into user (id) \
    #      values ('lalala' );")   
    
    

    conn.commit()
    conn.close()
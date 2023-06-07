from mysql.connector import connect, Error
# from password_generator import PasswordGenerator


config = {
    'host':              '45.95.234.227',
    'user':              'donny_Admin',
    'password':          '5i1<NhOZsW&A^R,=',
    'database':          'donny_DiscordServer',
    'raise_on_warnings': True
}


class DataBase:
    def __init__(self):
        self.con = None

    def connect(self):
        try:
            self.con = connect(**config)
            # print('[Database] Connection is success!')
        except Error as e:
            print(f'[Database] Connection is failed!\nError: {e}')

        else:
            return self.con


    def add_user(self, user_id):
        self.connect()
        with self.con.cursor(buffered=True) as cur:
            cur.execute(f'''INSERT INTO wallets VALUES (%s, 0)''', (user_id,))
            self.con.commit()

        self.con.close()

    def get_balance(self, user_id) -> float:
        self.connect()
        result = None
        with self.con.cursor(buffered=True) as cur:
            cur.execute(f"SELECT `user_money` FROM wallets WHERE `user_id`= %s ", (user_id,))
            result = cur.fetchone()

        self.con.close()
        return result[0]

    def reset_user(self, user_id):
        self.connect()
        with self.con.cursor(buffered=True) as cur:
            cur.execute(f'''UPDATE wallets SET `user_money`= %s WHERE (`user_id` = %s) ''',(0, user_id,))
            self.con.commit()

        self.con.close()

    def is_user_exist(self, user_id):
        self.connect()
        result = None
        with self.con.cursor(buffered=True) as cur:
            cur.execute(f"SELECT * FROM wallets WHERE `user_id`= %s ", (user_id,))
            result = len(cur.fetchall())

        self.con.close()
        return bool(result)

    def add_cash(self, user_id, ammount):
        self.connect()
        with self.con.cursor(buffered=True) as cur:
            cur.execute(f'''UPDATE wallets SET `user_money`=`user_money` + %s WHERE (`user_id` = %s) ''', (ammount, user_id, ))
            self.con.commit()

        self.con.close()

    def minus_cash(self, user_id, ammount):
        self.connect()
        with self.con.cursor(buffered=True) as cur:
            cur.execute(f'''UPDATE wallets SET `user_money`=`user_money` - %s WHERE (`user_id` = %s) ''',
                        (ammount, user_id,))
            self.con.commit()

        self.con.close()

    def create_clan(self, clan_name, clan_lead_id, code, chat_id):
        self.connect()
        with self.con.cursor(buffered=True) as cur:
            cur.execute(f'''INSERT INTO clans VALUES (0, %s, %s, 0, %s, %s)''', (clan_name, clan_lead_id, code, chat_id, ))
            self.con.commit()

        self.con.close()

    # def is_user_clan_lead(self, user):

    def add_clan_member(self, user, clan):
        self.connect()
        with self.con.cursor(buffered=True) as cur:
            cur.execute(f'''INSERT INTO clan_members VALUES (%s, %s)''',(user, clan, ))
            self.con.commit()

        self.con.close()

    def get_clan_members(self, clan):
        ...


    def is_clan_exist(self, clan_id = None, name = None, code=None):
        self.connect()
        result = None
        with self.con.cursor(buffered=True) as cur:
            cur.execute(f"SELECT * FROM clans WHERE (`title`= %s OR `id` = %s OR `inv_code` = %s) ", (name, clan_id, code, ))
            if code is None:
                result = len(cur.fetchall())

                self.con.close()
                return bool(result)
            else:
                result = cur.fetchone()

                self.con.close()
                return result

Data = DataBase()
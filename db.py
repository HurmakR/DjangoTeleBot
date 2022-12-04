import sqlite3

class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def get_category(self):
        result = self.cursor.execute("SELECT Category FROM Cat ORDER BY Category")
        return result

    def get_model(self, category):
        result = self.cursor.execute(f"SELECT * from Model WHERE ModelCat = (?) ORDER BY id; ", [category])
        return result

    def get_price(self, model):
        result = self.cursor.execute(f"SELECT Parts.PartName, PartPrice.pricePart FROM PartPrice INNER JOIN Parts ON Parts.id = PartPrice.idPart INNER JOIN Model ON Model.id = PartPrice.idModel WHERE Model.Modelname = (?)", [model])
        return result

    def add_log(self, name, surname, nick, data, time):
        if surname:
            fullname = name + ' ' + surname
        else:
            fullname = name
        self.cursor.execute(f'INSERT INTO Log (name, telegram_id, data, date) VALUES (?, ? ,? ,?)', [fullname, nick, data, time])
        print('successfully added: db.py 27')
        self.conn.commit()

    def close(self):
        self.conn.close()


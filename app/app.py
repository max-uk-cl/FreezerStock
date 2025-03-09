"""App for managing the stock of items in freezer"""
import sqlite3
import json
from flask import Flask
from flask import g
DATABASE = "/data/stock.db"

def get_db():
    """Gets database path to connect"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
def insert_method(ean):
    """Method to insert item where EAN is the product code"""
    cursor = get_db().cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS StockItems"
    "(EAN STRING,Stock INTEGER,PRIMARY KEY(EAN))")
    def insert(ean_code):
        try:
            cursor.execute("INSERT INTO StockItems VALUES (?,1)",(ean_code))
        except ValueError:
            cursor.execute("UPDATE StockItems SET Stock = Stock + 1 WHERE EAN = (?) ",(ean_code))
    insert(ean)
    get_db().commit()
def get_method():
    """Method for getting all the values in the table"""
    cursor = get_db().cursor()
    def get_stock():
        try:
            cursor.execute("SELECT * FROM StockItems")
            stock_value = cursor.fetchall()
            json_stock_value = json.dumps(stock_value)
            return json_stock_value
        except OSError:
            return "Something went wrong"
    return get_stock()
def delete_method(ean):
    """Method to reduce the stock of a product by 1"""
    cursor = get_db().cursor()
    def delelete_item(ean_code):
        cursor.execute("SELECT Stock FROM StockItems WHERE EAN = (?)",(ean_code))
        stock_amount = cursor.fetchall()
        if stock_amount[0][0] > 0:
            cursor.execute("UPDATE StockItems SET Stock = Stock - 1 WHERE EAN = (?)",(ean_code))

    delelete_item(ean)
    get_db().commit()


app = Flask(__name__)
@app.route('/', methods=['GET'])
def get_tasks():
    """Return app ok"""
    return "App OK"
@app.get('/api/insert/<ean_code>')
def dev_insert(ean_code):
    """Calls insert method"""
    insert_method(ean_code)
    return " "
@app.get('/api/delete/<ean_code>')
def dev_del(ean_code):
    """Calls delete method"""
    delete_method(ean_code)
    return " "
@app.get('/api/get')
def dev_get():
    """Calls get method"""
    stock = get_method()
    print(stock)
    return stock
@app.teardown_appcontext
def close_connection(exception):
    """Closes connection with database"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

import sqlite3
from flask import Flask
from flask import request
from flask import g
import json
DATABASE = "/data/stock.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
def insertMethod(EAN):
    
    cursor = get_db().cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS StockItems (EAN STRING,Stock INTEGER,PRIMARY KEY(EAN))")
    def insert(eanCode):
        try:
            cursor.execute("INSERT INTO StockItems VALUES (?,1)",(eanCode))
        except:
            cursor.execute("UPDATE StockItems SET Stock = Stock + 1 WHERE EAN = (?) ",(eanCode))
    insert(EAN)
    get_db().commit()
def getMethod():
    cursor = get_db().cursor()
    def getStock():
        try:
            cursor.execute("SELECT * FROM StockItems")
            stockValue = cursor.fetchall()
            jsonStockValue = json.dumps(stockValue)
            return jsonStockValue
        except:
            return "Something went wrong"
    return getStock()
def deleteMethod(EAN):
    cursor = get_db().cursor()
    def deleleteItem(eanCode):
        cursor.execute("SELECT Stock FROM StockItems WHERE EAN = (?)",(eanCode))
        stockAmount = cursor.fetchall()
        if (stockAmount[0][0] > 0):
            cursor.execute("UPDATE StockItems SET Stock = Stock - 1 WHERE EAN = (?)",(eanCode))

    deleleteItem(EAN)
    get_db().commit()


app = Flask(__name__)
@app.route('/', methods=['GET'])
def get_tasks():
    return "App OK"
@app.get('/api/insert/<id>')
def devInsert(id):
    insertMethod(id)
    return " "
@app.get('/api/delete/<id>')
def devDel(id):
    deleteMethod(id)
    return " "
@app.get('/api/get')
def devGet():
    stock = getMethod()
    print(stock)
    return stock
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

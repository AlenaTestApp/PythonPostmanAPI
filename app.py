from flask import Flask, request, jsonify, g
import sqlite3
import os

APP = Flask(__name__)
DB_PATH = os.getenv("DB_PATH", os.path.join(os.path.dirname(__file__), "data.db"))


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@APP.teardown_appcontext
def close_db(_):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            car_type TEXT NOT NULL,
            make TEXT NOT NULL,
            year INTEGER NOT NULL,
            price REAL NOT NULL,
            discount INTEGER DEFAULT 0,
            stock INTEGER DEFAULT 0
        )
    """)
    db.commit()


@APP.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}


@APP.route("/products", methods=["POST"])
def create_product():
    data = request.get_json(force=True, silent=True) or {}
    car_type = data.get("car_type")
    make = data.get("make")
    year = data.get("year")
    price = data.get("price")
    discount = data.get("discount", 0)
    stock = data.get("stock", 0)
    if car_type is None or make is None or year is None or price is None:
        return jsonify({"error": "car_type, make, year, price are required"}), 400
    db = get_db()
    cur = db.execute("INSERT INTO products (car_type, make, year, price, discount, stock) VALUES (?, ?, ?, ?, ?, ?)",
                     (car_type, make, int(year), float(price), float(discount), int(stock)))
    db.commit()
    pid = cur.lastrowid
    return jsonify({"id": pid, "car_type": car_type, "make": make, "year": year, "price": float(price),
                    "discount": discount, "stock": int(stock)}), 201


@APP.route("/products", methods=["GET"])
def list_products():
    rows = get_db().execute("SELECT * FROM products").fetchall()
    return jsonify([dict(r) for r in rows])


@APP.route("/products/<int:pid>", methods=["GET"])
def get_product(pid):
    row = get_db().execute("SELECT * FROM products WHERE id = ?", (pid,)).fetchone()
    if not row:
        return jsonify({"message": f"Product with id '{pid}' not found"}), 404
    return jsonify(dict(row))


@APP.route("/products/<int:pid>", methods=["PATCH"])
def update_product(pid):
    data = request.get_json(force=True, silent=True) or {}
    fields, vals = [], []
    for key in ("name", "make", "year", "price", "discount", "stock"):
        if key in data:
            fields.append(f"{key} = ?"); vals.append(data[key])
    if not fields:
        return jsonify({"error": "nothing to update"}), 400
    db = get_db()
    cur = db.execute(f"UPDATE products SET {', '.join(fields)} WHERE id = ?", (*vals, pid))
    db.commit()
    if cur.rowcount == 0:
        return jsonify({"message": f"Product with id '{pid}' not found"}), 404
    return get_product(pid)


@APP.route("/products/<int:pid>", methods=["DELETE"])
def delete_product(pid):
    db = get_db()
    cur = db.execute("DELETE FROM products WHERE id = ?", (pid,))
    db.commit()
    if cur.rowcount == 0:
        return jsonify({"message": f"Product with id '{pid}' not found"}), 404
    return "", 204


@APP.route("/which_db", methods=["GET"])
def which_db():
    return jsonify({"db_path": DB_PATH})


if __name__ == "__main__":
    # Initialize DB once at startup
    with APP.app_context():
        init_db()
    APP.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)

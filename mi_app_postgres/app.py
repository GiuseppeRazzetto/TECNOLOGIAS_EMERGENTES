from flask import Flask, request, jsonify, send_from_directory
import psycopg2

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host="db",
        database="testdb",
        user="postgres",
        password="1234"
    )

@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

@app.route("/items", methods=["GET"])
def get_items():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM items")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(rows)
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/items", methods=["POST"])
def add_item():
    try:
        data = request.json
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO items (name) VALUES (%s)", (data["name"],))
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "inserted"}
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)

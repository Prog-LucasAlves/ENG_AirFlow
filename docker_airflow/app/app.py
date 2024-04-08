from flask import Flask, render_template
import psycopg2
import os

import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())

app = Flask(__name__)


def get_db_connection():
    con = psycopg2.connect(
        user=os.getenv("POSTGRES_USER_APP"),
        password=os.getenv("POSTGRES_PASSWORD_APP"),
        database=os.getenv("POSTGRES_DB_APP"),
        host=os.getenv("HOST_DB"),
    )

    return con


@app.route("/")
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM moedas;")
    books = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", title="Pares de Moedas", books=books)


"""
@app.route('/home')
def home():
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")
    return render_template(
        "index.html",
        content="l" + formatted_now
    )


@app.route('/about')
def about():
    return render_template(
        "index.html",
        content='Lucas'
    )
"""

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

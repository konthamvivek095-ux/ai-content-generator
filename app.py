import os

if not os.path.exists("database.db"):
    from init_db import *  # noqa: F403

from flask import Flask, render_template, request, redirect, session
import hashlib

from db import get_connection
from scraper import extract_content
from llm_service import generate_content
from pdf_generator import generate_pdf

app = Flask(__name__)
app.secret_key = "supersecretkey"


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )
            conn.commit()

        except Exception:
            return render_template(
                "register.html",
                error="User already exists"
            )

        conn.close()

        return redirect("/login")

    return render_template("register.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, hashed_password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect("/")
        else:
            return render_template(
                "login.html",
                error="Invalid credentials"
            )

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route("/", methods=["GET", "POST"])
def index():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        url = request.form["url"]
        audience = request.form.get("audience", "General")
        style = request.form.get("style", "Professional")
        word_count = request.form.get("word_count", 500)

        data = extract_content(url)

        title = data["title"]
        content = data["content"]

        prompt = f"""
Write a professional blog article.

Title: {title}
Audience: {audience}
Style: {style}
Word Count: {word_count}

Content:
{content[:4000]}
"""

        ai_text = generate_content(prompt)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO articles
            (title, source_url, scraped_content, ai_content, user_id)
            VALUES (?, ?, ?, ?, ?)
        """, (
            title,
            url,
            content,
            ai_text,
            session["user_id"]
        ))

        conn.commit()
        conn.close()

        pdf_file = generate_pdf(title, ai_text)

        return render_template(
            "result.html",
            article=ai_text,
            pdf_file=pdf_file
        )

    return render_template("index.html")


# ---------------- HISTORY ----------------
@app.route("/history")
def history():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM articles
        WHERE user_id=?
        ORDER BY created_at DESC
    """, (session["user_id"],))

    articles = cursor.fetchall()

    conn.close()

    return render_template(
        "history.html",
        articles=articles
    )


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
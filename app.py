from flask import Flask
from flask import Flask, request
import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
conn = None
cur = None

if DATABASE_URL:
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS users") 
        cur.execute("""
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                name TEXT
            )
        """)
        print("✅ Database connected and table ready!")
    except Exception as e:
        print(f"❌ Database error: {e}")
        conn = None
        cur = None
else:
    print("❌ DATABASE_URL not set")

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>User Manager</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }

            body {
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .card {
                background: white;
                border-radius: 20px;
                padding: 50px 40px;
                text-align: center;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                max-width: 500px;
                width: 90%;
            }

            .emoji { font-size: 60px; margin-bottom: 20px; }

            h1 { font-size: 2rem; color: #333; margin-bottom: 10px; }

            p { color: #666; margin-bottom: 30px; font-size: 1rem; line-height: 1.6; }

            .badge {
                background: #e8f5e9;
                color: #2e7d32;
                padding: 6px 16px;
                border-radius: 20px;
                font-size: 0.85rem;
                font-weight: bold;
                display: inline-block;
                margin-bottom: 30px;
            }

            .btn {
                display: inline-block;
                margin: 8px;
                padding: 12px 24px;
                border-radius: 10px;
                text-decoration: none;
                font-weight: bold;
                font-size: 0.95rem;
                transition: transform 0.2s, box-shadow 0.2s;
            }

            .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }

            .btn-primary {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
            }

            .btn-secondary {
                background: #f5f5f5;
                color: #333;
                border: 2px solid #ddd;
            }

            .footer { margin-top: 30px; font-size: 0.8rem; color: #aaa; }
        </style>
    </head>
    <body>
        <div class="card">
            <div class="emoji">🚀</div>
            <h1>User Manager App</h1>
            <p>Welcome to Rugambwa's User Management system. Add users and view them instantly.</p>
            <div class="badge">✅ Deployment Successful</div>
            <br>
            <a href="/add" class="btn btn-primary">➕ Add User</a>
            <a href="/users" class="btn btn-secondary">👥 View Users</a>
            <div class="footer">Always here to serve you</div>
        </div>
    </body>
    </html>
    """

@app.route("/add", methods=["GET", "POST"])
def add_user_form():
    if request.method == "POST":
        name = request.form.get("name")
        if name and cur:
            cur.execute("INSERT INTO users (name) VALUES (%s)", (name,))
            conn.commit()
            return f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>User Added</title>
                <style>
                    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                    body {{
                        font-family: 'Segoe UI', sans-serif;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        min-height: 100vh;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    }}
                    .card {{
                        background: white;
                        border-radius: 20px;
                        padding: 50px 40px;
                        text-align: center;
                        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                        max-width: 500px;
                        width: 90%;
                    }}
                    .emoji {{ font-size: 60px; margin-bottom: 20px; }}
                    h1 {{ font-size: 2rem; color: #333; margin-bottom: 10px; }}
                    p {{ color: #666; margin-bottom: 30px; }}
                    .btn {{
                        display: inline-block;
                        margin: 8px;
                        padding: 12px 24px;
                        border-radius: 10px;
                        text-decoration: none;
                        font-weight: bold;
                        transition: transform 0.2s;
                    }}
                    .btn:hover {{ transform: translateY(-2px); }}
                    .btn-primary {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; }}
                    .btn-secondary {{ background: #f5f5f5; color: #333; border: 2px solid #ddd; }}
                </style>
            </head>
            <body>
                <div class="card">
                    <div class="emoji">🎉</div>
                    <h1>{name} added!</h1>
                    <p>The user has been saved to the database successfully.</p>
                    <a href="/add" class="btn btn-primary">➕ Add Another</a>
                    <a href="/users" class="btn btn-secondary">👥 View Users</a>
                </div>
            </body>
            </html>
            """
        return "Please enter a valid name."

    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Add User</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .card {
                background: white;
                border-radius: 20px;
                padding: 50px 40px;
                text-align: center;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                max-width: 500px;
                width: 90%;
            }
            .emoji { font-size: 60px; margin-bottom: 20px; }
            h1 { font-size: 2rem; color: #333; margin-bottom: 10px; }
            p { color: #666; margin-bottom: 30px; }
            input[type="text"] {
                width: 100%;
                padding: 14px 18px;
                border: 2px solid #ddd;
                border-radius: 10px;
                font-size: 1rem;
                margin-bottom: 20px;
                outline: none;
                transition: border 0.2s;
            }
            input[type="text"]:focus { border-color: #667eea; }
            .btn {
                display: inline-block;
                margin: 8px;
                padding: 12px 24px;
                border-radius: 10px;
                text-decoration: none;
                font-weight: bold;
                font-size: 1rem;
                cursor: pointer;
                border: none;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
            .btn-primary {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                width: 100%;
            }
            .btn-back { background: #f5f5f5; color: #333; border: 2px solid #ddd !important; }
            .footer { margin-top: 30px; font-size: 0.8rem; color: #aaa; }
        </style>
    </head>
    <body>
        <div class="card">
            <div class="emoji">👤</div>
            <h1>Add a User</h1>
            <p>Type in a name to add them to the database.</p>
            <form method="POST">
                <input type="text" name="name" placeholder="Enter name e.g. Gloria" autofocus required>
                <button type="submit" class="btn btn-primary">➕ Add User</button>
            </form>
            <br>
            <a href="/" class="btn btn-back">← Back to Home</a>
            <div class="footer">Built with Flask · PostgreSQL · Railway</div>
        </div>
    </body>
    </html>
    """

@app.route("/users")
def get_users():
    if cur:
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        rows = "".join(f"""
            <tr>
                <td>{user[0]}</td>
                <td>{user[1]}</td>
            </tr>
        """ for user in users)

        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>All Users</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: 'Segoe UI', sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }}
                .card {{
                    background: white;
                    border-radius: 20px;
                    padding: 40px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    max-width: 600px;
                    width: 90%;
                }}
                .emoji {{ font-size: 50px; text-align: center; margin-bottom: 15px; }}
                h1 {{ text-align: center; color: #333; margin-bottom: 25px; }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 25px;
                }}
                th {{
                    background: linear-gradient(135deg, #667eea, #764ba2);
                    color: white;
                    padding: 12px;
                    text-align: left;
                }}
                td {{
                    padding: 12px;
                    border-bottom: 1px solid #eee;
                    color: #444;
                }}
                tr:hover td {{ background: #f9f9f9; }}
                .empty {{ text-align: center; color: #aaa; padding: 30px; }}
                .btn {{
                    display: inline-block;
                    margin: 6px;
                    padding: 12px 24px;
                    border-radius: 10px;
                    text-decoration: none;
                    font-weight: bold;
                    transition: transform 0.2s;
                }}
                .btn:hover {{ transform: translateY(-2px); }}
                .btn-primary {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; }}
                .btn-secondary {{ background: #f5f5f5; color: #333; border: 2px solid #ddd; }}
                .actions {{ text-align: center; }}
                .count {{
                    text-align: center;
                    color: #888;
                    font-size: 0.9rem;
                    margin-bottom: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="card">
                <div class="emoji">👥</div>
                <h1>All Users</h1>
                <p class="count">{len(users)} user(s) in the database</p>
                {"<table><tr><th>#</th><th>Name</th></tr>" + rows + "</table>" if users else '<p class="empty">No users yet. Add one!</p>'}
                <div class="actions">
                    <a href="/add" class="btn btn-primary">➕ Add User</a>
                    <a href="/" class="btn btn-secondary">← Home</a>
                </div>
            </div>
        </body>
        </html>
        """
    return "Database not connected"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
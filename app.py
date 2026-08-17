from flask import Flask, request, jsonify, render_template, session
import sqlite3
import secrets

# templates နှင့် static folder လမ်းကြောင်းကို စံနှုန်းအတိုင်း သတ်မှတ်ခြင်း
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = secrets.token_hex(16)
DB_NAME = "database.db"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# templates folder ထဲက index.html ကို စနစ်တကျ ခေါ်ယူခြင်း
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit-form', methods=['POST'])
def submit_form():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)", (name, email, message))
        conn.commit()
        conn.close()
        return jsonify({"status": "Success", "message": "အချက်အလက်များကို အောင်မြင်စွာ သိမ်းဆည်းပြီးပါပြီ။"})
    except Exception as e:
        return jsonify({"status": "Error", "message": "ဒေတာဘေ့စ်အမှားအယွင်း ဖြစ်ပွားခဲ့သည်။"})

@app.route('/admin-login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['logged_in'] = True 
        return jsonify({"status": "Success", "message": "အကောင့်ဝင်ခြင်း အောင်မြင်ပါသည်။"})
    else:
        return jsonify({"status": "Error", "message": "Username သို့မဟုတ် Password မှားယွင်းနေပါသည်။"})

@app.route('/admin-logout', methods=['GET'])
def admin_logout():
    session.pop('logged_in', None)
    return jsonify({"status": "Success", "message": "အကောင့်ထဲမှ ထွက်လိုက်ပါပြီ။"})

@app.route('/get-contacts', methods=['GET'])
def get_contacts():
    if not session.get('logged_in'):
        return jsonify({"status": "Error", "message": "ကျေးဇူးပြု၍ အရင်ဆုံး Log In ဝင်ပေးပါ။"}), 401
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contacts ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()
        contacts_list = []
        for row in rows:
            contacts_list.append({"id": row[0], "name": row[1], "email": row[2], "message": row[3]})
        return jsonify(contacts_list)
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})

@app.route('/delete-contact/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    if not session.get('logged_in'):
        return jsonify({"status": "Error", "message": "ခွင့်ပြုချက်မရှိပါ။"}), 401
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        conn.commit()
        conn.close()
        return jsonify({"status": "Success", "message": "စာရင်းကို ဖျက်ပစ်လိုက်ပါပြီ။"})
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080, debug=True)

from flask import Flask, request, jsonify, send_from_directory
import sqlite3

app = Flask(__name__)
DB_NAME = "database.db"

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

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('.', path)

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
        return jsonify({"status": "Success", "message": "အချက်အလက်များကို ဒေတာဘေ့စ်ထဲသို့ အောင်မြင်စွာ သိမ်းဆည်းပြီးပါပြီ။"})
    except Exception as e:
        return jsonify({"status": "Error", "message": "ဒေတာဘေ့စ်အမှားအယွင်း ဖြစ်ပွားခဲ့သည်။"})

@app.route('/get-contacts', methods=['GET'])
def get_contacts():
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

# 🌟 ဒေတာဘေ့စ်ထဲက ID အလိုက် လှမ်းဖျက်ပေးမည့် API လမ်းကြောင်းအသစ်
@app.route('/delete-contact/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        conn.commit()
        conn.close()
        return jsonify({"status": "Success", "message": "စာရင်းကို ဒေတာဘေ့စ်ထဲမှ ဖျက်ပစ်လိုက်ပါပြီ။"})
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080, debug=True)

import sqlite3

def save_rule(authority, item, decision, reference):
    conn = sqlite3.connect("rules.db")
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO baggage_rules
        (authority, item, decision, reference, approved_by)
        VALUES (?, ?, ?, ?, 'admin')
    """, (authority, item, decision, reference))

    conn.commit()
    conn.close()

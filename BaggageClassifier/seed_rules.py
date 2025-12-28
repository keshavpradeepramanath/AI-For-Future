import sqlite3

conn = sqlite3.connect("rules.db")
cur = conn.cursor()

rules = [
    ("IATA", "phone", "✅ Cabin Allowed", "IATA PED Regulations"),
    ("IATA", "laptop", "✅ Cabin Allowed", "IATA Cabin Baggage Rules"),
    ("IATA", "scissors", "🧳 Check-in Only", "IATA Sharp Objects Policy"),
    ("IATA", "knife", "❌ Not Allowed", "IATA Prohibited Items List"),
    ("IATA", "pen", "✅ Cabin Allowed", "IATA Cabin Baggage Rules")
]

cur.executemany("""
INSERT INTO baggage_rules (authority, item, decision, reference, approved_by)
VALUES (?, ?, ?, ?, 'system')
""", rules)

conn.commit()
conn.close()

print("✅ Sample rules inserted.")

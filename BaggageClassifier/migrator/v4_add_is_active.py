def upgrade(cur):
    # Check existing columns
    cur.execute("PRAGMA table_info(baggage_rules)")
    columns = [row[1] for row in cur.fetchall()]

    if "is_active" not in columns:
        cur.execute("""
            ALTER TABLE baggage_rules
            ADD COLUMN is_active INTEGER DEFAULT 1
        """)

def upgrade(cur):
    cur.execute("""
        ALTER TABLE baggage_rules
        ADD COLUMN confidence_level REAL DEFAULT 1.0
    """)

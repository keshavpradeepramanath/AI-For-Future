def upgrade(cur):
    cur.execute("""
        ALTER TABLE baggage_rules
        ADD COLUMN effective_from DATE
    """)

    cur.execute("""
        ALTER TABLE baggage_rules
        ADD COLUMN effective_to DATE
    """)

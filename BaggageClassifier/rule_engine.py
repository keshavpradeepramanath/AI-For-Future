def evaluate_item(item, attributes, airline, rules):
    iata_rules = rules["IATA"].get(item)

    if not iata_rules:
        return "⚠️ Uncertain", "No official rule found"

    for cond in iata_rules["conditions"]:
        # simplified for demo
        if "battery_wh" in cond:
            if attributes["battery_wh"] <= 100:
                return "✅ Cabin Allowed", iata_rules["reference"]

    airline_override = rules["Airlines"].get(airline, {}).get(item)
    if airline_override:
        return airline_override["override"], "Airline-specific rule"

    return "🧳 Check-in Only", iata_rules["reference"]

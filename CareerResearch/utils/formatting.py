def format_final_plan(raw_text: str) -> str:
    """
    Final formatter with safety fallback.
    Never returns empty text.
    """
    if not raw_text or not raw_text.strip():
        return "[Error] Council returned empty response."

    text = raw_text.strip()

    try:
        text = normalize_heading(text)
        text = clean_bullets(text)
        text = remove_duplicate_lines(text)

        ordered = enforce_section_order(text)

        # 🔥 SAFETY NET
        if ordered.strip():
            return ordered.strip()

        # If section enforcement failed, return cleaned text instead
        return text

    except Exception as e:
        # Absolute fallback
        return f"[Formatting error]\n\n{text}"

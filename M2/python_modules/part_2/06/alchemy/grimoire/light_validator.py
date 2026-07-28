def validate_ingredients(ingredients: str) -> str:
    from .light_spellbook import light_spell_allowed_ingredients

    normalized = ingredients.lower()
    allowed = light_spell_allowed_ingredients()
    is_valid = any(item in normalized for item in allowed)
    status = "VALID" if is_valid else "INVALID"
    return f"{ingredients} - {status}"
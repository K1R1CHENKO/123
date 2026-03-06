def render_hud(player, lighting, mob_count: int) -> str:
    inv = ", ".join(f"{k}:{v}" for k, v in sorted(player.inventory.items.items())) or "empty"
    return (
        f"POS=({player.x},{player.y},{player.z}) "
        f"Sun={lighting.sun_intensity:.2f} "
        f"Mobs={mob_count} "
        f"Inventory=[{inv}]"
    )

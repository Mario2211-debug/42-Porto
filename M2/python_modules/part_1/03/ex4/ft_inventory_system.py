import sys
from typing import Dict


def main() -> None:
    print("=== Inventory System Analysis ===")

    inventory: Dict[str, int] = {}
    seen = set()

    for arg in sys.argv[1:]:
        if ":" not in arg:
            print(f"Error - invalid parameter '{arg}'")
            continue
        try:
            item, qty_str = arg.split(":", 1)
            if not item or not qty_str:
                raise ValueError
            qty = int(qty_str)

            if item in seen:
                print(f"Redundant item '{item}' - discarding")
                continue

            inventory[item] = qty
            seen.add(item)
        except ValueError as e:
            print(f"Quantity error for '{item}': {e}: '{qty_str}'")

    if not inventory:
        print("No valid items in inventory.")
        return

    print(f"Got inventory: {inventory}")

    item_list = list(inventory.keys())
    print(f"Item list: {item_list}")

    total_qty = sum(inventory.values())
    print(f"Total quantity of the {len(inventory)} items: {total_qty}")

    for item, qty in inventory.items():
        percentage = (qty / total_qty) * 100
        print(f"Item {item} represents {percentage:.1f}%")

    most_item = max(inventory.items(),
                    key=lambda x: (x[1], - list(inventory.keys()).index(x[0])))
    least_item = min(inventory.items(),
                     key=lambda x: (x[1], list(inventory.keys()).index(x[0])))

    print(f"Item most abundant: {most_item[0]} with quantity {most_item[1]}")
    print(f"Item least abundant: {least_item[0]} "
          f"with quantity {least_item[1]}")

    inventory["magic_item"] = 1
    print(f"Updated inventory: {inventory}")


if __name__ == "__main__":
    main()

"""A command-line inventory manager created for CPS 310

Author: Nicolas Coffman
Course: CPS 310

"""

INVENTORY_FILE = "inventory.txt"

def display_menu():
    """Display the available Inventory Manager options."""
    print("\n\nInventory Manager")
    print("1. View inventory")
    print("2. Add an item")
    print("3. Update an item quantity")
    print("4. Remove an item")
    print("5. Search inventory")
    print("6. View inventory summary")
    print("7. Exit")

def view_inventory(inventory):
    """Display all entries in the inventory"""
    if not inventory:
        print("No inventory items found.")
        return

    print("\nInventory Entries:")

    for number, inventory in enumerate(inventory, start=1):
        print(f"{number}. {inventory["name"]} | {inventory["category"]} | Quantity: {inventory["quantity"]}", end="")


def load_inventory(filename):
    """Load inventory from a text file and return a completed list"""
    inventory = []

    try:
        with open(filename, "r") as file:
            for line in file:
                if not line.strip():
                    continue
                split = line.split("|")
                entry = {"name": split[0], "category": split[1], "quantity": split[2]}
                inventory.append(entry)
    except FileNotFoundError:
        return []
    return inventory


def main():
    """Run the Inventory manager enu until the user chooses to exit."""
    inventory = load_inventory(INVENTORY_FILE)

    while True:
        display_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            view_inventory(inventory)
        elif choice == "2":
            pass
        elif choice == "3":
            pass
        elif choice == "4":
            pass
        elif choice == "5":
            pass
        elif choice == "6":
            pass
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Please enter a valid option.")


if __name__ == "__main__":
    main()


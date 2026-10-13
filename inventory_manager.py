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

def add_item(inventory):
    illegal = "|"
    name = input("Item's name: ").strip()
    
    if not name:
        print("The item name cannot be empty.")
        return
    elif illegal in name:
        print("The item name may not contain '|'")
        return

    #Ensuring no conflicting name values
    value_exists = any(
        i["name"].lower() == name.lower()
        for i in inventory
    )
    if value_exists:
        print(f"Rejected: A variation of '{name}' already exists.")
        return
    
    category = input("Item's category: ").strip()
    
    if not category:
        print("The category cannot be empty.")
        return
    elif illegal in category:
        print("The category may not contain '|'")
        return
    
    try:
        quantity = int(input("Item's quantity: "))
    except ValueError:
        print("Quantity must be a whole number.")
        return
    if (quantity < 0):
        print("Quantity cannot be negative.")
        return

    #If all of those checks pass, add the new item to the inventory
    entry = {"name": name, "category": category, "quantity": quantity}
    inventory.append(entry)
    save_inventory(inventory, INVENTORY_FILE)
    print("Item added succesfully.")



def view_inventory(inventory):
    """Display all entries in the inventory"""
    if not inventory:
        print("No inventory items found.")
        return

    print("\nInventory Entries:")

    for number, inventory in enumerate(inventory, start=1):
        print(f"{number}. {inventory["name"]} | {inventory["category"]} | Quantity: {inventory["quantity"]}")


def load_inventory(filename):
    """Load inventory from a text file and return a completed list"""
    inventory = []

    try:
        with open(filename, "r") as file:
            for line in file:
                if not line.strip():
                    continue
                split = line.strip().split("|")
                entry = {"name": split[0], "category": split[1], "quantity": split[2]}
                inventory.append(entry)
    except FileNotFoundError:
        return []
    return inventory

def save_inventory(inventory, filename):
    """Save all inventory items to a text file"""
    with open(filename, "w") as file:
        for item in inventory:
            file.write(f"{item.get('name')}|{item.get('category')}|{item.get('quantity')}\n")

def main():
    """Run the Inventory manager enu until the user chooses to exit."""
    inventory = load_inventory(INVENTORY_FILE)

    while True:
        display_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            view_inventory(inventory)
        elif choice == "2":
            add_item(inventory)
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


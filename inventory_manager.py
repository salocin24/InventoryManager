"""A command-line inventory manager created for CPS 310

Project: Inventory Manager | HW1
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
    """Add an item/entry to the inventory"""
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

def remove_item(inventory):
    """Removing an item from the passed in inventory"""
    view_inventory(inventory)
    
    if not inventory:
        print("Inventory is empty.")
        return
    
    try:
        item = int(input("\nEnter the item number to remove: "))
    except ValueError:
        print("Item number must be a whole number.")
        return
        
    if item < 1 or item > len(inventory):
        print("Must be a valid item number.")
        return


    removed_item = inventory.pop(item - 1)
    print(f"Item removed: {removed_item['name']}")
    save_inventory(inventory, INVENTORY_FILE)

def update_quantity(inventory):
    """Updating the quantity of a given item number from the inventory"""

    view_inventory(inventory)

    if not inventory:
        print("Inventory is empty.")
        return

    try:
        item = int(input("\nEnter the item number to update: "))
    except ValueError:
            print("Item number must be a whole number.")
            return
    
    if item < 1 or item > len(inventory):
        print("Must be a valid item number.")
        return
    
    try:
        new_quantity = int(input("Enter the new quantity: "))
    except ValueError:
        print("New quantity must be a whole number.")
        return
    if (new_quantity < 0):
        print("New quantity cannot be negative.")
        return

    inventory[item - 1]["quantity"] = new_quantity
    save_inventory(inventory, INVENTORY_FILE)
    print(f"Updated '{inventory[item - 1]['name']}' to quantity {new_quantity}.")

def search_inventory(inventory):
    """Searches the inventory given a full or partial item name"""
    name = input("Enter all or part of an item name you're searching for: ").strip()

    if not name:
        print("Search term cannot be empty.")
        return

    matches = []
    for i in inventory:
        if name.lower() in i["name"].lower():
            matches.append(i)

    if not matches:
        print(f"No items found matching '{item}'.")
        return

    print("\nMatching Items:")
    for number, item in enumerate(matches, start=1):
        print(f"{number}. {item["name"]} | {item["category"]} | Quantity: {item["quantity"]}")

def display_summary(inventory):
    """Displays general summarized information of a given inventory"""
    low_stock_threshold = 5

    unique = len(inventory)
    total_quantity = 0
    low_stock_items = 0

    # Fill a temp dictionary with every category so we can count items per
    category_counts = {}
    for item in inventory:
        category = item["category"].lower()
        category_counts[category] = 0

    for item in inventory:
        quantity = int(item["quantity"])
        total_quantity += quantity
        if quantity < low_stock_threshold:
            low_stock_items += 1

        category = item["category"].lower()
        category_counts[category] += 1

    print("\nInventory Summary")
    print(f"Unique items: {unique}")
    print(f"Total quantity: {total_quantity}")
    print(f"Low-stock items: {low_stock_items}")

    print("\nItems per category:")
    for category, count in category_counts.items():
        print(f"{category}: {count}")
    

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
            update_quantity(inventory)
        elif choice == "4":
            remove_item(inventory)
        elif choice == "5":
            search_inventory(inventory)
        elif choice == "6":
            display_summary(inventory)
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Please enter a valid option.")


if __name__ == "__main__":
    main()


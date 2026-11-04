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

##ADD ITEM SECTION
#VALIDATE NEW ITEM HELPER
def validate_new_item(inventory, name, category, quantity):
    illegal = "|"
    name = name.strip()
    category = category.strip()

    if not name:
        raise ValueError("The item name cannot be empty.")
    if illegal in name:
        raise ValueError("The item name may not contain '|'")

    #Ensuring no conflicting name values
    value_exists = any(
        i["name"].lower() == name.lower()
        for i in inventory
    )
    if value_exists:
        raise ValueError(f"Rejected: A variation of '{name}' already exists.")

    if not category:
        raise ValueError("The category cannot be empty.")
    if illegal in category:
        raise ValueError("The category may not contain '|'")

    try:
        quantity = int(quantity)
    except ValueError:
        raise ValueError("Quantity must be a whole number.")
    if quantity < 0:
        raise ValueError("Quantity cannot be negative.")

    return {"name": name, "category": category, "quantity": quantity}    

def add_item(inventory):
    """Add an item/entry to the inventory"""
    name = input("Item's name: ")
    category = input("Item's category: ")
    quantity = input("Item's quantity: ")

    try:
        entry = validate_new_item(inventory, name, category, quantity)
    except ValueError as error:
        print(error)
        return

    #If all of those checks pass, add the new item to the inventory
    inventory.append(entry)
    save_inventory(inventory, INVENTORY_FILE)
    print("Item added succesfully.")

##REMOVE ITEMS SECTION
#REMOVE ITEM HELPER
def remove_item_by_number(inventory, item_number):
    if item_number < 1 or item_number > len(inventory):
        return None
    return inventory.pop(item_number - 1)


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
        
    removed_item = remove_item_by_number(inventory, item)

    if removed_item is None:
        print("Must be a valid item number.")
        return

    print(f"Item removed: {removed_item['name']}")
    save_inventory(inventory, INVENTORY_FILE)

##UPDATE QUANTITY SECTION
#UPDATE ITEM QUANT HELPER
def update_item_quantity(inventory, item_number, new_quantity):
    if item_number < 1 or item_number > len(inventory):
        raise ValueError("Must be a valid item number.")
    if new_quantity < 0:
        raise ValueError("New quantity cannot be negative.")

    inventory[item_number - 1]["quantity"] = new_quantity
    return inventory[item_number - 1]

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
    
    try:
        new_quantity = int(input("Enter the new quantity: "))
    except ValueError:
        print("New quantity must be a whole number.")
        return
    
    try:
        updated_item = update_item_quantity(inventory, item, new_quantity)
    except ValueError as error:
        print(error)
        return

    save_inventory(inventory, INVENTORY_FILE)
    print(f"Updated '{inventory[item - 1]['name']}' to quantity {new_quantity}.")

## SEARCH SECTION
##SEARCH HELPER
def find_matching_items(inventory, search_term):
    search_term = search_term.strip().lower()
    if not search_term:
        return []
    matches = []
    for i in inventory:
        if search_term.lower() in i["name"].lower():
            matches.append(i)
    return matches


##SEARCH
def search_inventory(inventory):
    """Searches the inventory given a full or partial item name"""
    name = input("Enter all or part of an item name you're searching for: ").strip()

    if not name:
        print("Search term cannot be empty.")
        return

    matches = find_matching_items(inventory, name)

    if not matches:
        print(f"No items found matching '{name}'.")
        return

    print("\nMatching Items:")
    for number, item in enumerate(matches, start=1):
        print(f"{number}. {item["name"]} | {item["category"]} | Quantity: {item["quantity"]}")

##SUMMARY SECTION
#CALCULATE SUMMARY HELPER
def calculate_summary(inventory):
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

    return {
        "unique_items": unique,
        "total_quantity": total_quantity,
        "low_stock_items": low_stock_items,
        "category_counts": category_counts,
    }

def display_summary(inventory):
    """Displays general summarized information of a given inventory"""
    summary = calculate_summary(inventory)

    print("\nInventory Summary")
    print(f"Unique items: {summary['unique_items']}")
    print(f"Total quantity: {summary['total_quantity']}")
    print(f"Low-stock items: {summary['low_stock_items']}")

    print("\nItems per category:")
    for category, count in summary["category_counts"].items():
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
                entry = {"name": split[0], "category": split[1], "quantity": int(split[2])}
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


# Inventory Manager

A command-line inventory manager written in Python for CPS 310 (HW1).

**Author:** Nicolas Coffman
**Course:** CPS 310

## Project Description

Inventory Manager is a menu-driven Python program for tracking items, their categories, and their quantities. The inventory is stored in a plain text file (`inventory.txt`), so changes persist between runs. Every change made through the program (add, update, remove) is saved to the file immediately.

## Current Features

- View every item in the inventory as a numbered list
- Add a new item with a name, category, and quantity
- Update the quantity of an existing item
- Remove an item by its number
- Search for items by full or partial name (case-insensitive)
- View a summary: unique item count, total quantity, low-stock count, and items per category
- Input validation:
  - Names and categories cannot be empty or contain `|`
  - Quantities must be whole numbers and cannot be negative
  - Duplicate item names (case-insensitive) are rejected
  - Item numbers must be within the valid range
- Automatic saving to `inventory.txt` after every change

## Requirements

- **Python 3.12 or newer** (the program uses f-strings with nested double quotes, which require 3.12+)
- No third-party packages; only the Python standard library is used

Check your Python version:

```bash
python3 --version
```

## Project Files

| File | Description |
|------|-------------|
| `inventory_manager.py` | The main program: menu, inventory operations, and file load/save logic |
| `inventory.txt` | The inventory data file, read on startup and rewritten after each change |
| `README.md` | Project documentation (this file) |

## Inventory Data Format

Each line in `inventory.txt` represents one item, with three fields separated by a pipe (`|`):

```
name|category|quantity
```

Example:

```
Laptop Charger|Electronics|8
Printer Paper|Office Supplies|25
Dry-Erase Markers|Classroom Supplies|4
Raspberry Pi|Electronics|3
Printer Ink|Office Supplies|2
```

- `name` — the item's name (cannot contain `|`)
- `category` — the item's category (cannot contain `|`)
- `quantity` — a non-negative whole number

Blank lines are skipped when the file is loaded. If `inventory.txt` does not exist, the program starts with an empty inventory and creates the file the first time an item is added.

## Running the Program

1. Clone the repository:

   ```bash
   git clone https://github.com/salocin24/InventoryManager.git
   cd InventoryManager
   ```

2. Run the program from inside the project folder:

   **Linux / macOS:**

   ```bash
   python3 inventory_manager.py
   ```

   **Windows (PowerShell or Command Prompt):**

   ```powershell
   py inventory_manager.py
   ```

> **Note:** Run the program from the project folder. `inventory.txt` is opened relative to the current working directory, so running it from elsewhere will start with an empty inventory.

## Menu Options

| Option | Action |
|--------|--------|
| 1 | View inventory — lists all items with their number, category, and quantity |
| 2 | Add an item — prompts for name, category, and quantity |
| 3 | Update an item quantity — choose an item by number and enter a new quantity |
| 4 | Remove an item — choose an item by number to delete it |
| 5 | Search inventory — find items by full or partial name |
| 6 | View inventory summary — totals, low-stock count (quantity below 5), and items per category |
| 7 | Exit — closes the program |

## Sample Interaction

Viewing the inventory, updating a quantity, and checking the summary:

```
Inventory Manager
1. View inventory
2. Add an item
3. Update an item quantity
4. Remove an item
5. Search inventory
6. View inventory summary
7. Exit
Choose an option: 3

Inventory Entries:
1. Laptop Charger | Electronics | Quantity: 8
2. Printer Paper | Office Supplies | Quantity: 25
3. Dry-Erase Markers | Classroom Supplies | Quantity: 4
4. Raspberry Pi | Electronics | Quantity: 3
5. Printer Ink | Office Supplies | Quantity: 2

Enter the item number to update: 5
Enter the new quantity: 10
Updated 'Printer Ink' to quantity 10.

...
Choose an option: 5
Enter all or part of an item name you're searching for: printer

Matching Items:
1. Printer Paper | Office Supplies | Quantity: 25
2. Printer Ink | Office Supplies | Quantity: 10

...
Choose an option: 6

Inventory Summary
Unique items: 5
Total quantity: 50
Low-stock items: 2

Items per category:
electronics: 2
office supplies: 2
classroom supplies: 1

...
Choose an option: 7
Goodbye!
```

## Testing Summary

The program was tested manually with 14 test cases covering every menu option, invalid input, a missing data file, and persistence between runs. Full details are in [`TESTING.md`](TESTING.md).

**Results:** All 14 tests pass.

**Areas covered:**
- **Adding items:** valid input, plus rejection of empty names, duplicate names, non-numeric quantities, and negative quantities
- **Updating and removing:** valid changes are saved to the file; invalid item numbers are rejected
- **Searching:** case-insensitive partial matches (e.g., `rasp` finds "Raspberry Pi") and searches with no matches
- **Viewing and summary:** empty-inventory message and correct summary totals
- **File handling:** the program starts cleanly without `inventory.txt`, creates it on first save, and keeps changes after a restart

**Bug found and fixed:** Searching for a term with no matches originally crashed the program (test 12). After the fix, it now displays a "No items found" message, and the retest passed.

## Git/GitHub Development Summary

The project was developed using Git for version control and hosted on GitHub.

Git commit history:
- Completed the TESTING.md file and corrected my searching function
- Merge pull request #2 from salocin24/feature/inventory-search
- (origin/feature/inventory-search) Added search_inventory(inventory) method
- Inventory search rollback to compelte github issue requirements
- Added the display_summary(inventory) and search_inventory(inventory) methods.
- Added the remove_item(inventory) method.
- Added update_quantity(inventory) - introduces the functinoality to update an existing entry's quantity.
- Added add_item(inventory) and save_inventory(inventory, filename) methods with extensive type/input checking.
- Constructed the boiler plate main() and display_menu(). Also added load_inventory(filename) and view_inventory(inventory)
- first commit

## Known Limitations

- Item names and categories cannot contain the `|` character, since it is used as the file delimiter.
- Item names and categories cannot be edited after an item is added; only the quantity can be changed.
- Item numbers are based on list position, so they shift after an item is removed.
- Categories are grouped case-insensitively in the summary and displayed in lowercase.
- A malformed line in `inventory.txt` (for example, missing a field) will cause the program to crash on startup.
- The low-stock threshold is fixed at 5 and cannot be changed by the user.
- The data file is located relative to the current working directory, not the script's location.

## Possible Future Improvements

- Allow editing an item's name and category
- Let the user set the low-stock threshold, or list which items are low-stock
- Skip or report malformed lines in `inventory.txt` instead of crashing
- Sort the inventory by name, category, or quantity
- Search by category as well as name
- Store data in CSV or JSON for more flexible formatting
- Add automated unit tests
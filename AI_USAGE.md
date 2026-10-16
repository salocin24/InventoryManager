# AI Usage Report

## Tools Used

- Claude (Anthropic), through the claude.ai chat interface

## How AI Was Used

I wrote most of the program myself and used Claude mainly to review my code against the assignment requirements and to help debug problems. Specifically:

- **Requirement checks:** I pasted each assignment requirement with my code and asked whether it met every point. This was done for `add_item()`, `update_quantity()`, `remove_item()`, and `search_inventory()`.
- **Debugging:** blank lines appearing in the output and saved file, a broken duplicate-name check, and a `TypeError` crash in `search_inventory()`.
- **New code:** Claude provided a first version of `search_inventory()` and helped me build the category-count dictionary in `display_summary()`.
- **Explanations:** I asked Claude to explain how a list comprehension works.
- **Documentation:** Claude drafted `README.md`, which I reviewed and edited. The testing summary in the README was condensed from my own `TESTING.md`.

## Example Prompts

1. *"all of the error checking is done. how does it look"* (with my `add_item()` code)
2. *"When saving my updated inventory to the .txt, it introduces blank new lines into the text file between each entry. also, when printing my dictionary in view_inventory(inventory) there are blank lines between each entry, even if there are not blank lines in the .txt file. what should i do"*
3. *"Requirement 5: Update an Item Quantity ... Do i meet the requirement?"* (with the full requirement text and my code)
4. *"explain the matches = line, expand it instead of putting it all in one line"*
5. *"how can i fill the dictionary before the loop with each category thats present in the inventory"*

## Suggestions Accepted

- **Duplicate check fix:** My original check compared the new name against every value in each item (name, category, and quantity), so a name like "Electronics" would be wrongly rejected. I changed it to compare against item names only.
- **Blank-line fix:** Lines read from the file still ended in `\n`, which carried into the quantity field. I added `.strip()` before splitting each line in `load_inventory()`.
- **`update_quantity()` fixes:** My empty-inventory check compared the function itself to `None`, which never worked. I replaced it with `if not inventory`. I also fixed a wrong error message and added the item name and new quantity to the confirmation.
- **`remove_item()` confirmation:** Changed it to print only the removed item's name instead of the whole dictionary.
- **Search crash:** A print line copied from `view_inventory()` used `inventory` instead of the loop variable `item`. Claude spotted the cause from the traceback.

## Suggestions Rejected or Modified

- **List comprehension in `search_inventory()`:** Claude's version built the list of matches in one line with a list comprehension. I had it expanded into a regular `for` loop, which I understand better and is the version in my final code. I also kept my own variable names and prompt text.
- **Category counting:** Claude first suggested an `if/else` that adds a category the first time it appears. I wanted a different approach: filling the dictionary with every category set to 0 before the main loop, so the loop only has to add 1.
- **Quantity type in `display_summary()`:** Claude's version added `item["quantity"]` directly to the total. This was incomplete, because quantities loaded from the file are strings. I converted them with `int()` before adding.
- **README:** The first draft included a testing table Claude made up from the code. I replaced it with a summary of my actual tests from `TESTING.md`. I also checked the run commands for my operating system and filled in my real Git history.

## Verification

- I ran every AI-assisted function myself before keeping it, using both valid and invalid input.
- I tested the full program with the 14 manual test cases in `TESTING.md`, covering every menu option, invalid input, a missing data file, and persistence between restarts. All tests pass.
- One test (searching with no matches) originally failed with a crash. I fixed it and re-ran the test until it passed.
- For the README, I checked each command and description against how the program actually behaves and reviewed the rendered page on GitHub.

## Code Understanding

### `search_inventory()`

The function asks for a search term and strips any spaces off. If nothing is left it shows an error and goes back to the main menu. If not, it loops through every item and lowercases both the search term and the item's name making it case insensitive. It uses `in` to check whether the term appears anywhere inside the name, which is what makes partial matches work like how `rasp` matches "Raspberry Pi." Each match is added to a list. If the list is empty, the function prints a "No items found" message. If not, it prints each match with a number using `enumerate()`.

### `display_summary()`

The unique item count is just the length of the inventory list and to count items per category, the function first loops through the inventory and adds every category to a dictionary with a starting value of 0. The .lower() function is performed on all categories so "Electronics" and "electronics" count as the same one. A second loop then goes through each item: it converts the quantity to an `int`, adds it to the total, counts the item as low-stock if its quantity is under 5, and adds 1 to its category's count. Finally, it prints the totals and each category with its count nicely.
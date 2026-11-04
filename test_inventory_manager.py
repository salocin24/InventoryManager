import pytest
from inventory_manager import *

@pytest.fixture
def inventory():
    ## 
    return [
        {"name": "Laptop Charger", "category": "Electronics", "quantity": 8},
        {"name": "Printer Paper", "category": "Office Supplies", "quantity": 25},
        {"name": "Raspberry Pi", "category": "Electronics", "quantity": 3},
        {"name": "USB Cable", "category": "Electronics", "quantity": 12},
    ]

#1.
def test_load_inventory_reads_valid_file(tmp_path, inventory):
    #Arrange
    test_file = tmp_path / "inventory2.txt"
    test_file.write_text(
        "Laptop Charger|Electronics|8\nPrinter Paper|Office Supplies|25\nRaspberry Pi|Electronics|3\nUSB Cable|Electronics|12",
        encoding="utf-8",
    )
    #Act
    result = load_inventory(test_file)

    #Assert
    #entry = {"name": split[0], "category": split[1], "quantity": split[2]}
    assert result == inventory
        # {"name": "Laptop Charger", "category": "Electronics", "quantity": 8},
        # {"name": "Printer Paper", "category": "Office Supplies", "quantity": 25},
        # {"name": "Raspberry Pi", "category": "Electronics", "quantity": 3},

#2.
def test_load_converts_quantities_to_int(tmp_path):
    #Arrange
    test_file = tmp_path / "inv.txt"
    test_file.write_text("Drill|Tools|7\n", encoding="utf-8")

    #Act
    result = load_inventory(test_file)

    #Assert
    assert result[0]["quantity"] == 7
    assert isinstance(result[0]["quantity"], int)

#3.
def test_load_skips_blank_lines(tmp_path):
    #Arrange
    test_file = tmp_path / "inv.txt"
    test_file.write_text("Drill|Tools|7\n\n     \nSaw|Tools|2\n", encoding="utf-8")

    #Act
    result = load_inventory(test_file)

    #Assert
    assert result[0]["name"] == "Drill"
    assert result[1]["name"] == "Saw"

#4.
def test_load_missing_file_returns_empty(tmp_path):
    #Arrange: a tmp_path file that was never created
    #Act/Assert
    assert load_inventory(tmp_path / "does_not_exist.txt") == []

#5.
## FILE SAVING SECTIONN
def test_save_writes_pipe_format(tmp_path, inventory):
    #Arrange
    test_file = tmp_path / "inv.txt"

    #Act
    save_inventory(inventory, test_file)

    #Assert
    assert test_file.read_text() == (
        "Laptop Charger|Electronics|8\n"
        "Printer Paper|Office Supplies|25\n"
        "Raspberry Pi|Electronics|3\n"
        "USB Cable|Electronics|12\n"
    )

#6.
def test_save_empty_inventory_writes_empty_file(tmp_path):
    #Arrange
    test_file = tmp_path / "inv.txt"
    
    #Act
    save_inventory([], test_file)

    #Assert
    assert test_file.read_text() == ""

#7. 
def test_save_then_load_round_trip(tmp_path, inventory):
    #Arrange
    test_file = tmp_path / "inv.txt"
    
    #Act
    save_inventory(inventory, test_file)
    result = load_inventory(test_file)

    #Assert
    assert result == inventory

##SEARCH SECTION
#8.
def test_search_exact_and_partial(inventory):
    #Arrange: inventory fixture
    #Act/Assert
    assert find_matching_items(inventory, "Raspberry Pi") == [inventory[2]]
    assert find_matching_items(inventory, "Charg") == [inventory[0]]

#9.
def test_search_ignores_case_and_returns_multiple(inventory):
    #Arrange: inventory fixture
    #Act/Assert
    #should match with laptop charger and printer paper
    assert find_matching_items(inventory, "AP") == [inventory[0], inventory[1]]

#10.
def test_search_no_match_and_blank_terms_return_empty(inventory):
    #Arrange: inventory fixture
    #Act/Assert
    assert find_matching_items(inventory, "Keyboard") == []
    assert find_matching_items(inventory, "") == []
    assert find_matching_items(inventory, "     ") == []

##REMOVE SECTION
#11.
def test_remove_first_middle_last(inventory):
    #Arrange
    first = list(inventory)
    middle = list(inventory)
    last = list(inventory)

    #Act
    remove_item_by_number(first, 1)
    remove_item_by_number(middle, 2)
    remove_item_by_number(last, 4)

    #Assert
    assert [i["name"] for i in first] == ["Printer Paper", "Raspberry Pi", "USB Cable"]
    assert [i["name"] for i in middle] == ["Laptop Charger", "Raspberry Pi", "USB Cable"]
    assert [i["name"] for i in last] == ["Laptop Charger", "Printer Paper", "Raspberry Pi"]

#12.
#Arrange
@pytest.mark.parametrize(
    "item_number",
    [0, -1, 5],
    ids=["zero", "negative", "past_end"],
)
def test_remove_rejects_invalid_item_number(inventory, item_number):
    #Assert/Act
    assert remove_item_by_number(inventory, item_number) is None
    assert len(inventory) == 4

##UPDATE SECTIONN
#13.
def test_update_changes_only_target_and_accepts_zero(inventory):
    #Arrange: inventory fixture
    #Act
    update_item_quantity(inventory, 2, 40)
    update_item_quantity(inventory, 1, 0)

    #Assert
    assert inventory[2 - 1]["quantity"] == 40
    assert inventory[1 - 1]["quantity"] == 0

#14.
@pytest.mark.parametrize(
    "item_number",
    [0, -1, 5],
    ids=[
        "zero", "negative", "past_end"
    ],
)
def test_update_rejects_invalid_item_number(inventory, item_number):
    #Arrange: inventory fixture + item_number from parametrize
    #Act/Assert
    with pytest.raises(ValueError):
        update_item_quantity(inventory, item_number, 10)

#15.
def test_update_rejects_negative_quantity(inventory):
    #Arrange: inventory fixture
    #Act/Assert
    with pytest.raises(ValueError):
        update_item_quantity(inventory, 1, -5)

    #Assert
    assert inventory[0]["quantity"] == 8
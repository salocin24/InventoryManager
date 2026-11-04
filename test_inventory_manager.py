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

##ADD ITEM VALIDATION
#16.
def test_validate_accepts_normal_item(inventory):
    #Arrange: inventory fixture
    #Act
    result = validate_new_item(inventory, " Drill ", " Tools ", "7")

    #Assert
    assert result == {"name": "Drill", "category": "Tools", "quantity": 7}

#17.
@pytest.mark.parametrize(
    "name, category, quantity",
    [
        ("", "Tools", "3"),
        ("Drill", "", "3"),
        ("Dr|ll", "Tools", "3"),
        ("Drill", "To|ols", "3"),
        ("Drill", "Tools", "-1"),
        ("Drill", "Tools", "abc"),
        ("Raspberry Pi", "Tools", "3"),
        ("RASPBERRY PI", "Tools", "3"),
    ],
    ids=[
        "empty_name",
        "empty_category",
        "pipe_in_name",
        "pipe_in_category",
        "negative_quantity",
        "nonnumeric_quantity",
        "duplicate_name",
        "duplicate_different_case",
    ],
)
def test_validate_rejects_invalid_item(inventory, name, category, quantity):
    #Arrange: inventory fixture + bad values from parametrize
    #Act/Assert
    with pytest.raises(ValueError):
        validate_new_item(inventory, name, category, quantity)

##SUMMARY SECTION
#18.
def test_summary_values(inventory):
    #Arrange: inventory fixture
    #Act
    summary = calculate_summary(inventory)

    #Assert
    assert summary["unique_items"] == 4
    assert summary["total_quantity"] == 48
    assert summary["low_stock_items"] == 1
    assert summary["category_counts"] == {"electronics": 3, "office supplies": 1}

#19.
def test_summary_empty_inventory():
    #Arrange: empty inventory
    #Act/Assert
    assert calculate_summary([]) == {
        "unique_items": 0,
        "total_quantity": 0,
        "low_stock_items": 0,
        "category_counts": {},
    }

#20.
@pytest.mark.parametrize(
    "quantity, expected_low",
    [(4, 1), (5, 0)],
    ids=["four_is_low", "five_is_not_low"],
)
def test_low_stock_boudary(quantity, expected_low):
    #Arrange
    item = [{"name": "Widget", "category" : "Parts", "quantity": quantity}]

    #Act/Assert
    assert calculate_summary(item)["low_stock_items"] == expected_low
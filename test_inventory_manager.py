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


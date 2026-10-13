from pathlib import Path

from services.menu_export_service import export_menu_records


def test_export_to_csv_and_json(tmp_path):
    records = [{"original_name": "Paneer Tikka", "translated_name": "Paneer Tikka", "status": "fallback"}]

    csv_path = tmp_path / "menu.csv"
    json_path = tmp_path / "menu.json"

    assert export_menu_records(records, "csv", str(csv_path)).endswith("menu.csv")
    assert export_menu_records(records, "json", str(json_path)).endswith("menu.json")

    csv_text = csv_path.read_text(encoding="utf-8")
    json_text = json_path.read_text(encoding="utf-8")

    assert "original_name" in csv_text
    assert "Paneer Tikka" in json_text

from database.menu_repository import delete_session, get_session, list_sessions, save_session


def test_database_init_and_session_lifecycle():
    session_id = save_session("Test menu", "English", "Hindi", ["Paneer Tikka", "Biryani"], notes="demo")

    sessions = list_sessions()
    assert any(item["id"] == session_id for item in sessions)

    saved = get_session(session_id)
    assert saved["title"] == "Test menu"
    assert saved["menu_data"] == ["Paneer Tikka", "Biryani"]

    assert delete_session(session_id) is True
    assert get_session(session_id) is None

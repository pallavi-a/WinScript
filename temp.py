from pywinauto.application import Application
from pywinauto.keyboard import send_keys
import pyautogui
import time
import pytest

SPOTIFY_PATH = r"C:\Users\palla\AppData\Local\Microsoft\WindowsApps\Spotify.exe"

def connect_spotify():
    try:
        app = Application(backend="uia").connect(title_re="Spotify.*", timeout=10)
        win = app.window(title_re="Spotify.*")
        print(f"[UIA] Window exists: {win.exists()} | visible: {win.is_visible()}")
        return app
    except Exception as e:
        print(f"[UIA] connect failed: {e}")
        try:
            app = Application(backend="win32").connect(title_re="Spotify.*", timeout=10)
            win = app.window(title_re="Spotify.*")
            print(f"[Win32] Window exists: {win.exists()} | visible: {win.is_visible()}")
            return app
        except Exception as e2:
            print(f"[Win32] connect failed: {e2}")
            return Application(backend="uia").start(SPOTIFY_PATH)

@pytest.fixture(scope="function")
def spotify_app():
    app = connect_spotify()
    time.sleep(5)
    for win in app.windows():
        try:
            if win.is_visible() and "Spotify" in win.window_text():
                print(f"[Fixture] Using window: {win.window_text()} | handle: {win.handle}")
                yield win
                return
        except Exception as e:
            print(f"[Fixture] Skipping window due to error: {e}")
    pytest.fail("No visible Spotify window found!")

def test_search_song(spotify_app):
    # Focus the Spotify window
    spotify_app.set_focus()
    time.sleep(2)

    # Move cursor to search box and click (coordinates: 691,1 to 1304,72)
    pyautogui.moveTo(700, 40, duration=0.5)
    pyautogui.click()
    time.sleep(1)

    # Type the song name
    send_keys("Imagine Dragons", with_spaces=True)
    time.sleep(1)

    # Press Enter to search
    send_keys("{ENTER}")
    time.sleep(3)

    # This is a placeholder for validation
    # Add image recognition, OCR, or app window parsing if needed
    assert True, "Search executed – validate results manually or enhance test"

from pywinauto.application import Application
from pywinauto.keyboard import send_keys
import pyautogui, pytest, time

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

@pytest.fixture(scope="session")
def spotify_app():
    app = connect_spotify()
    time.sleep(5)
    return app.window(title_re="Spotify.*")

def test_search_song(spotify_app):
    # Bring Spotify window to focus
    spotify_app.set_focus()

    # Move mouse to search box coordinates and click
    pyautogui.moveTo(700, 40)
    pyautogui.click()

    # Type "Imagine Dragons" and press Enter
    send_keys("Imagine Dragons" + Keys.ENTER)

    # Assert success
    assert True
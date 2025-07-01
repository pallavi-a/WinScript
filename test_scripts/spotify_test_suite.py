from pywinauto.application import Application
from pywinauto.keyboard import send_keys
import pytest, time

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
    # do NOT close Spotify

def test_browse_playlists(spotify_app):
    spotify_app.set_focus()
    send_keys("p")
    time.sleep(2)
    assert "Browse playlists" in spotify_app.window_text(), "Playlist browsing not available"

def test_search_song(spotify_app):
    spotify_app.set_focus()
    send_keys("s")
    time.sleep(2)
    send_keys("title of the song")
    time.sleep(2)
    assert "title of the song" in spotify_app.window_text(), "Song not found in results"

def test_find_artist(spotify_app):
    spotify_app.set_focus()
    send_keys("a")
    time.sleep(2)
    send_keys("name of the artist")
    time.sleep(2)
    assert "name of the artist" in spotify_app.window_text(), "Artist not found in results"
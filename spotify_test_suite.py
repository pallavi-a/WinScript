from pywinauto.application import Application
from pywinauto.keyboard import send_keys
import pytest, time, os

#comment added new update 8

SPOTIFY_PATH = os.path.join(os.environ['APPDATA'], 'Local', 'Microsoft', 'WindowsApps', 'Spotify.exe')

def connect_spotify():
    try:
        app = Application(backend="uia").connect(title_re="Spotify.*", timeout=10)
        return app
    except Exception as e:
        try:
            app = Application(backend="win32").connect(title_re="Spotify.*", timeout=10)
            return app
        except Exception as e2:
            return Application(backend="uia").start(SPOTIFY_PATH)

@pytest.fixture(scope="function")
def spotify_app():
    app = connect_spotify()
    time.sleep(5)
    for win in app.windows():
        if win.is_visible() and "Spotify" in win.window_text():
            yield win
            break
    else:
        pytest.fail("No visible Spotify window found!")

@pytest.mark.parametrize("tc, title", [(1, "As a user, I should be able to navigate to the search bar using the Tab key..."), (2, "Given a playlist open on the desktop application...")])
def test_spotify_playback(spotify_app, tc, title):
    spotify_app.set_focus()

    # Step 1: Focus on the search bar and input song title
    send_keys('{TAB}')  # Move to the first focusable element (search bar)
    send_keys(title[2].replace(" ", "{ENTER}") + '{ENTER}')  # Type in the song title and press Enter

    # Step 2: Verify that the track is selected
    send_keys('{TAB}')  # Move to the next focusable element (selected track)
    assert spotify_app.get_focused_control().texts()[0].replace("\n", "") == title[1]  # Check if the selected track matches the expected one

    # Step 3: Confirm that clicking the Play button initiates playback of the song
    send_keys('{SPACE}')  # Start playback by pressing Spacebar
    time.sleep(10)  # Wait for the song to start playing

    assert spotify_app.get_focused_control().texts()[0] == "Play" or spotify_app.get_focused_control().texts()[0] == "Pause"  # Check if the Play button changed its state (play -> pause)

# from flask import Flask, render_template_string, request, redirect, url_for, send_file
# import csv
# import os
# from io import StringIO
# from pathlib import Path
# import requests

# app = Flask(__name__)

# OLLAMA_URL = "http://localhost:11434/api/generate"  # Ollama endpoint
# MODEL = "codegemma"
# CSV_FILE = "test_scenarios.csv"
# SCRIPT_DIR = Path("test_scripts")
# SCRIPT_DIR.mkdir(exist_ok=True)

# # Function to call Ollama + CodeGemma for test scenario generation
# def generate_test_scenarios(area, count):
#     prompt = f"""
# Generate {count} UI test scenarios for the Windows Spotify application in the area of '{area}'.
# Provide each scenario as a line in the format: Description of the scenario.
# """

#     response = requests.post(OLLAMA_URL, json={
#         "model": MODEL,
#         "prompt": prompt,
#         "stream": False
#     })

#     if response.status_code != 200:
#         scenarios = [{
#             "Test Case ID": "TC_ERROR",
#             "Area": area,
#             "Description": f"Failed to generate test cases: {response.text}"
#         }]
#     else:
#         text = response.json().get("response", "")
#         lines = [line.strip("- ") for line in text.strip().split("\n") if line.strip()]
#         scenarios = [
#             {
#                 "Test Case ID": f"TC_{i+1}",
#                 "Area": area,
#                 "Description": line
#             } for i, line in enumerate(lines[:int(count)])
#         ]

#     # Save to CSV file
#     with open(CSV_FILE, 'w', newline='') as f:
#         writer = csv.DictWriter(f, fieldnames=["Test Case ID", "Area", "Description"])
#         writer.writeheader()
#         writer.writerows(scenarios)

#     return scenarios

# def generate_test_script(description):
#     return f"""
# from pywinauto import Application

# # Test Script: {description}
# def test_spotify_scenario():
#     app = Application(backend='uia').start('Spotify.exe')
#     # Add steps based on: {description}
#     pass
# """

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         area = request.form['area']
#         count = request.form['count']
#         generate_test_scenarios(area, count)
#         return redirect(url_for('generate_scripts'))

#     return render_template_string('''
#         <h2>LLM Test Scenario Generator</h2>
#         <form method="post">
#             Area for testing: <input type="text" name="area" required><br>
#             Number of test cases: <input type="number" name="count" required><br>
#             <input type="submit" value="Generate Test Scenarios">
#         </form>
#     ''')

# @app.route('/generate-scripts')
# def generate_scripts():
#     if not os.path.exists(CSV_FILE):
#         return "No test scenarios found."

#     with open(CSV_FILE, newline='') as f:
#         reader = csv.DictReader(f)
#         for row in reader:
#             script_content = generate_test_script(row['Description'])
#             script_file = SCRIPT_DIR / f"{row['Test Case ID']}.py"
#             with open(script_file, 'w') as sf:
#                 sf.write(script_content)

#     return redirect(url_for('review_scripts'))

# @app.route('/review-scripts')
# def review_scripts():
#     script_links = [f'<li><a href="/edit/{script.name}">{script.name}</a></li>' for script in SCRIPT_DIR.glob("*.py")]
#     return f"<h2>Review Test Scripts</h2><ul>{''.join(script_links)}</ul>"

# @app.route('/edit/<filename>', methods=['GET', 'POST'])
# def edit_script(filename):
#     script_path = SCRIPT_DIR / filename
#     if request.method == 'POST':
#         with open(script_path, 'w') as f:
#             f.write(request.form['content'])
#         return redirect(url_for('review_scripts'))

#     content = open(script_path).read()
#     return render_template_string('''
#         <h2>Editing {{filename}}</h2>
#         <form method="post">
#             <textarea name="content" rows="20" cols="80">{{content}}</textarea><br>
#             <input type="submit" value="Save">
#         </form>
#     ''', filename=filename, content=content)

# if __name__ == '__main__':
#     app.run(debug=True)

# from flask import Flask, render_template_string, request, redirect, url_for, send_file
# import csv
# import os
# from io import StringIO
# from pathlib import Path
# import requests

# app = Flask(__name__)

# OLLAMA_URL = "http://localhost:11434/api/generate"  # Ollama endpoint
# MODEL = "codegemma"
# CSV_FILE = "test_scenarios.csv"
# SCRIPT_DIR = Path("test_scripts")
# SCRIPT_DIR.mkdir(exist_ok=True)
# COMBINED_SCRIPT_FILE = SCRIPT_DIR / "spotify_test_suite.py"

# # Function to call Ollama + CodeGemma for test scenario generation
# def generate_test_scenarios(area, count):
#     prompt = f"""
# Generate {count} UI test scenarios for the Windows Spotify application in the area of '{area}'.
# Provide each scenario as a line in the format: Description of the scenario.
# """

#     response = requests.post(OLLAMA_URL, json={
#         "model": MODEL,
#         "prompt": prompt,
#         "stream": False
#     })

#     if response.status_code != 200:
#         scenarios = [{
#             "Test Case ID": "TC_ERROR",
#             "Area": area,
#             "Description": f"Failed to generate test cases: {response.text}"
#         }]
#     else:
#         text = response.json().get("response", "")
#         lines = [line.strip("- ") for line in text.strip().split("\n") if line.strip()]
#         scenarios = [
#             {
#                 "Test Case ID": f"TC_{i+1}",
#                 "Area": area,
#                 "Description": line
#             } for i, line in enumerate(lines[:int(count)])
#         ]

#     # Save to CSV file
#     with open(CSV_FILE, 'w', newline='') as f:
#         writer = csv.DictWriter(f, fieldnames=["Test Case ID", "Area", "Description"])
#         writer.writeheader()
#         writer.writerows(scenarios)

#     return scenarios

# # New: Function to manually generate test scripts using LLM prompt
# def generate_combined_script(scenarios):
#     prompt = """Generate Python test functions using pywinauto for the following Spotify test scenarios. Each function should be named using the test case ID and include the steps as Python code. Hardcode the Spotify path as 'C:\\Users\\palla\\AppData\\Local\\Microsoft\\WindowsApps\\Spotify.exe'.

# """
#     for scenario in scenarios:
#         prompt += f"{scenario['Test Case ID']}: {scenario['Description']}\n"

#     response = requests.post(OLLAMA_URL, json={
#         "model": MODEL,
#         "prompt": prompt,
#         "stream": False
#     })

#     if response.status_code != 200:
#         script_content = f"""# Failed to generate test scripts:\n# {response.text}"""
#     else:
#         script_body = response.json().get("response", "")
#         script_content = f"from pywinauto import Application\n\n# Combined Spotify Test Suite\n\n{script_body}"

#     with open(COMBINED_SCRIPT_FILE, 'w') as f:
#         f.write(script_content)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         area = request.form['area']
#         count = request.form['count']
#         generate_test_scenarios(area, count)
#         return redirect(url_for('generate_scripts'))

#     return render_template_string('''
#         <h2>LLM Test Scenario Generator</h2>
#         <form method="post">
#             Area for testing: <input type="text" name="area" required><br>
#             Number of test cases: <input type="number" name="count" required><br>
#             <input type="submit" value="Generate Test Scenarios">
#         </form>
#     ''')

# @app.route('/generate-scripts')
# def generate_scripts():
#     if not os.path.exists(CSV_FILE):
#         return "No test scenarios found."

#     with open(CSV_FILE, newline='') as f:
#         reader = csv.DictReader(f)
#         scenarios = list(reader)

#     generate_combined_script(scenarios)
#     return redirect(url_for('edit_combined_script'))

# @app.route('/edit-combined-script', methods=['GET', 'POST'])
# def edit_combined_script():
#     if request.method == 'POST':
#         with open(COMBINED_SCRIPT_FILE, 'w') as f:
#             f.write(request.form['content'])
#         return redirect(url_for('edit_combined_script'))

#     content = open(COMBINED_SCRIPT_FILE).read() if COMBINED_SCRIPT_FILE.exists() else ""
#     return render_template_string('''
#         <h2>Editing Combined Spotify Test Suite</h2>
#         <form method="post">
#             <textarea name="content" rows="30" cols="100">{{content}}</textarea><br>
#             <input type="submit" value="Save">
#         </form>
#     ''', content=content)

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template_string, request, redirect, url_for, send_file
import csv
import os
from io import StringIO
from pathlib import Path
import requests

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"  # Ollama endpoint
MODEL = "codegemma"
CSV_FILE = "test_scenarios.csv"
SCRIPT_DIR = Path("test_scripts")
SCRIPT_DIR.mkdir(exist_ok=True)
COMBINED_SCRIPT_FILE = SCRIPT_DIR / "spotify_test_suite.py"

# Function to call Ollama + CodeGemma for test scenario generation
def generate_test_scenarios(area, count):
    prompt = f"""
Generate {count} UI test scenarios for the Windows Spotify application in the area of '{area}'.
Provide each scenario as a line in the format: Description of the scenario.
"""

    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    })

    if response.status_code != 200:
        scenarios = [{
            "Test Case ID": "TC_ERROR",
            "Area": area,
            "Description": f"Failed to generate test cases: {response.text}"
        }]
    else:
        text = response.json().get("response", "")
        lines = [line.strip("- ") for line in text.strip().split("\n") if line.strip()]
        scenarios = [
            {
                "Test Case ID": f"TC_{i+1}",
                "Area": area,
                "Description": line
            } for i, line in enumerate(lines[:int(count)])
        ]

    # Save to CSV file
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Test Case ID", "Area", "Description"])
        writer.writeheader()
        writer.writerows(scenarios)

    return scenarios

# New: Function to manually generate test scripts using LLM prompt
def generate_combined_script(scenarios):
    # Create content string from CSV rows
    content = ""
    for scenario in scenarios:
        content += f"{scenario['Test Case ID']},{scenario['Area']},{scenario['Description']}\n"

    # Use expert prompt
    prompt = f"""You are an expert Python developer skilled in Windows desktop automation and UI testing.

Your task: Write a **pytest-based test script** in Python to automate a user action on the Windows Spotify desktop app.

Scenario:
The user wants to search for the song "Imagine Dragons" using keyboard and mouse automation. The known screen coordinates for the search box are (691,1)–(1304,72), and the mouse click should happen at point (700, 40).

Use the following strict coding instructions:

1. Use these imports (and others only if necessary):
     from pywinauto.application import Application
     from pywinauto.keyboard import send_keys
     import pyautogui, pytest, time

2. Define a constant path:
     SPOTIFY_PATH = r"C:\\Users\\palla\\AppData\\Local\\Microsoft\\WindowsApps\\Spotify.exe"

3. Provide this helper function (do not rename):
     def connect_spotify():
         try:
             app = Application(backend="uia").connect(title_re="Spotify.*", timeout=10)
             win = app.window(title_re="Spotify.*")
             print(f"[UIA] Window exists: {{win.exists()}} | visible: {{win.is_visible()}}")
             return app
         except Exception as e:
             print(f"[UIA] connect failed: {{e}}")
             try:
                 app = Application(backend="win32").connect(title_re="Spotify.*", timeout=10)
                 win = app.window(title_re="Spotify.*")
                 print(f"[Win32] Window exists: {{win.exists()}} | visible: {{win.is_visible()}}")
                 return app
             except Exception as e2:
                 print(f"[Win32] connect failed: {{e2}}")
                 return Application(backend="uia").start(SPOTIFY_PATH)

4. Define a pytest fixture named `spotify_app`:
     - It connects to the Spotify app
     - Yields the visible window with "Spotify" in its title
     - Sleeps for 5 seconds before starting

5. Create a pytest function `test_search_song(spotify_app)` that:
     - Uses the `spotify_app` fixture
     - Brings the Spotify window to focus
     - Moves the mouse to coordinate (700, 40) and clicks
     - Types the text "Imagine Dragons" and presses Enter using `send_keys`
     - Asserts success with a placeholder (e.g. `assert True`)
     - Includes comments for each step

Output valid Python code only. Do not include markdown or explanations.
"""
    
    
    # f"""
    # You are an expert Python developer with knowledge of Windows desktop automation and UI testing.

    # Write a test case to search for a song in the spotify app.
    # Use the following pixel coordinates for the search box (691,1)–(1304,72)

    # Your task: **output ONE python test file** for the Windows Spotify desktop client,
    # using ONLY keyboard automation (no UI selectors).

    # STRICT CODING RULES (follow exactly):
    # 1. Output MUST be valid Python code **only** (no ``` fences, no markdown).
    # 2. Start with these imports (and add any others you need):
    #     from pywinauto.application import Application
    #     import pytest, time
    # 3. Define constant  
    #     SPOTIFY_PATH = r"C:\\Users\\palla\\AppData\\Local\\Microsoft\\WindowsApps\\Spotify.exe"
    # 4. Provide a helper `connect_spotify()` exactly like this (reuse, do not rename):

    #     def connect_spotify():
    #         try:
    #             app = Application(backend="uia").connect(title_re="Spotify.*", timeout=10)
    #             win = app.window(title_re="Spotify.*")
    #             print(f"[UIA] Window exists: {{win.exists()}} | visible: {{win.is_visible()}}")
    #             return app
    #         except Exception as e:
    #             print(f"[UIA] connect failed: {{e}}")
    #             try:
    #                 app = Application(backend="win32").connect(title_re="Spotify.*", timeout=10)
    #                 win = app.window(title_re="Spotify.*")
    #                 print(f"[Win32] Window exists: {{win.exists()}} | visible: {{win.is_visible()}}")
    #                 return app
    #             except Exception as e2:
    #                 print(f"[Win32] connect failed: {{e2}}")
    #                 return Application(backend="uia").start(SPOTIFY_PATH)

    # 5. Provide ONE fixture:

    #     @pytest.fixture(scope="function")
    #     def spotify_app():
    #         app = connect_spotify()
    #         time.sleep(5)
    #         for win in app.windows():
    #             try:
    #                 if win.is_visible() and "Spotify" in win.window_text():
    #                     print(f"[Fixture] Using window: {{win.window_text()}} | handle: {{win.handle}}")
    #                     yield win
    #                     return
    #             except Exception as e:
    #                 print(f"[Fixture] Skipping window due to error: {{e}}")
    #         pytest.fail("No visible Spotify window found!")
    #         # do NOT close Spotify

    # 6. Write ONE test function per test case that:
    # • uses the `spotify_app` fixture  
    # • brings the window to the foreground with `spotify_app.set_focus()`

    # • contains clear `assert` statements with helpful messages (if possible)

    # 7. No `if __name__ == "__main__":` block, no extra commentary.
    # """

    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    })

    if response.status_code != 200:
        script_content = f"""# Failed to generate test scripts:\n# {response.text}"""
    else:
        script_content = response.json().get("response", "")

    with open(COMBINED_SCRIPT_FILE, 'w') as f:
        f.write(script_content)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        area = request.form['area']
        count = request.form['count']
        generate_test_scenarios(area, count)
        return redirect(url_for('generate_scripts'))

    return render_template_string('''
        <h2>LLM Test Scenario Generator</h2>
        <form method="post">
            Area for testing: <input type="text" name="area" required><br>
            Number of test cases: <input type="number" name="count" required><br>
            <input type="submit" value="Generate Test Scenarios">
        </form>
    ''')

@app.route('/generate-scripts')
def generate_scripts():
    if not os.path.exists(CSV_FILE):
        return "No test scenarios found."

    with open(CSV_FILE, newline='') as f:
        reader = csv.DictReader(f)
        scenarios = list(reader)

    generate_combined_script(scenarios)
    return redirect(url_for('edit_combined_script'))

@app.route('/edit-combined-script', methods=['GET', 'POST'])
def edit_combined_script():
    if request.method == 'POST':
        with open(COMBINED_SCRIPT_FILE, 'w') as f:
            f.write(request.form['content'])
        return redirect(url_for('edit_combined_script'))

    content = open(COMBINED_SCRIPT_FILE).read() if COMBINED_SCRIPT_FILE.exists() else ""
    return render_template_string('''
        <h2>Editing Combined Spotify Test Suite</h2>
        <form method="post">
            <textarea name="content" rows="30" cols="100">{{content}}</textarea><br>
            <input type="submit" value="Save">
        </form>
    ''', content=content)

if __name__ == '__main__':
    app.run(debug=True)

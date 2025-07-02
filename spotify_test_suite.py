import pyautogui

import time

import pygetwindow as gw

import subprocess

import os

#comment

def launch_spotify(spotify_path):

    if not any("Spotify" in w.title for w in gw.getWindowsWithTitle("Spotify")):

        print("Launching Spotify...")

        subprocess.Popen(spotify_path)

        time.sleep(5)  # Wait for Spotify to launch



def focus_spotify_window():

    try:

        window = gw.getWindowsWithTitle("Spotify")[0]

        if window:

            window.activate()

            time.sleep(1)

            return True

    except IndexError:

        print("Spotify window not found.")

    return False



def search_song(search_box_coords, song_name, spotify_path):

    launch_spotify(spotify_path)

    if focus_spotify_window():

        pyautogui.moveTo(search_box_coords[0], search_box_coords[1], duration=0.5)

        pyautogui.click()

        time.sleep(0.5)

        pyautogui.write(song_name, interval=0.1)

        pyautogui.press('enter')

        print(f"Searched for: {song_name}")

    else:

        print("Could not focus Spotify window.")



# Example usage

spotify_path = r"C:\\Users\\palla\\AppData\\Local\\Microsoft\\WindowsApps\\Spotify.exe"  # Replace with actual path

search_box_coords = (700, 40)  # Replace with actual coordinates

search_song(search_box_coords, "Bohemian Rhapsody", spotify_path)
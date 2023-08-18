import PySimpleGUI as sg
import json
import keyboard
import os

# Setting up the directory
home_dir = os.path.expanduser("~")
documents_path = os.path.join(home_dir, "Documents")
target_dir = os.path.join(documents_path, "Ryzz3nn", "XDeathCounter")
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# Load settings
try:
    with open(os.path.join(target_dir, "settings.json"), "r") as settings_file:
        settings = json.load(settings_file)
except FileNotFoundError:
    settings = {
        "death_key": "-"
    }
    with open(os.path.join(target_dir, "settings.json"), "w") as settings_file:
        json.dump(settings, settings_file)

sg.theme('DarkBrown4')

death_counter = 0
death_action_taken = False

def increment_death_counter():
    global death_counter
    death_counter += 1
    update_display()
    save_to_file()

def decrement_death_counter():
    global death_counter
    if death_counter > 0:
        death_counter -= 1
        update_display()
        save_to_file()

def reset_counters():
    global death_counter
    death_counter = 0
    update_display()
    save_to_file()

def update_display():
    window['-DEATH-VALUE-'].update(value=death_counter)

def save_to_file():
    with open(os.path.join(target_dir, "count.txt"), "w", encoding='utf-8') as file:
        file.write(f"💀 {death_counter}\n")
    window['-STATUS-'].update("Deaths saved to count.txt")

layout = [
    [sg.Text("Death Counter", font=("bahnschrift Condensed", 24), justification='center')],
    [sg.HorizontalSeparator()],
    [sg.Text("Deaths", font=("bahnschrift Condensed", 18), size=(12, 1), justification='center')],
    [sg.Button("+", size=(4, 1), key='-DEATH-INC-'),
     sg.Text(death_counter, size=(8, 1), key='-DEATH-VALUE-', font=("bahnschrift Condensed", 14), justification='center'),
     sg.Button("-", size=(4, 1), key='-DEATH-DEC-')],
    [sg.Button("Reset Counts"), sg.Button("Settings")],
    [sg.Text("", size=(20, 1), key='-STATUS-', text_color='green', justification='center')]
]

window = sg.Window("DeathCounter", layout, finalize=True, resizable=True, size=(400, 200))

while True:
    event, values = window.read(timeout=100)

    if keyboard.is_pressed(settings['death_key']) and not death_action_taken:
        increment_death_counter()
        death_action_taken = True
    elif not keyboard.is_pressed(settings['death_key']):
        death_action_taken = False

    if event == sg.WIN_CLOSED:
        break
    elif event == '-DEATH-INC-':
        increment_death_counter()
    elif event == '-DEATH-DEC-':
        decrement_death_counter()
    elif event == 'Settings':
        settings_layout = [
            [sg.Text("Settings", font=("bahnschrift Condensed", 18))],
            [sg.Text("Death Key:"), sg.InputText(settings.get('death_key', '-'), key='-DEATH-KEY-')],
            [sg.Button("Save Settings")]
        ]
        settings_window = sg.Window("Settings", settings_layout, finalize=True)

        while True:
            settings_event, settings_values = settings_window.read()
            if settings_event == sg.WIN_CLOSED:
                break
            elif settings_event == "Save Settings":
                settings['death_key'] = settings_values['-DEATH-KEY-']
                with open(os.path.join(target_dir, "settings.json"), "w") as settings_file:
                    json.dump(settings, settings_file)
                settings_window.close()
                break
    elif event == 'Reset Counts':
        reset_counters()

import tkinter as tk
from tkinter import ttk
import time
from threading import Thread
import random
import platform

# Developer options (set to "yes", "no", or specific step)
DEV_ALWAYS_BLUESCREEN_END = "no"  # Always trigger a bluescreen at the end
DEV_ALWAYS_BLUESCREEN_PAUSE = "no"  # Always trigger a bluescreen during the loading pause
DEV_ALWAYS_BLUESCREEN_RETRY = "no"  # Always trigger a bluescreen on retry button
DEV_DISABLE_PAUSE = "no"  # Disable the random pause in loading
DEV_FORCE_NORMAL_END = "no"  # Always show the result screen (overrides bluescreen)
DEV_SKIP_LOADING = "no"  # Skip the loading animation
DEV_FORCE_BLUESCREEN_STEP = "none"  # Options: "start", "pause", "end"

# Global variables for components that need to be accessed across functions
user_age = None
age_entry = None
submit_button = None
progress_var = None
result_label = None


def start_loading():
    """Starts the loading animation."""
    global user_age
    user_age = age_entry.get()  # Store the age before destroying the widget

    def loading_task():
        if DEV_FORCE_BLUESCREEN_STEP == "start":
            show_fake_bluescreen()
            return

        paused = False  # Track whether the loading paused
        for i in range(101):  # 0% to 100%
            if DEV_SKIP_LOADING == "yes":
                break

            if not paused and i == random.randint(30, 70) and DEV_DISABLE_PAUSE == "no":
                pause_duration = random.uniform(1, 5)
                time.sleep(pause_duration)  # Simulate pause
                paused = True

                # Handle bluescreen during pause
                if DEV_FORCE_BLUESCREEN_STEP == "pause" or (
                    DEV_ALWAYS_BLUESCREEN_PAUSE == "yes"
                    or (random.random() < 1 / 10 and DEV_FORCE_NORMAL_END == "no")
                ):
                    show_fake_bluescreen()
                    return

            progress_var.set(i)
            time.sleep(0.1)  # Simulate loading (10 seconds total)

        # Handle bluescreen at the end
        if DEV_FORCE_BLUESCREEN_STEP == "end" or (
            DEV_ALWAYS_BLUESCREEN_END == "yes"
            or (random.random() < 1 / 3 and DEV_FORCE_NORMAL_END == "no")
        ):
            show_fake_bluescreen()
        else:
            show_result_screen()

    age_entry.config(state="disabled")
    submit_button.config(state="disabled")
    result_label.config(text="Loading...")
    progress_var.set(0)
    Thread(target=loading_task).start()


def show_result_screen():
    """Clears the window and displays the guessed age."""
    for widget in root.winfo_children():
        widget.destroy()

    result_label = tk.Label(root, text=f"You are {user_age} years old!", font=("Arial", 16))
    result_label.pack(pady=50)

    retry_button = tk.Button(root, text="Retry", font=("Arial", 12), command=retry_process)
    retry_button.pack(pady=10)

    exit_button = tk.Button(root, text="Exit", font=("Arial", 12), command=root.destroy)
    exit_button.pack(pady=10)


def retry_process():
    """Handles retry functionality with a chance of bluescreen."""
    if DEV_ALWAYS_BLUESCREEN_RETRY == "yes" or (random.random() < 1 / 5 and DEV_FORCE_NORMAL_END == "no"):
        show_fake_bluescreen()
    else:
        reset_to_main_screen()


def reset_to_main_screen():
    """Resets the application to the main screen."""
    for widget in root.winfo_children():
        widget.destroy()
    create_main_screen()


def show_fake_bluescreen():
    """Displays a fake fullscreen blue screen."""
    # Remove all existing widgets (including any main screen or bluescreen)
    for widget in root.winfo_children():
        widget.destroy()

    os_name = platform.system()
    if os_name == "Windows":
        bsod_text = "\n:(\n\nYour PC ran into a problem and needs to restart.\nWe're just collecting some error info, and then we'll restart for you.\n\nStop Code: CRITICAL_PROCESS_DIED"
    elif os_name == "Darwin":
        bsod_text = "\nYour computer restarted because of a problem.\nPress a key or wait a few seconds to continue starting up."
    else:
        bsod_text = "\nKernel panic - not syncing: Fatal exception in interrupt\n\nCall Trace:\n [<ffffffff810d31a>] panic+0xc8/0x20d\n [<ffffffff810d33f>] ? printk+0x41/0x44"

    # Make the window fullscreen
    root.attributes("-fullscreen", True)
    root.configure(bg="blue" if os_name == "Windows" else "black")

    # Add blue screen or kernel panic text
    bluescreen_label = tk.Label(
        root,
        text=bsod_text,
        font=("Consolas", 14),
        fg="white",
        bg="blue" if os_name == "Windows" else "black",
        justify="center"
    )
    bluescreen_label.pack(pady=100)

    # Add an instruction to quit
    escape_label = tk.Label(
        root,
        text="Press 'Esc' to restart." if os_name != "Darwin" else "Press any key to restart.",
        font=("Consolas", 16),
        fg="white",
        bg="blue" if os_name == "Windows" else "black",
    )
    escape_label.pack(pady=20)

    # Bind the Esc key to reset
    root.bind("<Escape>", lambda event: reset_to_main_screen())


def submit_event(event=None):
    """Handles the submit action for button or Enter key."""
    start_loading()


def create_main_screen():
    """Creates the main screen UI."""
    global age_entry, submit_button, progress_var, result_label

    # Add a title label
    title_label = tk.Label(root, text="---- Age Guesser 9000 ----", font=("Arial", 16))
    title_label.pack(pady=20)

    # Add a label and entry for age
    age_label = tk.Label(root, text="How old are you?", font=("Arial", 12))
    age_label.pack()

    age_entry = tk.Entry(root, font=("Arial", 12))
    age_entry.pack(pady=10)

    # Bind Enter key to submission
    age_entry.bind("<Return>", submit_event)

    # Add a submit button
    submit_button = tk.Button(root, text="Submit", font=("Arial", 12), command=submit_event)
    submit_button.pack(pady=10)

    # Add a progress bar
    progress_var = tk.IntVar()
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate", variable=progress_var)
    progress_bar.pack(pady=20)

    # Add a result label
    result_label = tk.Label(root, text="", font=("Arial", 12))
    result_label.pack()


# Create the main application window
root = tk.Tk()
root.title("Age Guesser 9000")
root.geometry("400x300")

create_main_screen()

# Start the Tkinter event loop
root.mainloop()

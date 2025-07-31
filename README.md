# The Haunted Desktop
Welcome to The Haunted Desktop, a fun Python application designed to make your computer feel like it's haunted by a playful (or spooky) spirit. This app runs in the background and creates a series of unnerving events to surprise and entertain.

## What It Does
Once launched, The Haunted Desktop will periodically trigger a variety of spooky events, including:

Ghostly Typing: A transparent window appears at a random location on your screen and types out eerie messages.

Flickering Window: The main application window will flicker in and out of view.

Erratic Mouse Jumps: The mouse cursor will suddenly leap to a random spot on the screen.

Sudden Spooky Messages: A startling message box will pop up with a creepy note.

Unsettling Sounds: A synthesized, spooky whisper will play at random intervals.

The application window provides a button to "Appease the Spirits," which will temporarily calm the hauntings before they inevitably return.

## Requirements
To run this application, you will need Python 3 and the following libraries:

PyQt6

pygame

You can install them using pip:

```
pip install PyQt6 pygame
```

How to Run
Save the code as a Python file (e.g., haunted_app.py).

Open your terminal or command prompt.

Navigate to the directory where you saved the file.

Run the application with the following command:

```
python haunted_app.py
```

To stop the haunting, simply close the main application window.

## Customizing the Haunting
You can easily change the behavior of the haunting by editing the haunted_app.py file. Here are some of the key settings you can modify:

### Event Frequency
To change how often a haunted event occurs, find the HauntingWorker class and its run method. Modify the number inside time.sleep():

In the HauntingWorker.run method:
Change this value to make events more or less frequent (value is in seconds).
```
time.sleep(15) 
```

### Pop-up Messages
To change the text that appears in the spooky pop-up messages, edit the messages list inside the show_spooky_message method:

# In the HauntedApp.show_spooky_message method:
```
messages = [
    "I'm watching you.", 
    "You are not alone.", 
    "Look behind you."
    # Add or change your custom messages here
]
```

### Ghostly Typing Phrases
To change what the ghost types on the screen, find the phrases list inside the HauntingWorker's run method:

In the HauntingWorker.run method:
```
phrases = [
    "GET OUT", 
    "ALWAYS WATCHING", 
    "HEAR THE SCRATCHING?",
    "IT'S COLD IN HERE", 
    "BEHIND THE DOOR"
    # Add or change your custom phrases here
]
```

### Appeasement Duration
To change how long the spirits remain calm after you click the "Appease" button, find the appease_spirits method and modify

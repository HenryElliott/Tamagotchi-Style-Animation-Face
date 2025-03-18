
# Tamagotchi-Style Animation Project

This project demonstrates the creation of an animated face with eyes that blink and follow the movement of the mouse cursor. Additionally, the eyes can occasionally switch to a "dead" state, where an "X" appears in place of the eyes, adding an eerie effect. The eyes also blink at random intervals, and their blinking can be controlled through specific timing events.

## Features
- **Blinking Eyes**: Eyes blink at random intervals with a smooth animation effect.
- **Mouse-Following Eyes**: The eyes track the mouse cursor within a limited range, simulating the effect of someone following you with their gaze.
- **Dead Eyes**: The eyes randomly switch to a "dead" state, represented by an "X," creating a spooky vibe.
- **Resizable Window**: The application window is resizable to suit your preference.

## Requirements
Before running the project, you'll need to install the following dependencies:

- **pygame**: A library for creating games and animations.
- **pyautogui**: A library for controlling and automating the mouse.
- **ctypes**: Used to position the application window on the screen.
- **math**: Provides mathematical functions for calculating eye movement.

Install the required libraries via pip:

```bash
pip install pygame pyautogui
```

## Installation & Setup
1. Clone or download the repository.
2. Install the necessary dependencies using pip (as mentioned above).
3. Run the script with the following command:

```bash
python blinking_eyes.py
```

## How It Works
- **Window Size**: The application runs in a 200x200 pixel window, but it is resizable.
- **Eye Animation**: Eyes are drawn as ellipses on the screen. They follow the mouse cursor within a specific range. When blinking, the eyes shrink and then expand smoothly.
- **Dead Eyes Effect**: The eyes randomly switch to a "dead" state, where an "X" is drawn in place of the eyes. This state lasts for 5 seconds.
- **Blinking Logic**: The eyes blink at random intervals (between 1 and 4 seconds). Each blink lasts for 15 frames, with a smooth opening and closing effect.

## Configuration
The following parameters can be adjusted in the code:

- **Eye Size**: Modify `EYE_WIDTH` and `EYE_HEIGHT` to adjust the size of the eyes.
- **Blink Speed**: Adjust `BLINK_FRAMES` and `FRAME_DELAY` to control the speed of the blink animation.
- **Open Time Range**: Modify `OPEN_TIME_MIN` and `OPEN_TIME_MAX` to set the time range between blinks.
- **Dead Eyes Chance**: Adjust `CHANGE_EYES_CHANCE` to control how often the eyes switch to the "dead" state.
- **Dead Eyes Event Interval**: Modify `DEAD_EYES_EVENT_INTERVAL` to change how frequently the "dead eyes" event occurs.

## Code Structure
1. **draw_ellipse**: Draws the eyes as ellipses on the screen.
2. **draw_mouth**: Draws a mouth that follows the mouse position.
3. **create_mask**: Creates a circular mask for the face outline.
4. **update_positions**: Updates the eye positions based on the mouse cursor.
5. **draw_dead_eyes**: Draws the "dead" eyes in the form of an "X."
6. **draw_face**: Updates and draws the entire face, including the eyes and mouth, checking for events like the "dead eyes" state.
7. **blink_logic**: Controls the blinking animation logic, determining when the eyes open and close.

## Example Animation

![Screenshot](screenshot.png)

## License
Feel free to modify and improve this project as needed. If you encounter any issues or have suggestions, please open an issue in the repository or reach out to me directly. Enjoy the animated eyes!

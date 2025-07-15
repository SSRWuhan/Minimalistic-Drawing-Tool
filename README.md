# Minimalistic-Drawing-Tool
This is a simple drawing tool to make simple game assets or to use as an interface for ai models like recognizing handwritten digits or something similar. This tool is based on a grid system. 
The grid dimensions are the image dimensions when saved or read from the screen. Below the attributes and methods for the tool are written,

### `.initialize( daemon = Boolean ):`
The `initialize()` method internally runs the the`.__run()` method which begins the GUI interface. This method takes in a boolean value, which is passed to the `thread` method from the Threading 
module as the `daemon` argument.

### `.window_buffer:`
The `window_buffer` attribute holds the current representation of the screen in an array with a shape of (width ,height, color channels)

## GUI usage
The buttons present on the GUI of the tool are described below,
- The File menu can be used to save and exit the tool
- The Edit menu can be used to change the color of paint brush
- The Settings menu can be used to change the window size, grid, size and cell size via the change resolution option, and the color channels can be changed by using the grayscale and rgb options.
- The spacebar can be pressed to clear the canvas

## Installation
This tool can be easily installed with `pip` using this command
```python
pip install https://github.com/SSRWuhan/Minimalistic-Drawing-Tool/releases/download/v1.0.0/minimalistic_drawing_tool-0.1.0-py3-none-any.whl
```

# Example
```python
import minimalistic_drawing_tool as mdt

app = mdt.mdt()


app.initialize(False)

```
# Demonstration
https://github.com/user-attachments/assets/41118aba-22fd-4dbd-b413-07314cf93d0a

##### Note: If drawing outside the screen is attempted then errors will occur.

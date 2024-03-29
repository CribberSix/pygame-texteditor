# Changelog

### 0.7.3: Added ability to customize the color of the cursor

The yaml files used to customize the editor now support a field called `caretColor` which can be used to customize the color of the cursor.

### 0.7.2: Added parameter to usage of pygment lexer

Added the parameter to `PythonLexer(ensurenl=False)` in order to avoid the issue from
[pygment](https://github.com/pygments/pygments/issues/610) as identified by [brno32](https://github.com/brno32)!


### 0.7.1: Bugfix for displaying line numbers correctly and doc-update

- Minor fix concerning a bug which caused the line number background to have a wrong width when first initialized.
- Improved documentation concerning README.md and [how-to-use.py](https://github.com/CribberSix/pygame-texteditor/blob/master/how-to-use.py).

### 0.7.0: QoL update - BREAKING CHANGES

- A lot of internal variables but also some parameters have been renamed to enable easier maintenance of the codebase. This might break existing implementations using the package if you hardcoded parameter names upon function calls or if you called internal variables.
- Removed unnecessary class attributes.
- Fixed a visual bug which caused the end of th escrollbar to be displayed outside the area of the texteditor.
- Fixed an issue [#11](https://github.com/CribberSix/pygame-texteditor/issues/11) which caused line numbers to be rendered incorrectly if a large font size was set.
- Fixed an isse [#12](https://github.com/CribberSix/pygame-texteditor/issues/10) which caused some lines to be un-selectable when a large font was set.
- Fixed an issue which caused the editor to crash if you used the arrow keys to scroll out of the visible lines.
- Fixed an issue which caused line numbers to extend over their background and even outside the editor if numbers went above two digits.

### 0.6.8: Font customization

Added option to use a custom (monospace) font, thanks to [brno32](https://github.com/brno32)'s contribution!

### 0.6.7: Cursor customization

Added option to have a static (or blinking) cursor.

### 0.6.5: Pygame version

Changed requirements concerning pygame to `>= 1.9.6` as version `2.0.1` has backwards compatibility.

### 0.6.4: Bugfix

Fixed highlight-rendering (adjusted to actual line height + gap!)

### 0.6.3: Font size customization

Implemented new function to customize font-size.

# Changelog for package 'pygame-texteditor"

### 0.7.0: QoL update

- Fixed a visual bug which caused the end of th escrollbar to be displayed outside the area of the texteditor.
- Fixed an issue [#11](https://github.com/CribberSix/pygame-texteditor/issues/11) which caused line numbers to be rendered incorrectly if a large font size was set.
- Fixed an isse [#12](https://github.com/CribberSix/pygame-texteditor/issues/10) which caused some lines to be un-selectable when a large font was set.

### 0.6.8: Font customization

Added option to use a custom (monospace) font, thanks to [brno32](https://github.com/brno32)'s contribution!

### 0.6.7: Cursor customziation

Added option to have a static (or blinking) cursor.

### 0.6.5: Pygame version

Changed requirements concerning pygame to `>= 1.9.6` as version `2.0.1` has backwards compatibility.

### 0.6.4: Bugfix

Fixed highlight-rendering (adjusted to actual line height + gap!)

### 0.6.3: Font size customization

Implemented new function to customize font-size.

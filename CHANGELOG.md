# Changelog

## 1.1.1

- Added: F1 opens the accessibility settings list, in the story and in menus. It has "Read voice acted lines" (off by default) and shows which speech output is in use.
- Added: Q opens the in-scene buttons during the story: Rewind, Skip and Pause menu. These were mouse-only buttons before.
- Added: when a prompt or the pause menu closes, the mod says what you were on before it: the current line in the story, or the selected item in a menu.
- Fixed: the Music, Sound and Voice volume sliders changed a setting the game never used, so music could stay silent with the slider turned up. They now control the game's real volumes, and the level you chose in 1.0 is moved to the real setting the first time the game starts.
- Fixed: pressing H a second time did nothing. H now hides the text window, and H, Enter or Space shows it again.
- Fixed: after Alt+Tab or Alt+F4, a stuck Alt key could stop every key from working. The mod now clears modifier keys that aren't actually held.

## 1.1.0

- New standalone installer.
- Speech now goes through Prism. If NVDA, JAWS, or another supported screen reader is running when the game starts, the mod speaks through it. Otherwise it uses built-in Windows speech. Tolk and the NVDA client files are no longer used.
- The mod no longer replaces the game's own screens.rpy. Its screens now live in screens_a11y.rpy, so uninstalling leaves the game exactly as it was.

## 1.0

- First release, using Tolk for speech.

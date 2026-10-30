# Brilliant Shadows Accessibility Mod — Version 1.0

An accessibility mod adding full text-to-speech support to make
[Brilliant Shadows - Part One of the Book of Gray Magic](https://store.steampowered.com/app/409920/Brilliant_Shadows__Part_One_of_the_Book_of_Gray_Magic/)
fully playable for blind users.

Developed by **Shaysters**, with the assistance of Claude (Anthropic) and Codex (OpenAI).

---

## Supported Screen Readers

On Windows, speech goes through Prism, which picks whatever is running.

| Platform | Speech output |
|----------|--------------|
| Windows | NVDA, JAWS and other screen readers supported by Prism |
| Windows | Windows SAPI (automatic fallback when no screen reader is running) |
| Linux | Orca (via speech-dispatcher) |

---

## Download

Grab the latest release from the [Releases](../../releases) page and follow the instructions in the included README.txt.

---

## Hotkeys

| Key | Action |
|-----|--------|
| R | Repeat the last spoken line |
| Up / Down | Navigate choices and menu items |
| Enter / Space | Advance dialogue or confirm |
| Page Up | Roll back to previous line |
| Page Down | Roll forward |
| Ctrl (hold) | Skip through already-seen lines |
| Tab | Toggle skipping on and off |
| F | Toggle fullscreen / windowed |
| H | Hide or show the text window |
| S | Take a screenshot |
| Delete | Delete selected save slot (on save screen) |
| Escape | Open the pause menu |
| Alt+F4 | Open the quit prompt |

Volume and text speed are adjustable from the Preferences screen using the Left and Right arrow keys.

---

## Notes

- The game does not include a built-in rewind system — this is by the developers' design. Press R to re-hear the last line.
- Your saves are not affected. This mod does not touch the game's story files.
- Prism (`prism.dll`) is licensed under the Mozilla Public License 2.0. Its license and the licenses of the libraries it uses are in the `prism_licenses` folder.

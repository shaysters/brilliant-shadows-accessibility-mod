# Brilliant Shadows Accessibility

Brilliant Shadows Accessibility is a mod that makes Brilliant Shadows - Part One of the Book of Gray Magic, the visual novel by Ithaqua Labs, playable with a screen reader. It reads dialogue, narration, choices and every menu, and makes everything usable from the keyboard, including buttons that were mouse-only.

On Windows it works with NVDA, JAWS and other screen readers, and falls back to Windows' built-in voices if no screen reader is running. On Linux it speaks through Orca (via speech-dispatcher). You play with the keyboard.

- Join the Discord to chat, get help or report problems: <https://discord.gg/KNDXhztGGK>
- Support shaysters on Ko-fi: <https://ko-fi.com/shaysters>

Version 1.1.2. See [CHANGELOG.md](CHANGELOG.md) for what has changed.

## Requirements

- Brilliant Shadows - Part One of the Book of Gray Magic, from Steam or itch.io:
  - Steam: <https://store.steampowered.com/app/409920/Brilliant_Shadows__Part_One_of_the_Book_of_Gray_Magic/>
  - itch.io: <https://ithaqualabs.itch.io/brilshads>
- A screen reader such as NVDA or JAWS (optional on Windows; without one, the mod uses Windows' built-in speech).

The mod has been tested with the Steam version. The itch.io and DRM-free versions should work too, but they haven't been tested yet.

## Installing

1. Close the game if it's running.
2. Download **BrilliantShadowsAccessibilityInstaller.exe** from the [latest release](https://github.com/shaysters/brilliant-shadows-accessibility-mod/releases/latest). It needs 64-bit Windows 10 or later.
3. Run it. Windows SmartScreen may warn that the app is unrecognized, because the installer is not code-signed. Choose **More info**, then **Run anyway**.
4. The installer finds your Steam copy of the game by itself. For an itch.io or DRM-free copy, or if it can't find the game, use the Browse button next to the game folder and choose the folder that contains `Brilliant Shadows.exe`.
5. Choose **Install**. The installer adds the mod and removes files left by older versions of the mod.
6. Start your screen reader, then start the game.

### Updating and uninstalling

Keep the installer. Run it again to update to the newest version, repair the mod, or uninstall it. Close the game first. The installer says on its first page when an update is available, and the mod tells you too, once the main menu has been read.

### Installing by hand

1. Download **BrilliantShadowsAccessibility.zip** from the [latest release](https://github.com/shaysters/brilliant-shadows-accessibility-mod/releases/latest).
2. Open the game folder, the one that contains `Brilliant Shadows.exe`. On a default Steam install that's:

   ```
   C:\Program Files (x86)\Steam\steamapps\common\Brilliant Shadows
   ```

   For itch.io or DRM-free copies, use the folder you installed the game to.
3. Extract the zip into that folder. `prism.dll` and the `prism_licenses` folder go next to `Brilliant Shadows.exe`, and the three `.rpy` files go into the `game` subfolder.
4. Start your screen reader, then start the game.

No game files are replaced, and your saves are not affected.

To uninstall a manual install, delete these:

- `prism.dll` and the `prism_licenses` folder in the game folder.
- In the `game` subfolder: `brilliant_shadows_accessibility.rpy`, `screens_a11y.rpy`, `zz_a11y_menu_override.rpy`, and the `.rpyc` files with the same names.

### Upgrading from version 1.0

Version 1.0 used Tolk and replaced the game's `screens.rpy`. The installer cleans this up for you. Before installing a newer version by hand:

1. Delete `Tolk.dll`, `nvdaControllerClient32.dll` and `nvdaControllerClient64.dll` from the game folder.
2. In the `game` subfolder, delete `brilliant_shadows_accessibility.rpyc` and `zz_a11y_menu_override.rpyc` if they are there.

The `screens.rpy` left by 1.0 can stay; it does no harm while the mod is installed. If you uninstall the mod and want the original back, use Steam: right click Brilliant Shadows, choose Properties, then Installed Files, then Verify integrity of game files.

## Keys

| Key | Where | What it does |
|---|---|---|
| Enter or Space | Story | Continue to the next line. |
| r | Story | Repeat the last line. |
| Page Up | Story | Roll back to the previous line. |
| Page Down | Story | Roll forward again. |
| Hold Ctrl | Story | Skip through lines you've already seen. |
| Tab | Story | Turn skipping on or off. |
| q | Story | Open the in-scene buttons: Rewind, Skip and Pause menu. |
| h | Story | Hide the text window. h, Enter or Space shows it again. |
| Escape | Story | Open the pause menu. |
| Up and Down | Menus and choices | Move between options. |
| Left and Right | Preferences | Change volume and text speed. |
| Enter or Space | Menus and choices | Select. |
| Delete | Save screen | Delete the selected save. |
| F1 | Everywhere | Open the accessibility settings. |
| f | Everywhere | Switch between fullscreen and windowed. |
| s | Everywhere | Take a screenshot. |
| Alt+F4 | Everywhere | Open the quit prompt. |

Notes:

- When a prompt or the pause menu closes, the mod says what you were on before it opened.
- Page Up, or Rewind in the q menu, goes back one line. On the very first line of the story this returns to the main menu, as the game's own rewind button does. Press r to hear the current line again.
- Lines with voice acting aren't read unless you turn them on in the settings. Narration is always read, and r repeats any line.

## Settings

Press F1 in the story or in any menu. Up and Down choose a setting, Left, Right or Enter change it, and Escape closes the list. Settings are saved automatically.

- **Read voice acted lines** (off by default): when off, lines that have voice acting aren't read, so the screen reader doesn't talk over the actors.
- **Speech output**: says whether Prism found NVDA, JAWS or another screen reader, or is using Windows' voice.

## Troubleshooting

The mod keeps a log next to `Brilliant Shadows.exe`:

```
a11y_log.txt
```

It says which speech output Prism found and records any errors. If something goes wrong, include the log when you report it.

- **No speech at all:** make sure `prism.dll` is next to `Brilliant Shadows.exe` and the three `.rpy` files are in the `game` subfolder, and that the game was started after installing.
- **No music after updating from 1.0:** version 1.0's music slider didn't change the game's real music volume. 1.1.1 moves the level you chose to the real setting the first time it starts. Check Music volume in Preferences.
- **Keys stop working after Alt+Tab:** the mod clears a stuck Alt key by itself within a moment. If keys still don't respond, press and release Alt once.

To report a problem or suggest something, open an issue on the [GitHub page](https://github.com/shaysters/brilliant-shadows-accessibility-mod/issues).

## Credits

This mod was developed by [Shaysters](https://github.com/shaysters), with the assistance of Claude (Anthropic) and Codex (OpenAI).

The installer is built with [Loadstone](https://github.com/bradjrenshaw/loadstone) by [Bradley Renshaw](https://github.com/bradjrenshaw).

Speech is provided by [Prism](https://github.com/ethindp/prism) by Ethin Probst, under the MPL-2.0 license. Its license and the licenses of the libraries it uses are in the `prism_licenses` folder.

Brilliant Shadows is made by Ithaqua Labs. This mod isn't affiliated with or endorsed by Ithaqua Labs.

## For developers

Release instructions are in [DEVELOPING.md](DEVELOPING.md).

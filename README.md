# Brilliant Shadows Accessibility Mod — Version 1.1.0

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

## Install with the installer (recommended)

The installer needs 64-bit Windows 10 or later and supports the Steam version of the game.

1. Download `BrilliantShadowsAccessibilityInstaller.exe` from the [latest release](https://github.com/shaysters/brilliant-shadows-accessibility-mod/releases/latest).
2. Close the game, then run the installer.
   Windows SmartScreen may warn that the app is unrecognized, because the installer is not code-signed. Choose "More info", then "Run anyway".
3. The installer finds the game through Steam. If it doesn't, use Browse to pick the folder that contains `Brilliant Shadows.exe`.
4. Press Install. The installer adds the mod and removes files left by older versions of the mod.
5. Start your screen reader, then launch the game.

Run the installer again at any time to update, repair, or uninstall the mod.

## Manual install

1. Download `BrilliantShadowsAccessibility.zip` from the [latest release](https://github.com/shaysters/brilliant-shadows-accessibility-mod/releases/latest).
2. Open the folder that contains `Brilliant Shadows.exe`, such as `C:\Program Files (x86)\Steam\steamapps\common\Brilliant Shadows`.
3. Extract the zip into that folder. `prism.dll` and the `prism_licenses` folder go next to `Brilliant Shadows.exe`, and the three `.rpy` files go into the `game` subfolder.
4. Start your screen reader, then launch the game.

No game files are replaced.

### Updating from version 1.0

Version 1.0 used Tolk and replaced the game's `screens.rpy`. Before installing 1.1.0 by hand:

1. Delete `Tolk.dll`, `nvdaControllerClient32.dll` and `nvdaControllerClient64.dll` from the game folder.
2. In the `game` subfolder, delete `brilliant_shadows_accessibility.rpyc` and `zz_a11y_menu_override.rpyc` if they are there.

The installer does both of these for you. The `screens.rpy` left by 1.0 can stay; it does no harm while the mod is installed.

### Uninstalling

Run the installer and choose Uninstall, or delete these by hand:

- `prism.dll` and the `prism_licenses` folder in the game folder.
- In the `game` subfolder: `brilliant_shadows_accessibility.rpy`, `screens_a11y.rpy`, `zz_a11y_menu_override.rpy`, and the `.rpyc` files with the same names.

If you ever installed version 1.0, it replaced the game's `screens.rpy`. To put the original back, use Steam: right click Brilliant Shadows, choose Properties, then Installed Files, then Verify integrity of game files.

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
- Voice-acted lines are not read aloud, so the screen reader does not talk over the actors. Narration is always read, and R repeats any line.
- Your saves are not affected. This mod does not touch the game's story files.
- Prism (`prism.dll`) is licensed under the Mozilla Public License 2.0. Its license and the licenses of the libraries it uses are in the `prism_licenses` folder.
- The installer is built with [Loadstone](https://github.com/bradjrenshaw/loadstone) by Bradley Renshaw.

---

## Publishing a release

For maintainers. Update `changes-latest.md`, build the zip with `powershell -ExecutionPolicy Bypass -File scripts\package-release.ps1`, create a draft GitHub release with the zip attached (`gh release create vX.Y.Z --draft --notes-file changes-latest.md dist\BrilliantShadowsAccessibility.zip`), then run the **Release** workflow from the Actions tab with the same tag. It builds the installer, writes `loadstone-release.json`, and publishes the release. The installer's package files are in `loadstone-packages/`, and its settings are in `installer/profile.json`.

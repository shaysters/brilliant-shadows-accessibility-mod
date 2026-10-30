Brilliant Shadows Accessibility Mod - Version 1.1.1

Brilliant Shadows - Part One of the Book of Gray Magic is available on Steam:
https://store.steampowered.com/app/409920/Brilliant_Shadows__Part_One_of_the_Book_of_Gray_Magic/

Developed by Shaysters, with the assistance of Claude (Anthropic) and Codex (OpenAI),
to add full text-to-speech support and make the game fully playable for blind users.

Supported screen readers:
  Windows: NVDA, JAWS and other screen readers (via Prism),
           or Windows SAPI (automatic fallback)
  Linux:   Orca (via speech-dispatcher)

----------------------------------------------------------------

Installing

The easiest way is the installer, BrilliantShadowsAccessibilityInstaller.exe,
from the same release page as this zip:
https://github.com/shaysters/brilliant-shadows-accessibility-mod/releases/latest
It finds the game, installs the mod, and can update or uninstall it later.

To install by hand instead:

1. Find your Brilliant Shadows game folder. With Steam it is usually:
     C:\Program Files (x86)\Steam\steamapps\common\Brilliant Shadows
   It contains a file called Brilliant Shadows.exe.

2. Extract the contents of this zip into that folder.
   prism.dll and the prism_licenses folder go next to Brilliant Shadows.exe,
   and the three .rpy files go into the game subfolder.
   No game files are replaced.

3. If you had version 1.0 installed, also delete these:
     In the game folder: Tolk.dll, nvdaControllerClient32.dll and
       nvdaControllerClient64.dll
     In the game subfolder: brilliant_shadows_accessibility.rpyc and
       zz_a11y_menu_override.rpyc

4. Launch the game with your screen reader already running.

Uninstalling

Delete prism.dll and the prism_licenses folder from the game folder, and from
the game subfolder delete brilliant_shadows_accessibility, screens_a11y and
zz_a11y_menu_override (both the .rpy and .rpyc files).

If you ever installed version 1.0, it replaced the game's screens.rpy. To put
the original back, use Steam: right click Brilliant Shadows, choose
Properties, then Installed Files, then Verify integrity of game files.

----------------------------------------------------------------

Hotkeys

  R              Repeat the last spoken line
  Up / Down      Navigate choices and menu items
  Enter / Space  Advance dialogue or confirm
  Page Up        Roll back to previous line
  Page Down      Roll forward
  Ctrl (hold)    Skip through already-seen lines
  Tab            Toggle skipping on and off
  Q              In-scene buttons: Rewind, Skip and Pause menu
                 (during the story)
  F1             Accessibility settings (in the story and in menus)
  F              Toggle fullscreen / windowed
  H              Hide the text window. H, Enter or Space shows it
                 again
  S              Take a screenshot
  Delete         Delete selected save slot (on save screen)
  Escape         Open the pause menu
  Alt+F4         Open the quit prompt

----------------------------------------------------------------

Settings

Press F1 in the story or in any menu. Up and Down choose, Left, Right or
Enter change a setting, and Escape closes the list. Settings are saved
automatically.

  Read voice acted lines   Off by default, so the screen reader does not
                           talk over the actors.
  Speech output            Says whether Prism found NVDA, JAWS or another
                           screen reader, or is using Windows' voice.

----------------------------------------------------------------

Troubleshooting

The mod writes a11y_log.txt next to Brilliant Shadows.exe. Please include it
when you report a problem.

- No music after updating from 1.0: version 1.0's music slider didn't change
  the game's real music volume. 1.1.1 moves the level you chose to the real
  setting the first time it starts. Check Music volume in Preferences.

- Keys stop working after Alt+Tab: the mod clears a stuck Alt key by itself
  within a moment. If keys still don't respond, press and release Alt once.

----------------------------------------------------------------

Notes

- Page Up, or Rewind in the Q menu, goes back one line. On the very first
  line of the story this returns to the main menu, as the game's own rewind
  button does. Press R at any time to hear the current line again.

- Voice acted lines are not read unless you turn them on in the F1 settings.
  Narration is always read.

- When a prompt or the pause menu closes, the mod says what you were on
  before it opened.

- Your saves are not affected. This mod does not touch the game's story files.

- Prism (prism.dll) is licensed under the Mozilla Public License 2.0.
  See the prism_licenses folder.


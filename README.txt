Brilliant Shadows Accessibility Mod - Version 1.1.0

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
  F              Toggle fullscreen / windowed
  H              Hide or show the text window
  S              Take a screenshot
  Delete         Delete selected save slot (on save screen)
  Escape         Open the pause menu
  Alt+F4         Open the quit prompt

----------------------------------------------------------------

Notes

- The game does not include a built-in rewind system. This is by the developers'
  design. Press R at any time to hear the last line again.

- Your saves are not affected. This mod does not touch the game's story files.

- Prism (prism.dll) is licensed under the Mozilla Public License 2.0.
  See the prism_licenses folder.


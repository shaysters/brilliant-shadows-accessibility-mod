Brilliant Shadows Accessibility Mod - Version 1.0

Brilliant Shadows - Part One of the Book of Gray Magic is available on Steam:
https://store.steampowered.com/app/409920/Brilliant_Shadows__Part_One_of_the_Book_of_Gray_Magic/

Developed by Shaysters, with the assistance of Claude (Anthropic) and Codex (OpenAI),
to add full text-to-speech support and make the game fully playable for blind users.

Supported screen readers:
  Windows: NVDA, JAWS, or Windows SAPI (automatic fallback)
  Linux:   Orca (via speech-dispatcher)

----------------------------------------------------------------

Installing

1. Run the game once and let it reach the main menu, then close it.
   This allows Ren'Py to create files the mod needs to replace.

2. Find your Brilliant Shadows game folder. This is wherever Steam installed it.
   The folder contains a file called BrilliantShadows.exe on Windows, or
   BrilliantShadows.sh on Linux.

3. Extract the contents of this zip into that game folder.
   Allow it to overwrite files when asked.

4. Inside the game folder, open the game subfolder and delete these files
   if they are present:
     screens.rpyc
     brilliant_shadows_accessibility.rpyc
     zz_a11y_menu_override.rpyc

5. Launch the game with your screen reader already running.

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


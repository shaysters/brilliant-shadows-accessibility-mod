# Brilliant Shadows Accessibility: developer notes

A drop-in Ren'Py mod for Brilliant Shadows (Ren'Py 6.99, 32-bit Python 2.7). There is nothing to compile: the game loads the `.rpy` files in `game` and builds its own `.rpyc` files from them.

## Files

| Path | Purpose |
|---|---|
| `game/brilliant_shadows_accessibility.rpy` | Speech (Prism through ctypes), settings, keys and the log. |
| `game/screens_a11y.rpy` | Accessible versions of the screens, based on Ren'Py's public-domain screen template. |
| `game/zz_a11y_menu_override.rpy` | Text-only replacements for the game's menus, read aloud and used from the keyboard. |
| `prism.dll` | Prism, 32-bit. It must sit next to `Brilliant Shadows.exe`. |
| `prism_licenses/` | Prism's license and the licenses of the libraries it uses. |
| `README.txt` | The short readme that goes inside the release zip. |

To test, copy the files into the game folder as described in the README and start the game. The mod writes `a11y_log.txt` next to `Brilliant Shadows.exe`.

## Packaging and releasing

Build the release zip into `dist\BrilliantShadowsAccessibility.zip`:

```
powershell -ExecutionPolicy Bypass -File scripts\package-release.ps1
```

To publish a release:

1. Update the version in the README, `README.txt`, `changes-latest.md` and `CHANGELOG.md`.
2. Build the zip.
3. Create a draft GitHub release with the zip attached:

   ```
   gh release create vX.Y.Z --draft --notes-file changes-latest.md dist\BrilliantShadowsAccessibility.zip
   ```

4. Run the **Release** workflow from the Actions tab with the same tag. It builds the installer, writes `loadstone-release.json`, and publishes the release.

The installer's package files are in `loadstone-packages`, and its settings are in `installer\profile.json`. The installer reads the package files straight from this repository, so changes to them reach players a few minutes after they're pushed.

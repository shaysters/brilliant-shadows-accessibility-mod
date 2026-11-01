# Brilliant Shadows Accessibility Core
# Drop into the game's "game" folder.

init -100 python:
    import ctypes
    import os
    import re
    import time
    import traceback as _traceback

    # ---------------------------------------------------------------------------
    # Logging — writes to a11y_log.txt next to the game executable.
    # Each game session appends a dated block so multiple runs are readable.
    # ---------------------------------------------------------------------------

    def _a11y_log(msg):
        try:
            log_path = os.path.join(config.basedir, "a11y_log.txt")
            stamp = time.strftime("%Y-%m-%d %H:%M:%S")
            with open(log_path, "a") as _f:
                _f.write("[{0}] {1}\n".format(stamp, msg))
        except Exception:
            pass

    def _a11y_log_exc(context):
        try:
            _a11y_log("EXCEPTION in {0}:\n{1}".format(context, _traceback.format_exc()))
        except Exception:
            pass

    _a11y_log("=" * 60)
    _a11y_log("Brilliant Shadows A11y mod loading.")

    class _A11ySpeechProviderPrism(object):
        """Windows speech via prism.dll, which picks the best output available:
        NVDA, JAWS and other screen readers, or SAPI when none is running."""
        def __init__(self):
            self.name = "Prism"
            self.available = False
            self._dll = None
            self._backend = None
            self._load_error = None
            try:
                self._load()
            except Exception as ex:
                self._load_error = str(ex)
                _a11y_log_exc("Prism load")

        def _load(self):
            import sys
            if not sys.platform.startswith("win"):
                self._load_error = "Not Windows."
                return
            path = None
            for d in (config.basedir, config.gamedir):
                candidate = os.path.join(d, "prism.dll")
                if os.path.exists(candidate):
                    path = candidate
                    break
            if path is None:
                self._load_error = "prism.dll not found."
                _a11y_log("Prism: " + self._load_error)
                return

            class PrismConfig(ctypes.Structure):
                _fields_ = [
                    ("version", ctypes.c_uint8),
                    ("registry", ctypes.c_void_p),
                    ("availability_callback", ctypes.c_void_p),
                    ("availability_userdata", ctypes.c_void_p),
                    ("availability_poll_interval_ms", ctypes.c_uint32),
                    ("availability_debounce_samples", ctypes.c_uint32),
                    ("availability_backoff_max_ms", ctypes.c_uint32),
                    ("availability_auto_power_manage", ctypes.c_bool),
                    ("availability_baseline_callback", ctypes.c_void_p),
                ]

            dll = ctypes.CDLL(path)
            dll.prism_config_init.restype = PrismConfig
            dll.prism_config_init.argtypes = []
            dll.prism_init.restype = ctypes.c_void_p
            dll.prism_init.argtypes = [ctypes.POINTER(PrismConfig)]
            dll.prism_registry_acquire_best.restype = ctypes.c_void_p
            dll.prism_registry_acquire_best.argtypes = [ctypes.c_void_p]
            dll.prism_backend_initialize.restype = ctypes.c_int
            dll.prism_backend_initialize.argtypes = [ctypes.c_void_p]
            dll.prism_backend_name.restype = ctypes.c_char_p
            dll.prism_backend_name.argtypes = [ctypes.c_void_p]
            dll.prism_backend_output.restype = ctypes.c_int
            dll.prism_backend_output.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_bool]
            dll.prism_backend_stop.restype = ctypes.c_int
            dll.prism_backend_stop.argtypes = [ctypes.c_void_p]

            self._cfg = dll.prism_config_init()
            ctx = dll.prism_init(ctypes.byref(self._cfg))
            if not ctx:
                self._load_error = "prism_init failed."
                _a11y_log("Prism: " + self._load_error)
                return
            backend = dll.prism_registry_acquire_best(ctx)
            if not backend:
                self._load_error = "No speech backend available."
                _a11y_log("Prism: " + self._load_error)
                return
            err = dll.prism_backend_initialize(backend)
            # 15 = PRISM_ERROR_ALREADY_INITIALIZED, which is fine.
            if err not in (0, 15):
                self._load_error = "Backend initialize returned error {0}.".format(err)
                _a11y_log("Prism: " + self._load_error)
                return
            self._dll = dll
            self._ctx = ctx
            self._backend = backend
            self.name = dll.prism_backend_name(backend) or "Prism"
            self.available = True
            _a11y_log("Prism provider ready (backend: {0}, loaded from: {1})".format(self.name, path))

        def speak(self, text):
            if not self.available:
                return False
            try:
                if not isinstance(text, unicode):
                    text = text.decode("utf-8", "replace")
                # interrupt=True cancels current speech before speaking.
                return self._dll.prism_backend_output(self._backend, text.encode("utf-8"), True) == 0
            except Exception:
                return False

        def stop(self):
            if not self.available:
                return False
            try:
                return self._dll.prism_backend_stop(self._backend) == 0
            except Exception:
                return False


    class _A11ySpeechProviderSpeechD(object):
        """Linux speech-dispatcher provider via spd-say (used by Orca)."""
        def __init__(self):
            self.name = "SpeechD"
            self.available = False
            self._load_error = None
            self._load()

        def _load(self):
            import sys
            if not sys.platform.startswith("linux"):
                self._load_error = "Not Linux."
                return
            try:
                import subprocess
                proc = subprocess.Popen(
                    ["spd-say", "--version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                proc.wait()
                self.available = True
                _a11y_log("SpeechD (Orca) provider ready.")
            except Exception as ex:
                self._load_error = str(ex)
                _a11y_log("SpeechD load error: " + str(ex))

        def speak(self, text):
            if not self.available:
                return False
            try:
                import subprocess
                # -C cancels current speech before speaking, matching NVDA behaviour.
                subprocess.Popen(
                    ["spd-say", "-C", text],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                return True
            except Exception:
                return False

        def stop(self):
            if not self.available:
                return False
            try:
                import subprocess
                subprocess.Popen(
                    ["spd-say", "-S"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                return True
            except Exception:
                return False


    class _A11yState(object):
        def __init__(self):
            self.enabled = True
            self.auto_speak = True
            self.last_text = ""
            self.last_raw = ""
            self.last_story_text = ""
            self.last_story_raw = ""
            _prism = _A11ySpeechProviderPrism()
            _speechd = _A11ySpeechProviderSpeechD()
            if _prism.available:
                self.provider = _prism
                self.backend = "prism"
            elif _speechd.available:
                self.provider = _speechd
                self.backend = "speechd"
            else:
                # Nothing available; keep Prism provider as the inactive reference
                # so provider.available is False and the Ren'Py TTS path is used.
                self.provider = _prism
                self.backend = "system"
            _a11y_log("Active provider: {0} (backend: {1})".format(
                self.provider.name if self.provider.available else "none (SAPI fallback)",
                self.backend,
            ))
            self._last_announced_status = ""
            self.last_menu = None
            self.review_history = []
            self.review_index = -1
            self.splash_done = False
            self.splash_text_visible = False
            self.splash_index = 0
            self.splash_time_index = 0
            self.launch_epoch = time.time()
            self._last_skipping = False
            self._interface_hidden = False
            self.last_show_text = ""
            self.last_show_text_ts = 0.0
            self.last_black_announce_ts = 0.0

        def sanitize_text(self, text):
            if text is None:
                return ""
            # Strip common Ren'Py markup tags.
            cleaned = re.sub(r"\{[^}]*\}", "", unicode(text) if "unicode" in globals() else str(text))
            cleaned = re.sub(r"\s+", " ", cleaned).strip()
            return cleaned

        def notify(self, message):
            try:
                renpy.notify(message)
            except Exception:
                pass

        def speak(self, text, force=False):
            cleaned = self.sanitize_text(text)
            if not cleaned:
                return

            self.last_raw = text
            self.last_text = cleaned

            if not self.enabled and not force:
                return

            if self.provider.available:
                self.provider.speak(cleaned)

        def stop(self):
            if self.provider.available:
                self.provider.stop()

        def mode_summary(self):
            provider_msg = self.provider.name if self.provider.available else "SAPI"
            return "Speech: {0}. Auto-speak: {1}. Provider: {2}. Backend mode: {3}.".format(
                "on" if self.enabled else "off",
                "on" if self.auto_speak else "off",
                provider_msg,
                self.backend.upper(),
            )

        def announce_mode(self):
            summary = self.mode_summary()
            self._last_announced_status = summary
            self.notify(summary)
            self.speak(summary, force=True)


    if not hasattr(store, "_a11y_state"):
        store._a11y_state = _A11yState()

    _A11Y_SPLASH_LINES = (
        "Ithaqua Labs Presents.",
        "With many thanks to IDHAS Studio.",
        "Brilliant Shadows. Part One of The Book of Gray Magic.",
    )
    _A11Y_SPLASH_TIMES = (1.0, 3.1, 5.2)
    _A11Y_BLOOPER_LINES = set((
        "Hepitor",
        "Helicopter",
        "Kitten",
        "Infernal Contraptions",
        "Chocolate",
        "Tongue Twisters",
        "HP",
        "Bel",
        "Blass Glower",
        "The Food",
        "The End!",
    ))

    def _a11y_apply_backend_policy():
        # Always disable Ren'Py's built-in self-voicing to avoid duplicate
        # speech when NVDA or JAWS is active. When neither is running, SAPI
        # is driven explicitly from this mod (narration/thought text only).
        try:
            if hasattr(store, "_preferences"):
                store._preferences.self_voicing = False
                p = store._a11y_state.provider
                if p and p.available:
                    store._a11y_state.backend = p.name.lower()
                else:
                    store._a11y_state.backend = "sapi"
        except Exception:
            pass
        try:
            currently_skipping = bool(getattr(config, "skipping", False))
            was_skipping = store._a11y_state._last_skipping
            if currently_skipping != was_skipping:
                store._a11y_state._last_skipping = currently_skipping
                if currently_skipping:
                    _a11y_speak_now("Skipping.")
                else:
                    _a11y_speak_now("Skipping stopped.")
        except Exception:
            pass

    _a11y_apply_backend_policy()

    def a11y_toggle_enabled():
        store._a11y_state.enabled = not store._a11y_state.enabled
        store._a11y_state.announce_mode()

    def a11y_toggle_auto_speak():
        store._a11y_state.auto_speak = not store._a11y_state.auto_speak
        store._a11y_state.announce_mode()

    def a11y_repeat_last():
        if store._a11y_state.last_story_text:
            try:
                nvda_active = bool(store._a11y_state.provider and store._a11y_state.provider.available)
            except Exception:
                nvda_active = False

            if nvda_active:
                store._a11y_state.speak(store._a11y_state.last_story_text, force=True)
            else:
                try:
                    renpy.display.tts.tts(store._a11y_state.last_story_text)
                except Exception:
                    pass
        else:
            store._a11y_state.notify("No story line to repeat.")

    def a11y_stop():
        store._a11y_state.stop()
        store._a11y_state.notify("Speech stopped.")

    def a11y_announce_status():
        store._a11y_state.announce_mode()

    def _a11y_speak_blooper_title(line):
        try:
            st = store._a11y_state
            st.last_story_raw = line
            st.last_story_text = line
            if not st.review_history or st.review_history[-1] != line:
                st.review_history.append(line)
                if len(st.review_history) > 400:
                    st.review_history = st.review_history[-400:]
            st.review_index = len(st.review_history) - 1

            nvda_active = bool(st.provider and st.provider.available)
            if nvda_active:
                st.speak(line, force=True)
            else:
                renpy.display.tts.tts(line)
        except Exception:
            pass

    def _a11y_voice_playing():
        # Ren'Py 6 API compatibility: prefer get_playing on the voice channel.
        try:
            playing = renpy.music.get_playing(channel="voice")
            if playing:
                return True
        except Exception:
            try:
                playing = renpy.music.get_playing("voice")
                if playing:
                    return True
            except Exception:
                pass

        try:
            return bool(renpy.music.is_playing(channel="voice"))
        except Exception:
            try:
                return bool(renpy.music.is_playing("voice"))
            except Exception:
                return False

    def a11y_read_line(who, what):
        # Don't speak during skip — lines go by too fast for TTS to be useful.
        try:
            if getattr(config, "skipping", False):
                return
        except Exception:
            pass

        # Explicit screen-level hook for dialogue/narration lines.
        if store.a11y_suppress_line_count > 0:
            store.a11y_suppress_line_count -= 1
            return

        if store.a11y_suppress_line_once:
            store.a11y_suppress_line_once = False
            return

        # If any menu/prompt is open, suppress line capture/read to avoid
        # stale dialogue being spoken over menu prompts (e.g. quit dialog).
        if _a11y_current_menu() is not None:
            return

        text = what
        try:
            if who:
                text = "{0}. {1}".format(who, what)
        except Exception:
            text = what

        try:
            cleaned = store._a11y_state.sanitize_text(text)
            if cleaned:
                try:
                    if cleaned in _A11Y_SPLASH_LINES:
                        idx = list(_A11Y_SPLASH_LINES).index(cleaned) + 1
                        if idx > store._a11y_state.splash_time_index:
                            store._a11y_state.splash_time_index = idx
                        if idx >= len(_A11Y_SPLASH_LINES):
                            store._a11y_state.splash_done = True
                except Exception:
                    pass
                store._a11y_state.last_story_raw = text
                store._a11y_state.last_story_text = cleaned
                if not store._a11y_state.review_history or store._a11y_state.review_history[-1] != cleaned:
                    store._a11y_state.review_history.append(cleaned)
                    if len(store._a11y_state.review_history) > 400:
                        store._a11y_state.review_history = store._a11y_state.review_history[-400:]
                store._a11y_state.review_index = len(store._a11y_state.review_history) - 1
        except Exception:
            pass

        try:
            nvda_active = bool(store._a11y_state.provider and store._a11y_state.provider.available)
        except Exception:
            nvda_active = False

        # For SAPI, auto-read narration/thought text only.
        if (not nvda_active) and who:
            return

        # Skip voiced speaker lines to avoid duplicating voice-acted dialogue,
        # unless turned on in the F1 settings. Narration is always read.
        if _a11y_voice_playing() and who and not persistent.a11y_read_voiced:
            return

        if nvda_active:
            store._a11y_state.speak(text)
        else:
            try:
                renpy.display.tts.tts(cleaned if 'cleaned' in locals() else text)
            except Exception:
                pass

    def a11y_review_prev():
        history = store._a11y_state.review_history
        if not history:
            store._a11y_state.notify("No text to review.")
            return
        idx = store._a11y_state.review_index
        if idx < 0:
            idx = len(history) - 1
        else:
            idx = max(0, idx - 1)
        store._a11y_state.review_index = idx
        store._a11y_state.speak(history[idx], force=True)

    def a11y_review_next():
        history = store._a11y_state.review_history
        if not history:
            store._a11y_state.notify("No text to review.")
            return
        idx = store._a11y_state.review_index
        if idx < 0:
            idx = len(history) - 1
        else:
            idx = min(len(history) - 1, idx + 1)
        store._a11y_state.review_index = idx
        store._a11y_state.speak(history[idx], force=True)

    def a11y_choice_on_show(items):
        # Capture and speak choice prompt text (caption rows with no action),
        # like "But where to go?" so it is available for Up-repeat.
        try:
            prompt = ""
            first_option = ""
            for caption, action, chosen in items:
                if not action:
                    prompt = store._a11y_state.sanitize_text(caption)
                    if prompt:
                        continue
                elif not first_option:
                    first_option = store._a11y_state.sanitize_text(caption)

            announce = prompt if prompt else "Make a choice."

            store._a11y_state.last_story_raw = announce
            store._a11y_state.last_story_text = announce

            if not store._a11y_state.review_history or store._a11y_state.review_history[-1] != announce:
                store._a11y_state.review_history.append(announce)
                if len(store._a11y_state.review_history) > 400:
                    store._a11y_state.review_history = store._a11y_state.review_history[-400:]
            store._a11y_state.review_index = len(store._a11y_state.review_history) - 1

            nvda_active = bool(store._a11y_state.provider and store._a11y_state.provider.available)
            if nvda_active:
                store._a11y_state.speak(announce, force=True)
                if first_option:
                    store._a11y_state.speak(first_option, force=True)
            else:
                renpy.display.tts.tts(announce)
                if first_option:
                    renpy.display.tts.tts(first_option)
        except Exception:
            pass

    def _a11y_choice_options(items):
        options = []
        for caption, action, chosen in items:
            if action:
                options.append((store._a11y_state.sanitize_text(caption), action))
        return options

    def a11y_choice_move(items, delta):
        try:
            options = _a11y_choice_options(items)
            if not options:
                return
            idx = getattr(store, "a11y_choice_index", 0)
            idx = (idx + delta) % len(options)
            store.a11y_choice_index = idx
            label = options[idx][0]
            nvda_active = bool(store._a11y_state.provider and store._a11y_state.provider.available)
            if nvda_active:
                store._a11y_state.speak(label, force=True)
            else:
                renpy.display.tts.tts(label)
        except Exception:
            _a11y_log_exc("a11y_choice_move(delta={0}, items_count={1})".format(
                delta, len(items) if items else 0))

    def a11y_choice_set(items, idx):
        try:
            options = _a11y_choice_options(items)
            if not options:
                return
            idx = max(0, min(idx, len(options) - 1))
            store.a11y_choice_index = idx
            label = options[idx][0]
            nvda_active = bool(store._a11y_state.provider and store._a11y_state.provider.available)
            if nvda_active:
                store._a11y_state.speak(label, force=True)
            else:
                renpy.display.tts.tts(label)
        except Exception:
            pass

    def a11y_choice_activate(items):
        try:
            options = _a11y_choice_options(items)
            if not options:
                return
            idx = getattr(store, "a11y_choice_index", 0)
            if idx < 0 or idx >= len(options):
                idx = 0
                store.a11y_choice_index = idx
            action = options[idx][1]
            ok = _a11y_run(action)
            if ok is False:
                store._a11y_state.notify("Choice activation failed.")
        except Exception:
            _a11y_log_exc("a11y_choice_activate(items_count={0}, index={1})".format(
                len(items) if items else 0, getattr(store, "a11y_choice_index", "?")))
            try:
                store._a11y_state.notify("Choice activation failed.")
            except Exception:
                pass

    def a11y_announce_credits():
        message = "Credits are on screen. Wait a few seconds to hear bloopers."
        try:
            nvda_active = bool(store._a11y_state.provider and store._a11y_state.provider.available)
        except Exception:
            nvda_active = False

        try:
            if nvda_active:
                store._a11y_state.speak(message, force=True)
            else:
                renpy.display.tts.tts(message)
        except Exception:
            try:
                renpy.notify(message)
            except Exception:
                pass

    if not hasattr(store, "a11y_main_index"):
        store.a11y_main_index = 0
    if not hasattr(store, "a11y_esc_index"):
        store.a11y_esc_index = 0
    if not hasattr(store, "a11y_save_index"):
        store.a11y_save_index = 0
    if not hasattr(store, "a11y_load_index"):
        store.a11y_load_index = 0
    if not hasattr(store, "a11y_pref_index"):
        store.a11y_pref_index = 0
    if not hasattr(store, "a11y_yesno_index"):
        store.a11y_yesno_index = 0
    if not hasattr(store, "a11y_choice_index"):
        store.a11y_choice_index = 0
    if not hasattr(store, "a11y_suppress_line_once"):
        store.a11y_suppress_line_once = False
    if not hasattr(store, "a11y_suppress_line_count"):
        store.a11y_suppress_line_count = 0

    def _a11y_current_menu():
        if renpy.get_screen("yesno_prompt"):
            return "yesno_prompt"
        if renpy.get_screen("preferences"):
            return "preferences"
        if renpy.get_screen("load"):
            return "load"
        if renpy.get_screen("save"):
            return "save"
        if renpy.get_screen("esc_menu"):
            return "esc_menu"
        if renpy.get_screen("a11y_main_menu"):
            return "main_menu"
        if renpy.get_screen("main_menu"):
            return "main_menu"
        return None

    def _a11y_menu_labels(menu):
        if menu == "main_menu":
            return ("Start", "Load", "Preferences", "Information", "Quit")
        if menu == "esc_menu":
            return ("Resume", "Save", "Load", "Preferences", "Main Menu", "Quit")
        if menu == "save":
            return ("Save slot 1", "Save slot 2", "Previous page", "Next page", "Back")
        if menu == "load":
            return ("Load slot 1", "Load slot 2", "Previous page", "Next page", "Back")
        if menu == "preferences":
            return ("Fullscreen", "Windowed", "Skip all", "Skip seen", "After choices stop", "After choices skip", "Transitions all", "Transitions none", "Back")
        if menu == "yesno_prompt":
            return ("Yes", "No")
        return ()

    def _a11y_menu_var(menu):
        if menu == "main_menu":
            return "a11y_main_index"
        if menu == "esc_menu":
            return "a11y_esc_index"
        if menu == "save":
            return "a11y_save_index"
        if menu == "load":
            return "a11y_load_index"
        if menu == "preferences":
            return "a11y_pref_index"
        if menu == "yesno_prompt":
            return "a11y_yesno_index"
        return None

    def _a11y_run(action):
        # Prefer Ren'Py's standard action runner so keyboard activation matches
        # normal button clicks (handles Action objects/lists reliably).
        if isinstance(action, (list, tuple)):
            any_ok = False
            for part in action:
                part_ok = _a11y_run(part)
                if part_ok is not False:
                    any_ok = True
            return any_ok

        try:
            renpy.display.behavior.run(action)
            return True
        except Exception:
            pass

        try:
            renpy.run(action)
            return True
        except Exception:
            try:
                action()
                return True
            except Exception:
                return False

    def a11y_nav_announce_current():
        menu = _a11y_current_menu()
        if menu is None:
            store._a11y_state.last_menu = None
            return

        labels = _a11y_menu_labels(menu)
        var_name = _a11y_menu_var(menu)
        if not labels or not var_name:
            return

        if store._a11y_state.last_menu != menu:
            idx = getattr(store, var_name, 0)
            if idx < 0 or idx >= len(labels):
                idx = 0
                setattr(store, var_name, idx)
            store._a11y_state.last_menu = menu
            a11y_focus(labels[idx])

    def a11y_nav_move(delta):
        menu = _a11y_current_menu()
        labels = _a11y_menu_labels(menu)
        var_name = _a11y_menu_var(menu)
        if not labels or not var_name:
            return

        idx = getattr(store, var_name, 0)
        idx = (idx + delta) % len(labels)
        setattr(store, var_name, idx)
        a11y_focus(labels[idx])

    def a11y_nav_activate():
        menu = _a11y_current_menu()
        var_name = _a11y_menu_var(menu)
        if not menu or not var_name:
            return

        idx = getattr(store, var_name, 0)

        if menu == "main_menu":
            if idx == 0:
                _a11y_run(Start())
            elif idx == 1:
                _a11y_run(ShowMenu("load"))
            elif idx == 2:
                _a11y_run(ShowMenu("preferences"))
            elif idx == 3:
                _a11y_run(OpenURL("http://ithaqualabs.com/home/?p=75"))
            else:
                _a11y_run(Quit())
            return

        if menu == "esc_menu":
            if idx == 0:
                _a11y_run(Return())
            elif idx == 1:
                _a11y_run(ShowMenu("save"))
            elif idx == 2:
                _a11y_run(ShowMenu("load"))
            elif idx == 3:
                _a11y_run(ShowMenu("preferences"))
            elif idx == 4:
                _a11y_run(MainMenu())
            else:
                _a11y_run(Quit(confirm=True))
            return

        if menu == "save":
            if idx == 0:
                _a11y_run(FileSave(1))
            elif idx == 1:
                _a11y_run(FileSave(2))
            elif idx == 2:
                _a11y_run(FilePagePrevious())
            elif idx == 3:
                _a11y_run(FilePageNext())
            else:
                _a11y_run(Return())
            return

        if menu == "load":
            if idx == 0:
                _a11y_run(FileLoad(1))
            elif idx == 1:
                _a11y_run(FileLoad(2))
            elif idx == 2:
                _a11y_run(FilePagePrevious())
            elif idx == 3:
                _a11y_run(FilePageNext())
            else:
                _a11y_run(Return())
            return

        if menu == "preferences":
            if idx == 0:
                _a11y_run(Preference("display", "fullscreen"))
            elif idx == 1:
                _a11y_run(Preference("display", "window"))
            elif idx == 2:
                _a11y_run(Preference("skip", "all"))
            elif idx == 3:
                _a11y_run(Preference("skip", "seen"))
            elif idx == 4:
                _a11y_run(Preference("after choices", "stop"))
            elif idx == 5:
                _a11y_run(Preference("after choices", "skip"))
            elif idx == 6:
                _a11y_run(Preference("transitions", "all"))
            elif idx == 7:
                _a11y_run(Preference("transitions", "none"))
            else:
                _a11y_run(Return())
            return

        if menu == "yesno_prompt":
            # yes/no prompt uses its local actions.
            return

    def _a11y_capture_text(text):
        # Keep filter mostly side-effect free to avoid queueing.
        # Exception: explicit blooper title cards should always be spoken.
        try:
            cleaned = store._a11y_state.sanitize_text(text)
            if cleaned in _A11Y_BLOOPER_LINES:
                _a11y_speak_blooper_title(cleaned)
        except Exception:
            pass
        return text

    _a11y_prev_filter = config.say_menu_text_filter

    def _a11y_text_filter(text):
        if _a11y_prev_filter is not None:
            text = _a11y_prev_filter(text)
        return _a11y_capture_text(text)

    config.say_menu_text_filter = _a11y_text_filter

    def _extend_keymap(binding, extra_keys):
        current = list(config.keymap.get(binding, []))
        changed = False
        for key in extra_keys:
            if key not in current:
                current.append(key)
                changed = True
        if changed:
            config.keymap[binding] = current

    def _remove_keys_from_binding(binding, keys):
        current = list(config.keymap.get(binding, []))
        new_current = [k for k in current if k not in keys]
        if new_current != current:
            config.keymap[binding] = new_current

    def _a11y_track_splash():
        # Detect launch splash "show text" sequence without patching script.rpy.
        try:
            st = store._a11y_state
            if st.splash_done:
                return

            # Time-based fallback: some Ren'Py 6 builds do not expose splash
            # text via showing("text"), so announce by startup timing.
            elapsed = time.time() - st.launch_epoch
            while st.splash_time_index < len(_A11Y_SPLASH_LINES) and elapsed >= _A11Y_SPLASH_TIMES[st.splash_time_index]:
                line = _A11Y_SPLASH_LINES[st.splash_time_index]
                st.last_story_raw = line
                st.last_story_text = line
                if not st.review_history or st.review_history[-1] != line:
                    st.review_history.append(line)
                    if len(st.review_history) > 400:
                        st.review_history = st.review_history[-400:]
                st.review_index = len(st.review_history) - 1

                nvda_active = bool(st.provider and st.provider.available)
                if nvda_active:
                    st.speak(line, force=True)
                else:
                    renpy.display.tts.tts(line)

                st.splash_time_index += 1

            if st.splash_time_index >= len(_A11Y_SPLASH_LINES):
                st.splash_done = True
                return

            text_showing = False
            try:
                text_showing = bool(renpy.showing("text"))
            except Exception:
                text_showing = False

            if text_showing and not st.splash_text_visible:
                st.splash_text_visible = True
                idx = st.splash_index
                if idx < len(_A11Y_SPLASH_LINES):
                    line = _A11Y_SPLASH_LINES[idx]
                    st.last_story_raw = line
                    st.last_story_text = line
                    if not st.review_history or st.review_history[-1] != line:
                        st.review_history.append(line)
                        if len(st.review_history) > 400:
                            st.review_history = st.review_history[-400:]
                    st.review_index = len(st.review_history) - 1

                    nvda_active = bool(st.provider and st.provider.available)
                    if nvda_active:
                        st.speak(line, force=True)
                    else:
                        renpy.display.tts.tts(line)
                st.splash_index = idx + 1
            elif (not text_showing) and st.splash_text_visible:
                st.splash_text_visible = False
                if st.splash_index >= len(_A11Y_SPLASH_LINES):
                    st.splash_done = True
        except Exception:
            pass

    def _a11y_extract_displayable_text(what):
        try:
            if what is None:
                return ""
            text_value = getattr(what, "text", None)
            if text_value is None:
                return ""

            if isinstance(text_value, (list, tuple)):
                parts = []
                for item in text_value:
                    if isinstance(item, basestring if "basestring" in globals() else str):
                        parts.append(item)
                    elif isinstance(item, (list, tuple)) and item:
                        head = item[0]
                        if isinstance(head, basestring if "basestring" in globals() else str):
                            parts.append(head)
                text_value = " ".join(parts)

            cleaned = store._a11y_state.sanitize_text(text_value)
            return cleaned
        except Exception:
            return ""

    _a11y_orig_show = renpy.show

    def _a11y_show_proxy(name, *args, **kwargs):
        try:
            st = store._a11y_state
            lowered_name = (name or "").lower()
            lowered_tag = (kwargs.get("tag", "") or "").lower()

            # Announce scene fades to black so silent transitions are detectable.
            if (lowered_name in ("black", "bg black") or lowered_name.startswith("bg black")):
                now_black = time.time()
                if (now_black - st.last_black_announce_ts) > 1.25:
                    st.last_black_announce_ts = now_black
                    line_black = "Black screen."
                    st.last_story_raw = line_black
                    st.last_story_text = line_black
                    if not st.review_history or st.review_history[-1] != line_black:
                        st.review_history.append(line_black)
                        if len(st.review_history) > 400:
                            st.review_history = st.review_history[-400:]
                    st.review_index = len(st.review_history) - 1

                    nvda_active = bool(st.provider and st.provider.available)
                    if nvda_active:
                        st.speak(line_black, force=True)
                    else:
                        renpy.display.tts.tts(line_black)

            tag_name = kwargs.get("tag", None) or name
            if tag_name == "text":
                spoken = _a11y_extract_displayable_text(kwargs.get("what", None))
                if spoken:
                    now = time.time()
                    # De-dupe rapid re-shows of the same card.
                    if spoken != st.last_show_text or (now - st.last_show_text_ts) > 0.75:
                        st.last_show_text = spoken
                        st.last_show_text_ts = now
                        st.last_story_raw = spoken
                        st.last_story_text = spoken
                        if not st.review_history or st.review_history[-1] != spoken:
                            st.review_history.append(spoken)
                            if len(st.review_history) > 400:
                                st.review_history = st.review_history[-400:]
                        st.review_index = len(st.review_history) - 1

                        nvda_active = bool(st.provider and st.provider.available)
                        if nvda_active:
                            st.speak(spoken, force=True)
                        else:
                            renpy.display.tts.tts(spoken)
        except Exception:
            pass
        return _a11y_orig_show(name, *args, **kwargs)

    renpy.show = _a11y_show_proxy

    def _a11y_speak_now(text):
        """Speak via whichever provider is active, bypassing enabled/auto flags."""
        try:
            p = store._a11y_state.provider
            if p and p.available:
                p.speak(text)
            else:
                renpy.display.tts.tts(text)
        except Exception:
            pass

    def a11y_toggle_fullscreen():
        try:
            is_full = bool(getattr(preferences, "fullscreen", False))
            if is_full:
                _a11y_run(Preference("display", "window"))
                _a11y_speak_now("Windowed mode.")
            else:
                _a11y_run(Preference("display", "fullscreen"))
                _a11y_speak_now("Fullscreen mode.")
        except Exception:
            pass

    def a11y_toggle_interface():
        # HideInterface waits until H, Enter, Space or a click, then returns.
        try:
            _a11y_speak_now("Text hidden. Press H, Enter or Space to show it again.")
            _a11y_run(HideInterface())
            _a11y_speak_now("Text visible.")
        except Exception:
            _a11y_log_exc("a11y_toggle_interface")

    def a11y_screenshot():
        try:
            _a11y_run(Screenshot())
            _a11y_speak_now("Screenshot saved.")
        except Exception:
            pass

    def a11y_save_delete():
        try:
            idx = store.a11y_save_index
            if idx == 0:
                _a11y_run(FileDelete(1))
                _a11y_speak_now("Save slot 1 deleted.")
            elif idx == 1:
                _a11y_run(FileDelete(2))
                _a11y_speak_now("Save slot 2 deleted.")
            else:
                _a11y_speak_now("No save slot selected.")
        except Exception:
            pass

    # Keyboard improvements for common VN interaction patterns.
    _extend_keymap("dismiss", ["K_RETURN", "K_KP_ENTER", "K_SPACE"])
    _extend_keymap("game_menu", ["K_ESCAPE"])
    _extend_keymap("rollback", ["K_PAGEUP"])
    _extend_keymap("rollforward", ["K_PAGEDOWN"])
    _extend_keymap("focus_left", ["K_LEFT", "repeat_K_LEFT"])
    _extend_keymap("focus_right", ["K_RIGHT", "repeat_K_RIGHT"])
    _extend_keymap("focus_up", ["K_UP", "repeat_K_UP"])
    _extend_keymap("focus_down", ["K_DOWN", "repeat_K_DOWN"])
    _extend_keymap("button_select", ["K_RETURN", "K_KP_ENTER", "K_SPACE"])

    _remove_keys_from_binding("quit", ["alt_K_F4", "K_F4"])

    if _a11y_track_splash not in config.overlay_functions:
        config.overlay_functions.append(_a11y_track_splash)


screen brilliant_shadows_a11y_hotkeys():
    zorder 200

    # Keep backend policy synchronized after startup as preferences become available.
    timer 0.50 repeat True action [Function(_a11y_apply_backend_policy), Function(_a11y_reread_check)]

    key "K_r" action Function(a11y_repeat_last)
    key "K_f" action Function(a11y_toggle_fullscreen)
    key "K_h" action Function(a11y_toggle_interface)
    key "K_s" action Function(a11y_screenshot)
    key "K_q" action Show("bs_a11y_popup", kind="scene")
    key "K_F1" action Show("bs_a11y_popup", kind="settings")
    key "alt_K_F4" action Function(a11y_open_quit_prompt, True)
    key "quit" action Function(a11y_open_quit_prompt, True)


init 999 python:
    if "brilliant_shadows_a11y_hotkeys" not in config.overlay_screens:
        config.overlay_screens.append("brilliant_shadows_a11y_hotkeys")


# ---------------------------------------------------------------------------
# Update check. Once per game start, asks GitHub for the latest release and
# says so if it's newer than this version. Reads the release manifest the
# installer itself uses (a plain redirect, no API token or rate limit).
# This Python has no SSL support, so the request goes through Windows' own
# curl.exe in the background, polled from a periodic callback. Nothing is
# sent except the request itself, and a failed check is only logged.
# ---------------------------------------------------------------------------

init 2 python:
    A11Y_VERSION = "1.1.2"
    _A11Y_UPDATE_URL = "https://github.com/shaysters/brilliant-shadows-accessibility-mod/releases/latest/download/loadstone-release.json"
    # The announcement waits for the main menu and this much silence, so it
    # neither cuts off the opening speech nor gets cut off by it.
    _A11Y_UPDATE_QUIET = 2.0

    _a11y_update = {"proc": None, "latest": None, "done": False}
    _a11y_last_speech = [time.time()]

    def _a11y_track_speech(provider):
        # Note when anything is spoken, so the update notice can wait for a pause.
        orig = provider.speak
        def speak(*args, **kwargs):
            _a11y_last_speech[0] = time.time()
            return orig(*args, **kwargs)
        provider.speak = speak

    try:
        _a11y_track_speech(store._a11y_state.provider)
    except Exception:
        _a11y_log_exc("update check speech tracking")

    def _a11y_update_announce(latest):
        text = "Brilliant Shadows Accessibility version {0} is available. Run the installer to update.".format(latest)
        st = store._a11y_state
        _a11y_log("Update announced.")
        # R repeats it until the story starts.
        if not st.last_story_text:
            st.last_story_text = text
        p = st.provider
        if p and p.available and getattr(p, "_dll", None):
            p._dll.prism_backend_output(p._backend, text.encode("utf-8"), False)
        else:
            _a11y_speak_now(text)

    def _a11y_version_tuple(s):
        try:
            return tuple(int(p) for p in s.split("."))
        except Exception:
            return None

    def _a11y_update_tick():
        u = _a11y_update
        if u["done"]:
            return
        try:
            if u["latest"]:
                # A newer version was found; announce it at the main menu after a pause.
                if renpy.get_screen("a11y_main_menu") and time.time() - _a11y_last_speech[0] >= _A11Y_UPDATE_QUIET:
                    u["done"] = True
                    _a11y_update_announce(u["latest"])
                return
            if u["proc"] is None:
                curl =os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "System32", "curl.exe")
                if not os.path.exists(curl):
                    curl = "curl"
                import subprocess
                startupinfo = None
                if hasattr(subprocess, "STARTUPINFO"):
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= 1  # STARTF_USESHOWWINDOW: keep the console hidden
                u["proc"] = subprocess.Popen(
                    [curl, "-s", "-L", "--max-time", "15", _A11Y_UPDATE_URL],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo)
                return
            if u["proc"].poll() is None:
                return
            out = u["proc"].stdout.read()
            m = re.search(r'"version"\s*:\s*"v?([0-9.]+)"', out or "")
            if not m:
                u["done"] = True
                _a11y_log("Update check skipped (exit code {0}).".format(u["proc"].returncode))
                return
            latest = m.group(1)
            _a11y_log("Update check: installed {0}, latest {1}".format(A11Y_VERSION, latest))
            lv, iv = _a11y_version_tuple(latest), _a11y_version_tuple(A11Y_VERSION)
            if lv and iv and lv > iv:
                u["latest"] = latest
            else:
                u["done"] = True
        except Exception:
            u["done"] = True
            _a11y_log_exc("update check")

    config.periodic_callbacks.append(_a11y_update_tick)


# ---------------------------------------------------------------------------
# Settings, saved volumes and keyboard safety.
# ---------------------------------------------------------------------------

init 1 python:
    if persistent.a11y_read_voiced is None:
        persistent.a11y_read_voiced = False

    # Version 1.0 stored its volume sliders in fields the game never used, so
    # the real volumes stayed where they were. Apply what the player chose
    # there once, then remove the old fields.
    for _a11y_old, _a11y_mixer in (("music_volume", "music"), ("sound_volume", "sfx"), ("voice_volume", "voice")):
        if _a11y_old in _preferences.__dict__:
            try:
                _preferences.set_volume(_a11y_mixer, float(_preferences.__dict__.pop(_a11y_old)))
                _a11y_log("Moved old {0} setting to the {1} volume.".format(_a11y_old, _a11y_mixer))
            except Exception:
                _a11y_log_exc("volume migration")

    def _a11y_reset_channel_volumes():
        # Version 1.0 also lowered the music channel itself, which is kept in
        # save files. Reset it so only the Preferences volume applies.
        for channel in ("music", "am2"):
            try:
                renpy.music.set_volume(1.0, channel=channel)
            except Exception:
                pass

    config.after_load_callbacks.append(_a11y_reset_channel_volumes)

    # Alt+Tab or Alt+F4 can leave SDL thinking Alt is still held, and then
    # every plain key is ignored. Clear any modifier no key is holding down.
    import pygame_sdl2 as _a11y_pygame

    _A11Y_MODIFIERS = (
        ((_a11y_pygame.K_LALT, _a11y_pygame.K_RALT), _a11y_pygame.KMOD_ALT),
        ((_a11y_pygame.K_LCTRL, _a11y_pygame.K_RCTRL), _a11y_pygame.KMOD_CTRL),
        ((_a11y_pygame.K_LSHIFT, _a11y_pygame.K_RSHIFT), _a11y_pygame.KMOD_SHIFT),
        ((_a11y_pygame.K_LGUI, _a11y_pygame.K_RGUI), _a11y_pygame.KMOD_META),
    )
    _A11Y_ALL_MODIFIERS = (_a11y_pygame.KMOD_ALT | _a11y_pygame.KMOD_CTRL |
                           _a11y_pygame.KMOD_SHIFT | _a11y_pygame.KMOD_META)

    def _a11y_unstick_modifiers():
        try:
            mods = _a11y_pygame.key.get_mods()
            if not mods & _A11Y_ALL_MODIFIERS:
                return
            pressed = _a11y_pygame.key.get_pressed()
            held = 0
            for keys, flag in _A11Y_MODIFIERS:
                if any(pressed[k] for k in keys):
                    held |= mods & flag
            if held != mods & _A11Y_ALL_MODIFIERS:
                _a11y_pygame.key.set_mods((mods & ~_A11Y_ALL_MODIFIERS) | held)
        except Exception:
            pass

    config.periodic_callbacks.append(_a11y_unstick_modifiers)

    # -----------------------------------------------------------------------
    # Saying what was selected when a prompt or menu closes, the way a
    # screen reader returns focus.
    # -----------------------------------------------------------------------

    store.a11y_reread_pending = False

    def a11y_after_prompt():
        try:
            menu = _a11y_current_menu()
            if menu == "preferences":
                a11y_pref_announce(getattr(store, "a11y_pref_index", 0))
                return
            if menu is not None and menu != "yesno_prompt":
                labels = _a11y_menu_labels(menu)
                var_name = _a11y_menu_var(menu)
                if labels and var_name:
                    idx = getattr(store, var_name, 0)
                    if 0 <= idx < len(labels):
                        _a11y_speak_now(labels[idx])
                        return
            if renpy.get_screen("say") is not None and store._a11y_state.last_story_text:
                _a11y_speak_now(store._a11y_state.last_story_text)
        except Exception:
            _a11y_log_exc("a11y_after_prompt")

    def a11y_mark_return():
        # Leaving the pause menu for the story: read the current line once back.
        if not renpy.context()._main_menu:
            store.a11y_reread_pending = True

    def _a11y_reread_check():
        # Called from the story hotkey overlay's timer.
        if store.a11y_reread_pending:
            store.a11y_reread_pending = False
            if renpy.get_screen("say") is not None and store._a11y_state.last_story_text:
                _a11y_speak_now(store._a11y_state.last_story_text)

    # -----------------------------------------------------------------------
    # Q: the in-scene buttons. F1: accessibility settings.
    # -----------------------------------------------------------------------

    store.a11y_popup_index = 0

    def _a11y_voiced_label():
        return "Read voice acted lines: {0}.".format("on" if persistent.a11y_read_voiced else "off")

    def _a11y_voiced_toggle(delta=1):
        persistent.a11y_read_voiced = not persistent.a11y_read_voiced
        _a11y_speak_now(_a11y_voiced_label())

    def _a11y_speech_label():
        p = store._a11y_state.provider
        return "Speech output: {0}.".format(p.name if p.available else "Ren'Py text to speech")

    def _a11y_scene_press(action):
        def run():
            renpy.hide_screen("bs_a11y_popup")
            return _a11y_run(action)
        return run

    def _a11y_popup_items(menu):
        # Each item is (label function, Enter function, Left/Right function).
        if menu == "settings":
            return [
                (_a11y_voiced_label, _a11y_voiced_toggle, _a11y_voiced_toggle),
                (_a11y_speech_label, None, None),
                (lambda: "Close", a11y_popup_close, None),
            ]
        return [
            (lambda: "Rewind. Go back one line.", _a11y_scene_press(Rollback()), None),
            (lambda: "Skip. Fast forward through lines you have read.", _a11y_scene_press(Skip()), None),
            (lambda: "Pause menu.", _a11y_scene_press(ShowMenu("esc_menu", transition=dissolve)), None),
            (lambda: "Close", a11y_popup_close, None),
        ]

    def a11y_popup_open(menu):
        store.a11y_popup_index = 0
        title = "Accessibility settings." if menu == "settings" else "In-scene buttons."
        _a11y_speak_now("{0} {1}".format(title, _a11y_popup_items(menu)[0][0]()))

    def a11y_popup_move(menu, delta):
        items = _a11y_popup_items(menu)
        store.a11y_popup_index = (store.a11y_popup_index + delta) % len(items)
        _a11y_speak_now(items[store.a11y_popup_index][0]())

    def a11y_popup_adjust(menu, delta):
        item = _a11y_popup_items(menu)[store.a11y_popup_index]
        if item[2] is None:
            return a11y_popup_move(menu, delta)
        item[2](delta)

    def a11y_popup_activate(menu):
        item = _a11y_popup_items(menu)[store.a11y_popup_index]
        if item[1] is None:
            _a11y_speak_now(item[0]())
            return
        if menu == "scene" and store.a11y_popup_index == 0 and not renpy.can_rollback():
            _a11y_speak_now("Unavailable. There is no earlier line to go back to.")
            return
        return item[1]()

    def a11y_popup_close():
        renpy.hide_screen("bs_a11y_popup")
        a11y_after_prompt()


screen bs_a11y_popup(kind):
    modal True
    zorder 300

    frame:
        xalign 0.5
        yalign 0.5
        xpadding 30
        ypadding 30
        has vbox
        text ("Accessibility settings" if kind == "settings" else "In-scene buttons")
        text "Up and Down choose, Enter selects, Escape closes." size 20

    on "show" action Function(a11y_popup_open, kind)
    key "K_UP" action Function(a11y_popup_move, kind, -1)
    key "K_DOWN" action Function(a11y_popup_move, kind, 1)
    key "K_LEFT" action Function(a11y_popup_adjust, kind, -1)
    key "K_RIGHT" action Function(a11y_popup_adjust, kind, 1)
    key "K_RETURN" action Function(a11y_popup_activate, kind)
    key "K_KP_ENTER" action Function(a11y_popup_activate, kind)
    key "K_SPACE" action Function(a11y_popup_activate, kind)
    key "dismiss" action Function(a11y_popup_activate, kind)
    key "K_ESCAPE" action Function(a11y_popup_close)
    key "game_menu" action Function(a11y_popup_close)
    key "K_q" action Function(a11y_popup_close)
    key "K_F1" action Function(a11y_popup_close)

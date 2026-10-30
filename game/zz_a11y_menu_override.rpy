# Text-only accessibility menu replacement for Brilliant Shadows.

init -95 python:
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
    if not hasattr(store, "a11y_yesno_pending_default"):
        store.a11y_yesno_pending_default = False
    if not hasattr(store, "a11y_quit_prompt_spoken_hotkey"):
        store.a11y_quit_prompt_spoken_hotkey = False

    def a11y_nvda_active():
        try:
            return bool(hasattr(store, "_a11y_state") and store._a11y_state.provider and store._a11y_state.provider.available)
        except Exception:
            return False

    def a11y_open_quit_prompt(from_hotkey=False):
        # Route all quit entry points through one prompt to keep behavior stable
        # between NVDA and SAPI.
        try:
            store.a11y_suppress_line_once = True
            store.a11y_suppress_line_count = 20
            if not a11y_nvda_active():
                # Hard-stop current self-voice utterance before speaking prompt.
                renpy.display.tts.tts("")
                if from_hotkey:
                    renpy.display.tts.tts("Do you want to quit?")
                    store.a11y_quit_prompt_spoken_hotkey = True
                else:
                    store.a11y_quit_prompt_spoken_hotkey = False
        except Exception:
            pass
        try:
            renpy.show_screen(
                "yesno_prompt",
                message="Do you want to quit?",
                yes_action=Quit(confirm=False),
                no_action=Hide("yesno_prompt"),
            )
        except Exception:
            # Fallback to engine confirm if screen call fails.
            renpy.run(Quit(confirm=True))

    def a11y_speak_label(label):
        try:
            if hasattr(store, "_a11y_state"):
                provider_ok = False
                try:
                    provider_ok = bool(store._a11y_state.provider and store._a11y_state.provider.available)
                except Exception:
                    provider_ok = False

                if provider_ok:
                    store._a11y_state.speak(label, force=True)
                else:
                    renpy.display.tts.tts(label)
            else:
                renpy.display.tts.tts(label)
        except Exception:
            try:
                renpy.notify(label)
            except Exception:
                pass

    def a11y_move(var_name, labels, delta):
        try:
            store.a11y_yesno_pending_default = False
        except Exception:
            pass
        size = len(labels)
        idx = getattr(store, var_name, 0)
        idx = (idx + delta) % size
        setattr(store, var_name, idx)
        a11y_speak_label(labels[idx])

    def a11y_set(var_name, idx, label):
        try:
            store.a11y_yesno_pending_default = False
        except Exception:
            pass
        setattr(store, var_name, idx)
        a11y_speak_label(label)

    def a11y_yesno_announce_default():
        try:
            if store.a11y_yesno_pending_default:
                store.a11y_yesno_pending_default = False
                a11y_speak_label("Yes")
        except Exception:
            pass

    def a11y_quit_intro(prompt_text):
        # Prompt once on show, then arrow movement speaks only Yes/No.
        try:
            if a11y_nvda_active():
                a11y_speak_label("{0} Yes.".format(prompt_text))
            else:
                store.a11y_yesno_pending_default = True
                if store.a11y_quit_prompt_spoken_hotkey:
                    store.a11y_quit_prompt_spoken_hotkey = False
                else:
                    renpy.display.tts.tts(prompt_text)
        except Exception:
            a11y_speak_label("Yes")

    def a11y_pause_intro():
        try:
            if a11y_nvda_active():
                a11y_speak_label("Resume")
            else:
                renpy.display.tts.tts("Pause menu. Resume.")
        except Exception:
            a11y_speak_label("Resume")

    # --- Preferences screen with slider support ---
    # Items 0-7 are toggle/action buttons. Items 8-11 are sliders adjusted with
    # Left/Right. Item 12 is Back.
    _A11Y_PREF_LABELS = (
        "Fullscreen", "Windowed",
        "Skip all", "Skip seen",
        "After choices stop", "After choices skip",
        "Transitions all", "Transitions none",
        "Text speed", "Music volume", "Sound volume", "Voice volume",
        "Back",
    )
    _A11Y_PREF_SLIDERS = frozenset((8, 9, 10, 11))

    def _a11y_pref_value(idx):
        try:
            if idx == 8:
                cps = getattr(preferences, "text_cps", 0)
                return "Instant" if cps == 0 else "{0} characters per second".format(int(cps))
            if idx == 9:
                return "{0} percent".format(int(round(getattr(preferences, "music_volume", 1.0) * 100)))
            if idx == 10:
                return "{0} percent".format(int(round(getattr(preferences, "sound_volume", 1.0) * 100)))
            if idx == 11:
                return "{0} percent".format(int(round(getattr(preferences, "voice_volume", 1.0) * 100)))
        except Exception:
            pass
        return None

    def a11y_pref_announce(idx):
        try:
            label = _A11Y_PREF_LABELS[idx]
            val = _a11y_pref_value(idx)
            a11y_speak_label("{0}: {1}".format(label, val) if val else label)
        except Exception:
            pass

    def a11y_pref_nav(delta):
        idx = getattr(store, "a11y_pref_index", 0)
        idx = (idx + delta) % len(_A11Y_PREF_LABELS)
        store.a11y_pref_index = idx
        a11y_pref_announce(idx)

    def a11y_pref_adjust(delta):
        idx = getattr(store, "a11y_pref_index", 0)
        if idx not in _A11Y_PREF_SLIDERS:
            a11y_pref_nav(delta)
            return
        try:
            if idx == 8:
                cps = int(getattr(preferences, "text_cps", 0))
                if delta > 0:
                    cps = cps + 10 if cps > 0 else 10
                    cps = min(200, cps)
                else:
                    cps = max(0, cps - 10)
                preferences.text_cps = cps
            elif idx == 9:
                vol = round(max(0.0, min(1.0, getattr(preferences, "music_volume", 1.0) + delta * 0.1)), 1)
                preferences.music_volume = vol
                try:
                    renpy.music.set_volume(vol, channel="music")
                except Exception:
                    try:
                        renpy.music.set_volume(vol, "music")
                    except Exception:
                        pass
            elif idx == 10:
                vol = round(max(0.0, min(1.0, getattr(preferences, "sound_volume", 1.0) + delta * 0.1)), 1)
                preferences.sound_volume = vol
            elif idx == 11:
                vol = round(max(0.0, min(1.0, getattr(preferences, "voice_volume", 1.0) + delta * 0.1)), 1)
                preferences.voice_volume = vol
        except Exception:
            pass
        a11y_pref_announce(idx)

    def a11y_pref_enter():
        idx = getattr(store, "a11y_pref_index", 0)
        if idx == 0:
            store._a11y_run(Preference("display", "fullscreen"))
        elif idx == 1:
            store._a11y_run(Preference("display", "window"))
        elif idx == 2:
            store._a11y_run(Preference("skip", "all"))
        elif idx == 3:
            store._a11y_run(Preference("skip", "seen"))
        elif idx == 4:
            store._a11y_run(Preference("after choices", "stop"))
        elif idx == 5:
            store._a11y_run(Preference("after choices", "skip"))
        elif idx == 6:
            store._a11y_run(Preference("transitions", "all"))
        elif idx == 7:
            store._a11y_run(Preference("transitions", "none"))
        elif idx in _A11Y_PREF_SLIDERS:
            a11y_pref_announce(idx)
        elif idx == 12:
            store._a11y_run(Return())

init -94 python:
    # Disable Ren'Py's menu narrator layer to avoid full-screen/title chatter.
    config.narrator_menu = False

init 100 python:
    # screens.rpy sets this later at init -2; force it back off for this mod.
    config.narrator_menu = False

init -93 python:
    pass  # main_menu screen redirect is handled by "screen main_menu: use a11y_main_menu"

screen a11y_main_menu:
    tag menu
    modal True

    add Solid("#111")

    frame:
        xalign 0.5
        yalign 0.5
        xpadding 30
        ypadding 30
        has vbox
        spacing 14

        textbutton ("Start" if a11y_main_index != 0 else "> Start"):
            action Start()
            hovered Function(a11y_set, "a11y_main_index", 0, "Start")
        textbutton ("Load" if a11y_main_index != 1 else "> Load"):
            action ShowMenu("load")
            hovered Function(a11y_set, "a11y_main_index", 1, "Load")
        textbutton ("Preferences" if a11y_main_index != 2 else "> Preferences"):
            action ShowMenu("preferences")
            hovered Function(a11y_set, "a11y_main_index", 2, "Preferences")
        textbutton ("Information" if a11y_main_index != 3 else "> Information"):
            action OpenURL("http://ithaqualabs.com/home/?p=75")
            hovered Function(a11y_set, "a11y_main_index", 3, "Information")
        textbutton ("Quit" if a11y_main_index != 4 else "> Quit"):
            action Function(a11y_open_quit_prompt)
            hovered Function(a11y_set, "a11y_main_index", 4, "Quit")

    on "show" action [SetVariable("a11y_main_index", 0), Function(a11y_speak_label, "Start")]
    key "K_UP" action Function(a11y_move, "a11y_main_index", ("Start", "Load", "Preferences", "Information", "Quit"), -1)
    key "K_DOWN" action Function(a11y_move, "a11y_main_index", ("Start", "Load", "Preferences", "Information", "Quit"), 1)
    key "K_LEFT" action Function(a11y_move, "a11y_main_index", ("Start", "Load", "Preferences", "Information", "Quit"), -1)
    key "K_RIGHT" action Function(a11y_move, "a11y_main_index", ("Start", "Load", "Preferences", "Information", "Quit"), 1)
    key "K_RETURN" action If(a11y_main_index == 0, Start(), If(a11y_main_index == 1, ShowMenu("load"), If(a11y_main_index == 2, ShowMenu("preferences"), If(a11y_main_index == 3, OpenURL("http://ithaqualabs.com/home/?p=75"), Function(a11y_open_quit_prompt)))))
    key "K_KP_ENTER" action If(a11y_main_index == 0, Start(), If(a11y_main_index == 1, ShowMenu("load"), If(a11y_main_index == 2, ShowMenu("preferences"), If(a11y_main_index == 3, OpenURL("http://ithaqualabs.com/home/?p=75"), Function(a11y_open_quit_prompt)))))
    key "dismiss" action If(a11y_main_index == 0, Start(), If(a11y_main_index == 1, ShowMenu("load"), If(a11y_main_index == 2, ShowMenu("preferences"), If(a11y_main_index == 3, OpenURL("http://ithaqualabs.com/home/?p=75"), Function(a11y_open_quit_prompt)))))
    key "button_select" action If(a11y_main_index == 0, Start(), If(a11y_main_index == 1, ShowMenu("load"), If(a11y_main_index == 2, ShowMenu("preferences"), If(a11y_main_index == 3, OpenURL("http://ithaqualabs.com/home/?p=75"), Function(a11y_open_quit_prompt)))))

screen main_menu:
    use a11y_main_menu


screen esc_menu:
    tag menu
    modal True
    default a11y_esc_announced = False

    add Solid("#111c")

    frame:
        xalign 0.5
        yalign 0.5
        xpadding 30
        ypadding 30
        has vbox
        spacing 12

        textbutton ("Resume" if a11y_esc_index != 0 else "> Resume"):
            action Return()
        textbutton ("Save" if a11y_esc_index != 1 else "> Save"):
            action ShowMenu("save")
        textbutton ("Load" if a11y_esc_index != 2 else "> Load"):
            action ShowMenu("load")
        textbutton ("Preferences" if a11y_esc_index != 3 else "> Preferences"):
            action ShowMenu("preferences")
        textbutton ("Main Menu" if a11y_esc_index != 4 else "> Main Menu"):
            action MainMenu()
        textbutton ("Quit" if a11y_esc_index != 5 else "> Quit"):
            action Function(a11y_open_quit_prompt)

    on "show" action SetVariable("a11y_esc_index", 0)
    if not a11y_esc_announced:
        timer 0.10 action [SetScreenVariable("a11y_esc_announced", True), Function(a11y_pause_intro)]
    key "game_menu" action Return()
    key "K_UP" action Function(a11y_move, "a11y_esc_index", ("Resume", "Save", "Load", "Preferences", "Main Menu", "Quit"), -1)
    key "K_DOWN" action Function(a11y_move, "a11y_esc_index", ("Resume", "Save", "Load", "Preferences", "Main Menu", "Quit"), 1)
    key "K_LEFT" action Function(a11y_move, "a11y_esc_index", ("Resume", "Save", "Load", "Preferences", "Main Menu", "Quit"), -1)
    key "K_RIGHT" action Function(a11y_move, "a11y_esc_index", ("Resume", "Save", "Load", "Preferences", "Main Menu", "Quit"), 1)
    key "K_RETURN" action If(a11y_esc_index == 0, Return(), If(a11y_esc_index == 1, ShowMenu("save"), If(a11y_esc_index == 2, ShowMenu("load"), If(a11y_esc_index == 3, ShowMenu("preferences"), If(a11y_esc_index == 4, MainMenu(), Function(a11y_open_quit_prompt))))))
    key "K_KP_ENTER" action If(a11y_esc_index == 0, Return(), If(a11y_esc_index == 1, ShowMenu("save"), If(a11y_esc_index == 2, ShowMenu("load"), If(a11y_esc_index == 3, ShowMenu("preferences"), If(a11y_esc_index == 4, MainMenu(), Function(a11y_open_quit_prompt))))))


init python:
    config.game_menu_action = [ FileTakeScreenshot(), ShowMenu("esc_menu", transition=dissolve) ]


screen save:
    tag menu
    modal True

    add Solid("#101218")

    frame:
        xalign 0.5
        yalign 0.5
        xpadding 30
        ypadding 30
        has vbox
        spacing 12

        textbutton ("Save Slot 1" if a11y_save_index != 0 else "> Save Slot 1"):
            action FileSave(1)
            hovered Function(a11y_set, "a11y_save_index", 0, "Save slot 1")
        textbutton ("Save Slot 2" if a11y_save_index != 1 else "> Save Slot 2"):
            action FileSave(2)
            hovered Function(a11y_set, "a11y_save_index", 1, "Save slot 2")
        textbutton ("Previous Page" if a11y_save_index != 2 else "> Previous Page"):
            action FilePagePrevious()
            hovered Function(a11y_set, "a11y_save_index", 2, "Previous page")
        textbutton ("Next Page" if a11y_save_index != 3 else "> Next Page"):
            action FilePageNext()
            hovered Function(a11y_set, "a11y_save_index", 3, "Next page")
        textbutton ("Back" if a11y_save_index != 4 else "> Back"):
            action Return()
            hovered Function(a11y_set, "a11y_save_index", 4, "Back")

    on "show" action [SetVariable("a11y_save_index", 0), Function(a11y_speak_label, "Save slot 1")]
    key "K_UP" action Function(a11y_move, "a11y_save_index", ("Save slot 1", "Save slot 2", "Previous page", "Next page", "Back"), -1)
    key "K_DOWN" action Function(a11y_move, "a11y_save_index", ("Save slot 1", "Save slot 2", "Previous page", "Next page", "Back"), 1)
    key "K_LEFT" action Function(a11y_move, "a11y_save_index", ("Save slot 1", "Save slot 2", "Previous page", "Next page", "Back"), -1)
    key "K_RIGHT" action Function(a11y_move, "a11y_save_index", ("Save slot 1", "Save slot 2", "Previous page", "Next page", "Back"), 1)
    key "K_RETURN" action If(a11y_save_index == 0, FileSave(1), If(a11y_save_index == 1, FileSave(2), If(a11y_save_index == 2, FilePagePrevious(), If(a11y_save_index == 3, FilePageNext(), Return()))))
    key "K_KP_ENTER" action If(a11y_save_index == 0, FileSave(1), If(a11y_save_index == 1, FileSave(2), If(a11y_save_index == 2, FilePagePrevious(), If(a11y_save_index == 3, FilePageNext(), Return()))))
    key "dismiss" action If(a11y_save_index == 0, FileSave(1), If(a11y_save_index == 1, FileSave(2), If(a11y_save_index == 2, FilePagePrevious(), If(a11y_save_index == 3, FilePageNext(), Return()))))
    key "button_select" action If(a11y_save_index == 0, FileSave(1), If(a11y_save_index == 1, FileSave(2), If(a11y_save_index == 2, FilePagePrevious(), If(a11y_save_index == 3, FilePageNext(), Return()))))
    key "K_DELETE" action Function(a11y_save_delete)


screen load:
    tag menu
    modal True

    add Solid("#101218")

    frame:
        xalign 0.5
        yalign 0.5
        xpadding 30
        ypadding 30
        has vbox
        spacing 12

        textbutton ("Load Slot 1" if a11y_load_index != 0 else "> Load Slot 1"):
            action FileLoad(1)
            hovered Function(a11y_set, "a11y_load_index", 0, "Load slot 1")
        textbutton ("Load Slot 2" if a11y_load_index != 1 else "> Load Slot 2"):
            action FileLoad(2)
            hovered Function(a11y_set, "a11y_load_index", 1, "Load slot 2")
        textbutton ("Previous Page" if a11y_load_index != 2 else "> Previous Page"):
            action FilePagePrevious()
            hovered Function(a11y_set, "a11y_load_index", 2, "Previous page")
        textbutton ("Next Page" if a11y_load_index != 3 else "> Next Page"):
            action FilePageNext()
            hovered Function(a11y_set, "a11y_load_index", 3, "Next page")
        textbutton ("Back" if a11y_load_index != 4 else "> Back"):
            action Return()
            hovered Function(a11y_set, "a11y_load_index", 4, "Back")

    on "show" action [SetVariable("a11y_load_index", 0), Function(a11y_speak_label, "Load slot 1")]
    key "K_UP" action Function(a11y_move, "a11y_load_index", ("Load slot 1", "Load slot 2", "Previous page", "Next page", "Back"), -1)
    key "K_DOWN" action Function(a11y_move, "a11y_load_index", ("Load slot 1", "Load slot 2", "Previous page", "Next page", "Back"), 1)
    key "K_LEFT" action Function(a11y_move, "a11y_load_index", ("Load slot 1", "Load slot 2", "Previous page", "Next page", "Back"), -1)
    key "K_RIGHT" action Function(a11y_move, "a11y_load_index", ("Load slot 1", "Load slot 2", "Previous page", "Next page", "Back"), 1)
    key "K_RETURN" action If(a11y_load_index == 0, FileLoad(1), If(a11y_load_index == 1, FileLoad(2), If(a11y_load_index == 2, FilePagePrevious(), If(a11y_load_index == 3, FilePageNext(), Return()))))
    key "K_KP_ENTER" action If(a11y_load_index == 0, FileLoad(1), If(a11y_load_index == 1, FileLoad(2), If(a11y_load_index == 2, FilePagePrevious(), If(a11y_load_index == 3, FilePageNext(), Return()))))
    key "dismiss" action If(a11y_load_index == 0, FileLoad(1), If(a11y_load_index == 1, FileLoad(2), If(a11y_load_index == 2, FilePagePrevious(), If(a11y_load_index == 3, FilePageNext(), Return()))))
    key "button_select" action If(a11y_load_index == 0, FileLoad(1), If(a11y_load_index == 1, FileLoad(2), If(a11y_load_index == 2, FilePagePrevious(), If(a11y_load_index == 3, FilePageNext(), Return()))))


screen preferences:
    tag menu
    modal True

    add Solid("#101218")

    frame:
        xalign 0.5
        yalign 0.5
        xpadding 30
        ypadding 30
        has vbox
        spacing 12

        textbutton ("Fullscreen" if a11y_pref_index != 0 else "> Fullscreen"):
            action Preference("display", "fullscreen")
            hovered Function(a11y_set, "a11y_pref_index", 0, "Fullscreen")
        textbutton ("Windowed" if a11y_pref_index != 1 else "> Windowed"):
            action Preference("display", "window")
            hovered Function(a11y_set, "a11y_pref_index", 1, "Windowed")
        textbutton ("Skip All" if a11y_pref_index != 2 else "> Skip All"):
            action Preference("skip", "all")
            hovered Function(a11y_set, "a11y_pref_index", 2, "Skip all")
        textbutton ("Skip Seen" if a11y_pref_index != 3 else "> Skip Seen"):
            action Preference("skip", "seen")
            hovered Function(a11y_set, "a11y_pref_index", 3, "Skip seen")
        textbutton ("After Choices: Stop" if a11y_pref_index != 4 else "> After Choices: Stop"):
            action Preference("after choices", "stop")
            hovered Function(a11y_set, "a11y_pref_index", 4, "After choices stop")
        textbutton ("After Choices: Skip" if a11y_pref_index != 5 else "> After Choices: Skip"):
            action Preference("after choices", "skip")
            hovered Function(a11y_set, "a11y_pref_index", 5, "After choices skip")
        textbutton ("Transitions: All" if a11y_pref_index != 6 else "> Transitions: All"):
            action Preference("transitions", "all")
            hovered Function(a11y_set, "a11y_pref_index", 6, "Transitions all")
        textbutton ("Transitions: None" if a11y_pref_index != 7 else "> Transitions: None"):
            action Preference("transitions", "none")
            hovered Function(a11y_set, "a11y_pref_index", 7, "Transitions none")
        textbutton ("Text Speed" if a11y_pref_index != 8 else "> Text Speed"):
            action Function(a11y_pref_announce, 8)
            hovered Function(a11y_set, "a11y_pref_index", 8, "Text speed")
        textbutton ("Music Volume" if a11y_pref_index != 9 else "> Music Volume"):
            action Function(a11y_pref_announce, 9)
            hovered Function(a11y_set, "a11y_pref_index", 9, "Music volume")
        textbutton ("Sound Volume" if a11y_pref_index != 10 else "> Sound Volume"):
            action Function(a11y_pref_announce, 10)
            hovered Function(a11y_set, "a11y_pref_index", 10, "Sound volume")
        textbutton ("Voice Volume" if a11y_pref_index != 11 else "> Voice Volume"):
            action Function(a11y_pref_announce, 11)
            hovered Function(a11y_set, "a11y_pref_index", 11, "Voice volume")
        textbutton ("Back" if a11y_pref_index != 12 else "> Back"):
            action Return()
            hovered Function(a11y_set, "a11y_pref_index", 12, "Back")

    on "show" action [SetVariable("a11y_pref_index", 0), Function(a11y_speak_label, "Fullscreen")]
    key "K_UP"    action Function(a11y_pref_nav, -1)
    key "K_DOWN"  action Function(a11y_pref_nav, 1)
    key "K_LEFT"  action Function(a11y_pref_adjust, -1)
    key "K_RIGHT" action Function(a11y_pref_adjust, 1)
    key "K_RETURN"      action Function(a11y_pref_enter)
    key "K_KP_ENTER"    action Function(a11y_pref_enter)
    key "dismiss"       action Function(a11y_pref_enter)
    key "button_select" action Function(a11y_pref_enter)


screen yesno_prompt:
    modal True

    add Solid("#111c")

    frame:
        xalign 0.5
        yalign 0.5
        xpadding 30
        ypadding 30
        has vbox
        spacing 14
        if a11y_nvda_active():
            text _(message) xalign 0.5
        textbutton ("Yes" if a11y_yesno_index != 0 else "> Yes"):
            action yes_action
        textbutton ("No" if a11y_yesno_index != 1 else "> No"):
            action no_action
    # Ignore repeated Alt+F4 while this prompt is open.
    key "alt_K_F4" action NullAction()

    on "show" action [SetVariable("a11y_yesno_index", 0), Function(a11y_quit_intro, _(message))]
    if not a11y_nvda_active():
        timer 1.20 action Function(a11y_yesno_announce_default)
    key "game_menu" action no_action
    key "K_ESCAPE" action [Function(a11y_speak_label, "No"), no_action]
    key "K_UP" action Function(a11y_move, "a11y_yesno_index", ("Yes", "No"), -1)
    key "K_DOWN" action Function(a11y_move, "a11y_yesno_index", ("Yes", "No"), 1)
    key "K_LEFT" action Function(a11y_move, "a11y_yesno_index", ("Yes", "No"), -1)
    key "K_RIGHT" action Function(a11y_move, "a11y_yesno_index", ("Yes", "No"), 1)
    key "K_RETURN" action If(a11y_yesno_index == 0, yes_action, no_action)
    key "K_KP_ENTER" action If(a11y_yesno_index == 0, yes_action, no_action)
    key "dismiss" action If(a11y_yesno_index == 0, yes_action, no_action)
    key "button_select" action If(a11y_yesno_index == 0, yes_action, no_action)

# This file is in the public domain. Feel free to modify it as a basis
# for your own screens.

##############################################################################
# Say
#
# Screen that's used to display adv-mode dialogue.
# http://www.renpy.org/doc/html/screen_special.html#say
screen say:

    # Defaults for side_image and two_window
    default side_image = None
    default two_window = False
    default a11y_last_spoken = ""

    # Decide if we want to use the one-window or two-window variant.
    if not two_window:

        # The one window variant.
        window:
            id "window"

            has vbox:
                style "say_vbox"

            if who:
                text who id "who"

            text what id "what"

    else:

        # The two window variant.
        vbox:
            style "say_two_window_vbox"

            if who:
                window:
                    style "say_who_window"

                    text who:
                        id "who"

            window:
                id "window"

                has vbox:
                    style "say_vbox"

                text what id "what"

    # If there's a side image, display it above the text.
    if side_image:
        add side_image
    else:
        add SideImage() xalign 0.0 yalign 1.0

    # Use the quick menu.
    use quick_menu

    # Auto-read whenever current line changes (dialogue or narration).
    if what and what != a11y_last_spoken:
        # Small delay lets voice channel start first, so voiced lines are skipped.
        timer 0.12 action [SetScreenVariable("a11y_last_spoken", what), Function(a11y_read_line, who, what)]

    # Hard fallback so dialogue always advances from keyboard.
    key "dismiss" action Return()
    key "K_RETURN" action Return()
    key "K_KP_ENTER" action Return()
    key "alt_K_F4" action Function(a11y_open_quit_prompt, True)
    key "quit" action Function(a11y_open_quit_prompt, True)
    key "K_UP" action Function(a11y_repeat_last)


init -99 python:
    def a11y_focus(label):
        try:
            text = unicode(label) if "unicode" in globals() else str(label)
            if hasattr(store, "_a11y_state"):
                store._a11y_state.speak(text)
            else:
                renpy.notify(text)
        except Exception:
            pass


##############################################################################
# Choice
#
# Screen that's used to display in-game menus.
# http://www.renpy.org/doc/html/screen_special.html#choice

screen choice:
    $ a11y_choice_actions = [action for caption, action, chosen in items if action]
    on "show" action [SetVariable("a11y_choice_index", 0), Function(a11y_choice_on_show, items)]
    key "K_UP" action Function(a11y_choice_move, items, -1)
    key "K_DOWN" action Function(a11y_choice_move, items, 1)
    key "K_LEFT" action Function(a11y_choice_move, items, -1)
    key "K_RIGHT" action Function(a11y_choice_move, items, 1)
    key "K_RETURN" action If(len(a11y_choice_actions) > 0, a11y_choice_actions[min(a11y_choice_index, len(a11y_choice_actions) - 1)], NullAction())
    key "K_KP_ENTER" action If(len(a11y_choice_actions) > 0, a11y_choice_actions[min(a11y_choice_index, len(a11y_choice_actions) - 1)], NullAction())
    key "dismiss" action If(len(a11y_choice_actions) > 0, a11y_choice_actions[min(a11y_choice_index, len(a11y_choice_actions) - 1)], NullAction())
    key "button_select" action If(len(a11y_choice_actions) > 0, a11y_choice_actions[min(a11y_choice_index, len(a11y_choice_actions) - 1)], NullAction())

    window:
        style "menu_window"


        xalign 0.5
        yalign 0.5

        vbox:
            style "menu"
            spacing 2
            $ action_idx = 0

            for caption, action, chosen in items:

                if action:

                    button:
                        action action
                        hovered Function(a11y_focus, caption)
                        style "menu_choice_button"

                        text caption style "menu_choice"

                    $ action_idx += 1

                else:
                    text caption style "menu_caption"
init python:
    style.menu_choice.color = "#fff"
    style.menu_choice.size = 40
    style.menu_choice_button.yminimum = 120

    style.menu_choice.hover_color = "#fff"
    style.menu_choice_button.background = Frame("ui/choice2.png",28,9)
    style.menu_choice_button.hover_background = Frame("ui/choice1.png",28,9)

init -2:
    $ config.narrator_menu = True

    style menu_window is default

    style menu_choice is button_text:
        clear


    style menu_choice_button is button:
        xminimum int(config.screen_width * 0.75)
        xmaximum int(config.screen_width * 0.75)


##############################################################################
# Input
#
# Screen that's used to display renpy.input()
# http://www.renpy.org/doc/html/screen_special.html#input

screen input:

    window style "input_window":
        has vbox

        text prompt style "input_prompt"
        input id "input" style "input_text"

    use quick_menu

##############################################################################
# Nvl
#
# Screen used for nvl-mode dialogue and menus.
# http://www.renpy.org/doc/html/screen_special.html#nvl

screen nvl:

    window:
        style "nvl_window"

        has vbox:
            style "nvl_vbox"

        # Display dialogue.
        for who, what, who_id, what_id, window_id in dialogue:
            window:
                id window_id

                has hbox:
                    spacing 10

                if who is not None:
                    text who id who_id

                text what id what_id

        # Display a menu, if given.
        if items:

            vbox:
                id "menu"

                for caption, action, chosen in items:

                    if action:

                        button:
                            style "nvl_menu_choice_button"
                            action action
                            hovered Function(a11y_focus, caption)

                            text caption style "nvl_menu_choice"

                    else:

                        text caption style "nvl_dialogue"

    add SideImage() xalign 0.0 yalign 1.0

    use quick_menu

##############################################################################
# Main Menu
#
# Screen that's used to display the main menu, when Ren'Py first starts
# http://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu:
    tag menu
    default a11y_main_index = 0
    add "dynamicLogo"

    add "dynamicLogo2"
    add "dynamicLogo3"
    add "dynamicLogo4"
    add "dynamicLogo5"
    add "dynamicLogo6"
    
    #imagebutton auto "ui/kickstarter_%s.png" xpos 500 ypos 150 focus_mask None action OpenURL("https://www.kickstarter.com/projects/ithaqualabs/pale-spectrum")
    
    imagemap:
        ground "ui/imageMapBase.png"
        hover "ui/imageMapOverlay.png"
        
        hotspot (959, 0, 407, 131) action [Function(a11y_focus, "Start"), Start()] hovered Function(a11y_focus, "Start")
        hotspot (959, 107, 407, 126) action [Function(a11y_focus, "Load"), ShowMenu('load')] hovered Function(a11y_focus, "Load")
        hotspot (959, 233, 407, 127) action [Function(a11y_focus, "Preferences"), ShowMenu('preferences')] hovered Function(a11y_focus, "Preferences")
        hotspot (959, 360, 407, 119) action [Function(a11y_focus, "Information"), OpenURL("http://ithaqualabs.com/home/?p=75")] hovered Function(a11y_focus, "Information")
        hotspot (959, 479, 407, 128) action [Function(a11y_focus, "Quit"), Quit()] hovered Function(a11y_focus, "Quit")#confirm=False)

    timer 0.05 action Function(a11y_focus, "Start")
    key "K_UP" action [SetScreenVariable("a11y_main_index", (a11y_main_index - 1) % 5), Function(a11y_focus, ("Start", "Load", "Preferences", "Information", "Quit")[((a11y_main_index - 1) % 5)])]
    key "K_DOWN" action [SetScreenVariable("a11y_main_index", (a11y_main_index + 1) % 5), Function(a11y_focus, ("Start", "Load", "Preferences", "Information", "Quit")[((a11y_main_index + 1) % 5)])]
    key "K_LEFT" action [SetScreenVariable("a11y_main_index", (a11y_main_index - 1) % 5), Function(a11y_focus, ("Start", "Load", "Preferences", "Information", "Quit")[((a11y_main_index - 1) % 5)])]
    key "K_RIGHT" action [SetScreenVariable("a11y_main_index", (a11y_main_index + 1) % 5), Function(a11y_focus, ("Start", "Load", "Preferences", "Information", "Quit")[((a11y_main_index + 1) % 5)])]
    key "K_RETURN" action If(a11y_main_index == 0, [Function(a11y_focus, "Start"), Start()], If(a11y_main_index == 1, [Function(a11y_focus, "Load"), ShowMenu("load")], If(a11y_main_index == 2, [Function(a11y_focus, "Preferences"), ShowMenu("preferences")], If(a11y_main_index == 3, [Function(a11y_focus, "Information"), OpenURL("http://ithaqualabs.com/home/?p=75")], [Function(a11y_focus, "Quit"), Quit()]))))
    key "K_KP_ENTER" action If(a11y_main_index == 0, [Function(a11y_focus, "Start"), Start()], If(a11y_main_index == 1, [Function(a11y_focus, "Load"), ShowMenu("load")], If(a11y_main_index == 2, [Function(a11y_focus, "Preferences"), ShowMenu("preferences")], If(a11y_main_index == 3, [Function(a11y_focus, "Information"), OpenURL("http://ithaqualabs.com/home/?p=75")], [Function(a11y_focus, "Quit"), Quit()]))))




##############################################################################
# Navigation
#
# Screen that's included in other screens to display the game menu
# navigation and background.
# http://www.renpy.org/doc/html/screen_special.html#navigation
screen navigation:
    tag menu
    # The background of the game menu.
    window:
        style "gm_root"
    
screen esc_menu:
    tag menu
    modal True
    default a11y_esc_index = 0
    frame xalign 0.5 yalign 0.2 background None:
        imagemap:
            ground "ui/popup_2.png"
            idle "ui/popup_1.png"
            
            hotspot (561, 175, 209, 102) action [Function(a11y_focus, "Resume"), Return()] hovered Function(a11y_focus, "Resume")
            hotspot (782, 233, 130, 78) action [Function(a11y_focus, "Save"), ShowMenu("save")] hovered Function(a11y_focus, "Save")
            hotspot (431, 343, 156, 99) action [Function(a11y_focus, "Load"), ShowMenu("load")] hovered Function(a11y_focus, "Load")
            hotspot (782, 335, 384, 79) action [Function(a11y_focus, "Preferences"), ShowMenu("preferences")] hovered Function(a11y_focus, "Preferences")
            hotspot (391, 506, 243, 112) action [Function(a11y_focus, "Main Menu"), MainMenu()] hovered Function(a11y_focus, "Main Menu")
            hotspot (782, 478, 142, 70) action [Function(a11y_focus, "Quit"), Quit(confirm=True)] hovered Function(a11y_focus, "Quit") #Use action "action Quit(confirm=False)" if you don't want them to confirm to quit. Else use "action ShowMenu("quit")"
        
    
    key "game_menu" action Hide("esc_menu", dissolve)
    timer 0.05 action Function(a11y_focus, "Resume")
    key "K_UP" action [SetScreenVariable("a11y_esc_index", (a11y_esc_index - 1) % 6), Function(a11y_focus, ("Resume", "Save", "Load", "Preferences", "Main Menu", "Quit")[((a11y_esc_index - 1) % 6)])]
    key "K_DOWN" action [SetScreenVariable("a11y_esc_index", (a11y_esc_index + 1) % 6), Function(a11y_focus, ("Resume", "Save", "Load", "Preferences", "Main Menu", "Quit")[((a11y_esc_index + 1) % 6)])]
    key "K_LEFT" action [SetScreenVariable("a11y_esc_index", (a11y_esc_index - 1) % 6), Function(a11y_focus, ("Resume", "Save", "Load", "Preferences", "Main Menu", "Quit")[((a11y_esc_index - 1) % 6)])]
    key "K_RIGHT" action [SetScreenVariable("a11y_esc_index", (a11y_esc_index + 1) % 6), Function(a11y_focus, ("Resume", "Save", "Load", "Preferences", "Main Menu", "Quit")[((a11y_esc_index + 1) % 6)])]
    key "K_RETURN" action If(a11y_esc_index == 0, [Function(a11y_focus, "Resume"), Return()], If(a11y_esc_index == 1, [Function(a11y_focus, "Save"), ShowMenu("save")], If(a11y_esc_index == 2, [Function(a11y_focus, "Load"), ShowMenu("load")], If(a11y_esc_index == 3, [Function(a11y_focus, "Preferences"), ShowMenu("preferences")], If(a11y_esc_index == 4, [Function(a11y_focus, "Main Menu"), MainMenu()], [Function(a11y_focus, "Quit"), Quit(confirm=True)])))))
    key "K_KP_ENTER" action If(a11y_esc_index == 0, [Function(a11y_focus, "Resume"), Return()], If(a11y_esc_index == 1, [Function(a11y_focus, "Save"), ShowMenu("save")], If(a11y_esc_index == 2, [Function(a11y_focus, "Load"), ShowMenu("load")], If(a11y_esc_index == 3, [Function(a11y_focus, "Preferences"), ShowMenu("preferences")], If(a11y_esc_index == 4, [Function(a11y_focus, "Main Menu"), MainMenu()], [Function(a11y_focus, "Quit"), Quit(confirm=True)])))))
    frame:
        has vbox
        
        

        



init python:
     config.game_menu_action = [ FileTakeScreenshot(), ShowMenu("esc_menu", transition=dissolve) ]

screen one_button_scr:
    pass



init -2:

    # Make all game menu navigation buttons the same size.
    style gm_nav_button:
        size_group "gm_nav"


##############################################################################
# Save, Load
#
# Screens that allow the user to save and load the game.
# http://www.renpy.org/doc/html/screen_special.html#save
# http://www.renpy.org/doc/html/screen_special.html#load

# Since saving and loading are so similar, we combine them into
# a single screen, file_picker. We then use the file_picker screen
# from simple load and save screens.


screen save:
    
    tag menu
    default a11y_save_index = 1

    imagemap:
        ground "ui/saveload1.jpg"
        idle "ui/save1.png"
        hover "ui/save2.png"
        cache False
 
     
        
        hotspot (642,153,51,96) clicked [Function(a11y_focus, "Page 1"), FilePage(1)] hovered Function(a11y_focus, "Page 1")
        hotspot (693,153,57,96) clicked [Function(a11y_focus, "Page 2"), FilePage(2)] hovered Function(a11y_focus, "Page 2")
        hotspot (749,153,51,96) clicked [Function(a11y_focus, "Page 3"), FilePage(3)] hovered Function(a11y_focus, "Page 3")
        hotspot (800,153,60,96) clicked [Function(a11y_focus, "Page 4"), FilePage(4)] hovered Function(a11y_focus, "Page 4")
        hotspot (860,153,56,96) clicked [Function(a11y_focus, "Page 5"), FilePage(5)] hovered Function(a11y_focus, "Page 5")
        hotspot (916,153,56,96) clicked [Function(a11y_focus, "Page 6"), FilePage(6)] hovered Function(a11y_focus, "Page 6")
        hotspot (971,153,56,96) clicked [Function(a11y_focus, "Page 7"), FilePage(7)] hovered Function(a11y_focus, "Page 7")
        hotspot (1027,153,60,96) clicked [Function(a11y_focus, "Page 8"), FilePage(8)] hovered Function(a11y_focus, "Page 8")
        hotspot (1086,153,61,96) clicked [Function(a11y_focus, "Page 9"), FilePage(9)] hovered Function(a11y_focus, "Page 9")
        
        hotspot (340,153,137,96) clicked [Function(a11y_focus, "Auto page"), FilePage("auto")] hovered Function(a11y_focus, "Auto page")
        hotspot (477,153,165,109) action [Function(a11y_focus, "Quick page"), FilePage("quick")] hovered Function(a11y_focus, "Quick page")
        hotspot (1146,153,143,96) action [Function(a11y_focus, "Next page"), FilePageNext()] hovered Function(a11y_focus, "Next page")
        
        hotspot (83,153,258,96) action [Function(a11y_focus, "Previous page"), FilePagePrevious()] hovered Function(a11y_focus, "Previous page")
        

        
        hotspot (152, 267, 523, 294) clicked [Function(a11y_focus, "Save slot 1"), FileSave(1)]:
            use load_save_slot(number=1) 
        hotspot (703, 268, 523, 294) clicked [Function(a11y_focus, "Save slot 2"), FileSave(2)]:
            use load_save_slot(number=2) 

        hotspot (477, 613, 383, 118) action [Function(a11y_focus, "Back"), Return()] hovered Function(a11y_focus, "Back")

    timer 0.05 action Function(a11y_focus, "Save slot 1")
    key "K_UP" action [SetScreenVariable("a11y_save_index", (a11y_save_index - 1) % 5), Function(a11y_focus, ("Previous page", "Save slot 1", "Save slot 2", "Next page", "Back")[((a11y_save_index - 1) % 5)])]
    key "K_DOWN" action [SetScreenVariable("a11y_save_index", (a11y_save_index + 1) % 5), Function(a11y_focus, ("Previous page", "Save slot 1", "Save slot 2", "Next page", "Back")[((a11y_save_index + 1) % 5)])]
    key "K_LEFT" action [SetScreenVariable("a11y_save_index", (a11y_save_index - 1) % 5), Function(a11y_focus, ("Previous page", "Save slot 1", "Save slot 2", "Next page", "Back")[((a11y_save_index - 1) % 5)])]
    key "K_RIGHT" action [SetScreenVariable("a11y_save_index", (a11y_save_index + 1) % 5), Function(a11y_focus, ("Previous page", "Save slot 1", "Save slot 2", "Next page", "Back")[((a11y_save_index + 1) % 5)])]
    key "K_RETURN" action If(a11y_save_index == 0, [Function(a11y_focus, "Previous page"), FilePagePrevious()], If(a11y_save_index == 1, [Function(a11y_focus, "Save slot 1"), FileSave(1)], If(a11y_save_index == 2, [Function(a11y_focus, "Save slot 2"), FileSave(2)], If(a11y_save_index == 3, [Function(a11y_focus, "Next page"), FilePageNext()], [Function(a11y_focus, "Back"), Return()]))))
    key "K_KP_ENTER" action If(a11y_save_index == 0, [Function(a11y_focus, "Previous page"), FilePagePrevious()], If(a11y_save_index == 1, [Function(a11y_focus, "Save slot 1"), FileSave(1)], If(a11y_save_index == 2, [Function(a11y_focus, "Save slot 2"), FileSave(2)], If(a11y_save_index == 3, [Function(a11y_focus, "Next page"), FilePageNext()], [Function(a11y_focus, "Back"), Return()]))))

 
         
screen load:
   
   tag menu
   default a11y_load_index = 1

   imagemap:
        ground "ui/saveload.jpg"
        idle "ui/load1.png"
        hover "ui/load2.png"
        cache False
        hotspot (642,153,51,96) clicked [Function(a11y_focus, "Page 1"), FilePage(1)] hovered Function(a11y_focus, "Page 1")
        hotspot (693,153,57,96) clicked [Function(a11y_focus, "Page 2"), FilePage(2)] hovered Function(a11y_focus, "Page 2")
        hotspot (749,153,51,96) clicked [Function(a11y_focus, "Page 3"), FilePage(3)] hovered Function(a11y_focus, "Page 3")
        hotspot (800,153,60,96) clicked [Function(a11y_focus, "Page 4"), FilePage(4)] hovered Function(a11y_focus, "Page 4")
        hotspot (860,153,56,96) clicked [Function(a11y_focus, "Page 5"), FilePage(5)] hovered Function(a11y_focus, "Page 5")
        hotspot (916,153,56,96) clicked [Function(a11y_focus, "Page 6"), FilePage(6)] hovered Function(a11y_focus, "Page 6")
        hotspot (971,153,56,96) clicked [Function(a11y_focus, "Page 7"), FilePage(7)] hovered Function(a11y_focus, "Page 7")
        hotspot (1027,153,60,96) clicked [Function(a11y_focus, "Page 8"), FilePage(8)] hovered Function(a11y_focus, "Page 8")
        hotspot (1086,153,61,96) clicked [Function(a11y_focus, "Page 9"), FilePage(9)] hovered Function(a11y_focus, "Page 9")
        
        hotspot (340,153,137,96) clicked [Function(a11y_focus, "Auto page"), FilePage("auto")] hovered Function(a11y_focus, "Auto page")
        hotspot (477,153,165,109) action [Function(a11y_focus, "Quick page"), FilePage("quick")] hovered Function(a11y_focus, "Quick page")
        hotspot (1146,153,143,96) action [Function(a11y_focus, "Next page"), FilePageNext()] hovered Function(a11y_focus, "Next page")
        
        hotspot (83,153,258,96) action [Function(a11y_focus, "Previous page"), FilePagePrevious()] hovered Function(a11y_focus, "Previous page")
        

        
        hotspot (152, 267, 523, 294) clicked [Function(a11y_focus, "Load slot 1"), FileLoad(1)]:
            use load_save_slot(number=1) 
        hotspot (703, 268, 523, 294) clicked [Function(a11y_focus, "Load slot 2"), FileLoad(2)]:
            use load_save_slot(number=2) 

        hotspot (477, 613, 383, 118) action [Function(a11y_focus, "Back"), Return()] hovered Function(a11y_focus, "Back")

   timer 0.05 action Function(a11y_focus, "Load slot 1")
   key "K_UP" action [SetScreenVariable("a11y_load_index", (a11y_load_index - 1) % 5), Function(a11y_focus, ("Previous page", "Load slot 1", "Load slot 2", "Next page", "Back")[((a11y_load_index - 1) % 5)])]
   key "K_DOWN" action [SetScreenVariable("a11y_load_index", (a11y_load_index + 1) % 5), Function(a11y_focus, ("Previous page", "Load slot 1", "Load slot 2", "Next page", "Back")[((a11y_load_index + 1) % 5)])]
   key "K_LEFT" action [SetScreenVariable("a11y_load_index", (a11y_load_index - 1) % 5), Function(a11y_focus, ("Previous page", "Load slot 1", "Load slot 2", "Next page", "Back")[((a11y_load_index - 1) % 5)])]
   key "K_RIGHT" action [SetScreenVariable("a11y_load_index", (a11y_load_index + 1) % 5), Function(a11y_focus, ("Previous page", "Load slot 1", "Load slot 2", "Next page", "Back")[((a11y_load_index + 1) % 5)])]
   key "K_RETURN" action If(a11y_load_index == 0, [Function(a11y_focus, "Previous page"), FilePagePrevious()], If(a11y_load_index == 1, [Function(a11y_focus, "Load slot 1"), FileLoad(1)], If(a11y_load_index == 2, [Function(a11y_focus, "Load slot 2"), FileLoad(2)], If(a11y_load_index == 3, [Function(a11y_focus, "Next page"), FilePageNext()], [Function(a11y_focus, "Back"), Return()]))))
   key "K_KP_ENTER" action If(a11y_load_index == 0, [Function(a11y_focus, "Previous page"), FilePagePrevious()], If(a11y_load_index == 1, [Function(a11y_focus, "Load slot 1"), FileLoad(1)], If(a11y_load_index == 2, [Function(a11y_focus, "Load slot 2"), FileLoad(2)], If(a11y_load_index == 3, [Function(a11y_focus, "Next page"), FilePageNext()], [Function(a11y_focus, "Back"), Return()]))))

screen load_save_slot:
    $ file_text = "% 2s. %s\n%s" % (
                        FileSlotName(number, 2),
                        FileTime(number, empty=_("Empty Slot")),
                        FileSaveName(number))


    add FileScreenshot(number) xpos 0 ypos 0
    text file_text xpos 0 ypos 10 size 40 color "#ffffff" outlines [ (2, "#302B54") ] kerning 2 font "Amaranth-Regular.tTF"
    
    key "save_delete" action FileDelete(number)
    
init -2 python:
    
    config.thumbnail_width = 524
    config.thumbnail_height = 293

##############################################################################
# Preferences
#
# Screen that allows the user to change the preferences.
# http://www.renpy.org/doc/html/screen_special.html#prefereces

screen preferences:
    tag menu
    default a11y_pref_index = 0
    imagemap:   
        ground "ui/preferences_2.jpg"
        idle "ui/preferences_3.png"
        hover "ui/preferences_5.png"
        selected_idle "ui/preferences_4.png" 
        selected_hover "ui/preferences_6.png" 
        alpha False
        
        hotspot (178, 261, 154, 48) action [Function(a11y_focus, "Fullscreen"), Preference("display", "fullscreen")] hovered Function(a11y_focus, "Fullscreen")
        hotspot (178, 224, 154, 36) action [Function(a11y_focus, "Windowed"), Preference("display", "window")] hovered Function(a11y_focus, "Windowed")
        hotspot (425, 220, 63, 48) action [Function(a11y_focus, "Skip all"), Preference("skip", "all")] hovered Function(a11y_focus, "Skip all")
        hotspot (425, 265, 85, 41) action [Function(a11y_focus, "Skip seen"), Preference("skip", "seen")] hovered Function(a11y_focus, "Skip seen")
        hotspot (892, 261, 232, 46) action [Function(a11y_focus, "After choices stop"), Preference("after choices", "stop")] hovered Function(a11y_focus, "After choices stop")
        hotspot (893, 220, 237, 42) action [Function(a11y_focus, "After choices skip"), Preference("after choices", "skip")] hovered Function(a11y_focus, "After choices skip")
        hotspot (503, 629, 339, 94) action [Function(a11y_focus, "Back"), Return()] hovered Function(a11y_focus, "Back")
        hotspot (624, 217, 87, 42) action [Function(a11y_focus, "Transitions all"), Preference("transitions", "all")] hovered Function(a11y_focus, "Transitions all")
        hotspot (632, 267, 90, 41) action [Function(a11y_focus, "Transitions none"), Preference("transitions", "none")] hovered Function(a11y_focus, "Transitions none")
                                                
        
        bar pos (547, 399) value Preference("text speed") style "pref_slider"
        bar pos (909, 541) value Preference("sound volume") style "pref_slider"
        bar pos (526, 541) value Preference("voice volume") style "pref_slider"
        bar pos (126, 541) value Preference("music volume") style "pref_slider"

        #bar pos (817, 399) value Preference("auto-forward time") style "pref_slider"

    timer 0.05 action Function(a11y_focus, "Fullscreen")
    key "K_UP" action [SetScreenVariable("a11y_pref_index", (a11y_pref_index - 1) % 9), Function(a11y_focus, ("Fullscreen", "Windowed", "Skip all", "Skip seen", "After choices stop", "After choices skip", "Transitions all", "Transitions none", "Back")[((a11y_pref_index - 1) % 9)])]
    key "K_DOWN" action [SetScreenVariable("a11y_pref_index", (a11y_pref_index + 1) % 9), Function(a11y_focus, ("Fullscreen", "Windowed", "Skip all", "Skip seen", "After choices stop", "After choices skip", "Transitions all", "Transitions none", "Back")[((a11y_pref_index + 1) % 9)])]
    key "K_LEFT" action [SetScreenVariable("a11y_pref_index", (a11y_pref_index - 1) % 9), Function(a11y_focus, ("Fullscreen", "Windowed", "Skip all", "Skip seen", "After choices stop", "After choices skip", "Transitions all", "Transitions none", "Back")[((a11y_pref_index - 1) % 9)])]
    key "K_RIGHT" action [SetScreenVariable("a11y_pref_index", (a11y_pref_index + 1) % 9), Function(a11y_focus, ("Fullscreen", "Windowed", "Skip all", "Skip seen", "After choices stop", "After choices skip", "Transitions all", "Transitions none", "Back")[((a11y_pref_index + 1) % 9)])]
    key "K_RETURN" action If(a11y_pref_index == 0, [Function(a11y_focus, "Fullscreen"), Preference("display", "fullscreen")], If(a11y_pref_index == 1, [Function(a11y_focus, "Windowed"), Preference("display", "window")], If(a11y_pref_index == 2, [Function(a11y_focus, "Skip all"), Preference("skip", "all")], If(a11y_pref_index == 3, [Function(a11y_focus, "Skip seen"), Preference("skip", "seen")], If(a11y_pref_index == 4, [Function(a11y_focus, "After choices stop"), Preference("after choices", "stop")], If(a11y_pref_index == 5, [Function(a11y_focus, "After choices skip"), Preference("after choices", "skip")], If(a11y_pref_index == 6, [Function(a11y_focus, "Transitions all"), Preference("transitions", "all")], If(a11y_pref_index == 7, [Function(a11y_focus, "Transitions none"), Preference("transitions", "none")], [Function(a11y_focus, "Back"), Return()]))))))))
    key "K_KP_ENTER" action If(a11y_pref_index == 0, [Function(a11y_focus, "Fullscreen"), Preference("display", "fullscreen")], If(a11y_pref_index == 1, [Function(a11y_focus, "Windowed"), Preference("display", "window")], If(a11y_pref_index == 2, [Function(a11y_focus, "Skip all"), Preference("skip", "all")], If(a11y_pref_index == 3, [Function(a11y_focus, "Skip seen"), Preference("skip", "seen")], If(a11y_pref_index == 4, [Function(a11y_focus, "After choices stop"), Preference("after choices", "stop")], If(a11y_pref_index == 5, [Function(a11y_focus, "After choices skip"), Preference("after choices", "skip")], If(a11y_pref_index == 6, [Function(a11y_focus, "Transitions all"), Preference("transitions", "all")], If(a11y_pref_index == 7, [Function(a11y_focus, "Transitions none"), Preference("transitions", "none")], [Function(a11y_focus, "Back"), Return()]))))))))

init -2 python:
    style.pref_slider.left_bar = "ui/slider_2.png"
    style.pref_slider.right_bar = "ui/slider_1.png"

    style.pref_slider.xmaximum = 263
    style.pref_slider.ymaximum = 81

    style.pref_slider.thumb = "ui/slider_thumb.png"
    style.pref_slider.thumb_offset = 20
    style.pref_slider.thumb_shadow = None


##############################################################################
# Yes/No Prompt
#
# Screen that asks the user a yes or no question.
# http://www.renpy.org/doc/html/screen_special.html#yesno-prompt

screen yesno_prompt:
    modal True
    default a11y_yesno_focus = 0

    window:
        style "gm_root"
        
    imagemap:
        ground "cg/rose_7.jpg"
        idle "ui/quit_2.png" 
        hover "ui/quit_1.png"
        
        hotspot (475, 326, 179, 135) action [Function(a11y_focus, "Yes"), yes_action] hovered Function(a11y_focus, "Yes")
        hotspot (705, 325, 181, 135) action [Function(a11y_focus, "No"), no_action] hovered Function(a11y_focus, "No")

    timer 0.05 action Function(a11y_focus, "Exit dialog. Use arrows to choose Yes or No, then press Enter.")
        
    frame:
        style_group "yesno"

        #xfill True
        xmargin .05
        ypos .1
        yanchor 0
        ypadding .05


        #has vbox:
            xalign .5
            yalign .5
            spacing 30

        label _(message):
            xalign 0.5



    # Right-click and escape answer "no".
    key "game_menu" action [SetScreenVariable("a11y_yesno_focus", 1), Function(a11y_focus, "No"), no_action]
    key "dismiss" action If(a11y_yesno_focus == 0, [Function(a11y_focus, "Yes"), yes_action], [Function(a11y_focus, "No"), no_action])
    key "button_select" action If(a11y_yesno_focus == 0, [Function(a11y_focus, "Yes"), yes_action], [Function(a11y_focus, "No"), no_action])
    key "K_RETURN" action If(a11y_yesno_focus == 0, [Function(a11y_focus, "Yes"), yes_action], [Function(a11y_focus, "No"), no_action])
    key "K_KP_ENTER" action If(a11y_yesno_focus == 0, [Function(a11y_focus, "Yes"), yes_action], [Function(a11y_focus, "No"), no_action])
    key "focus_left" action [SetScreenVariable("a11y_yesno_focus", 0), Function(a11y_focus, "Yes")]
    key "focus_right" action [SetScreenVariable("a11y_yesno_focus", 1), Function(a11y_focus, "No")]
    key "focus_up" action [SetScreenVariable("a11y_yesno_focus", 0), Function(a11y_focus, "Yes")]
    key "focus_down" action [SetScreenVariable("a11y_yesno_focus", 1), Function(a11y_focus, "No")]
    key "K_LEFT" action [SetScreenVariable("a11y_yesno_focus", 0), Function(a11y_focus, "Yes")]
    key "K_RIGHT" action [SetScreenVariable("a11y_yesno_focus", 1), Function(a11y_focus, "No")]
    key "K_UP" action [SetScreenVariable("a11y_yesno_focus", 0), Function(a11y_focus, "Yes")]
    key "K_DOWN" action [SetScreenVariable("a11y_yesno_focus", 1), Function(a11y_focus, "No")]

init -2:
    style yesno_button:
        size_group "yesno"

    style yesno_label_text:
        text_align 0.5
        layout "subtitle"
        
init python:
    style.yesno_label.color = "#fff"
    style.yesno_label_text.size = 50



##############################################################################
# Quick Menu
#
# A screen that's included by the default say screen, and adds quick access to
# several useful functions.
screen quick_menu:

    # Add an in-game quick menu.
    hbox:
        style_group "quick"

        xalign 1.0
        yalign 1.0

  #      textbutton _("Back") action Rollback()
  #      textbutton _("Save") action ShowMenu('save')
   #     textbutton _("Q.Save") action QuickSave()
   #     textbutton _("Q.Load") action QuickLoad()
    #    textbutton _("Skip") action Skip()
    #    textbutton _("F.Skip") action Skip(fast=True, confirm=True)
     #   textbutton _("Auto") action Preference("auto-forward", "toggle")
     #   textbutton _("Prefs") action ShowMenu('preferences')

init -2:
    style quick_button:
        is default
        background None
        xpadding 5

    style quick_button_text:
        is default
        size 12
        idle_color "#8888"
        hover_color "#ccc"
        selected_idle_color "#cc08"
        selected_hover_color "#cc0"
        insensitive_color "#4448"

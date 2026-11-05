from board_v4 import (draw_console_line_at_row, is_pressed, button_A, button_B, sleep, tft_clear, set_status_bar_enabled, px, tft_init, addr_clear)
import st7789py as st7789

game = {
    "start" : {
        "prompt" : ["You wake up with a pounding headache",
                    "While hiking you slid down a steep",
                    "slope and hit your head on a rock",
                    "Your goal: SURVIVE",
                    "A: Search the area",
                    "B: Head Southeast"],
        "A" :"search-area",
        "B" :"go-southeast"
    },
    "search-area" : {
        "prompt" : ["You find some deep animal tracks",
                    "You don't know what they belong too",
                    "They seem fresh",
                    "You also hear water nearby",
                    "A: Follow tracks",
                    "B: Follow the sound of water"],
        "A" : "follow-tracks",
        "B" : "follow-water"
    },
    "follow-tracks" : {
        "prompt" : ["You come across a grizzly bear",
                    "It is not looking for a pot",
                    "of honey; you die",
                    "The end"],
        "A" : "start",
        "B" : "start"
    },
    "follow-water" : {
        "prompt" : ["You find clean running water",
                    "An old mill is near the water",
                    "It looks like someone lives there",
                    "Do you enter?",
                    "A: Enter",
                    "B: Leave"],
        "A" : "enter",
        "B" : "leave"
    },
    "enter" : {
        "prompt" : ["A nice old lady greets you",
                    "She gives you a warm meal and",
                    "helps you find your way home",
                    "The end"],
        "A" : "start",
        "B" : "start"
    },
    "leave" : {
        "prompt" : ["Night falls and you are cold",
                    "Shivering, you cover yourself with",
                    "foliage and try to get warm",
                    "You slowly close your eyes; you die",
                    "The end"],
        "A" : "start",
        "B" : "start"
    },
    "go-southeast" : {
        "prompt" : ["You make your way southeast",
                    "You find a trail and get on it",
                    "Eventually, you reach the end",
                    "It was the trail you started on",
                    "You are greeted with a beautiful",
                    "view and sigh with relief",
                    "You make your way back home",
                    "The end"],
        "A" : "start",
        "B" : "start"
    }
}


def wait_for_button_release(button):
    while is_pressed(button):
        sleep(100)

def do_button(state, button_str, button):    
    next_state = game[state[button_str]]
    display_prompt(next_state["prompt"])
    wait_for_button_release(button) 
    return next_state

def display_prompt(prompt):
    tft_clear()
    for i in range(len(prompt)):
        draw_console_line_at_row(i, prompt[i], st7789.WHITE)

def main():    
    tft_init(include_status_bar=False)    
    state = game["start"]
    display_prompt(state["prompt"])    
    while True:
        if is_pressed(button_A):
            state = do_button(state, "A", button_A)
        elif is_pressed(button_B):
            state = do_button(state, "B", button_B)        

main()
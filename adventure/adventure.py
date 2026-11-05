from board_v4 import (draw_console_line_at_row, is_pressed, button_A, button_B, sleep, tft_clear, set_status_bar_enabled, px, tft_init, addr_clear)
import st7789py as st7789

game = {
    "start" : {
        "prompt" : ["Welcome to the ADVENTURE GAME!",
                    "You are at home and you hear a knock.",
                    "A: OPEN the door",
                    "B: IGNORE the knock."],
        "A" :"open-door",
        "B" :"ignore-knock"
    },
    "open-door" : {
        "prompt" : ["You open the door and see a SQUIRREL.",
                    "The squirrel has a gleam in its eye.",
                    "A: PET the squirrel.",
                    "B: OFFER the squirrel a nut"],
        "A" : "pet-squirrel",
        "B" : "offer-nut"
    },
    "pet-squirrel" : {
        "prompt" : ["You reach out to the squirrel.",
                    "The squirrel bites your hand.",
                    "You turn into a squirrel, too!",
                    "The end."],
        "A" : "start",
        "B" : "start"
    },
    "offer-nut" : {
        "prompt" : ["You offer the squirrel a nut.",
                    "The squirrel becomes a prince.",
                    "The prince gives you a gold coin.",
                    "The end."],
        "A" : "start",
        "B" : "start"
    },
    "ignore-knock" : {
        "prompt" : ["You ignore the knock.",
                    "The door comes crashing in.",
                    "A bear enters the room and mauls you.",
                    "The end."],
        "A" : "start",
        "B" : "start"
    }
}

# Alternate game: Hut in the woods
hut_game = {
    "hut-start": {
        "prompt": ["You find a lonely HUT in the woods.",
                   "Smoke rises from the chimney.",
                   "A: ENTER the hut.",
                   "B: CIRCLE around the hut."],
        "A": "enter-hut",
        "B": "circle-hut"
    },
    "enter-hut": {
        "prompt": ["Inside is dark and quiet.",
                   "A fire pit sits in the center.",
                   "A: LIGHT the fire.",
                   "B: OPEN the trapdoor."],
        "A": "light-fire",
        "B": "open-trapdoor"
    },
    "circle-hut": {
        "prompt": ["You circle the hut and find tracks.",
                   "A lantern swings by the back door.",
                   "A: FOLLOW the footprints.",
                   "B: KNOCK on the back door."],
        "A": "follow-footprints",
        "B": "knock-backdoor"
    },
    "light-fire": {
        "prompt": ["The fire catches and a kettle appears.",
                   "A: ADD strange herbs.",
                   "B: BOIL plain water."],
        "A": "ending-herbs",
        "B": "ending-water"
    },
    "open-trapdoor": {
        "prompt": ["Cold air rises from below.",
                   "A: DESCEND the ladder.",
                   "B: SEAL the trapdoor shut."],
        "A": "ending-ladder",
        "B": "ending-seal"
    },
    "follow-footprints": {
        "prompt": ["The tracks lead to a moonlit clearing.",
                   "A: CALL out loudly.",
                   "B: HIDE behind a log."],
        "A": "ending-call",
        "B": "ending-hide"
    },
    "knock-backdoor": {
        "prompt": ["An old ranger opens a tiny hatch.",
                   "A: TRADE your coin for a map.",
                   "B: RUN back into the forest."],
        "A": "ending-map",
        "B": "ending-run"
    },
    "ending-herbs": {
        "prompt": ["The brew glows blue.",
                   "You gain night vision.",
                   "You become guardian of the woods.",
                   "The end."],
        "A": "hut-start", "B": "hut-start"
    },
    "ending-water": {
        "prompt": ["The steam clears your mind.",
                   "You sleep peacefully by the fire.",
                   "At dawn, the hut is gone.",
                   "The end."],
        "A": "hut-start", "B": "hut-start"
    },
    "ending-ladder": {
        "prompt": ["Below, you find a chest of silver.",
                   "A fox bows and claims you as chief.",
                   "You rule the hidden burrow.",
                   "The end."],
        "A": "hut-start", "B": "hut-start"
    },
    "ending-seal": {
        "prompt": ["The floor shakes, then goes still.",
                   "A whisper thanks you for sealing it.",
                   "The woods are safe tonight.",
                   "The end."],
        "A": "hut-start", "B": "hut-start"
    },
    "ending-call": {
        "prompt": ["Wolves surround you, then sit calmly.",
                   "You sing with them until sunrise.",
                   "You are accepted by the wild pack.",
                   "The end."],
        "A": "hut-start", "B": "hut-start"
    },
    "ending-hide": {
        "prompt": ["You wait silently.",
                   "Poachers pass without seeing you.",
                   "You save a family of deer.",
                   "The end."],
        "A": "hut-start", "B": "hut-start"
    },
    "ending-map": {
        "prompt": ["The map reveals old forest shrines.",
                   "You become a famous pathfinder.",
                   "The ranger salutes your journey.",
                   "The end."],
        "A": "hut-start", "B": "hut-start"
    },
    "ending-run": {
        "prompt": ["You sprint through fog and roots.",
                   "You emerge at your own doorstep.",
                   "The hut was never found again.",
                   "The end."],
        "A": "hut-start", "B": "hut-start"
    }
}

game.update(hut_game)

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

def choose_start_state():
    display_prompt([
        "Choose your adventure:",
        "A: Original (SQUIRREL)",
        "B: Hut in the woods",
        "Press A or B"
    ])

    while True:
        if is_pressed(button_A):
            wait_for_button_release(button_A)
            return "start"
        elif is_pressed(button_B):
            wait_for_button_release(button_B)
            return "hut-start"

def main():    
    tft_init(include_status_bar=False)
    start_state = choose_start_state()
    state = game[start_state]
    display_prompt(state["prompt"])    
    while True:
        if is_pressed(button_A):
            state = do_button(state, "A", button_A)
        elif is_pressed(button_B):
            state = do_button(state, "B", button_B)        

main()
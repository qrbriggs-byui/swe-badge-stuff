# Color Memory — e-Badge v4 (learning_Python).
# Remember the hidden color of each LED and press its matching direction button.

import random
import utime

from board_v4 import (
    DISPLAY_W,
    NUM_ADDR_LEDS,
    addr_clear,
    addr_set,
    addr_show,
    button_A,
    button_B,
    button_down,
    button_left,
    button_right,
    button_up,
    font,
    is_pressed,
    st7789,
    tft,
    tft_init,
)


# Direction buttons select the matching hidden color.
COLOR_CHOICES = (
    ((255, 0, 0), button_up, "RED = UP"),
    ((0, 255, 0), button_down, "GREEN = DOWN"),
    ((0, 0, 255), button_left, "BLUE = LEFT"),
    ((255, 255, 255), button_right, "WHITE = RIGHT"),
)

FLASH_COUNT = 4
FLASH_MS = 180
FRAME_MS = 20
TIMER_UPDATE_MS = 100
# Divide each RGB channel by this value for this game only. Higher values are dimmer.
GAME_LED_DIM = 16
CURRENT_LED_BLINK_MS = 500

tft_init(include_status_bar=False)
random.seed(utime.ticks_ms())


def button_states():
    """Return the current state of each game button in a fixed order."""
    return (
        is_pressed(button_up),
        is_pressed(button_down),
        is_pressed(button_left),
        is_pressed(button_right),
        is_pressed(button_A),
        is_pressed(button_B),
    )


def wait_for_release():
    while any(button_states()):
        utime.sleep_ms(FRAME_MS)


def draw_centered(text, y, color=st7789.WHITE):
    width = len(text) * getattr(font, "WIDTH", 8)
    x = max(0, (DISPLAY_W - width) // 2)
    tft.text(font, text, x, y, color, st7789.BLACK)


def show_instructions():
    tft.fill(st7789.BLACK)
    draw_centered("COLOR GAUNTLET", 12, st7789.CYAN)
    draw_centered("Remember each LED color", 42)
    draw_centered("UP = RED", 72, st7789.RED)
    draw_centered("DOWN = GREEN", 92, st7789.GREEN)
    draw_centered("LEFT = BLUE", 112, st7789.BLUE)
    draw_centered("RIGHT = WHITE", 132)
    draw_centered("Wrong? Start again.", 162, st7789.YELLOW)
    draw_centered("Press any button", 198, st7789.CYAN)


def draw_play_screen():
    tft.fill(st7789.BLACK)
    draw_centered("COLOR GAUNTLET", 8, st7789.CYAN)
    draw_centered("UP red  DN green", 38)
    draw_centered("LT blue  RT white", 56)
    draw_centered("Time: 0.0 sec", 92, st7789.YELLOW)
    draw_centered("LED 1 / %d" % NUM_ADDR_LEDS, 122)


def draw_timer(elapsed_ms):
    text = "Time: %.1f sec" % (elapsed_ms / 1000.0)
    width = len(text) * getattr(font, "WIDTH", 8)
    x = max(0, (DISPLAY_W - width) // 2)
    tft.fill_rect(0, 88, DISPLAY_W, 18, st7789.BLACK)
    tft.text(font, text, x, 92, st7789.YELLOW, st7789.BLACK)


def light_pattern(colors, current_index, current_visible=True):
    """Draw the pattern, with the current LED optionally shown or hidden."""
    for index in range(NUM_ADDR_LEDS):
        if index == current_index and not current_visible:
            addr_set(index, 0, 0, 0)
        else:
            set_game_led(index, colors[index])
    addr_show()


def set_game_led(index, color):
    """Set one LED at this game's reduced brightness."""
    addr_set(
        index,
        color[0] // GAME_LED_DIM,
        color[1] // GAME_LED_DIM,
        color[2] // GAME_LED_DIM,
    )


def flash_wrong():
    for _ in range(FLASH_COUNT):
        for index in range(NUM_ADDR_LEDS):
            set_game_led(index, (255, 255, 255))
        addr_show()
        utime.sleep_ms(FLASH_MS)
        addr_clear()
        utime.sleep_ms(FLASH_MS)


def celebrate():
    """Show a changing, random four-color pattern for a few seconds."""
    stop_at = utime.ticks_add(utime.ticks_ms(), 3000)
    while utime.ticks_diff(stop_at, utime.ticks_ms()) > 0:
        for index in range(NUM_ADDR_LEDS):
            color = COLOR_CHOICES[random.randrange(4)][0]
            set_game_led(index, color)
        addr_show()
        utime.sleep_ms(120)


def new_pattern():
    colors = []
    for _ in range(NUM_ADDR_LEDS):
        # Once a color has appeared twice in a row, leave it out of the next draw.
        choices = COLOR_CHOICES
        if len(colors) >= 2 and colors[-1] == colors[-2]:
            choices = tuple(choice for choice in COLOR_CHOICES if choice[0] != colors[-1])
        colors.append(choices[random.randrange(len(choices))][0])
    return colors


def wait_for_button_press():
    while not any(button_states()):
        utime.sleep_ms(FRAME_MS)
    return utime.ticks_ms()


def run_game(started_at):
    colors = new_pattern()
    current = 0
    last_timer_update = started_at
    last_blink = utime.ticks_ms()
    current_visible = True
    prev_buttons = button_states()
    draw_play_screen()
    light_pattern(colors, current, current_visible)

    while current < NUM_ADDR_LEDS:
        now = utime.ticks_ms()
        elapsed = utime.ticks_diff(now, started_at)
        if utime.ticks_diff(now, last_blink) >= CURRENT_LED_BLINK_MS:
            current_visible = not current_visible
            light_pattern(colors, current, current_visible)
            last_blink = now
        if utime.ticks_diff(now, last_timer_update) >= TIMER_UPDATE_MS:
            draw_timer(elapsed)
            last_timer_update = now

        states = button_states()
        # Only act once per press; holding a button cannot skip several LEDs.
        pressed = [states[i] and not prev_buttons[i] for i in range(4)]
        prev_buttons = states
        selected = None
        for choice_index in range(4):
            if pressed[choice_index]:
                selected = choice_index
                break

        if selected is not None:
            expected = next(
                i for i, choice in enumerate(COLOR_CHOICES)
                if choice[0] == colors[current]
            )
            if selected == expected:
                current += 1
                if current < NUM_ADDR_LEDS:
                    current_visible = True
                    last_blink = utime.ticks_ms()
                    light_pattern(colors, current, current_visible)
                    tft.fill_rect(0, 118, DISPLAY_W, 20, st7789.BLACK)
                    draw_centered("LED %d / %d" % (current + 1, NUM_ADDR_LEDS), 122)
                else:
                    light_pattern(colors, -1)
            else:
                flash_wrong()
                current = 0
                current_visible = True
                last_blink = utime.ticks_ms()
                light_pattern(colors, current, current_visible)
                tft.fill_rect(0, 118, DISPLAY_W, 20, st7789.BLACK)
                draw_centered("LED 1 / %d" % NUM_ADDR_LEDS, 122)
                # Ignore any buttons still held after the flash.
                wait_for_release()
                prev_buttons = button_states()

        utime.sleep_ms(FRAME_MS)

    elapsed = utime.ticks_diff(utime.ticks_ms(), started_at)
    celebrate()
    addr_clear()
    tft.fill(st7789.BLACK)
    draw_centered("YOU WIN!", 54, st7789.GREEN)
    draw_centered("Time: %.1f sec" % (elapsed / 1000.0), 92, st7789.YELLOW)
    draw_centered("Press any button", 136, st7789.CYAN)
    draw_centered("for a new pattern", 156, st7789.CYAN)


try:
    addr_clear()
    show_instructions()
    wait_for_release()
    game_started_at = wait_for_button_press()
    wait_for_release()

    while True:
        run_game(game_started_at)
        wait_for_release()
        # Start a new round directly from the win screen with a fresh pattern.
        game_started_at = wait_for_button_press()
        wait_for_release()
except KeyboardInterrupt:
    addr_clear()

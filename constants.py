import math

FPS = 60
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

SCALE_1 = 1
SCALE_2 = 2
SCALE_3 = 3

SHOOTER_DIAG_OFFSET = 25

TILE_SIZE = 32 * SCALE_3
CHAR_SIZE = 32
TILE_TYPES = 17
ROWS = 30
COLS = 60
SCROLL_THRESH_X = 500
SCROLL_THRESH_Y = 300
NEAR_RANGE = 50
FAR_RANGE = 1000
LINE_OF_SIGHT = 500

SPEED = 4

BULLET_SPEED = 10
VILLAIN_BULLET_SPEED = 3
VILLAIN_SPEED = SPEED - 1
DIAGONAL_COEFFICIENT = (math.sqrt(2)/2)

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG = (40, 25, 25)

PANEL = (50, 50, 50)

TIPS = [
    "You can use combinations of W,A,S,D to move diagonally. Enjoy surviving!",
    "The villains won't come to you if there is a wall in between.",
    "The blaze will make you faster. But will expire in 9 seconds.",
    "Avoid the flaggers as much as you can. They slow you down. It's good that their effects don't last forever!"
]

FINAL_LEVEL = 7
LEVEL_CLEAR_MESSAGE = [
    {
        "messages": ["Congratulations Agent!", "We are proud of you.", "The agency has decided to continue the contract with you.", "You are ready for your next mission."],
        "new_item": ""
    },
    {
        "messages": ["Level completed!", "That's a great progress. Keep pushing and never surrender..."],
        "new_item": "COINS",
        "new_item_description": "The coins that you collect on the way, shall help you with additional health."
    },
    {
        "messages": ["Level completed!", "The villains are now aware of your advances.", "Beware agent. They are coming in large armies..."],
        "new_item": "",
        "new_item_description": ""
    },
    {
        "messages": ["Level completed!", "Once again you have proven your mettle.", "The agency is proud of you."],
        "new_item": "AID",
        "new_item_description": "Regain your lost health by collecting these health pills."
    },
    {
        "messages": ["Level 5 finished"],
        "new_item": ""
    },
    {
        "messages": ["Level 6 finished"],
        "new_item": ""
    },
    {
        "messages": ["You have successfully finished the game. The agency is proud to have an agent like you.", "Keep in touch and we will bring more challenging missions in the future."],
        "new_item": "TROPHY",
        "new_item_description": "Farewell comrade!"
    }
]
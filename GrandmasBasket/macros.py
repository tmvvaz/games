"""
This file is for preferences and macros.
"""
import pygame
import os


WIDTH, HEIGHT           = 0, 1
RESOLUTION              = 1600, 900
FPS                     = 30

BOTTOM_PADDING          = 50

DIR_RES                 = "resources/"
RES_IMAGES              = DIR_RES + "images/"
RES_AUDIO               = DIR_RES + "audio/"

FONT_TYPE               = "Comic Sans MS"
FONT_COLOR              = (255, 255, 255)

# static elements
IMG_BACKGROUND          = "background.png"
IMG_FOREGROUND          = "foreground.png"

# basket states
IMG_BASKET_EMPTY        = "basket.png"
IMG_BASKET_FULL         = "basket_full.png"
IMG_BASKET_FULL_TOTAL   = "basket_full_total.png"
IMG_BASKET_LOADED       = "basket_loaded.png"
IMG_BASKET_INCLINED_L   = "basket_inclined_left.png"
IMG_BASKET_INCLINED_R   = "basket_inclined_right.png"

# grandma states
IMG_GRANDMA_UNHAPPY     = "grandma_unhappy.png"
IMG_GRANDMA_MAD         = "grandma_mad.png"
IMG_GRANDMA_ANGRY       = "grandma_angry.png"
IMG_GRANDMA_RAGED       = "grandma_raged.png"

# falling items
IMG_SHIRT_BLUE          = "item_shirt_blue.png"
IMG_SHIRT_GREEN         = "item_shirt_green.png"
IMG_SHIRT_RED           = "item_shirt_red.png"
IMG_SHIRT_ORANGE        = "item_shirt_orange.png"
IMG_SHIRT_PURPLE        = "item_shirt_purple.png"
IMG_NECKLACE            = "item_necklace.png"
IMG_PAN                 = "item_pan.png"
IMG_BOXERS              = "item_boxers.png"

# clouds and passing elements
IMG_CLOUD_S             = "cloud_S.png"
IMG_CLOUD_MS            = "cloud_MS.png"
IMG_CLOUD_M             = "cloud_M.png"
IMG_CLOUD_ML            = "cloud_ML.png"
IMG_CLOUD_L             = "cloud_L.png"
IMG_CLOUD_XL            = "cloud_XL.png"

# game over screen
IMG_OVER_FACE_OPEN      = "over_face_open.png"
IMG_OVER_FACE_CLOSED    = "over_face_closed.png"
IMG_OVER_BODY           = "over_grandma_body.png"

KEY_CLOUDS              = "clouds"
KEY_BACKGROUND          = "background"
KEY_BASKET              = "basket_states"
KEY_ITEMS               = "items"
KEY_GRANDMA             = "grandma"
KEY_OVER                = "over"

KEY_HUMOR_UNHAPPY       = "unhappy"         # neutral state
KEY_HUMOR_MAD           = "mad"
KEY_HUMOR_ANGRY         = "angry"
KEY_HUMOR_RAGED         = "raged"           # one more item on the ground and the player loses the game

TEXT_START              = "space bar to help grandma"
TEXT_LOST               = "space bar to try again"
TEXT_PAUSE              = "space bar to continue"
TEXT_SCORE              = "GIVEN: "
TEXT_BEST_SCORE         = "BEST : "

# audio TODO misses converting this to .wav
AUDIO_MAIN_THEME        = "main_theme.mp3"
AUDIO_SCORE             = "action_score.mp3"
AUDIO_TAKE_ITEM         = "action_take_item.mp3"
AUDIO_OVER_SCREAM       = "over_scream.mp3"


def load_audio(name):
    return pygame.mixer.Sound(RES_AUDIO + name)


def load_image(name):
    image_path = RES_IMAGES + name
    return pygame.image.load(os.path.join(image_path)).convert_alpha()


def get_image_map():
    return {
                  KEY_GRANDMA :
                      {IMG_GRANDMA_UNHAPPY  : load_image(IMG_GRANDMA_UNHAPPY),
                       IMG_GRANDMA_MAD      : load_image(IMG_GRANDMA_MAD),
                       IMG_GRANDMA_ANGRY    : load_image(IMG_GRANDMA_ANGRY),
                       IMG_GRANDMA_RAGED    : load_image(IMG_GRANDMA_RAGED)},
                  KEY_BASKET :
                      {IMG_BASKET_EMPTY      : load_image(IMG_BASKET_EMPTY),
                       IMG_BASKET_FULL       : load_image(IMG_BASKET_FULL),
                       IMG_BASKET_FULL_TOTAL : load_image(IMG_BASKET_FULL_TOTAL),
                       IMG_BASKET_LOADED     : load_image(IMG_BASKET_LOADED)},
                  KEY_ITEMS :
                      {IMG_SHIRT_BLUE   : load_image(IMG_SHIRT_BLUE),
                       IMG_SHIRT_RED    : load_image(IMG_SHIRT_RED),
                       IMG_SHIRT_GREEN  : load_image(IMG_SHIRT_GREEN),
                       IMG_SHIRT_ORANGE : load_image(IMG_SHIRT_ORANGE),
                       IMG_SHIRT_PURPLE : load_image(IMG_SHIRT_PURPLE),
                       IMG_BOXERS       : load_image(IMG_BOXERS),
                       IMG_NECKLACE     : load_image(IMG_NECKLACE),
                       IMG_PAN          : load_image(IMG_PAN)},
                  KEY_BACKGROUND :
                      {IMG_BACKGROUND   : load_image(IMG_BACKGROUND),
                       IMG_FOREGROUND       : load_image(IMG_FOREGROUND),
                       KEY_CLOUDS:
                          {IMG_CLOUD_S  : load_image(IMG_CLOUD_S),
                           IMG_CLOUD_MS : load_image(IMG_CLOUD_MS),
                           IMG_CLOUD_M  : load_image(IMG_CLOUD_M),
                           IMG_CLOUD_ML : load_image(IMG_CLOUD_ML),
                           IMG_CLOUD_L  : load_image(IMG_CLOUD_L),
                           IMG_CLOUD_XL : load_image(IMG_CLOUD_XL)}
                       },
                  KEY_OVER :
                      {IMG_OVER_FACE_OPEN   : load_image(IMG_OVER_FACE_OPEN),
                       IMG_OVER_FACE_CLOSED : load_image(IMG_OVER_FACE_CLOSED),
                       IMG_OVER_BODY        : load_image(IMG_OVER_BODY)}
    }

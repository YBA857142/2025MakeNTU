import time
from rpi_ws281x import PixelStrip, Color


def init():
    for i in range(strip.numPixels()-1):
        strip.setPixelColor(i, Color(255, 0, 0))
    strip.show()
    time.sleep(0.25)
    for i in range(strip.numPixels()-1):
        strip.setPixelColor(i, Color(0, 255, 0))
    strip.show()
    time.sleep(0.25)
    for i in range(strip.numPixels()-1):
        strip.setPixelColor(i, Color(0, 0, 255))
    strip.show()
    time.sleep(0.25)
  
    idx = strip.numPixels() - 1
    strip.setPixelColor(idx, Color(255, 0, 0))
    strip.show()

def set_strip_color(strip, prev_rgb, cur_rgb, has_hit):
    if has_hit:
        idx = strip.numPixels() - 1
        strip.setPixelColor(idx, Color(0, 255, 0) if has_hit else Color(255, 0, 0))
    else:
        r = max(0, min(255, cur_rgb[0])) - prev_rgb[0]
        g = max(0, min(255, cur_rgb[1])) - prev_rgb[1]
        b = max(0, min(255, cur_rgb[2])) - prev_rgb[2]
        dcolor = (r ** 2 + g ** 2 + b ** 2) ** 0.5 + 1
        r = int(r * min(dcolor, 51.2) / dcolor + prev_rgb[0])
        g = int(g * min(dcolor, 51.2) / dcolor + prev_rgb[1])
        b = int(b * min(dcolor, 51.2) / dcolor + prev_rgb[2])
        for i in range(strip.numPixels()-1):
            strip.setPixelColor(i, Color(r, g, b))
    strip.show()

def clear_strip(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()


if __name__ == '__main__':

    try:
        LED_COUNT = 11
        LED_PIN = 18
        LED_BRIGHTNESS = 10
        LED_FREQ_HZ = 800000
        LED_DMA = 10
        LED_INVERT = False
        LED_CHANNEL = 0

        strip = PixelStrip(LED_COUNT,LED_PIN,LED_FREQ_HZ,LED_DMA,LED_INVERT,LED_BRIGHTNESS,LED_CHANNEL)
        strip.begin()
        init()
        set_strip_color((100, 100, 100), (100, 100, 100), 0)
        time.sleep(3)
        # while True:
        #     time.sleep(1)
    finally:
        clear_strip()

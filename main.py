from machine import Pin, ADC, PWM
from utime import sleep

"""
    Pico Wisdom: Displays wise phrases and their authors. Designed to be part of
    an informational picture frame. Built with a Pico W (although Wi-Fi not used)
    and a Waveshare 4.2v2 e-ink display. Runs off 3xAA (ideally lithium) through a
    Pololu 2808 push button circuit. Connect GPIO 1 to the OFF pin of the Pololu.
    Connect a passive piezo buzzer to GPIO 5 and GND. User presses button wired to
    Pololu which powers up Pico. A new phrase is selected on boot, different to the
    last. The Pico will then signal to the Pololu to power off.
    
    Assuming about 10 presses a day, Pico doing ~40mA and display 24mW, that's about 8
    years of battery life. Pololu circuit standby uses .01uA, which would equate to
    34,000 years (batteries will degrade before then)! Display will add a "Low battery"
    when the batteries need changing. Uses a slimmed down, optimized version (fewer
    flickers) of Peter Hinch's micropython-nano-gui for graphics. 
    
    Dave Burke, 2025.
"""

phrases = [
    ["The important thing is not to stop questioning.", "Albert Einstein"],
    ["Genius is one percent inspiration, ninety-nine percent perspiration.", "Thomas Edison"],
    ["It does not matter how slowly you go as long as you do not stop.", "Confucius"],
    ["Our greatest glory is not in never falling, but in rising up every time we fall.", "Confucius"],
    ["The journey of a thousand miles begins with a single step.", "Lao Tzu"],
    ["A healthy outside starts from the inside.", "Robert Urich"],
    ["The greatest wealth is health.", "Virgil"],
    ["Look deep into nature, and then you will understand everything better.", "Albert Einstein"],
    ["The body achieves what the mind believes.", "Napoleon Hill"],
    ["Knowing yourself is the beginning of all wisdom.", "Aristotle"],
    ["Laughter is the best medicine.", "Proverb"],
    ["Fall seven times, stand up eight.", "Japanese Proverb"],
    ["Stay hungry, stay foolish.", "Steve Jobs"],
    ["Science is simply common sense at its best.", "Thomas Huxley"],
    ["What we think, we become.", "Buddha"],
    ["Wisdom begins in wonder.", "Socrates"],
    ["The only true wisdom is in knowing you know nothing.", "Socrates"],
    ["I think, therefore I am.", "Rene Descartes"],
    ["Small deeds done are better than great deeds planned.", "Peter Marshall"],
    ["The expert in anything was once a beginner.", "Helen Hayes"],
    ["Do what you can, with what you have, where you are.", "Theodore Roosevelt"],
    ["Action is the foundational key to all success.", "Pablo Picasso"],
    ["A little knowledge that acts is worth infinitely more than much knowledge that is idle.", "Kahlil Gibran"],
    ["Learn from yesterday, live for today, hope for tomorrow.", "Albert Einstein"],
    ["You're braver than you believe, and stronger than you seem, and smarter than you think.", "A.A. Milne"],
    ["It's not that I'm so smart, it's just that I stay with problems longer.", "Albert Einstein"],
    ["The best way to predict the future is to create it.", "Peter Drucker"],
    ["None of us is as smart as all of us.", "Ken Blanchard"],
    ["Be silly, be honest, be kind.", "Ralph Waldo Emerson"],

    # Irish
    ["Mistakes are the portals of discovery.", "James Joyce"],
    ["If we winter this one out, we can summer anywhere.", "Seamus Heaney"],
    ["Life isn't about finding yourself. Life is about creating yourself.", "George Bernard Shaw"],
    ["Be yourself; everyone else is already taken.", "Oscar Wilde"],

    # Dylan's quotes
    ["The early bird catches the worm. But who's thinking about the worm?", "Dylan Burke"],
    ["You're never too old to learn, Gagga.", "Dylan Burke"],
    ["About longevity: You should also think about researching ways of extending peoples' perception of time.", "Dylan Burke"],
    ["Can we go on holidays more with our friends? That's what I like the most.", "Dylan Burke"],

    # Bruce Lee
    ["The key to immortality is first living a life worth remembering.", "Bruce Lee"],
    ["Knowledge will give you power, but character respect.", "Bruce Lee"],
    ["Be like water, my friend.", "Bruce Lee"],

    # Synapse School changemakers
    ["An investment in knowledge pays the best interest.", "Benjamin Franklin"],
    ["Energy and persistence conquer all things.", "Benjamin Franklin"],
    ["Life is architecture and architecture is the mirror of life.", "I.M. Pei"],
    ["\"Si, se puede\" (Yes, it is possible).", "Dolores Huerta"],
    ["3 ways to ultimate success: The 1st way is to be kind. The 2nd way is to be kind. The 3rd way is to be kind.", "Fred Rogers"],
    ["Fight for the things that you care about, but do it in a way that will lead others to join you.", "Ruth Bader Ginsburg"],
    ["Don't raise your voice, improve your argument.", "Desmond Tutu"],
    ["People look at us as the label of our disability. And it is a part of who we are, but it is not who we are.", "Judy Heumann"]
]

LAST_INDEX_FILENAME = "last_index.txt"  # ensure different phrase with each boot
CRITICAL_VOLTAGE = 3.25

go_asleep_pin = Pin(1, Pin.OUT, value=0)  # GPIO 1 connected to OFF pin on Pololu
buzzer = PWM(Pin(5))  # passive piezo buzzer connected to GPIO 5 and GND

def store_last_index(index):
    with open(LAST_INDEX_FILENAME, 'w') as file:
        file.write(str(index))

def recall_last_index():
    try:
        with open(LAST_INDEX_FILENAME, 'r') as file:
            return int(file.read().strip())
    except OSError as e:
        return 0
    
def get_phrase_and_author():
    last_index = recall_last_index()
    while True:
        index = random.randint(0, len(phrases) - 1)
        if not index == last_index: break
    store_last_index(index)
    return phrases[index][0], phrases[index][1]

def measure_vsys():
    Pin(25, Pin.OUT, value=1)  # disable Wi-Fi on Pico W
    Pin(29, Pin.IN, pull=None)
    reading = ADC(3).read_u16() * 9.9 / 2**16
    Pin(25, Pin.OUT, value=0, pull=Pin.PULL_DOWN)
    Pin(29, Pin.ALT, pull=Pin.PULL_DOWN, alt=7)
    return reading

def turn_wifi_off():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.deinit()
    
def play_beep():
    buzzer.freq(2048)
    buzzer.duty_u16(1000)
    sleep(0.15)
    buzzer.duty_u16(0)

if __name__=='__main__':
    play_beep()
    turn_wifi_off()
    
    # Inline rest of imports to greatly minimize button-to-beep time
    import random
    from color_setup import ssd
    from gui.core.writer import CWriter
    from gui.widgets.label import Label
    from gui.widgets.textbox import Textbox
    import gui.fonts.arial35 as arial35
    import gui.fonts.courier20 as courier20
    
    # Phrase textbox and author label
    phrase, author = get_phrase_and_author()
    writer = CWriter(ssd, arial35, verbose=False)
    writer.set_clip(True, True, False)
    Textbox(writer, 60, 15, 370, 5, clip=False).append(phrase + " ")
    writer = CWriter(ssd, courier20, verbose=False)
    writer.set_clip(True, True, False)
    Label(writer, 240, 15, '-' + author)
    
    # (Maybe) low battery label
    vsys = measure_vsys()
    if vsys < CRITICAL_VOLTAGE:
        import gui.fonts.arial10 as arial10
        writer = CWriter(ssd, arial10, verbose=False)
        writer.set_clip(True, True, False)
        Label(writer, 280, 326, 'Low battery')
        
    # Refresh display, then signal Pololu to power us down
    ssd.show()
    go_asleep_pin.on()
    
    


# Pico-Wisdom
Displays wise phrases and their authors upon button press. Designed to be part of an informational picture frame with super long battery life (years)
Built with a Pico W (although Wi-Fi not used) and an e-ink display. Runs off 3xAA through a Pololu push button circuit. 

## Parts list
- Raspberry Pi Pico W (although Wi-Fi not currently used) - https://www.raspberrypi.com/products/raspberry-pi-pico/
- Pololu 2808 push button circuit - https://www.pololu.com/product/2808
- Waveshare 4.2" e-ink display (v2) - https://www.waveshare.com/4.2inch-e-paper-module.htm
- Push button - https://www.amazon.com/dp/B08SKJ6V7Z?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_1
- Passive piezo buzzer CYT1008 - https://www.amazon.com/dp/B01NCOXB2Q?ref_=ppx_hzsearch_conn_dt_b_fed_asin_title_1
- 3xAA battery holder - https://www.amazon.com/Battery-Storage-Charging-Parallel-Batteries/dp/B0B3YFPB53/ref=sr_1_3?crid=V98JT7CMVI0G

## Wiring diagram
Powered by 3xAA batteries through the Pololu 2808. User presses button wired to Pololu which powers up Pico. A beep is played and a new phrase is selected on boot, different to the last. The Pico will then signal to the Pololu via GPIO 1 to power off.

<img src="Schematic.jpg?"/>

## Battery life estimate
Assuming about 10 pushes a day, Pico doing ~40mA and display 24mW, that's about 8 years of battery life. Pololu circuit standby uses .01uA, which would equate to 34,000 years (batteries will degrade before then)! Recommend using lithium AA batteries for longest life. Display will add a "Low battery" when the batteries need changing. 

#!/usr/bin/env python3
"""
PWM Tone Generator

based on https://www.coderdojotc.org/micropython/sound/04-play-scale/
"""

import machine
import utime

# GP16 is the speaker pin
SPEAKER_PIN = 16

# create a Pulse Width Modulation Object on this pin
speaker = machine.PWM(machine.Pin(SPEAKER_PIN))


def playtone(frequency: float, duration: float) -> None:
    speaker.duty_u16(1000)
    speaker.freq(int(frequency))
    utime.sleep(duration)


def quiet():
    speaker.duty_u16(0)


freq: float = 30
duration: float = .5  # seconds

print("Playing frequency (Hz):")
song: float = [659.25,659.25,659.25,523.25,659.25,783.99,523.25,783.99,659.25,880,987.77,932.33,880,783.99,659.25,783.99,880,698.46,783.99,659.25,523.25,587.33,987.77]
for i in song:
    print(i)
    playtone(i, duration)
    quiet()
    utime.sleep(.1)

# Turn off the PWM
quiet()

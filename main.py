#!/home/manuel/virtualenv/hardware/bin/python
from serial import Serial
from serial.tools import list_ports_linux
import time
import subprocess

print("Multimedia keyboard handler")

arduino = None
try:
    while True:
        for port in list_ports_linux.comports():
            if(port[2] != 'n/a'):
                print("Checking: ", port[0])
                arduino = Serial(port[0], timeout=5)
                agree = arduino.read()
                if(agree == b'Z'):
                    arduino.write(b'K')
                    break
        else:
            print("No multimedia keyboard found, waiting for retry...")
            time.sleep(10)
            continue
        print("Arduino Keyboard found")
        break

    i = j = k = m = n = o = 0

    play = True

    commands = {
        'A': ['xdotool', 'key', 'XF86AudioMute'],
        'B': ['xdotool', 'key', 'XF86AudioLowerVolume'],
        'C': ['xdotool', 'key', 'XF86AudioRaiseVolume'],
        'D': ['xdotool', 'key', 'XF86AudioPlay'] if play else ['xdotool', 'key', 'XF86AudioPause'],
        'E': ['xdotool', 'key', 'XF86AudioNext'],
        'F': ['xdotool', 'key', 'XF86AudioPrev'],
    }

    while True:
        char = arduino.read()
        if char == b'A':
            print(char, "Mute", i)
            subprocess.call(commands.get(char.decode()))
            i += 1
        if char == b'B':
            print(char, "Volume down", j)
            subprocess.call(commands.get(char.decode()))
            j += 1

        if char == b'C':
            print(char, "Volume up", k)
            subprocess.call(commands.get(char.decode()))
            k += 1

        if char == b'D':
            print(char, "Play/Pause", m)
            subprocess.call(commands.get(char.decode()))
            m += 1

        if char == b'E':
            print(char, "Next", n)
            subprocess.call(commands.get(char.decode()))
            n += 1

        if char == b'F':
            print(char, "Prev", o)
            subprocess.call(commands.get(char.decode()))
            o += 1
except (KeyboardInterrupt, BlockingIOError) as e:
    pass
finally:
    arduino.close()

#!/home/manuel/virtualenv/hardware/bin/python
from serial import Serial
from serial.tools import list_ports_linux
from handlers import WatchEventHandler
from queue import Queue
import setproctitle
import pyinotify
import time
import os
import sh

version = "0.9-MOC"

setproctitle.setproctitle("multikeys")
print("Multimedia keyboard handler ", version)

arduino = wm = wdd = notifier = None
try:
    while True:
        for port in list_ports_linux.comports():
            if(port[2] != 'n/a'):
                print("Checking: ", port[0])
                arduino = Serial(port[0], timeout=5)
                agree = arduino.read()
                if(agree == b'Z'):
                    arduino.write(b'K')
                    arduino.timeout = None
                    break
        else:
            print("No multimedia keyboard found, waiting for retry...")
            time.sleep(10)
            continue
        print("Arduino Keyboard found")
        break

    moc_dir = "{}/.moc/".format(os.environ.get('HOME'))

    running_queue = Queue(maxsize=1)

    wm = pyinotify.WatchManager()

    mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE

    notifier = pyinotify.ThreadedNotifier(wm, WatchEventHandler(running_queue))

    os.chdir(moc_dir)

    is_moc_running = os.path.exists(os.path.join(moc_dir, 'pid'))

    i = j = k = m = n = o = 0

    commands = {
        'A': ['key', 'XF86AudioMute'],
        'B': ['key', 'XF86AudioLowerVolume'],
        'C': ['key', 'XF86AudioRaiseVolume'],
        'D': ['key', 'XF86AudioPlay'],
        'E': ['key', 'XF86AudioNext'],
        'F': ['key', 'XF86AudioPrev'],
    }

    moc_commands = {
        'D': ['-G'],
        'E': ['-f'],
        'F': ['-r'],
    }

    notifier.start()

    wdd = wm.add_watch(moc_dir, mask, rec=False)

    while True:
        char = arduino.read()
        if running_queue.full():
            is_moc_running = running_queue.get_nowait()

        if char == b'A':
            print(char, "Mute", i)
            sh.xdotool(commands.get(char.decode()))
            i += 1
        if char == b'B':
            print(char, "Volume down", j)
            sh.xdotool(commands.get(char.decode()))
            j += 1

        if char == b'C':
            print(char, "Volume up", k)
            sh.xdotool(commands.get(char.decode()))
            k += 1

        if char == b'D':
            print(char, "Play/Pause", m)
            if is_moc_running:
                sh.mocp(moc_commands.get(char.decode()))
            else:
                sh.xdotool(commands.get(char.decode()))
            m += 1

        if char == b'E':
            print(char, "Next", n)
            if is_moc_running:
                sh.mocp(moc_commands.get(char.decode()))
            else:
                sh.xdotool(commands.get(char.decode()))
            n += 1

        if char == b'F':
            print(char, "Prev", o)
            if is_moc_running:
                sh.mocp(moc_commands.get(char.decode()))
            else:
                sh.xdotool(commands.get(char.decode()))
            o += 1
except (KeyboardInterrupt, BlockingIOError) as e:
    pass
finally:
    wm.rm_watch(1)
    notifier.stop()
    arduino.close()

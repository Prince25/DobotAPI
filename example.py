from core.effectors.gripper import Gripper
from core.effectors.suctioncup import SuctionCup
from core.dobot import Position, Dobot
from core.utils import get_coms_port
import time
import coloredlogs
import logging as console

coloredlogs.install(level=console.DEBUG,
                    fmt="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")

port = get_coms_port()
bot = Dobot(port, False)
bot.connect()

posGrab = Position(324.22, -31.75, 14.42, -5.59)
posRelease = Position(173.75, 268.69, 48.04, 57.11)
posMiddle = Position(239.45, 0.83, 140.17, 0.20)

gripper = Gripper(bot)
sucktioncup = SuctionCup(bot)

moving = False


def main():
    bot.ir_toggle(True)
    lastGrab = time.time()
    max_delay = 20

    while time.time()-lastGrab < max_delay:
        if(not bot.get_ir()):
            bot.conveyor_belt(0.25, 1)
        else:
            bot.conveyor_belt(0, 1)
            bot.move_to_position(posGrab)
            sucktioncup.suck()
            bot.move_to_position(posMiddle)
            bot.move_to_position(posRelease)
            sucktioncup.blow()
            sucktioncup.idle()
            bot.move_to_position(posMiddle)
            lastGrab = time.time()

        time.sleep(0.1)

    else:
        bot.move_to_position(posMiddle)
        bot.close()


try:
    main()
except KeyboardInterrupt:
    bot.move_to_position(posMiddle)
    bot.close()

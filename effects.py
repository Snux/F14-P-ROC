# Mode to handle various simple effects that other modes will use.
# Does not contain any direct switch handlers of its own.
# This needs to be a mode rather than a plain class so that we can use some
# of the modes features like delayed calls.

from procgame import *

class Effects(game.Mode):

    def __init__(self,game):
        super(Effects,self).__init__(game=game,priority=2)

    def flickerOn(self,lamp,duration=0.75,schedule=0x55555555):
        """
        Flickers a lamp briefly and then switches it on
        Optionally specify the duration of the flicker and the lamp schedule

        Usage from other modes :
        self.games.effects.flickerOn(lamp='shootAgain')
        self.games.effects.flickerOn(lamp='shootAgain', duration=3.0)
        """
        self.game.lamps[lamp].schedule(schedule=schedule, cycle_seconds=duration, now=True)
        self.delay(name='lampon',event_type=None,delay=duration,handler=self.game.lamps[lamp].enable)

    
    def flickerOff(self,lamp,duration=0.75,schedule=0x55555555):
        """
        Flickers a lamp briefly and then switches it off
        Normally used to indicate something was hit but nothing special happened
        Optionally specify the duration of the flicker and the lamp schedule

        Usage from other modes :
        self.games.effects.flickerOff(lamp='shootAgain')
        self.games.effects.flickerOff(lamp='shootAgain', duration=3.0)
        """
        self.game.lamps[lamp].schedule(schedule=schedule, cycle_seconds=duration, now=True)
        self.delay(name='lampoff',event_type=None,delay=duration,handler=self.game.lamps[lamp].disable)

    def scheduleTomcat(self):
        """
        Schedule the 12 TOMCAT lamps to strobe in left/right/left pattern
        Used instead of a lampshow so that individual lamps can later still
        be controlled independently of the show
        """
        self.game.lamps['lowerLeftT'].schedule( schedule=0b11100000000000000000000111000000, cycle_seconds=0, now=False)
        self.game.lamps['lowerLeftO'].schedule( schedule=0b01110000000000000000001110000000, cycle_seconds=0, now=False)
        self.game.lamps['lowerLeftM'].schedule( schedule=0b00111000000000000000011100000000, cycle_seconds=0, now=False)
        self.game.lamps['upperLeftT'].schedule( schedule=0b00011100000000000000111000000000, cycle_seconds=0, now=False)
        self.game.lamps['upperLeftO'].schedule( schedule=0b00001110000000000001110000000000, cycle_seconds=0, now=False)
        self.game.lamps['upperLeftM'].schedule( schedule=0b00000111000000000011100000000000, cycle_seconds=0, now=False)
        self.game.lamps['upperRightC'].schedule(schedule=0b00000011100000000111000000000000, cycle_seconds=0, now=False)
        self.game.lamps['upperRightA'].schedule(schedule=0b00000001110000001110000000000000, cycle_seconds=0, now=False)
        self.game.lamps['upperRightT'].schedule(schedule=0b00000000111000011100000000000000, cycle_seconds=0, now=False)
        self.game.lamps['lowerRightC'].schedule(schedule=0b00000000011100111000000000000000, cycle_seconds=0, now=False)
        self.game.lamps['lowerRightA'].schedule(schedule=0b00000000001101100000000000000000, cycle_seconds=0, now=False)
        self.game.lamps['lowerRightT'].schedule(schedule=0b00000000000111000000000000000000, cycle_seconds=0, now=False)






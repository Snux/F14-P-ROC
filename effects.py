# Mode to handle various simple effects that other modes will use.
# Does not contain any direct switch handlers of its own.
# This needs to be a mode rather than a plain class so that we can use some
# of the modes features like delayed calls and DMD usage

from procgame import *
from procgame.dmd import font_named


class Effects(game.Mode):

    def __init__(self,game):
        super(Effects,self).__init__(game=game,priority=2)
        
    def flickerOn(self,lamp,duration=0.75,schedule=0x55555555):
        """
        Flickers a lamp briefly and then switches it on
        Optionally specify the duration of the flicker and the lamp schedule

        Usage from other modes :
        self.game.effects.flickerOn(lamp='shootAgain')
        self.game.effects.flickerOn(lamp='shootAgain', duration=3.0)
        """
        self.game.lamps[lamp].schedule(schedule=schedule, cycle_seconds=duration, now=True)
        self.delay(name=lamp+"on",event_type=None,delay=duration,handler=self.game.lamps[lamp].enable)
     
    
    def flickerOff(self,lamp,duration=0.75,schedule=0x55555555):
        """
        Flickers a lamp briefly and then switches it off
        Normally used to indicate something was hit but nothing special happened
        Optionally specify the duration of the flicker and the lamp schedule

        Usage from other modes :
        self.game.effects.flickerOff(lamp='shootAgain')
        self.game.effects.flickerOff(lamp='shootAgain', duration=3.0)
        """
        self.game.lamps[lamp].schedule(schedule=schedule, cycle_seconds=duration, now=True)
        self.delay(name=lamp+"off",event_type=None,delay=duration,handler=self.game.lamps[lamp].disable)

    def display_text(self,txt,txt2=None,time=2,blink=2):
        if txt2==None:
            self.layer = dmd.TextLayer(128/2, 7, font_named("beware11.dmd"), "center", opaque=True).set_text(txt,seconds=time,blink_frames=blink)
        else:
            self.press_layer = dmd.TextLayer(128/2, -5, font_named("beware15.dmd"), "center").set_text(txt,seconds=time)
            self.start_layer = dmd.TextLayer(128/2, 10, font_named("beware15.dmd"), "center").set_text(txt2,seconds=time, blink_frames=blink)
            self.start_layer.composite_op = 'blacksrc'
            self.layer = dmd.GroupedLayer(128, 32, [self.press_layer,self.start_layer])
        self.delay(name='dmdoff',event_type=None,delay=time,handler=self.display_clear)


    def display_clear(self):
        try:
            del self.layer
        except:
            pass

    def light_bonus(self):
        """
        Display the current bonus multiplier and bonus count for
        the player on the playfield lamps
        """

        # Multiplier is easy
        if self.game.current_player().bonusMultiplier > 1:
            for x in range(2, self.game.current_player().bonusMultiplier):
                self.game.lamps["bonus"+str(x)+"X"].enable()

        # For the bonus we need to work through the binary value
        bonus = self.game.current_player().bonus
        bonusbin = "0"*(7-len(bin(bonus)[2:]))+bin(bonus)[2:]
        digitvalue=64
        for digit in list(bonusbin):
            if digit == "1":
                self.game.lamps["bonus"+str(digitvalue)+"K"].enable()
            else:
                self.game.lamps["bonus"+str(digitvalue)+"K"].disable()
            digitvalue /= 2


    






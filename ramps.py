# Placeholder for running the ramps.  Basically just keep the kickouts clear

from procgame import *

class Ramps(game.Mode):

    def __init__(self,game):
        super(Ramps,self).__init__(game=game,priority=2)
        self.missile_tracking = False

    def sw_vUK_active_for_100ms(self,sw):
        self.game.lampctrl.play_show('topstrobe', repeat=False)
        self.game.effects.display_text(txt="MISSILE",txt2="LAUNCH")
        self.delay(name='kick',event_type=None,delay=1,handler=self.kickvuk)
        self.missile_tracking = True

    def kickvuk(self):
        self.game.coils.upKicker.pulse()

    def sw_leftCenterEject_active_for_100ms(self,sw):
        self.game.coils.centreLeftEject.pulse()

    def sw_rightCenterEject_active_for_100ms(self,sw):
        self.game.coils.centreRightEject.pulse()

    def sw_rightEject_active_for_800ms(self,sw):
        if self.missile_tracking:
            self.game.effects.display_text(txt="TARGET",txt2="MISSED")
            self.missile_tracking = False
        self.game.coils.rightEject.pulse()

    def sw_inlaneLeft_active(self,sw):
        self.game.lampctrl.play_show('fireright', repeat=False)
        self.delay(name='fire',event_type=None,delay=0.5,handler=self.game.update_lamps)

    def sw_inlaneRight_active(self,sw):
        self.game.lampctrl.play_show('fireleft', repeat=False)
        self.delay(name='fire',event_type=None,delay=0.5,handler=self.game.update_lamps)


    def sw_slingL_active(self,sw):
        self.game.score(100)
    
    def sw_slingR_active(self,sw):
        self.game.score(100)

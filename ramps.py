# Placeholder for running the ramps.  Basically just keep the kickouts clear

from procgame import *

class Ramps(game.Mode):

    def __init__(self,game):
        super(Ramps,self).__init__(game=game,priority=2)
        self.missile_tracking = False
        self.launch_bonus_tracking = False
        self.launch_bonus = 10000
        self.kill_lit=False
        self.lite_kill_enabled=False

    def sw_vUK_active_for_200ms(self,sw):
        if self.launch_bonus_tracking:
            self.game.score(self.launch_bonus)
            self.game.effects.display_text(txt="LAUNCH",txt2=str(self.launch_bonus))
            if self.launch_bonus < 100000:
                self.launch_bonus *= 2
            self.launchBonusOver()
        else :
            self.game.lampctrl.play_show('topstrobe', repeat=False)
            self.game.effects.display_text(txt="MISSILE",txt2="LAUNCH")
            self.missile_tracking = True
        self.delay(name='kick',event_type=None,delay=1,handler=self.kickvuk)

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
        self.game.lampctrl.play_show('fireright', repeat=True)
        self.delay(name='fire',event_type=None,delay=2.5,handler=self.launchBonusOver)
        self.launch_bonus_tracking = True
        if self.lite_kill_enabled:
            self.enable_kill()

    def light_enable_kill(self):
        self.lite_kill_enabled=True
        self.game.lamps.inLanes.enable()

    def clear_enable_kill(self):
        self.lite_kill_enabled=False
        self.game.lamps.inLanes.disable()


    def enable_kill(self):
        self.game.lamps.kill.enable()
        self.kill_lit=True
        self.delay(name='endkill',event_type=None,delay=1.5,handler=self.disable_kill)

    def disable_kill(self):
        self.kill_lit=False
        self.game.lamps.kill.disable()

    def launchBonusOver(self):
        self.launch_bonus_tracking = False
        self.game.lampctrl.stop_show()
        self.game.update_lamps()

    def sw_inlaneRight_active(self,sw):
        self.game.lampctrl.play_show('fireleft', repeat=False)
        self.delay(name='fire',event_type=None,delay=0.5,handler=self.game.update_lamps)
        if self.lite_kill_enabled:
            self.enable_kill()



    def sw_slingL_active(self,sw):
        self.game.score(100)
        self.game.sound.play('slinglow')
    
    def sw_slingR_active(self,sw):
        self.game.score(100)
        self.game.sound.play('slinglow')

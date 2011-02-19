# Placeholder for running the ramps.  Basically just keep the kickouts clear

import procgame.game

class Ramps(procgame.game.Mode):

    def __init__(self,game):
        super(Ramps,self).__init__(game=game,priority=2)

    def sw_vUK_active_for_100ms(self,sw):
        self.game.coils.upKicker.pulse()

    def sw_leftCenterEject_active_for_100ms(self,sw):
        self.game.coils.centreLeftEject.pulse()

    def sw_rightCenterEject_active_for_100ms(self,sw):
        self.game.coils.centreRightEject.pulse()

    def sw_rightEject_active_for_800ms(self,sw):
        print "Eject"
        self.game.coils.rightEject.pulse()
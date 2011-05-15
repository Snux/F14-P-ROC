from procgame import *

class F14Player(game.Player):

    def __init__(self, name):
	super(F14Player, self).__init__(name)

        self.targetmade={}
	self.targetmade['target1']=False
        self.targetmade['target2']=False
        self.targetmade['target3']=False
        self.targetmade['target4']=False
        self.targetmade['target5']=False
        self.targetmade['target6']=False

        
        self.nextkill='alpha'
        self.extraBallLit=False


        self.bonus=0
        self.bonusMultiplier=1

        # kickBackLit for each player is either on, off or counting
        self.kickBackLit='off'



	
		
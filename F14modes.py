# Game modes

from procgame import *

class TomcatHurryup(game.Mode):

    def __init__(self,game):
        super(TomcatHurryup,self).__init__(game=game,priority=3)
        self.tomcatTargets={}
        for switch in self.game.switches:
            if switch.name[0:5] in ('upper','lower'):
                self.add_switch_handler(name=switch.name, event_type='active', \
                        delay=None, handler=self.targetHit)
                self.tomcatTargets[switch.name]=False
                self.game.effects.cancel_delayed(name=switch.name) #clear pending flickers
        
    def mode_started(self):
        self.scheduleTomcat()
        self.game.coils.beacons.enable()
        self.remind()

    def remind(self):
        self.game.effects.display_text(txt="SHOOT",txt2="TOMCAT")
        self.delay(name='remind',event_type=None,delay=5,handler=self.remind)

    def mode_stopped(self):
        self.game.coils.beacons.disable()
        for x in self.tomcatTargets:
            self.tomcatTargets[x]=False
        for x in self.tomcatTargets:
            self.game.lamps[x].disable()
        
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


    def targetHit(self,sw):
        self.game.lamps[sw.name].enable()
        self.tomcatTargets[sw.name]=True
        if sum([i for i in self.tomcatTargets.values()])==12:
            self.game.effects.display_text(txt="TOMCAT BONUS 100 K",time=3.5)
            self.game.score(100000)
            self.game.modes.remove(self.game.tomcathurryup)
        return True

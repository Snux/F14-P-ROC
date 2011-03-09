# Tomcat main game and mode

from procgame import *
from procgame.dmd import font_named

import pinproc
import time
import trough
import player
import ramps
import effects
import F14modes

import attract

import locale
locale.setlocale(locale.LC_ALL, "") # Used to put commas in the score.
fnt_path = "/shared/dmd/"
sound_path = "./sound/"
font_14x10 = font_named('Font14x10.dmd')
font_jazz18 = font_named("Jazz18-18px.dmd")

lampshow_files = ["./lamps/sweepleftright.lampshow", \
#                  "./lamps/f14fireright.lampshow", \
#                  "./lamps/sweepleftright.lampshow", \
                 ]

class BaseGameMode(game.Mode):
	"""A mode that runs whenever the game is in progress."""
	def __init__(self, game):
		super(BaseGameMode, self).__init__(game=game, priority=1)
                self.yagovHurryUpActive=False
                self.rescue={}
                self.bonusXRight = 'off'
                self.bonusXLeft = 'off'
                self.tomcatTargets={}
                self.lastBonusLoop = time.clock()
    	
	def mode_started(self):
		self.game.trough.changed_handlers.append(self.trough_changed)
                anim = dmd.Animation().load("./dmd/tomcat3.dmd")
                self.layer = dmd.AnimatedLayer(frames=anim.frames, repeat=True, frame_time=1)

                for switch in self.game.switches:
                    if switch.name.find('target', 0) != -1:
                        self.add_switch_handler(name=switch.name, event_type='active', \
				delay=0.01, handler=self.target1_6)
                    if switch.name[0:5] in ('upper','lower'):
                        self.add_switch_handler(name=switch.name, event_type='active', \
                                delay=0.01, handler=self.targetTOMCAT)
                        self.tomcatTargets[switch.name]=False
                        self.game.lamps[switch.name].disable()


                self.add_switch_handler(name='leftRescue',event_type='active', \
                                delay=0.01, handler=self.rescueHit)
                self.add_switch_handler(name='rightRescue',event_type='active', \
                                delay=0.01, handler=self.rescueHit)

                
                self.add_switch_handler(name='bonusXRight',event_type='active', \
                                delay=0.01, handler=self.rescueHit)
                self.add_switch_handler(name='bonusXLeft',event_type='active', \
                                delay=0.01, handler=self.bonusLane)

                if self.game.current_player().kickBackLit == 'on':
                    self.make_kickBack_active()
                else:
                    self.make_kickBack_inactive()

                #self.scheduleTomcat()

        def bonusLane(self,sw):
            if time.clock() - self.lastBonusLoop < 1:
                pass
            else:
                self.lastBonusLoop=time.clock()
                if sw.name[6:]=="Right":
                    if self.bonusXRight == 'on':
                        self.game.inc_bonusMultiplier()
                        self.cancel_delayed(name="rightoff")
                    self.game.lamps[sw.name].schedule(schedule=0x0F0F0F0F, cycle_seconds=2.0, now=True)
                    self.delay(name="rightoff",event_type=None,delay=2.0,handler=self.bonusLaneOff,param="Right")
                    self.bonusXRight = 'on'
                else:
                    if self.bonusXLeft == 'on':
                        self.game.inc_bonusMultiplier()
                        self.cancel_delayed(name="leftoff")
                    self.game.lamps[sw.name].schedule(schedule=0x0F0F0F0F, cycle_seconds=2.0, now=True)
                    self.delay(name="leftoff",event_type=None,delay=2.0,handler=self.bonusLaneOff,param="Left")
                    self.bonusXLeft = 'on'


        def bonusLaneOff(self,side):
            if side == "Right":
                self.bonusXRight = 'off'
                self.game.lamps["bonusXRight"].disable()
            else:
                self.bonusXLeft = 'off'
                self.game.lamps["bonusXLeft"].disable()


        def sw_rampEntry_active(self,sw):
            try:
                del self.layer
            except:
                pass
        
        def targetTOMCAT(self,sw):
            self.tomcatTargets[sw.name]=True
            if sw.name[0:5]=="upper":
                otherside="lower"+sw.name[5:]
            else:
                otherside="upper"+sw.name[5:]
            self.tomcatTargets[otherside]=True
            self.game.score(10)
            if sum([i for i in self.tomcatTargets.values()])==12: # all targets lit
                self.game.modes.add(self.game.tomcathurryup)
            else:
                #self.game.lamps.lowerLeftT.schedule(schedule=0x55555555, cycle_seconds=0.75, now=True)
                #self.delay(name='lowerLeftT',event_type=None,delay=0.75,handler=self.game.lamps.lowerLeftT.enable)
                #self.game.lamps.upperLeftT.schedule(schedule=0x55555555, cycle_seconds=0.75, now=True)
                #self.delay(name='upperLeftT',event_type=None,delay=0.75,handler=self.game.lamps.upperLeftT.enable)
                self.game.effects.flickerOn(sw.name)
                self.game.effects.flickerOn(otherside)
                

        
        def make_kickBack_active(self):
            self.game.current_player().kickBackLit='on'
            self.rescue['leftRescue']='on'
            self.rescue['rightRescue']='on'
            self.rescueSet(param='set')
            self.game.lamps['kickBack'].enable()

        def make_kickBack_inactive(self):
            self.game.current_player().kickBackLit='off'
            self.rescueSet(param='timeout')
            self.game.lamps['kickBack'].disable()

        def mode_stopped(self): # naming is inconsistent with game_ended/ball_ended
            self.game.trough.changed_handlers.remove(self.trough_changed)
            self.game.modes.remove(self.game.tomcathurryup)
            self.game.effects.display_clear()
            self.stop_lamps()
                
	def trough_changed(self):
            if self.game.trough.is_full():
		self.game.end_ball()

        def stop_lamps(self):
            self.game.lampctrl.stop_show()

        
        def sw_yagov_active(self,sw):
            self.game.coils.yagovKickBack.pulse()
            if self.yagovHurryUpActive==True:
                self.game.lampctrl.play_show('topstrobe', repeat=False)
                self.yagovHurryUpActive=False
                self.game.score(10000)
    
        def sw_outlaneL_active_for_10ms(self,sw):
            if self.game.current_player().kickBackLit != 'off':
                self.game.coils.rescueKickBack.pulse()
            if self.game.current_player().kickBackLit == 'on':
                self.game.current_player().kickBackLit = 'counting'
                self.game.lamps['kickBack'].schedule(schedule=0x0F0F0F0F, cycle_seconds=5, now=True)
                self.delay(name='kickBackDelay', event_type=None, delay=5.0, handler=self.make_kickBack_inactive)

        def rescueHit(self,sw):
            self.rescue[sw.name]='on'
            self.game.score(50)
            if self.game.current_player().kickBackLit != 'on':
                if self.rescue['leftRescue']=='on' and self.rescue['rightRescue']=='on':
                    self.make_kickBack_active()
                    self.game.effects.display_text(txt="KICKBACK", txt2="ACTIVE")
                    self.game.score(1000)
                    self.cancel_delayed(name='rescueDelay')
                else:
                    if sw.name == 'leftRescue':
                        self.rescue['rightRescue']='counting'
                    if sw.name == 'rightRescue':
                        self.rescue['leftRescue']='counting'
                    self.delay(name='rescueDelay', event_type=None, delay=2.0, handler=self.rescueSet, param='timeout')
            self.rescueSet(param='set')
            
        def rescueSet(self,param):
            if param=='timeout':
                self.rescue['leftRescue']='off'
                self.rescue['rightRescue']='off'
            for x in ['leftRescue','rightRescue']:
                if self.rescue[x] == 'off':
                    self.game.lamps[x].schedule(schedule=0x00FF00FF, cycle_seconds=0, now=True)
                elif self.rescue[x] == 'counting':
                    self.game.lamps[x].schedule(schedule=0x33333333, cycle_seconds=0, now=True)
                else:
                    self.game.lamps[x].enable()

        def target1_6(self,sw):
            self.game.score(100)
            self.game.bonus(1)
            self.game.effects.flickerOn(sw.name)   # switch on the lamp at the target
            self.game.current_player().targetmade[sw.name]=True
            if sum([i for i in self.game.current_player().targetmade.values()])==6:
                self.hurryUpStart();



        def hurryUpStart(self):
            for x in self.game.current_player().targetmade:
                self.game.lamps[x].schedule(schedule=0x00FF00FF, cycle_seconds=2, now=True)
                self.game.current_player().targetmade[x]=False
            self.game.effects.display_text(txt="SHOOT YAGOV!!")
            self.make_kickBack_active()
            self.yagovHurryUpActive=True
            self.game.lampctrl.play_show('fireleft', repeat=True)
            self.delay(name='hurryUp', event_type=None, delay=5.0, handler=self.hurryUpEnd)
            self.game.sound.play('inbound')

        def hurryUpEnd(self):
            self.yagovHurryUpActive=False
            self.game.lampctrl.stop_show()
        
	



class TomcatGame(game.BasicGame):
	
	trough = None
	base_game_mode = None
       	
	def __init__(self):
		super(TomcatGame, self).__init__(pinproc.MachineTypeWPC95)
		self.load_config('F14.yaml')
		self.lampctrl = lamps.LampController(self)
                self.sound = sound.SoundController(self)
                self.sound.register_sound('startup', sound_path+"Jet_F14_TakeOff.wav")
                self.sound.register_sound('inbound', sound_path+"inbound.wav")
                self.sound.set_volume(5)
                # Register lampshow files
		self.lampshow_keys = []
		key_ctr = 0
		for file in lampshow_files:
			key = 'attract' + str(key_ctr)
			self.lampshow_keys.append(key)
			self.lampctrl.register_show(key, file)
			key_ctr += 1
		self.lampctrl.register_show('fireleft','./lamps/f14fireleft.lampshow')
                self.lampctrl.register_show('topstrobe','./lamps/topstrobe.lampshow')

		self.trough = trough.Trough(game=self)
		self.base_game_mode = BaseGameMode(game=self)
                self.effects = effects.Effects(game=self)
                self.tomcathurryup = F14modes.TomcatHurryup(game=self)
                self.ramp = ramps.Ramps(game=self)
                self.attract_mode = attract.Attract(game=self)
                self.reset()


        def update_player_record(self, key, record):
		p = self.current_player()
		p.info_record[key] = record

	def get_player_record(self, key):
		p = self.current_player()
		if key in p.info_record:
			return p.info_record[key]
		else:
			return []

        def bonus(self, bonus):
            self.current_player().bonus += bonus
            if self.current_player().bonus > 127:
                self.current_player().bonus = 127
            self.effects.light_bonus()

        def inc_bonusMultiplier(self):
            if self.current_player().bonusMultiplier < 8:
                self.current_player().bonusMultiplier += 1
                self.effects.light_bonus()

	# GameController Methods
	def create_player(self, name):
		return player.F14Player(name)

	def reset(self):
		super(TomcatGame,self).reset()
		self.modes.add(self.trough)
                self.modes.add(self.ramp)
                self.modes.add(self.effects)
                self.modes.add(self.attract_mode)

        def enable_flippers(self,enable):
            if enable:
                self.coils.flipperEnable.pulse(0)
            else:
                self.coils.flipperEnable.disable()
            
	def start_ball(self):
		super(TomcatGame, self).start_ball()
	
	def game_started(self):
		self.log("GAME STARTED")
		super(TomcatGame, self).game_started()
		# Don't start_ball() here, since Attract does that after calling start_game().
	
	def ball_starting(self):
		self.log("BALL STARTING")
                print "Start " + self.current_player().name
		super(TomcatGame, self).ball_starting()
         
                for x in self.current_player().targetmade:
                    #print x + " " + str(self.current_player().targetmade[x])
                    if self.current_player().targetmade[x] == False:
                        self.lamps[x].disable()
                    else:
                        self.lamps[x].enable()

		# TODO: Check that there is not already a ball in the shooter lane.
		# TODO: Pulse the trough until we get a hit from the shooter lane switch.
		self.coils.trough.pulse() # eject a ball into the shooter lane
		
		self.enable_flippers(True)
		self.modes.add(self.base_game_mode)

	def ball_ended(self):
		"""Called by end_ball(), which is itself called by base_game_mode.trough_changed."""
		self.log("BALL ENDED")
                print "End " + self.current_player().name
                self.modes.remove(self.base_game_mode)
		self.enable_flippers(False)
		super(TomcatGame, self).ball_ended()

	def game_ended(self):
		self.log("GAME ENDED")
		super(TomcatGame, self).game_ended()
		self.modes.remove(self.base_game_mode)
		self.modes.add(self.attract_mode)

## main:

def main():
	game = None
	try:
	 	game = TomcatGame()
		game.run_loop()
	finally:
		del game

if __name__ == '__main__':
	main()

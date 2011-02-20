# MIT License
# 
# Copyright (c) 2011 Adam Preble
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from procgame import *
from procgame.dmd import font_named

import pinproc
import trough
import ramps
import attract

import locale
locale.setlocale(locale.LC_ALL, "") # Used to put commas in the score.
fnt_path = "/shared/dmd/"
font_14x10 = font_named('Font14x10.dmd')
font_jazz18 = font_named("Jazz18-18px.dmd")



lampshow_files = ["./lamps/sweepleftright.lampshow", \
#                  "./lamps/f14fireright.lampshow", \
#                  "./lamps/sweepleftright.lampshow", \
                 ]

class scoreMode(game.Mode):

        def __init__(self, game):
            super(scoreMode,self).__init__(game=game, priority=2)

        def mode_started(self):
            for switch in self.game.switches:
		if switch.name.find('target', 0) != -1:
		       self.add_switch_handler(name=switch.name, event_type='active', \
				delay=None, handler=self.plus100)

        def plus100(self,sw):
            print sw.name
            self.game.score(100)
            self.game.lamps[sw.name].enable()

            
class BaseGameMode(game.Mode):
	"""A mode that runs whenever the game is in progress."""
	def __init__(self, game):
		super(BaseGameMode, self).__init__(game=game, priority=1)
	
	def mode_started(self):
		self.game.trough.changed_handlers.append(self.trough_changed)
	
	def mode_stopped(self): # naming is inconsistent with game_ended/ball_ended
		self.game.trough.changed_handlers.remove(self.trough_changed)

	def trough_changed(self):
		if self.game.trough.is_full():
			self.game.end_ball()
	



class TomcatGame(game.BasicGame):
	
	trough = None
	base_game_mode = None
	
	def __init__(self):
		super(TomcatGame, self).__init__(pinproc.MachineTypeWPC)
		self.load_config('F14.yaml')
		self.lampctrl = lamps.LampController(self)
                tiny7 = dmd.Font(fnt_path+"04B-03-7px.dmd")
                font_jazz18 = dmd.Font(fnt_path+"Jazz18-18px.dmd")
                font_14x10 = dmd.Font(fnt_path+"Font14x10.dmd")
                font_18x12 = dmd.Font(fnt_path+"Font18x12.dmd")
                font_07x4 = dmd.Font(fnt_path+"Font07x4.dmd")
                font_07x5 = dmd.Font(fnt_path+"Font07x5.dmd")
                font_09Bx7 = dmd.Font(fnt_path+"Font09Bx7.dmd")
	        # Register lampshow files
		self.lampshow_keys = []
		key_ctr = 0
		for file in lampshow_files:
			key = 'attract' + str(key_ctr)
			self.lampshow_keys.append(key)
			self.lampctrl.register_show(key, file)
			key_ctr += 1
		pass

		self.trough = trough.Trough(game=self)
		self.base_game_mode = BaseGameMode(game=self)
                self.ramp = ramps.Ramps(game=self)
                self.attract_mode = attract.Attract(game=self)
                self.score_mode = scoreMode(game=self)
                self.reset()


	
	# GameController Methods
	
	def reset(self):
		super(TomcatGame,self).reset()
		
		self.modes.add(self.trough)
                self.modes.add(self.ramp)
                self.modes.add(self.score_mode)
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
		super(TomcatGame, self).ball_starting()
		
		# TODO: Check that there is not already a ball in the shooter lane.
		# TODO: Pulse the trough until we get a hit from the shooter lane switch.
		self.coils.trough.pulse() # eject a ball into the shooter lane
		
		self.enable_flippers(True)
		self.modes.add(self.base_game_mode)

	def ball_ended(self):
		"""Called by end_ball(), which is itself called by base_game_mode.trough_changed."""
		self.log("BALL ENDED")
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

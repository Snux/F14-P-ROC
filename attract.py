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
from random import *


class PrepareToStart(game.Mode):
	"""Manages waiting for the game to be ready to start."""
	def __init__(self, game):
		super(PrepareToStart, self).__init__(game=game, priority=9)
	
	def mode_started(self):
		self.game.trough.changed_handlers.append(self.trough_changed)
		self.pulse_and_delay()
	
	def mode_stopped(self):
		self.game.trough.changed_handlers.remove(self.trough_changed)
	
	def trough_changed(self):
		self.check_ready()
	
	def check_ready(self):
		"""Perform checks on the system state to see if we are ready to start the game."""
                print "Checking ready"
		if self.game.trough.is_full():
                        print "Ready"
			self.ready()
			return True
		print "Not Ready"
		return False
	
	def pulse_and_delay(self):
		ready = self.check_ready()
		if not ready:
			self.game.coils.jetBumper.pulse()
			#self.game.coils.lowerRightPopper.pulse()
			self.delay(name='pulse_and_delay',
			           event_type=None,
			           delay=5.0,
			           handler=self.pulse_and_delay)
		
	def ready(self):
		"""Called to indicate that the game is ready to start."""
		# Remove attract mode from mode queue - Necessary?
		self.game.modes.remove(self)
		# Initialize game	
		self.game.start_game()
		# Add the first player
		self.game.add_player()
                #self.game.add_player()
		# Start the ball.  This includes ejecting a ball from the trough.
		self.game.start_ball()



class Attract(game.Mode):
	"""A mode that runs whenever the game is in progress."""
        
	def __init__(self, game):
            super(Attract, self).__init__(game=game, priority=9)
                        
	def change_lampshow(self):
            shuffle(self.game.lampshow_keys)
            self.game.lampctrl.play_show(self.game.lampshow_keys[0], repeat=True)
            self.delay(name='lampshow', event_type=None, delay=10, handler=self.change_lampshow)
            
        def mode_started(self):
            self.change_lampshow()
            anim = dmd.Animation().load("./dmd/f14launch.dmd")
            self.takeoff_layer = dmd.AnimatedLayer(frames=anim.frames, hold=False, repeat=False, frame_time=5)
            
	    self.f14_splash_layer = dmd.FrameLayer(opaque=True, frame=dmd.Animation().load('./dmd/f14bw2.dmd').frames[0])
            self.f14_sunset_layer = dmd.FrameLayer(opaque=True, frame=dmd.Animation().load('./dmd/f14sun.dmd').frames[0])
            self.f14_layer = dmd.FrameLayer(opaque=True, frame=dmd.Animation().load('./dmd/tomcat20beware.dmd').frames[0])

            self.press_layer = dmd.TextLayer(128/2, -8, font_named("beware22aa.dmd"), "center").set_text("PRESS")
            self.start_layer = dmd.TextLayer(128/2, 8, font_named("beware22aa.dmd"), "center").set_text("START")
            self.start_layer.composite_op = 'blacksrc'
            self.press_start_layer = dmd.GroupedLayer(128, 32, [self.press_layer,self.start_layer])
            gen = dmd.MarkupFrameGenerator()
            gen.font_plain=font_named("beware11.dmd")
            gen.font_bold=font_named("beware20aa.dmd")
            credits_frame = gen.frame_for_markup("""

#CREDITS#

[Rules + Coding]
[Mark Sunnucks]

[Special thanks]
[G. Stellenberg]
[A. Preble]
[S. van der Staaij]

[P-ROC]
[pyprocgame]

""")

            self.credits_layer = dmd.PanningLayer(width=128, height=32, frame=credits_frame, origin=(0,0), translate=(0,1), bounce=False)
            self.credits_layer.composite_op = 'blacksrc'
            self.credits_overlay_layer = dmd.GroupedLayer(128, 32, [self.takeoff_layer,self.credits_layer])
            script = [{'seconds':5.0, 'layer':self.f14_splash_layer},
		          {'seconds':5.0, 'layer':self.press_start_layer},
			  {'seconds':20.0, 'layer':self.credits_overlay_layer},
                          {'seconds':5.0, 'layer':self.f14_sunset_layer},
                          {'seconds':5.0, 'layer':self.press_start_layer}]
                          
            self.layer = dmd.ScriptedLayer(width=128, height=32, script=script)

	def mode_stopped(self):
            self.game.lampctrl.stop_show()
            
                

	def sw_startButton_active(self, sw):
		self.game.modes.remove(self)
		# TODO: PrepareToStart should just be 'startup ball search.'
		#       We don't want to start the game immediately after we find the balls.
		self.game.modes.add(PrepareToStart(game=self.game))

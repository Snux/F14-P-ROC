# Loader

# Original code from Jim (myPinballs) and Koen (DutchPinball)


from procgame import *
from procgame.dmd import font_named
import os




class Loader(game.Mode):

	def __init__(self, game, priority):
            super(Loader, self).__init__(game, priority)

            self.selection=0

            # Define the versions we want to run and what will run them
            self.versions=['Williams ROM Release Version','Williams ROM version Proto3','Williams ROM version Proto4','Williams ROM version Proto5','TOMCAT 2.0']
            self.runners=['(using Pinmame F14_L1)','(using Pinmame F14_P3)','(using Pinmame F14_P4)','(using Pinmame F14_P5)','(using pyProcgame)']

            self.reset()


        def reset(self):
            self.text1a_layer = dmd.TextLayer(64, 1, font_named("04B-03-7px.dmd"), "center", opaque=False).set_text("Choose game with flippers")
            self.text1b_layer = dmd.TextLayer(64, 9, font_named("04B-03-7px.dmd"), "center", opaque=False).set_text("then press start to select")

            self.text2_layer = dmd.TextLayer(64, 18, font_named("04B-03-7px.dmd"), "center", opaque=False)
            self.text3_layer = dmd.TextLayer(64, 25, font_named("04B-03-7px.dmd"), "center", opaque=False)

            self.layer = dmd.GroupedLayer(128, 32, [self.text3_layer,self.text2_layer, self.text1a_layer, self.text1b_layer])#set clear time


        def mode_started(self):
            self.select()

        def mode_tick(self):
            pass

        def select(self,dir=0):

            
            self.selection+=dir
            
            if self.selection<0:
               self.selection=len(self.versions)-1

            if self.selection==len(self.versions):
                self.selection=0
            
            self.text3_layer.set_text(self.runners[self.selection])
            self.text2_layer.set_text(self.versions[self.selection],blink_frames=20)

            



        def sw_startButton_active(self, sw):

            # PYPROC is at position 4 on the list
            if self.selection < 4:
		self.launch_williams(self.selection)
            else:
		self.launch_mypinballs()


        def sw_flipperLwL_active(self, sw):
            self.select(dir=-1)


        def sw_flipperLwR_active(self, sw):
            self.select(dir=1)


        def launch_williams(self, choice):
		self.stop_proc()
                # Call the pinmame executable to take over from here, further execution of Python code is halted.
                # Positions 15 to 21 in the runner string contain the ROM name, so strip that out
                os.chdir("e:\mame\proc");
                os.system(r"pinmamep "+self.runners[choice][15:21]+" -window -p-roc f14.yaml -alpha_on_dmd -skip_disclaimer -skip_gameinfo")


		#Pinmame executable was:
		# - Quit by a delete on the keyboard
		# - Interupted by flipper buttons + start button combo

		# Reset mode & restart P-ROC / pyprocgame
		self.mode_started()
		self.restart_proc()


	def launch_mypinballs(self):
		self.stop_proc()

		# Import and run the startup script, further execution of this script is halted until the run_loop is stopped.
		import F14
		F14.main()

		# Reset mode & restart P-ROC / pyprocgame
		self.mode_started()
		self.restart_proc()


        def stop_proc(self):

                self.game.end_run_loop()
		while len(self.game.dmd.frame_handlers) > 0:
			del self.game.dmd.frame_handlers[0]
		del self.game.proc

	def restart_proc(self):
		self.game.proc = self.game.create_pinproc()
		self.game.proc.reset(1)
		self.game.load_config(self.game.yamlpath)
		self.game.enable_flippers(True)
		self.game.dmd.frame_handlers.append(self.game.proc.dmd_draw)
		self.game.dmd.frame_handlers.append(self.game.set_last_frame)
		self.game.run_loop()

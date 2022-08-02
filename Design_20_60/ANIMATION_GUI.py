from PySide2 import QtCore
from PySide import QtGui

class MyGui(QtGui.QWidget):

	# Initializing the number of teeths in each of the gears
	sun_gear = 20 # Cut005
	planet_gear1 = 40 # Cut006
	planet_gear2 = 40 # Cut007
	planet_gear3 = 40 # Cut008
	ring_gear = 100 # Fusion001
	
	# Initialize the gear offset angle
	sg_offset = 0 # Sun gear
	pg1_offset = 0 # Planet gear
	pg2_offset = 0 # Planet gear
	pg3_offset = 0 # Planet gear
	rg_offset = 280 # Ring gear
	
	r = 0 # Initializing the angle of rotation

	def __init__(self):
		super(MyGui, self).__init__()
		# Setting the Window
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self.setWindowTitle("Gear Folding Comb")
		self.resize(265,75)
		self.show()

		# Setting the Buttons
		self.bt_play = QtGui.QPushButton("PLAY",self)
		self.bt_reset = QtGui.QPushButton("RESET",self)
		self.bt_pause = QtGui.QPushButton("PAUSE",self)

		# Back-end connection of the buttons with user-defined functions
		QtCore.QObject.connect(self.bt_play, QtCore.SIGNAL("pressed()"),self.bt_play_click)
		QtCore.QObject.connect(self.bt_reset, QtCore.SIGNAL("pressed()"),self.bt_reset_click)
		QtCore.QObject.connect(self.bt_pause, QtCore.SIGNAL("pressed()"),self.bt_pause_click)
		
		# Setting out the Layout
		layout = QtGui.QGridLayout()
		layout.addWidget(self.bt_play, 0,0)
		layout.addWidget(self.bt_reset, 0,1)
		layout.addWidget(self.bt_pause, 0,2)
		self.setLayout(layout)

		self.timer = QtCore.QTimer()

	# Action performed by the "PLAY" button
	def bt_play_click(self):
		self.timer.timeout.connect(self.play)
		self.timer.start(1)

	# Action performed by the "RESET" button
	def bt_reset_click(self):
		self.timer.timeout.connect(self.reset)
		self.timer.start(1)

	# Action performed by the "PAUSE" button
	def bt_pause_click(self):
		self.timer.stop()

	# Action to be performed when "close" button is clicked
	def closeEvent(self, event):
		App.Console.PrintMessage("closing\n")
		self.timer.stop()

	# ________Forward Motion________
	def play(self):
		global r, sun_gear, planet_gear1, planet_gear2, planet_gear3, ring_gear, sg_offset, pg1_offset, pg2_offset, pg3_offset, rg_offset
		if r in range(0,180):
			# Sun gear
			rots = sg_offset + r
			FreeCAD.getDocument('Proj_Design').getObject('Cut005').Placement = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),rots))
			# Planet gear1
			rot1 = pg1_offset + (sun_gear/planet_gear1)*r
			FreeCAD.getDocument('Proj_Design').getObject('Cut006').Placement = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),-rot1))	
			# PLanet gear2
			rot2 = pg2_offset + (sun_gear/planet_gear2)*r
			FreeCAD.getDocument('Proj_Design').getObject('Cut007').Placement = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),-rot2))
			# Planer gear 3
			rot3 = pg3_offset + (sun_gear/planet_gear3)*r
			FreeCAD.getDocument('Proj_Design').getObject('Cut008').Placement = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),-rot3))
		# Ring gear
		if r in range(0,75):
			rot4 = rg_offset + r
			FreeCAD.getDocument('Proj_Design').getObject('Fusion001').Placement = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),rot4))
		# Comb body
		if r in range(0,180):
			FreeCAD.getDocument('Proj_Design').getObject('Body').Placement = App.Placement(App.Vector(0,0,-2.5),App.Rotation(App.Vector(0,0,1),-r))
		r+=1

	# ________Resetting the Motion________
	def reset(self):
		# Sun gear
		FreeCAD.getDocument('Proj_Design').getObject('Cut005').Placement = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),0))
		# Planet gear1
		FreeCAD.getDocument('Proj_Design').getObject('Cut006').Placement = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),0))	
		# Planet gear2
		FreeCAD.getDocument('Proj_Design').getObject('Cut007').Placement = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),0))
		# Planet gear3
		FreeCAD.getDocument('Proj_Design').getObject('Cut008').Placement = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),0))
		# Ring gear
		FreeCAD.getDocument('Proj_Design').getObject('Fusion001').Placement = App.Placement(App.Vector(0,0,0),App.Rotation(App.Vector(0,0,1),-75))
		# Comb body
		FreeCAD.getDocument('Proj_Design').getObject('Body').Placement = App.Placement(App.Vector(0,0,-2.5),App.Rotation(App.Vector(0,0,1),0))

gui = MyGui()
import os

import tkinter.filedialog as filedialog
import pygame

from app.controller import Controller

if __name__ == '__main__':

	original_dir = os.getcwd()

	chosen_dir = filedialog.askdirectory()

	# Initialize GUI
	f = Controller(chosen_dir)
	f.pack()

	# Initialize pygame
	pygame.init()

	# Initialize the clock
	clock = pygame.time.Clock()

	# Start playing songs
	f.focus_force()
	f.play()

	# Write the GUI loop manually
	while True:
		clock.tick(60)

		for event in pygame.event.get():
			if event.type == Controller.MUSIC_ENDED:
				f.play_next()

		# Update GUI
		f.update_frame()
		f.update_listbox()
		f.update_seekbar()

		# Built-in update methods
		f.update_idletasks()
		f.update()

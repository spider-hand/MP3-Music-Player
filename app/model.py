import os
import math
import random

from mutagen.mp3 import MP3 
from mutagen.id3 import ID3

import pygame

class Model:
	def __init__(self, directory):
		os.chdir(directory)
		self.song_dir = os.getcwd()

		self.song_list = []
		self.real_names = []
		self.shuffle_list = []
		self.is_stopped = False
		self.is_repeat = False
		self.is_shuffle = False

		for file in os.listdir(directory):
			if file.endswith(".mp3"):
				self.realdir = os.path.realpath(file)
				try:
					self.audio = ID3(self.realdir)
					self.real_names.append(self.audio['TIT2'].text[0])
				except:
					self.real_names.append(file)
				self.song_list.append(file)

		self.current_song_index = 0

	def play(self):
		pygame.mixer.music.load(self.song_list[self.current_song_index])
		pygame.mixer.music.set_volume(0.5)
		pygame.mixer.music.play()

	def play_next(self):
		if self.is_repeat:
			pygame.mixer.music.load(self.song_list[self.current_song_index])
			pygame.mixer.music.play()
		elif self.is_shuffle:
			self.play_shuffle()
		else:
			self.current_song_index = \
			(self.current_song_index + 1) % len(self.song_list)
			pygame.mixer.music.load(self.song_list[self.current_song_index])
			pygame.mixer.music.play()

	def play_pause_song(self):
		if self.is_stopped:
			if pygame.mixer.music.get_busy():
				pygame.mixer.music.unpause()
			else:
				pygame.mixer.music.play()
			self.is_stopped = False
		else:
			pygame.mixer.music.pause()
			self.is_stopped = True

	def play_shuffle(self):
		self.current_song_index = random.randint(0, len(self.song_list) - 1)
		# Prevent the same song from being played repeatedly
		while self.current_song_index in self.shuffle_list:
			self.current_song_index = random.randint(0, len(self.song_list) - 1)
		self.shuffle_list.append(self.current_song_index)

		if len(self.shuffle_list) == len(self.song_list):
			self.shuffle_list = []
		pygame.mixer.music.load(self.song_list[self.current_song_index])
		if not self.is_stopped:
			pygame.mixer.music.play()

	def play_selected_song(self):
		pygame.mixer.music.load(self.song_list[self.current_song_index])
		pygame.mixer.music.play()

	def previous_song(self):
		if self.is_shuffle:
			self.play_shuffle()
		else:
			self.current_song_index = \
			(self.current_song_index - 1) % len(self.song_list)
			pygame.mixer.music.load(self.song_list[self.current_song_index])
			if not self.is_stopped:
				pygame.mixer.music.play()

	def next_song(self):
		if self.is_shuffle:
			self.play_shuffle()
		else:
			self.current_song_index = \
			(self.current_song_index + 1) % len(self.song_list)
			pygame.mixer.music.load(self.song_list[self.current_song_index])
			if not self.is_stopped:
				pygame.mixer.music.play()

	def rewind_song(self):
		if self.is_stopped:
			self.previous_song()
		# Go back to the previous song if the button is clicked within three seconds after a song started
		elif self.get_current_playing_position() <= 2:
			self.previous_song()
		else:
			pygame.mixer.music.play(start=0.0)

	def get_current_song(self):
		return self.real_names[self.current_song_index]

	def get_artist(self):
		mp3 = MP3(self.song_list[self.current_song_index])
		tags = mp3.tags
		try:
			return tags.get('TPE1', 'No artist name')
		except:
			return 'No artist name'

	def get_album(self):
		mp3 = MP3(self.song_list[self.current_song_index])
		tags = mp3.tags
		try:
			return tags.get('TALB', 'No album title')
		except:
			return 'No album title'

	def get_current_playing_position(self):
		pos_mi = pygame.mixer.music.get_pos()
		sec = math.floor(pos_mi / 1000)
		return sec

	def get_current_song_length(self):
		mp3 = MP3(self.song_list[self.current_song_index])
		info = mp3.info
		return info.length

	def convert_song_length(self):
		length = float(self.get_current_song_length())
		length = math.floor(length)
		return length

	def change_volume(self, volume):
		pygame.mixer.music.set_volume(volume)

import tkinter as Tk
import pygame

from app.model import Model
from app.views import MainFrame, Artwork, Seekbar, TextFrame, Buttons, ScrollListBox,\
 VolumeWindow

class Controller(Tk.Frame):
	MUSIC_ENDED = pygame.USEREVENT + 1

	def __init__(self, directory, master=None):
		Tk.Frame.__init__(self, master)
		self.master.title('MP3 Player')
		self.master.resizable(0, 0)

		self.model = Model(directory)

		self.init_mixer()

		self.main_frame = MainFrame(self)
		self.artwork = Artwork(self, self.main_frame.main_frame)
		self.seekbar = Seekbar(self, self.main_frame.main_frame)
		self.text_frame = TextFrame(self, self.main_frame.main_frame)
		self.buttons = Buttons(self, self.main_frame.main_frame)
		self.listbox = ScrollListBox(self, self.main_frame.main_frame)
		self.volume_window = VolumeWindow(self)

	def init_mixer(self):
		pygame.mixer.init()
		pygame.mixer.music.set_endevent(Controller.MUSIC_ENDED)

	def play(self):
		self.model.play()
		self.reset_seekbar()

	def play_next(self):
		self.model.play_next()
		self.reset_seekbar()

	def update_frame(self):
		current_song = self.model.get_current_song()
		artist = self.model.get_artist()
		album = self.model.get_album()
		self.text_frame.set_current(current_song, artist, album)

	def update_listbox(self):
		self.listbox.listbox_itself.selection_clear(0, len(self.model.song_list))
		self.listbox.listbox_itself.selection_set(self.model.current_song_index)

	def update_seekbar(self):
		sec = self.model.get_current_playing_position()
		self.seekbar.set_current_second(sec)

	def reset_seekbar(self):
		seekbar_length = self.model.convert_song_length()
		self.seekbar.reset_seekbar(seekbar_length)

	def mode_repeat(self):
		if not self.model.is_repeat:
			self.model.is_repeat = True
			self.model.is_shuffle = False
			self.buttons.mode_repeat()
		else:
			self.model.is_repeat = False
			self.buttons.mode_repeat_off()

	def mode_shuffle(self):
		if not self.model.is_shuffle:
			self.model.is_shuffle = True
			self.model.is_repeat = False
			self.buttons.mode_repeat_off()
			self.buttons.mode_shuffle()
		else:
			self.model.is_shuffle = False
			self.buttons.mode_shuffle_off()

	def play_pause_song(self, event):
		self.model.play_pause_song()
		if self.model.is_stopped:
			self.buttons.play()
		else:
			self.buttons.pause()

	def previous_song(self, event):
		self.model.previous_song()
		self.reset_seekbar()

	def next_song(self, event):
		self.model.next_song()
		self.reset_seekbar()

	def rewind_song(self, event):
		self.model.rewind_song()
		self.reset_seekbar()

	def on_enter(self):
		self.buttons.on_enter()

	def on_leave(self):
		self.text_frame.on_leave()

	def show_hide_listbox(self):
		self.listbox.show_hide_listbox()

	def get_song_list(self):
		return self.model.real_names

	def select_song(self, event):
		self.model.current_song_index, = self.listbox.listbox_itself.curselection()
		self.model.is_stopped = False
		self.model.play_selected_song()
		self.reset_seekbar()

	def control_volume(self):
		if self.volume_window.is_visible:
			self.volume_window.is_visible = False
		else:
			self.volume_window.is_visible = True
		self.volume_window.set_window_visible()

	def change_volume(self, event):
		current_volume = self.volume_window.volume.get() / 100
		self.model.change_volume(current_volume)

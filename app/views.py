import os

import tkinter as Tk

APP_DIR = os.path.abspath(os.path.dirname(__file__))
IMAGE_DIR = os.path.join(APP_DIR, '../images')

class MainFrame:
	def __init__(self, controller):
		self.controller = controller
		self.main_frame = Tk.Frame(self.controller)
		self.main_frame.pack()


class Artwork:
	def __init__(self, controller, parent):
		self.controller = controller
		self.parent = parent
		self.artwork_frame = Tk.Frame(self.parent)
		self.artwork_frame.pack()
		self.artwork_image = Tk.PhotoImage(file=IMAGE_DIR+'/artwork/artwork.gif')
		self.artwork_label = Tk.Label(self.artwork_frame, image=self.artwork_image)
		self.artwork_label.pack()


class Seekbar:
	def __init__(self, controller, parent):
		self.controller = controller
		self.parent = parent
		self.seekbar_frame = Tk.Frame(self.parent)
		self.seekbar_frame.pack()
		self.scale_label = Tk.Label(self.seekbar_frame, text='00:00')
		self.scale_label.grid(column=0, row=0)
		self.seekbar_itself = Tk.Scale(
			self.seekbar_frame,
			orient='h',
			showvalue=False,
			length=270,
			command=self.set_current_scale_position,
			)
		self.seekbar_itself.grid(column=1, row=0)

	def set_current_second(self, sec):
		self.seekbar_itself.set(sec)

	def set_current_scale_position(self, value):
		value = int(value)
		minutes = value / 60
		seconds = value % 60
		self.scale_label.configure(text='%2.2d:%2.2d' % (minutes, seconds))

	def reset_seekbar(self, length):
		self.seekbar_itself.configure(to=length)


class TextFrame:
	def __init__(self, controller, parent):
		self.controller = controller
		self.parent = parent
		self.text_frame = Tk.Frame(self.parent)
		self.text_frame.pack()
		self.controller.bind('<Enter>', self.on_enter)
		self.song_name = Tk.StringVar()
		self.song_label = Tk.Label(
			self.text_frame,
			textvariable=self.song_name,
			font=('Yo Gothic UI', 12, 'bold'),
			)
		self.song_label.pack()
		self.artist_album_label = Tk.Label(
			self.text_frame,
			text='',
			font=('Yo Gothic UI', 8, 'bold'))
		self.artist_album_label.pack()

	def set_current(self, song, artist, album):
		self.song_name.set(song)
		self.artist_album_label.configure(text="%s - %s" % (artist, album))

	def on_enter(self, event):
		self.parent.pack_propagate(False)
		self.text_frame.pack_forget()
		self.controller.on_enter()

	def on_leave(self):
		self.text_frame.pack()


class Buttons:
	def __init__(self, controller, parent):
		self.controller = controller
		self.parent = parent
		self.button_frame = Tk.Frame(self.parent)
		self.controller.bind('<Leave>', self.on_leave)

		self.volume_img = Tk.PhotoImage(file=IMAGE_DIR+'/buttons/volume.gif')
		self.volume_button = Tk.Button(
			self.button_frame, 
			image=self.volume_img , 
			relief=Tk.FLAT, 
			command=self.controller.control_volume
			)
		self.volume_button.pack(padx=5, pady=5, side=Tk.LEFT)

		self.shuffle_off_img = \
			Tk.PhotoImage(file=IMAGE_DIR+'/buttons/shuffle_off.gif')
		self.shuffle_img = Tk.PhotoImage(file=IMAGE_DIR+'/buttons/shuffle.gif')
		self.shuffle_button = Tk.Button(
			self.button_frame, 
			image=self.shuffle_off_img, 
			relief=Tk.FLAT, 
			command=self.controller.mode_shuffle
			)
		self.shuffle_button.pack(padx=5, pady=5, side=Tk.LEFT)

		self.back_img = Tk.PhotoImage(file=IMAGE_DIR+'/buttons/back.gif')
		self.previous_button = Tk.Button(
			self.button_frame, 
			image=self.back_img, 
			relief=Tk.FLAT
			)
		self.previous_button.pack(padx=5, pady=5, side=Tk.LEFT)

		self.play_img = Tk.PhotoImage(file=IMAGE_DIR+'/buttons/play.gif')
		self.pause_img = Tk.PhotoImage(file=IMAGE_DIR+'/buttons/pause.gif')
		self.play_pause_button = Tk.Button(
			self.button_frame, 
			image=self.pause_img, 
			relief=Tk.FLAT
			)
		self.play_pause_button.pack(padx=5, pady=5, side=Tk.LEFT)

		self.next_img = Tk.PhotoImage(file=IMAGE_DIR+'/buttons/next.gif')
		self.next_button = Tk.Button(
			self.button_frame, 
			image=self.next_img, 
			relief=Tk.FLAT
			)
		self.next_button.pack(padx=5, pady=5, side=Tk.LEFT)

		self.repeat_off_img = \
			Tk.PhotoImage(file=IMAGE_DIR+'/buttons/repeat_off.gif')
		self.repeat_img = Tk.PhotoImage(file=IMAGE_DIR+'/buttons/repeat.gif')
		self.repeat_button = Tk.Button(
			self.button_frame, 
			image=self.repeat_off_img , 
			relief=Tk.FLAT, 
			command=self.controller.mode_repeat
			)
		self.repeat_button.pack(padx=5, pady=5, side=Tk.LEFT)

		self.show_hide_img = Tk.PhotoImage(file=IMAGE_DIR+'/buttons/show_hide.gif')
		self.show_hide_button = Tk.Button(
			self.button_frame, 
			image=self.show_hide_img, 
			relief=Tk.FLAT, 
			command=self.controller.show_hide_listbox
			)
		self.show_hide_button.pack(padx=5, pady=5, side=Tk.LEFT)

		self.previous_button.bind('<Button-1>', self.controller.rewind_song)
		self.previous_button.bind('<Double-1>', self.controller.previous_song)
		self.play_pause_button.bind('<Button-1>', self.controller.play_pause_song)
		self.next_button.bind('<Button-1>', self.controller.next_song)

	def on_enter(self):
		self.button_frame.pack()

	def on_leave(self, event):
		self.button_frame.pack_forget()
		self.controller.on_leave()

	def mode_repeat(self):
		self.repeat_button.configure(image=self.repeat_img)

	def mode_repeat_off(self):
		self.repeat_button.configure(image=self.repeat_off_img)

	def mode_shuffle(self):
		self.shuffle_button.configure(image=self.shuffle_img)

	def mode_shuffle_off(self):
		self.shuffle_button.configure(image=self.shuffle_off_img)

	def play(self):
		self.play_pause_button.configure(image=self.play_img)

	def pause(self):
		self.play_pause_button.configure(image=self.pause_img)


class ScrollListBox:
	def __init__(self, controller, parent):
		self.controller = controller
		self.parent = parent
		self.listbox_frame = Tk.Frame(self.controller)
		self.listbox_frame.pack()
		self.yscroll = Tk.Scrollbar(self.listbox_frame, orient=Tk.VERTICAL)
		self.yscroll.pack(side=Tk.RIGHT, fill=Tk.Y, expand=1)
		self.listbox_itself = Tk.Listbox(
			self.listbox_frame,
			width=40,
			font=('Yu Gothic UI', 10, 'bold'),
			yscrollcommand=self.yscroll.set
			)
		self.yscroll.configure(command=self.listbox_itself.yview)
		self.listbox_itself.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)
		self.listbox_itself.bind("<<ListboxSelect>>", self.controller.select_song)
		self.is_listbox_shown = True

		self.set_song_list()

	def show_hide_listbox(self):
		if self.is_listbox_shown:
			self.parent.pack_propagate(True)
			self.listbox_frame.pack_forget()
			self.is_listbox_shown = False
		else:
			self.parent.pack_propagate(False)
			self.listbox_frame.pack()
			self.is_listbox_shown = True

	def set_song_list(self):
		song_list = self.controller.get_song_list()
		for song in reversed(song_list):
			self.listbox_itself.insert(0, song)


class VolumeWindow:
	def __init__(self, controller):
		self.controller = controller
		self.top = Tk.Toplevel(self.controller)
		self.volume_frame = Tk.Frame(self.top)
		self.volume_frame.pack()
		self.volume = Tk.IntVar()
		self.volume.set(50)
		self.volume_bar = Tk.Scale(
			self.volume_frame,
			orient='h',
			variable=self.volume,
			command=self.controller.change_volume,
			)
		self.volume_bar.pack()
		self.is_visible = False
		self.set_window_visible()

		# Set the event that is triggered when the window is closed
		self.top.protocol('WM_DELETE_WINDOW', self.volume_window_off)

	def volume_window_off(self):
		self.is_visible = False
		self.set_window_visible()

	def set_window_visible(self):
		if self.is_visible:
			self.top.deiconify()
		else:
			self.top.withdraw()

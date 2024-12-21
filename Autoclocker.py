from pynput.keyboard import Key, Listener, Controller
from pynput.mouse import Button, Controller as MouseCont
import time
import tkinter as tk
from threading import *
import csv
import datetime

keyboard = Controller()
mouse = MouseCont()
loopOn = False

sensitiveKey = '\\'

isSettingKeyNow = False

def sleepInterrupted(duration):
	global loopOn

	aTime = datetime.datetime.now() + datetime.timedelta(0, 0, 0, duration)

	while 0 <= (aTime - datetime.datetime.now()).total_seconds() and loopOn == True:
		time.sleep(0.01)

	return

def mainThread(chars, delay, type, dur):
	if type == "keyboard":
		while loopOn:
			#time.sleep(delay / 1000) 
			sleepInterrupted(delay)
			for char in chars:
				if loopOn:
					keyboard.press(char)
					#time.sleep(dur / 1000)
					sleepInterrupted(dur)
				keyboard.release(char)
	else:
		btn = Button.left

		if chars == "Left":
			btn = Button.left
		elif chars == "Right":
			btn = Button.right
		elif chars == "Middle":
			btn = Button.middle
		
		while loopOn:
			sleepInterrupted(delay)
			if loopOn:
				mouse.press(btn)
				sleepInterrupted(dur)
			mouse.release(btn)


if __name__ == "__main__":
	currentThread = Thread(target = mainThread, args = ("a", 1))

	root=tk.Tk()
	
	# setting the windows size
	root.geometry("300x296")

	name_var=tk.StringVar()
	passw_var=tk.StringVar()
	dur_var = tk.StringVar()
	keyField = tk.StringVar()
	variable = tk.StringVar(root)

	fields = []
	rows = []

	with open('user_settings.csv', 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		fields = next(csvreader)
		for row in csvreader:
			rows.append(row)

	passw_var.set(rows[1][1])
	dur_var.set(rows[3][1])
	name_var.set(rows[5][1])
	variable.set(rows[7][1])

	sensitiveKey = rows[9][1]
	keyField.set(sensitiveKey)

	v = tk.IntVar(root)
	v.set(1)

	v.set(rows[11][1])

	aType = tk.IntVar(root)
	aType.set(1)

	aType.set(rows[13][1])
	
	
	def StartLoop():
		global isSettingKeyNow
		if not isSettingKeyNow:
			root.focus_set()
			global loopOn
			global v
			global variable
			global currentThread

			if loopOn:
				loopOn = False

				#currentThread.join()
				sub_btn.config(text="Start")
			else:
				delay = float(passw_var.get())
				dur = float(dur_var.get())

				if v.get() == 1:
					chars = name_var.get()

					loopOn = True
					currentThread = Thread(target = mainThread, args = (chars, delay, "keyboard", dur))
					currentThread.start()
				else:
					chars = name_var.get()

					loopOn = True
					currentThread = Thread(target = mainThread, args = (variable.get(), delay, "mouse", dur))
					currentThread.start()
				sub_btn.config(text="Stop")
		
	def ReadKey():
		global isSettingKeyNow
		isSettingKeyNow = True
		root.focus_set()
		keyField.set("Press any key...")

	def RemoveKey():
		global isSettingKeyNow
		global sensitiveKey
		isSettingKeyNow = False
		sensitiveKey = ''
		keyField.set("")

	def on_press(key):
		global sensitiveKey
		global isSettingKeyNow

		try:
			if isSettingKeyNow:
				sensitiveKey = key.char
				keyField.set(sensitiveKey)
				isSettingKeyNow = False
			else:
				if key.char == sensitiveKey:
					if aType.get() == 1:
						StartLoop()
					else:
						global loopOn
						if not loopOn:
							StartLoop()


			
			return True
		except AttributeError as ex:
			pass
	
	def on_release(key):
		global sensitiveKey
		global isSettingKeyNow

		try:
			if not isSettingKeyNow:
				if key.char == sensitiveKey and aType.get() == 2:
					StartLoop()
			
			return True
		except AttributeError as ex:
			pass
	
	listener = Listener(on_press=on_press)
	listener.start()

	listener_release = Listener(on_release=on_release)
	listener_release.start()

	root.title("Autoclocker")

	smallFont = ('calibre',10,'normal')
	defaultFont = ('calibre',12, 'normal')
	boldFont = ('calibre',13, 'bold')

	# Input type frame
	input_frame = tk.LabelFrame(root, text="Input", font=boldFont, padx=10, pady=10)

	name_label = tk.Label(input_frame, text = 'Keys', font=defaultFont)
	name_entry = tk.Entry(input_frame,textvariable = name_var, font=smallFont, width=18)

	mouse_label = tk.Label(input_frame, text = 'Mouse', font=defaultFont)

	b1= tk.Radiobutton(input_frame, text='', variable=v, value=1)
	b2 = tk.Radiobutton(input_frame, text='', variable=v, value=2)

	options= ["Left", "Right", "Middle"]
	w = tk.OptionMenu(input_frame, variable, *options)
	w.config(width=15)
	
	# Delay settings frame
	delay_frame = tk.LabelFrame(root, text="Delay", font=boldFont, padx=1, pady=10)

	passw_label = tk.Label(delay_frame, text = 'Delay', font = defaultFont)
	passw1_label = tk.Label(delay_frame, text = 'ms', font = smallFont)
	passw_entry=tk.Entry(delay_frame, textvariable = passw_var, font = smallFont, width=18)

	d_label = tk.Label(delay_frame, text = 'Duration', font = defaultFont)
	d1_label = tk.Label(delay_frame, text = 'ms', font = smallFont)
	d_entry=tk.Entry(delay_frame, textvariable = dur_var, font = smallFont, width=18)

	# Activation settings frame
	activation_frame = tk.LabelFrame(root, text="Activation", font=boldFont, padx=5, pady=10)

	s_label = tk.Label(activation_frame, text = 'Trigger', font = defaultFont)
	s_btn=tk.Button(activation_frame,text = 'Set', command = ReadKey, width=5)
	srem_btn=tk.Button(activation_frame,text = 'Delete', command = RemoveKey, width=6)
	s_entry=tk.Entry(activation_frame, textvariable = keyField, font = smallFont, width=8)
	s_entry.configure(state='readonly')
	
	sub_btn=tk.Button(activation_frame,text = 'Start', command = StartLoop, width=8)

	radioHold = tk.Radiobutton(activation_frame, text='Hold', variable=aType, value=2, font=smallFont)
	radioPress = tk.Radiobutton(activation_frame, text='Press', variable=aType, value=1, font=smallFont)
	

	# Packing input frame
	input_frame.pack(padx=5, pady=0, fill="x")

	b1.grid(row=1,column=2,padx=(10,5))
	b2.grid(row=2,column=2,padx=(10,5))

	name_label.grid(row=1,column=0, padx=(10,5))
	name_entry.grid(row=1,column=1, padx=(10,5))
	mouse_label.grid(row=2, column=0, padx=(10,5))

	w.grid(row=2, column=1, padx=(10,5))

	# Packing delay frame
	delay_frame.pack(padx=5, pady=0, fill="x")

	passw_label.grid(row=1,column=0, padx=(10,5))
	passw_entry.grid(row=1,column=1, padx=(10,5))
	passw1_label.grid(row=1,column=2, padx=(10,5))

	d_label.grid(row=2,column=0, padx=(10,5))
	d_entry.grid(row=2,column=1, padx=(10,5))
	d1_label.grid(row=2,column=2, padx=(10,5))

	# Packing activation frame
	activation_frame.pack(padx=5, pady=0, fill="x")

	s_label.grid(row=0,column=0, padx=(10,5))
	s_entry.grid(row=0,column=1, padx=(15,5))
	s_btn.grid(row=0,column=2, padx=(8,5))
	srem_btn.grid(row=0,column=3, padx=(8,5))

	sub_btn.grid(row=1,column=0, pady=(5,0), padx=(3,0))

	radioHold.grid(row=1, column=2, pady=(5,0))
	radioPress.grid(row=1, column=1, pady=(5,0))

	root.resizable(False, False)

	root.iconbitmap("clocker.ico")
	
	root.mainloop() # Window infinite loop

	loopOn = False # Close all threads

	listener.stop()

	fields = ['type', 'val']

	# print(variable.get())

	rows = [['delay', passw_var.get()],
			['duration', dur_var.get()],
			['key', name_var.get()],
			['mouse', variable.get()],
			['sense', sensitiveKey],
			['mode', v.get()],
			['activation', aType.get()]]
	
	with open('user_settings.csv', 'w') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(fields)
		csvwriter.writerows(rows)
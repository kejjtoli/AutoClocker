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
			time.sleep(.5)
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
	root.geometry("590x210")
	
	# declaring string variable
	# for storing name and password

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
					StartLoop()
			
			return True
		except AttributeError as ex:
			pass
	
	listener = Listener(on_press=on_press)
	listener.start()

	# creating a label for 
	# name using widget Label

	b1= tk.Radiobutton(root, text='', variable=v, value=1)
	b2 = tk.Radiobutton(root, text='', variable=v, value=2)

	root.title("Autoclocker")

	main_label = tk.Label(root, text = 'Input Type:', font=('calibre',13, 'bold'))
	main_label1 = tk.Label(root, text = 'Timing:', font=('calibre',13, 'bold'))
	main_label2 = tk.Label(root, text = 'Run:', font=('calibre',13, 'bold'))

	name_label = tk.Label(root, text = 'Keys', font=('calibre',12, 'normal'))
	name_entry = tk.Entry(root,textvariable = name_var, font=('calibre',10,'normal'))

	mouse_label = tk.Label(root, text = 'Mouse', font=('calibre',12, 'normal'))
	
	spacer = tk.Frame(root, height=20)

	spacer1 = tk.Frame(root, height=20)

	spacer2 = tk.Frame(root, height=10)

	passw_label = tk.Label(root, text = 'Delay', font = ('calibre',12,'normal'))
	passw1_label = tk.Label(root, text = 'ms', font = ('calibre',10,'normal'))
	passw_entry=tk.Entry(root, textvariable = passw_var, font = ('calibre',10,'normal'))

	d_label = tk.Label(root, text = 'Duration', font = ('calibre',12,'normal'))
	d1_label = tk.Label(root, text = 'ms', font = ('calibre',10,'normal'))
	d_entry=tk.Entry(root, textvariable = dur_var, font = ('calibre',10,'normal'))

	s_label = tk.Label(root, text = 'Trigger Key', font = ('calibre',12,'normal'))
	s_btn=tk.Button(root,text = 'Set Key', command = ReadKey, width=8)
	srem_btn=tk.Button(root,text = 'Delete Key', command = RemoveKey, width=8)
	s_entry=tk.Entry(root, textvariable = keyField, font = ('calibre',10,'normal'))
	s_entry.configure(state='readonly')
	
	sub_btn=tk.Button(root,text = 'Start', command = StartLoop, width=20)

	options= ["Left", "Right", "Middle"]
	w = tk.OptionMenu(root, variable, *options)
	w.config(width=17)
	
	
	b1.grid(row=1,column=2)
	b2.grid(row=2,column=2)

	name_label.grid(row=1,column=0, padx=(10,5))
	name_entry.grid(row=1,column=1)
	mouse_label.grid(row=2, column=0, padx=(10,5))
	#mouse_entry.grid(row=1, column=1)
	passw_label.grid(row=1,column=3, padx=(0,5))
	passw_entry.grid(row=1,column=4)
	passw1_label.grid(row=1,column=5)

	d_label.grid(row=2,column=3, padx=(0,5))
	d_entry.grid(row=2,column=4)
	d1_label.grid(row=2,column=5)

	s_label.grid(row=7,column=0, padx=(10,5))
	s_entry.grid(row=7,column=1)
	s_btn.grid(row=7,column=2)
	srem_btn.grid(row=7,column=3, padx=5)

	sub_btn.grid(row=8,column=1, pady=10)
	w.grid(row=2, column=1)
	main_label.grid(row=0, column=1, pady=(10,5))
	main_label1.grid(row=0, column=4, pady=(10,5))
	main_label2.grid(row=6, column=1, pady=(10,5))

	root.resizable(False, False)

	root.iconbitmap("clocker.ico")
	
	# performing an infinite loop 
	# for the window to display
	root.mainloop()
	loopOn = False # Close all threads
	listener.stop()

	fields = ['type', 'val']

	print(variable.get())

	rows = [['delay', passw_var.get()],
			['duration', dur_var.get()],
			['key', name_var.get()],
			['mouse', variable.get()],
			['sense', sensitiveKey],
			['mode', v.get()]]
	
	with open('user_settings.csv', 'w') as csvfile:
		# creating a csv writer object
		csvwriter = csv.writer(csvfile)
		# writing the fields
		csvwriter.writerow(fields)
		# writing the data rows
		csvwriter.writerows(rows)
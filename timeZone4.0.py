from tkinter import *
import datetime
import pytz
from tkinter import messagebox

# timezone calculator app

root = Tk()
root.title('Timezone Calculator')
root.iconbitmap('ClockIcon.ico')
root.resizable(FALSE, FALSE)

availableZones = ['US-PAC', 'US-C', 'US-E', 'UK', 'SP', 'TH', 'PI', 'CN',
                  'AU-WA', 'AU-QLD', 'AU-NSW', 'AU-VIC']

timeZones = {'US-PAC': 'US/Pacific', 'US-C': 'US/Central', 'US-E': 'US/Eastern',
             'UK': 'GB', 'SP': 'Europe/Madrid', 'TH': 'Asia/Bangkok', 'PI': 'Asia/Manila',
             'CN': 'Asia/Shanghai', 'AU-WA': 'Australia/West', 'AU-QLD': 'Australia/Queensland',
             'AU-NSW': 'Australia/NSW', 'AU-VIC': 'Australia/Victoria'}

# Choose Timezone Label
choose_tz_label = Label(root, text='Timezone:  ')
choose_tz_label.grid(row=0, column=0, sticky=E)

# Timezone Dropdown selector
selectedTZ = StringVar()
selectedTZ.set(availableZones[0])
availableTZDropdown = OptionMenu(root, selectedTZ, *availableZones)
availableTZDropdown.grid(row=0, column=1)  # need to check format but works

# Current time Checkbox # 1 = check // 0 = off
currentTime = StringVar()
currentTime.set('0')
currentCheckbox = Checkbutton(root, text='Current Time', variable=currentTime)
currentCheckbox.grid(row=1, column=0)

# Target time checkbox and entry
targetTime = StringVar()
targetTime.set('0')
targetTimeCheckbox = Checkbutton(root, text='Target Time', variable=targetTime)
targetTimeCheckbox.grid(row=1, column=1)

# Target time H and M boxes
hour_label = Label(root, text='Hour:')
hour_label.grid(row=1, column=2, sticky=E)
target_hourBox = Entry(root, width=5)
target_hourBox.grid(row=1, column=3)

minute_label = Label(root, text='Minute:')
minute_label.grid(row=1, column=4)
target_minBox = Entry(root, width=5)
target_minBox.grid(row=1, column=5)

outputBox = Text(root, width=45)  # text box or entry box
outputBox.grid(row=6, column=0, columnspan=6)


# Help Button Functionality // Help text ideally stored as txt on users machine
def get_help():
    help_window = Toplevel()
    help_window.title('Help')
    help_window.iconbitmap('ClockIcon.ico')
    help_box = Text(help_window, width=70, height=30)

    help_txt = '''Welcome to the Help Page!
1) "Timezone"
This dropdown is used alongside the "TargetTime" function.
Choose a timezone you wish to base a time calculation from.

2) "Current Time"
Check this box and hit "GO!" to show a list of current
times.

3) "Target Time"
Check this box, enter a target time (hour and minute) 
and then hit GO!
This will show you times around the world relative to the 
timezone and target time you have chosen.

** Example Usage **
A client lives in China. They are free for a meeting at 16:00
Chinese Local time.
1. Choose CN (China) from the drop down list
2. Check target time box
3. Enter Hour = 16 and Minute = 00
4. Hit Go!

The output will give you relative times across the world to help 
coordinate your meeting!
'''

    help_box.grid(row=0, column=0)
    help_box.insert('end-1c', help_txt)
    help_box.configure(state=DISABLED)


# Help Button
help_button = Button(root, text='HELP', command=get_help)
help_button.grid(row=0, column=5)


def clear():
    outputBox.configure(state=NORMAL)
    outputBox.delete('1.0', 'end')
    outputBox.configure(state=DISABLED)


clearButton = Button(root, text='CLEAR', command=clear, bg='orange')
clearButton.grid(row=3, column=0)


def calc():
    outputBox.configure(state=NORMAL)
    if currentTime.get() == '1' and targetTime.get() == '0':
        outputBox.insert('end-1c', f'Current times are: \n\n')

        for tz in timeZones:
            adj_time = datetime.datetime.now(pytz.timezone(timeZones[tz]))
            str_adj_time = adj_time.strftime('%A, %H:%M')
            outputBox.insert('end-1c', f'{tz} = {str_adj_time}\n'.rjust(25))

    elif currentTime.get() == '0' and targetTime.get() == '1':
        try:
            current_tz = timeZones[selectedTZ.get()]
            current_py_tz = datetime.datetime.now(pytz.timezone(current_tz))
            str_current_py_tz = current_py_tz.strftime('%A, %H:%M')
            dt_current_obj = datetime.datetime.strptime(str_current_py_tz, '%A, %H:%M')
            target_hour = target_hourBox.get()
            target_min = target_minBox.get()
            str_specified_time = f'{str(target_hour)}:{str(target_min)}'
            specified_time = datetime.datetime.strptime(str_specified_time, '%H:%M')
            outputBox.insert('end-1c', f'Calculating based on target time:\n'
                                       f' {str_specified_time} in timezone {current_tz}\n\n')

            if specified_time < dt_current_obj is True:
                difference = dt_current_obj - specified_time  # issue here - fixed with == True
            else:
                difference = specified_time - dt_current_obj

            # Apply target hour relevant (difference) changes to TZ listed
            for tz in timeZones:
                adj_time = datetime.datetime.now(pytz.timezone(timeZones[tz])) + difference
                str_adj_time = adj_time.strftime('%A, %H:%M')
                outputBox.insert('end-1c', f'{tz} = {str_adj_time}\n'.rjust(25))
        except ValueError:
            messagebox.showinfo('Input Error', 'Please enter a valid hour (0-23) and minute (0-59)')

    elif currentTime.get() == '0' and targetTime.get() == '0':
        outputBox.insert('end-1c', 'Please choose an option\n')
        messagebox.showinfo('Input Error', 'Choose at least one option...')

    else:
        outputBox.insert('end-1c', 'Cannot select both at same time\n')
        messagebox.showinfo('Input Error', 'Cannot select both (current and target) at same time...')

    outputBox.insert('end-1c', '*' * 25 + '\n\n')
    outputBox.configure(state=DISABLED)


calcButton = Button(root, text='GO!', command=calc, bg='green')
calcButton.grid(row=3, column=2)

root.mainloop()

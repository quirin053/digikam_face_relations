import PySimpleGUI as sg
import people as pl

musterpeople = pl.People('dk_muster')
max_m = pl.Person(3, "Max Mustermann", 42)
sabine_m = pl.Person(5, "Sabine Mustermann", 23)
musterpeople.add_person(max_m)
musterpeople.add_person(sabine_m)
# Tab Appearances
tabAppearances_layout = [[sg.Text("Cutoff:"),sg.Input(default_text='5', key='-ACUTOFF-')],
                        [sg.Button('Draw All', key='-DRAWALL-')],
                        [sg.Combo([p.name for p in musterpeople], default_value=musterpeople.get_by_index(0).name, key='-ACOMBO-'),
                            sg.Button('Draw', key='-DRAWSELECTED-')]]

# Tab Connections
tabConnections_layout = [[sg.Text("Roots:"),sg.Input(default_text='10', key='-ROOTS-')],
                            [sg.Text("Leafs:"),sg.Input(default_text='10', key='-LEAFS-')],
                            [sg.Text("Cutoff:"),sg.Input(default_text='5', key='-CCUTOFF-')],
                            [sg.Checkbox('Graph Buttons', default=False, key='-GRAPHBUTTONS-')],
                            [sg.Button('All Connections', key='-ALLCONNECTIONS-')],
                            [sg.Combo([p.name for p in musterpeople], default_value=musterpeople.get_by_index(0).name, key='-CCOMBO-'),
                                sg.Button('Connections', key='-SELECTEDCONNECTIONS-')],
                            [sg.Text("Graph Depth:"),sg.Input(default_text='2',key='-GRAPHDEPTH-')]]

# Define the window's contents
layout = [[sg.TabGroup([[sg.Tab('Appearances', tabAppearances_layout),
                        sg.Tab('Connections', tabConnections_layout)]])],
            [sg.Button('Read')]]

# Create the window
window = sg.Window('Digikam Faces', layout)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    # Output a message to the window
    window['-OUTPUT-'].update('Hello ' + values['-CUTOFF-'] + "! Thanks for trying PySimpleGUI")

# Finish up by removing from the screen
window.close()
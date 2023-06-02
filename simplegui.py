import PySimpleGUI as sg

# Tab Appearances
tabAppearances_layout = [[sg.Text("Cutoff:"),sg.Input(key='-CUTOFF-')]]

# Tab Connections
tabConnections_layout = [[sg.Text("Roots:"),sg.Input(key='-ROOTS-')],
                            [sg.Text("Leafs:"),sg.Input(key='-LEAFS-')],
                            [sg.Text("Cutoff:"),sg.Input(key='-CUTOFF-')],
                            [sg.Text("Graph Size:"),sg.Input(key='-GRAPHSIZE-')],
                            [sg.Checkbox('Graph Buttons', default=False, key='-GRAPHBUTTONS-')]]

# Define the window's contents
layout = [[sg.TabGroup([[sg.Tab('Appearances', tabAppearances_layout), sg.Tab('Connections', tabConnections_layout)]])],
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
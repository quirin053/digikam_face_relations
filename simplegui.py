import PySimpleGUI as sg

class GUI:
    def __init__(self,people,actions):
        self.people = people
        self.actions = actions
        self.combovalues = [p.name for p in self.people]
        self.window = self.build_window()

    def build_window(self):

        # Tab Appearances
        tabAppearances_layout = [[sg.Text("Cutoff:"),sg.Input(default_text='5', key='-ACUTOFF-')],
                                [sg.Button('Draw All', key='-DRAWALL-')],
                                [sg.Combo(self.combovalues, default_value=self.combovalues[0], key='-ACOMBO-'),
                                    sg.Button('Draw', key='-DRAWSELECTED-')]]

        # Tab Connections
        tabConnections_layout = [[sg.Text("Roots:"),sg.Input(default_text='10', key='-ROOTS-')],
                                    [sg.Text("Leafs:"),sg.Input(default_text='10', key='-LEAFS-')],
                                    [sg.Text("Cutoff:"),sg.Input(default_text='5', key='-CCUTOFF-')],
                                    [sg.Checkbox('Graph Buttons', default=False, key='-GRAPHBUTTONS-')],
                                    [sg.Button('All Connections', key='-ALLCONNECTIONS-')],
                                    [sg.Combo(self.combovalues, default_value=self.combovalues[0], key='-CCOMBO-'),
                                        sg.Button('Connections', key='-SELECTEDCONNECTIONS-')],
                                    [sg.Text("Graph Depth:"),sg.Input(default_text='2',key='-GRAPHDEPTH-')]]

        # Define the window's contents
        layout = [[sg.TabGroup([[sg.Tab('Appearances', tabAppearances_layout),
                                sg.Tab('Connections', tabConnections_layout)]])]]

        # Create the window
        window = sg.Window('Digikam Faces', layout)
        return window

    def run(self):
        # Display and interact with the Window using an Event Loop
        while True:
            event, values = self.window.read()
            # See if user wants to quit or window was closed
            if event == sg.WINDOW_CLOSED:
                break
            elif event == '-DRAWALL-':
                self.actions['draw_all'](self.people,int(values['-ACUTOFF-']))
            elif event == '-DRAWSELECTED-':
                index = self.combovalues.index(values['-ACOMBO-'])
                id = self.people.get_by_index(index).id
                self.actions['draw_selected'](self.people,id,int(values['-ACUTOFF-']))
            elif event == '-ALLCONNECTIONS-':
                self.actions['draw_connections'](self.people,int(values['-ROOTS-']),int(values['-LEAFS-']),int(values['-CCUTOFF-']),values['-GRAPHBUTTONS-'])
            elif event == '-SELECTEDCONNECTIONS-':
                index = self.combovalues.index(values['-CCOMBO-'])
                root = self.people.get_by_index(index)
                self.actions['draw_selected_connections'](self.people,root,int(values['-GRAPHDEPTH-']),int(values['-CCUTOFF-']),values['-GRAPHBUTTONS-'])
            print(event, values)

        # Finish up by removing from the screen
        self.window.close()
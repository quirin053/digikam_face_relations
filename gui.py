import tkinter as tk
from tkinter import ttk

def build(Menschen,draw_all,draw_selected,ptags,draw_connections,draw_selected_connections):
    # GUI
    root = tk.Tk()
    root.title("Digikam Face Ralations")

    # Tabs
    tabControl = ttk.Notebook(root)
    tabAppearances = ttk.Frame(tabControl)
    tabConnections = ttk.Frame(tabControl)
    tabHistory = ttk.Frame(tabControl)
    tabControl.add(tabAppearances, text='Appearances')
    tabControl.add(tabConnections, text='Relations')
    tabControl.add(tabHistory, text='History')
    tabControl.pack(expand = 1, fill ="both")

    # Tab Appearances
    comboAppearances = ttk.Combobox(tabAppearances, values=[m.name for m in Menschen], state="readonly")
    comboAppearances.current(0)
    button_draw = tk.Button(tabAppearances, text="draw for selected")
    button_draw.bind("<Button-1>", lambda button: draw_selected(Menschen,Menschen.get_by_index(comboAppearances.current()).id,filter=int(cutoffAppearances.get())))
    button_drawall = tk.Button(tabAppearances, text="draw all")
    button_drawall.bind("<Button-1>", lambda button: draw_all(Menschen,int(cutoffAppearances.get())))
    cutoffAppearances = tk.Entry(tabAppearances)
    cutoffAppearances.insert(0, "5")
    cutoffLabelAppearances = tk.Label(tabAppearances, text="Cutoff:")

    cutoffLabelAppearances.grid(row=0, column=0)
    cutoffAppearances.grid(row=0, column=1)
    button_drawall.grid(row=1, column=0, columnspan=2)
    comboAppearances.grid(row=2, column=0, columnspan=2)
    button_draw.grid(row=3, column=0, columnspan=2)

    # Tab Connections
    comboConnections = ttk.Combobox(tabConnections, values=[m.name for m in Menschen], state="readonly")
    comboConnections.current(0)
    mainp = tk.Entry(tabConnections)
    mainp.insert(0, "10")
    mainpLabel = tk.Label(tabConnections, text="Roots:")
    secondp = tk.Entry(tabConnections)
    secondp.insert(0, "10")
    secondpLabel = tk.Label(tabConnections, text="Leafs:")
    cutoffConnections = tk.Entry(tabConnections)
    cutoffConnections.insert(0, "5")
    cutoffLabelConnections = tk.Label(tabConnections, text="Cutoff:")
    button_drawconnections = tk.Button(tabConnections, text="draw connections")
    show_buttons = tk.BooleanVar()
    cb_buttons = tk.Checkbutton(tabConnections, text="Graph Buttons", variable=show_buttons, onvalue=True, offvalue=False)
    button_drawconnections.bind("<Button-1>", lambda button: draw_connections(Menschen,int(mainp.get()),int(secondp.get()),int(cutoffConnections.get()),show_buttons.get()))
    entry_graphdepth = tk.Entry(tabConnections)
    entry_graphdepth.insert(0, "2")
    graphdepthLabel = tk.Label(tabConnections, text="Graph Depth:")
    button_connectionsSelected = tk.Button(tabConnections, text="connections for selected")
    button_connectionsSelected.bind("<Button-1>", lambda button: draw_selected_connections(Menschen,Menschen.get_by_index(comboConnections.current()),int(entry_graphdepth.get()),int(cutoffConnections.get()),show_buttons.get()))

    mainpLabel.grid(row=0, column=0)
    mainp.grid(row=0, column=1)
    secondpLabel.grid(row=1, column=0)
    secondp.grid(row=1, column=1)
    cutoffLabelConnections.grid(row=2, column=0)
    cutoffConnections.grid(row=2, column=1)
    cb_buttons.grid(row=3, column=0, columnspan=2)
    button_drawconnections.grid(row=4, column=0, columnspan=2)
    comboConnections.grid(row=5, column=0, columnspan=2)
    graphdepthLabel.grid(row=6, column=0)
    entry_graphdepth.grid(row=6, column=1)
    button_connectionsSelected.grid(row=7, column=0, columnspan=2)

    # Tab History
    constructionlabel = tk.Label(tabHistory, text="Under Construction")
    constructionlabel.pack()

    return root
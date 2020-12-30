# -*- coding: utf-8 -*

# TODO: Package this GUI
import tkinter.filedialog
import Tkinter as tk
import ttk
import ruamel_yaml as yaml
import insertCode as inCd
import logging
import os
import csv

root = tk.Tk()
root.title('TensorFI')
root.geometry('890x700')

main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=1)

my_canvas = tk.Canvas(main_frame)
my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

my_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=tk.RIGHT,fill=tk.Y)

my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion= my_canvas.bbox("all")))

second_frame = tk.Frame(my_canvas)
my_canvas.create_window((0,0), window=second_frame, anchor='nw')

# Global variable
opsList = []
insList = []

# Code to add widgets

# Generate default.yaml file
def generateYaml():
    seed = seedEntry.get()
    scalarFaultType = scalarCombo.get()
    tensorFaultType = tensorCombo.get()
    skipCount = skipEntry.get()
    injectMode = injectCombo.get()

    paramsDict = {'ScalarFaultType': 'None', 'TensorFaultType': 'bitFlip-element', 'Ops': None,
              'Instances': None, 'InjectMode': 'errorRate'}
    paramsDict['ScalarFaultType'] = scalarFaultType
    paramsDict['TensorFaultType'] = tensorFaultType
    paramsDict['InjectMode'] = injectMode
    if opsList != []:
        paramsDict['Ops'] = opsList
    if insList != []:
        paramsDict['Instances'] = insList
    if seed != '':
        paramsDict['Seed'] = int(seed)
    if skipCount != '':
        paramsDict['SkipCount'] = int(skipCount)

    with open('testGen.yaml', 'w') as f:
        data = yaml.dump(paramsDict, f, Dumper=yaml.RoundTripDumper)

    geneLabel1 = tk.Label(second_frame, text='Successfully generated!')
    geneLabel1.grid(row=9, column=5)
    geneLabel1.after(1000, geneLabel1.destroy)

def addOp():
    if modeCombo2.get() == 'Single':
        opsEle = opsCombo.get() + ' = ' + opsEntry.get()
        opsList.append(opsEle)

    else:
        opsEle = opsCombo.get()

    opsLabel1 = tk.Label(second_frame, text='Successfully added!')
    opsLabel1.grid(row=7, column=5)
    opsLabel1.after(1000, opsLabel1.destroy)

def addIns():
    insEle = insCombo.get() + ' = ' + insEntry.get()
    insList.append(insEle)
    insLabel1 = tk.Label(second_frame, text='Successfully added!')
    insLabel1.grid(row=8, column=5)
    insLabel1.after(1000, insLabel1.destroy)

# ------------------------
# Callback function

def on_trace_choice(name, index, mode):
    refresh()

def refresh( ):
    choice = injectCombo.get()
    if choice == 'errorRate':
        opsCombo.configure(state="normal")
        opsEntry.config(state='normal')
        opButt.config(state='normal')
        insCombo.configure(state="disabled")
        insEntry.config(state='disabled')
        insButt.config(state='disabled')
        if modeCombo2.get() == 'Multiple':
            opsEntry2.config(state="normal")
            opsEntry3.config(state="normal")
        else:
            opsEntry2.config(state="disabled")
            opsEntry3.config(state="disabled")
    else:
        opsCombo.configure(state="disabled")
        opsEntry.config(state='disabled')
        opsEntry2.config(state='disabled')
        opsEntry3.config(state='disabled')
        opButt.config(state='disabled')
        insCombo.config(state='normal')
        insEntry.config(state='normal')
        insButt.config(state='normal')

#--------------
# Parameters Part
#Labels
# FIXME: How to align  'Parameters' with 'ScalarFaultType' - Beautify the GUI
paraTitlelabel = tk.Label(second_frame, text="YAML File Parameters", font = ('Times New Roman', 12, 'bold')).grid(row=0, column=0, padx = 5, pady = 25, sticky = 'w')


injectLabel = tk.Label(second_frame, font = ("Times New Roman", 10), text="InjectMode: ")\
                    .grid(row = 5, column = 0, padx = 5, pady = 5, sticky = 'w')
modeLabel = tk.Label(second_frame, font = ("Times New Roman", 10), text="Mode: ")\
                    .grid(row = 5, column = 2, padx = 5, pady = 5, sticky = 'w')
scalarLabel = tk.Label(second_frame, font = ("Times New Roman", 10), text="ScalarFaultType: ")\
                    .grid(row = 6, column = 0, padx = 5, pady = 5, sticky = 'w')
tensorLabel = tk.Label(second_frame, font = ("Times New Roman", 10), text="TensorFaultType: ")\
                    .grid(row = 6, column = 2, padx = 5, pady = 5, sticky = 'w')
opsLabel = tk.Label(second_frame, font = ("Times New Roman", 10), text="Ops: ")\
                    .grid(row = 7, column = 0, padx = 5, pady = 5, sticky = 'w')
ProbLabel = tk.Label(second_frame, font = ("Times New Roman", 10), text="Probability: ")\
                    .grid(row = 7, column = 2, padx = 5, pady = 5, sticky = 'w')
# ops2Label = tk.Label(second_frame, font = ("Times New Roman", 10), text=": ")\
#                     .grid(row = 7, column = 4)
# ops3Label = tk.Label(second_frame, font = ("Times New Roman", 10), text=": ")\
#                     .grid(row = 7, column = 5, sticky = 'w')
insLabel = tk.Label(second_frame, font = ("Times New Roman", 10), text="Instances: ")\
                    .grid(row = 8, column = 0, padx = 5, pady = 5, sticky = 'w')
numLabel = tk.Label(second_frame, font = ("Times New Roman", 10), text="Number: ")\
                    .grid(row = 8, column = 2, padx = 5, pady = 5, sticky = 'w')
seedLabel = tk.Label(second_frame, font = ("Times New Roman", 10), text="Seed: ")\
                    .grid(row = 9, column = 0, padx = 5, pady = 5, sticky = 'w')
skipLabel = tk.Label(second_frame, font = ("Times New Roman", 10), text="SkipCount: ")\
                    .grid(row = 9, column = 2, padx = 5, pady = 5, sticky = 'w')

# Combobox
choiceVar = tk.StringVar()
injectCombo = ttk.Combobox(second_frame, width = 15, font = ("Times New Roman", 10), textvariable=choiceVar, values=['errorRate', 'dynamicInstance', 'oneFaultPerRun'])
injectCombo.grid(row=5, column=1, sticky = 'w')
injectCombo.current(0)
choiceVar.trace("w", on_trace_choice)

choiceVar2 = tk.StringVar()
modeCombo2 = ttk.Combobox(second_frame, width = 15, font = ("Times New Roman", 10), textvariable=choiceVar2, values=['Single', 'Multiple'])
modeCombo2.grid(row=5, column=3, sticky = 'w')
modeCombo2.current(0)
choiceVar2.trace("w", on_trace_choice)


scalarCombo = ttk.Combobox(second_frame, width = 15, font = ("Times New Roman", 10), values=['None', 'Rand', 'Zero', 'Rand-element', 'bitFlip-element', 'bitFlip-tensor'])
scalarCombo.grid(row=6, column=1, sticky = 'w')
scalarCombo.current(0)

tensorCombo = ttk.Combobox(second_frame, width = 15, font = ("Times New Roman", 10), values=['None', 'Rand', 'Zero', 'Rand-element', 'bitFlip-element', 'bitFlip-tensor'])
tensorCombo.grid(row=6, column=3, sticky = 'w')
tensorCombo.current(4)

opsCombo = ttk.Combobox(second_frame, width = 15, font = ("Times New Roman", 10), values=['ABSOLUTE', 'ADD', 'ASSIGN', 'ALL', 'ARGMAX', 'ARGMIN', 'BIASADD', 'CAST', 'COUNT-NONZERO', 'CONV2D', 'ELU', 'END', 'EQUAL', 'EXPAND-DIMS',
                                                                        'FILL', 'FLOOR-MOD', 'GREATER-EQUAL', 'IDENTITY', 'LESS-EQUAL', 'LOG', 'LRN', 'MATMUL', 'MAX-POOL', 'MEAN', 'MINIMUM', 'MUL', 'NEGATIVE', 'NOT-EQUAL', 'NOOP',
                                                                        'ONE-HOT', 'PACK', 'POW', 'RANDOM_UNIFORM', 'RANK', 'RANGE', 'REALDIV', 'RELU', 'RESHAPE', 'RSQRT', 'SIGMOID', 'SIZE', 'SHAPE', 'SOFT-MAX', 'SQUARE', 'STRIDED-SLICE',
                                                                        'SUB',  'SUM', 'SWITCH', 'TANH', 'UNPACK'])
opsCombo.grid(row=7, column=1, sticky = 'w')
opsCombo.current(0)

insCombo = ttk.Combobox(second_frame, width = 15, font = ("Times New Roman", 10), values=['ABSOLUTE', 'ADD', 'ASSIGN', 'ALL', 'ARGMAX', 'ARGMIN', 'BIASADD', 'CAST', 'COUNT-NONZERO', 'CONV2D', 'ELU', 'END', 'EQUAL', 'EXPAND-DIMS',
                                                                        'FILL', 'FLOOR-MOD', 'GREATER-EQUAL', 'IDENTITY', 'LESS-EQUAL', 'LOG', 'LRN', 'MATMUL', 'MAX-POOL', 'MEAN', 'MINIMUM', 'MUL', 'NEGATIVE', 'NOT-EQUAL', 'NOOP',
                                                                        'ONE-HOT', 'PACK', 'POW', 'RANDOM_UNIFORM', 'RANK', 'RANGE', 'REALDIV', 'RELU', 'RESHAPE', 'RSQRT', 'SIGMOID', 'SIZE', 'SHAPE', 'SOFT-MAX', 'SQUARE', 'STRIDED-SLICE',
                                                                        'SUB',  'SUM', 'SWITCH', 'TANH', 'UNPACK'], state="disabled")
insCombo.grid(row=8, column=1, sticky = 'w')
insCombo.current(0)


# Entry - Enter the value
opsEntry = tk.Entry(second_frame, bd=3, width = 5)
opsEntry.grid(row=7, column = 3, sticky = 'w')
opsEntry2 = tk.Entry(second_frame, bd=3, width = 5, state="disabled")
opsEntry2.grid(row=7, column = 3)
opsEntry3 = tk.Entry(second_frame, bd=3,width = 5, state="disabled")
opsEntry3.grid(row=7, column = 3, sticky = 'e')
opsEntry.focus()
insEntry = tk.Entry(second_frame,width = 8, bd=5, state="disabled")
insEntry.grid(row=8, column = 3, sticky = 'w')
seedText = tk.StringVar()
seedEntry = tk.Entry(second_frame,width = 8, bd=3,textvariable=seedText)
seedEntry.grid(row=9, column=1, sticky = 'w')
seedText.set(100000)
skipText = tk.StringVar()
skipEntry = tk.Entry(second_frame,width = 8,bd=3,textvariable=skipText)
skipEntry.grid(row=9, column=3, sticky = 'w')
skipText.set(1)

# Button - Click to generate default.yaml file
opButt = tk.Button(second_frame, font = ("Times New Roman", 10),text="Add", command=addOp)
opButt.grid(row=7, column=4)
insButt = tk.Button(second_frame, font = ("Times New Roman", 10),text="Add", command=addIns, state="disabled")
insButt.grid(row=8, column=4)
geneButt = tk.Button(second_frame, font = ("Times New Roman", 10),text="Generate", command=generateYaml).grid(row=9, column=4)



#------------------------
# Fault injection
emptyTuple = ()
# BrowseFiles
def browseFiles():
    filename = tkinter.filedialog.askopenfilename(initialdir=os.path.dirname(os.path.abspath(__file__)),
                                          title="Select a File",
                                          filetypes=(("Python files",
                                                      "*.py*"),))
    global sourcefile
    if filename != '':
        sourcefile = filename

    if filename == emptyTuple:
        fileButt.configure(text="Select")
    else:
        head, tail = os.path.split(sourcefile)
        fileButt.configure(text=tail)

def browseConfFiles():
    filename = tkinter.filedialog.askopenfilename(initialdir=os.path.dirname(os.path.abspath(__file__)),
                                                  title="Select a File",
                                                  filetypes=(("YAML files",
                                                              "*.yaml*"),))
    global confile
    if filename != '':
        confile = filename

    if filename == emptyTuple:
        fileConfButt.configure(text="Select")
    else:
        head, tail = os.path.split(confile)
        fileConfButt.configure(text=tail)

def browseLogDir():
    dirname = tkinter.filedialog.askdirectory()
    global dirpath
    if dirname != '':
        dirpath = dirname
    if dirname == emptyTuple:
        logdButt.configure(text="Select")
    else:
        head, tail = os.path.split(dirpath)
        logdButt.configure(text=tail)



#TODO: Add exceptions
def injectFaults():
    # filename = fileButt.cget('text')
    # parse_src_import = inCd.addImport(filename)
    # loglValue = eval(loglCombo.get())
    # if modeCombo.get()=='Run':
    #     loglValue = 0

    # FIXME:
    # parse_src_fi = addFi(parse_src_import, 'correct_prediction', {'x': 'X_test', 'y': 'y_test'}, 'lenet-sdcrates.csv',
    #                      10, 'X_test', 'y_test',
                         # 'testGen.yaml', "faultLogs/", logging.DEBUG, 'False', 'convolutional', 'fi_')

    # parse_src_fi = inCd.addFi(parse_src_import, correPreEntry.get(), Dict, 'sdcRates.csv',int(numFIEntry.get()), testXEntry.get(), testYEntry.get(), confile, dirpath, loglValue, disCombo.get(), nameEntry.get(), fipEntry.get())

    # Execute the parsed code
    # exec(compile(parse_src_fi, filename="<ast>", mode="exec"), globals())
    with open('sdcRates.csv', 'r') as csvfile:
        # creating a csv reader object
        csvreader = csv.reader(csvfile)
        sdc = ''
        for row in csvreader:
            for col in row:
                print(col)
                sdc = col
    sdcOnceLabel.configure(text = 'SDC rates: '+sdc)


#-------
# Callback function
def on_trace_mode(name, index, mode):
    refresh_mode()
def refresh_mode( ):
    mode = modeCombo.get()
    if mode == 'Run':
        loglLabel.grid_forget()
        loglCombo.grid_forget()
        namelabel.grid_forget()
        nameEntry.grid_forget()
        fiplabel.grid_forget()
        fipEntry.grid_forget()
    else:
        loglLabel.grid(row=13, column = 2, padx = 5, pady = 5, sticky = 'w')
        loglCombo.grid(row=13, column = 3, padx = 5, pady = 5, sticky = 'w')
        namelabel.grid(row=14, column = 0, padx = 5, pady = 5, sticky = 'w')
        nameEntry.grid(row=14, column = 1, padx = 5, pady = 5, sticky = 'w')
        fiplabel.grid(row=14, column = 2, padx = 5, pady = 5, sticky = 'w')
        fipEntry.grid(row=14, column = 3, padx = 5, pady = 5, sticky = 'w')


# Label
fiTitleLabel = tk.Label(second_frame, text="Fault injection", font = ('Times New Roman', 12, 'bold')).grid(row=10, column=0, padx = 5, pady = 25, sticky = 'w')
sourLabel = tk.Label(second_frame, text="Source file: ", font = ("Times New Roman", 10)).grid(row = 11, column = 0, padx = 5, pady = 5, sticky = 'w')
confLabel = tk.Label(second_frame, text="configFileName:", font = ("Times New Roman", 10)).grid(row=11, column = 2, padx = 5, pady = 5, sticky = 'w')
logdLabel = tk.Label(second_frame, text="logDir:", font = ("Times New Roman", 10)).grid(row=12, column = 0, padx = 5, pady = 5, sticky = 'w')
disLabel = tk.Label(second_frame, text="disableInjections:", font = ("Times New Roman", 10)).grid(row=12, column = 2, padx = 5, pady = 5, sticky = 'w')
modeLabel = tk.Label(second_frame, text="Mode:", font = ("Times New Roman", 10)).grid(row=13, column = 0, padx = 5, pady = 5, sticky = 'w')
# Debugging mode
loglLabel = tk.Label(second_frame, text="logLevel:", font = ("Times New Roman", 10))
# loglLabel.grid(row=13, column=10, padx = 10, pady = 25)
namelabel = tk.Label(second_frame, text="name:", font = ("Times New Roman", 10))
# namelabel.grid(row=14, column=0, padx = 10, pady = 25)
fiplabel = tk.Label(second_frame, text="fiPrefix:", font = ("Times New Roman", 10))
# fiplabel.grid(row=14, column=10, padx = 10, pady = 25)

# Combobox
disCombo = ttk.Combobox(second_frame, font = ("Times New Roman", 10), values=['False', 'True'], width = 8)
disCombo.grid(row=12, column = 3, padx = 5, pady = 5, sticky = 'w')
disCombo.current(0)

modeVar = tk.StringVar()
modeCombo = ttk.Combobox(second_frame, font = ("Times New Roman", 10), textvariable=modeVar, values=['Run', 'Debug'], width = 8)
modeCombo.grid(row=13, column = 1, padx = 5, pady = 5, sticky = 'w')
modeCombo.current(0)
modeVar.trace("w", on_trace_mode)

# Default to be 0
loglCombo = ttk.Combobox(second_frame, font = ("Times New Roman", 10), values=[10, 20, 30], width = 8)
# loglCombo.grid(row=13, column=15)
loglCombo.current(0)

# Entry
nameEntry = tk.Entry(second_frame,bd=3, width = 8)
# nameEntry.grid(row=14, column=5)
fipEntry = tk.Entry(second_frame,bd=3, width = 8)
# fipEntry.grid(row=14, column=15)

# Button
fileButt = tk.Button(second_frame, font = ("Times New Roman", 10),text="Select", command=browseFiles)
fileButt.grid(row=11, column = 1, padx = 5, pady = 5, sticky = 'w')
fileConfButt = tk.Button(second_frame, font = ("Times New Roman", 10),text="Select", command=browseConfFiles)
fileConfButt.grid(row=11, column = 3, padx = 5, pady = 5, sticky = 'w')
logdButt = tk.Button(second_frame, font = ("Times New Roman", 10),text="Select", command=browseLogDir)
logdButt.grid(row=12, column = 1, padx = 5, pady = 5, sticky = 'w')

# -------------------------------
# Statistics setting

# Generate feed_dict
Dict = {}
def addDict():
    key = feedKeyEntry.get()
    value = feedValEntry.get()
    Dict[key] = value
    feedLabel1 = tk.Label(second_frame, text='Successfully added!')
    feedLabel1.grid(row=17, column=20)
    feedLabel1.after(1000, feedLabel1.destroy)


# Label
staTitleLabel = tk.Label(second_frame, text="Statistics settings", font = ('Times New Roman', 12, 'bold')).grid(row=15, column=0, padx = 5, pady = 25, sticky = 'w')
corrPreLabel = tk.Label(second_frame, text="Correct Prediction: ", font = ("Times New Roman", 10)).grid(row=16, column = 0, padx = 5, pady = 5, sticky = 'w')
numFILabel = tk.Label(second_frame, text="Number of injections: ", font = ("Times New Roman", 10)).grid(row=16, column = 2, padx = 5, pady = 5, sticky = 'w')
feedKeyLabel = tk.Label(second_frame, text="Feed key: ", font = ("Times New Roman", 10))
feedKeyLabel.grid(row=17, column = 0, padx = 5, pady = 5, sticky = 'w')
feedValLabel = tk.Label(second_frame, text="Feed value: ", font = ("Times New Roman", 10))
feedValLabel.grid(row=17, column = 2, padx = 5, pady = 5, sticky = 'w')
testXLabel = tk.Label(second_frame, text="Test set (X): ", font = ("Times New Roman", 10))
testXLabel.grid(row=18, column = 0, padx = 5, pady = 5, sticky = 'w')
testYLabel = tk.Label(second_frame, text="Test set (Y): ", font = ("Times New Roman", 10))
testYLabel.grid(row=18, column = 2, padx = 5, pady = 5, sticky = 'w')

# Entry
correPreEntry = tk.Entry(second_frame,bd=3, width = 15)
correPreEntry.grid(row=16, column = 1, padx = 5, pady = 5, sticky = 'w')
numFIEntry = tk.Entry(second_frame,bd=3, width = 15)
numFIEntry.grid(row=16, column = 3, padx = 5, pady = 5, sticky = 'w')
feedKeyEntry = tk.Entry(second_frame,bd=3, width = 15)
feedKeyEntry.grid(row=17, column = 1, padx = 5, pady = 5, sticky = 'w')
feedValEntry = tk.Entry(second_frame,bd=3, width = 15)
feedValEntry.grid(row=17, column = 3, padx = 5, pady = 5, sticky = 'w')
testXEntry = tk.Entry(second_frame,bd=3, width = 15)
testXEntry.grid(row=18, column = 1, padx = 5, pady = 5, sticky = 'w')
testYEntry = tk.Entry(second_frame,bd=3, width = 15)
testYEntry.grid(row=18, column = 3, padx = 5, pady = 5, sticky = 'w')

# Button
feedDicButt = tk.Button(second_frame, font = ("Times New Roman", 10),text="Add", command=addDict)
feedDicButt.grid(row=17, column = 4, padx = 5, pady = 5, sticky = 'w')
# feeButt = tk.Button(second_frame, font = ("Times New Roman", 10),text="Print", command=printt)
# feeButt.grid(row=18, column=0)
fiButt = tk.Button(second_frame, font = ("Times New Roman", 10),text="Inject", command=injectFaults)
fiButt.grid(row=18, column = 4, padx = 5, pady = 5, sticky = 'w')

#-----------------
# Results
resTitleLabel = tk.Label(second_frame, text="Results", font = ('Times New Roman', 12, 'bold')).grid(row=19, column = 0, padx = 5, pady = 25, sticky = 'w')
sdcOnceLabel = tk.Label(second_frame, text="SDC rates: ", font=('Times New Roman', 10))
sdcOnceLabel.grid(row=20, column = 0, padx = 5, pady = 5, sticky = 'w')


root.mainloop()
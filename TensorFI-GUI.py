# -*- coding: utf-8 -*

# TODO: Package this GUI
import tkinter.filedialog
import Tkinter as tk
import ttk
import ruamel_yaml as yaml
import insertCode as inCd
import logging
import os


root = tk.Tk()
root.title('TensorFI')
root.geometry('850x700')

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
    geneLabel1.grid(row=9, column=20)
    geneLabel1.after(1000, geneLabel1.destroy)

def addOp():
    opsEle = opsCombo.get() + ' = ' + opsEntry.get()
    opsList.append(opsEle)
    opsLabel1 = tk.Label(second_frame, text='Successfully added!')
    opsLabel1.grid(row=6, column=25)
    opsLabel1.after(1000, opsLabel1.destroy)

def addIns():
    insEle = insCombo.get() + ' = ' + insEntry.get()
    insList.append(insEle)
    insLabel1 = tk.Label(second_frame, text='Successfully added!')
    insLabel1.grid(row=6, column=25)
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
    else:
        opsCombo.configure(state="disabled")
        opsEntry.config(state='disabled')
        opButt.config(state='disabled')
        insCombo.config(state='normal')
        insEntry.config(state='normal')
        insButt.config(state='normal')

#--------------
# Parameters Part
#Labels
# FIXME: How to align  'Parameters' with 'ScalarFaultType' - Beautify the GUI
paraTitlelabel = tk.Label(second_frame, text="YAML File Parameters", font = ("Times New Roman", 10)).grid(row=0, column=0)


injectLabel = tk.Label(second_frame, font = ("Times New Roman", 10), text="InjectMode: ")\
                    .grid(row = 5, column = 0, padx = 10, pady = 25)
scalarLabel = tk.Label(second_frame, font = ("Times New Roman", 10), text="ScalarFaultType: ")\
                    .grid(row = 6, column = 0, padx = 10, pady = 25)
tensorLabel = tk.Label(second_frame, font = ("Times New Roman", 10), text="TensorFaultType: ")\
                    .grid(row = 6, column = 10, padx = 10, pady = 25)
opsLabel = tk.Label(second_frame, font = ("Times New Roman", 10), text="Ops: ")\
                    .grid(row = 7, column = 0, padx = 10, pady = 25)
ProbLabel = tk.Label(second_frame, font = ("Times New Roman", 10), text="Probability: ")\
                    .grid(row = 7, column = 10, padx = 10, pady = 25)
insLabel = tk.Label(second_frame, font = ("Times New Roman", 10), text="Instances: ")\
                    .grid(row = 8, column = 0, padx = 10, pady = 25)
numLabel = tk.Label(second_frame, font = ("Times New Roman", 10), text="Number: ")\
                    .grid(row = 8, column = 10, padx = 10, pady = 25)
seedLabel = tk.Label(second_frame, font = ("Times New Roman", 10), text="Seed: ")\
                    .grid(row = 9, column = 0, padx = 10, pady = 25)
skipLabel = tk.Label(second_frame, font = ("Times New Roman", 10), text="SkipCount: ")\
                    .grid(row = 9, column = 10, padx = 10, pady = 25)

# Combobox
choiceVar = tk.StringVar()
injectCombo = ttk.Combobox(second_frame, font = ("Times New Roman", 10), textvariable=choiceVar, values=['errorRate', 'dynamicInstance', 'oneFaultPerRun'])
injectCombo.grid(row=5, column=5)
injectCombo.current(0)
choiceVar.trace("w", on_trace_choice)

scalarCombo = ttk.Combobox(second_frame, font = ("Times New Roman", 10), values=['None', 'Rand', 'Zero', 'Rand-element', 'bitFlip-element', 'bitFlip-tensor'])
scalarCombo.grid(row=6, column=5)
scalarCombo.current(0)

tensorCombo = ttk.Combobox(second_frame, font = ("Times New Roman", 10), values=['None', 'Rand', 'Zero', 'Rand-element', 'bitFlip-element', 'bitFlip-tensor'])
tensorCombo.grid(row=6, column=15)
tensorCombo.current(4)

opsCombo = ttk.Combobox(second_frame, font = ("Times New Roman", 10), values=['ABSOLUTE', 'ADD', 'ASSIGN', 'ALL', 'ARGMAX', 'ARGMIN', 'BIASADD', 'CAST', 'COUNT-NONZERO', 'CONV2D', 'ELU', 'END', 'EQUAL', 'EXPAND-DIMS',
                                                                        'FILL', 'FLOOR-MOD', 'GREATER-EQUAL', 'IDENTITY', 'LESS-EQUAL', 'LOG', 'LRN', 'MATMUL', 'MAX-POOL', 'MEAN', 'MINIMUM', 'MUL', 'NEGATIVE', 'NOT-EQUAL', 'NOOP',
                                                                        'ONE-HOT', 'PACK', 'POW', 'RANDOM_UNIFORM', 'RANK', 'RANGE', 'REALDIV', 'RELU', 'RESHAPE', 'RSQRT', 'SIGMOID', 'SIZE', 'SHAPE', 'SOFT-MAX', 'SQUARE', 'STRIDED-SLICE',
                                                                        'SUB',  'SUM', 'SWITCH', 'TANH', 'UNPACK'])
opsCombo.grid(row=7, column=5)
opsCombo.current(0)

insCombo = ttk.Combobox(second_frame, font = ("Times New Roman", 10), values=['ABSOLUTE', 'ADD', 'ASSIGN', 'ALL', 'ARGMAX', 'ARGMIN', 'BIASADD', 'CAST', 'COUNT-NONZERO', 'CONV2D', 'ELU', 'END', 'EQUAL', 'EXPAND-DIMS',
                                                                        'FILL', 'FLOOR-MOD', 'GREATER-EQUAL', 'IDENTITY', 'LESS-EQUAL', 'LOG', 'LRN', 'MATMUL', 'MAX-POOL', 'MEAN', 'MINIMUM', 'MUL', 'NEGATIVE', 'NOT-EQUAL', 'NOOP',
                                                                        'ONE-HOT', 'PACK', 'POW', 'RANDOM_UNIFORM', 'RANK', 'RANGE', 'REALDIV', 'RELU', 'RESHAPE', 'RSQRT', 'SIGMOID', 'SIZE', 'SHAPE', 'SOFT-MAX', 'SQUARE', 'STRIDED-SLICE',
                                                                        'SUB',  'SUM', 'SWITCH', 'TANH', 'UNPACK'], state="disabled")
insCombo.grid(row=8, column=5)
insCombo.current(0)


# Entry - Enter the value
opsEntry = tk.Entry(second_frame, bd=5)
opsEntry.grid(row=7, column = 15)
opsEntry.focus()
insEntry = tk.Entry(second_frame, bd=5, state="disabled")
insEntry.grid(row=8, column = 15)
seedText = tk.StringVar()
seedEntry = tk.Entry(second_frame,bd=3,textvariable=seedText)
seedEntry.grid(row=9, column=5)
seedText.set(100000)
skipText = tk.StringVar()
skipEntry = tk.Entry(second_frame,bd=3,textvariable=skipText)
skipEntry.grid(row=9, column=15)
skipText.set(1)

# Button - Click to generate default.yaml file
opButt = tk.Button(second_frame, font = ("Times New Roman", 10),text="Add operation", command=addOp)
opButt.grid(row=7, column=20)
insButt = tk.Button(second_frame, font = ("Times New Roman", 10),text="Add instance", command=addIns, state="disabled")
insButt.grid(row=8, column=20)
geneButt = tk.Button(second_frame, font = ("Times New Roman", 10),text="Generate", command=generateYaml).grid(row=9, column=20)

#------------------------
# Fault injection
emptyTuple = ()
# BrowseFiles
def browseFiles():
    filename = tkinter.filedialog.askopenfilename(initialdir=os.path.dirname(os.path.abspath(__file__)),
                                          title="Select a File",
                                          filetypes=(("Python files",
                                                      "*.py*"),))

    if filename == emptyTuple:
        fileButt.configure(text="Select file")
    else: fileButt.configure(text=filename)

def browseConfFiles():
    filename = tkinter.filedialog.askopenfilename(initialdir=os.path.dirname(os.path.abspath(__file__)),
                                                  title="Select a File",
                                                  filetypes=(("YAML files",
                                                              "*.yaml*"),))
    if filename == emptyTuple:
        fileConfButt.configure(text="Select YAML file")
    else: fileConfButt.configure(text=filename)

def browseLogDir():
    dirname = tkinter.filedialog.askdirectory()
    if dirname == emptyTuple:
        logdButt.configure(text="Select log directory")
    else: logdButt.configure(text=dirname)


#TODO: Add exceptions
def injectFaults():
    filename = fileButt.cget('text')
    parse_src_import = inCd.addImport(filename)
    loglValue = eval(loglCombo.get())
    if modeCombo.get()=='Run':
        loglValue = 0

    parse_src_fi = inCd.addFi(parse_src_import, fileConfButt.cget('text'), logdButt.cget('text'), loglValue, disCombo.get(), nameEntry.get(), fipEntry.get())
    # Execute the parsed code
    exec(compile(parse_src_fi, filename="<ast>", mode="exec"), globals())

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
        loglLabel.grid(row=13, column=10)
        loglCombo.grid(row=13, column=15)
        namelabel.grid(row=14, column=0)
        nameEntry.grid(row=14, column=5)
        fiplabel.grid(row=14, column=10)
        fipEntry.grid(row=14, column=15)


# Label
fiTitleLabel = tk.Label(second_frame, text="Fault injection", font = ("Times New Roman", 10)).grid(row=10, column=0, padx = 10, pady = 25)
sourLabel = tk.Label(second_frame, text="Source file: ", font = ("Times New Roman", 10)).grid(row=11, column=0, padx = 10, pady = 25)
confLabel = tk.Label(second_frame, text="configFileName:", font = ("Times New Roman", 10)).grid(row=11, column=10, padx = 10, pady = 25)
logdLabel = tk.Label(second_frame, text="logDir:", font = ("Times New Roman", 10)).grid(row=12, column=0, padx = 10, pady = 25)
disLabel = tk.Label(second_frame, text="disableInjections:", font = ("Times New Roman", 10)).grid(row=12, column=10, padx = 10, pady = 25)
modeLabel = tk.Label(second_frame, text="Mode:", font = ("Times New Roman", 10)).grid(row=13, column=0, padx = 10, pady = 25)
# Debugging mode
loglLabel = tk.Label(second_frame, text="logLevel:", font = ("Times New Roman", 10))
# loglLabel.grid(row=13, column=10, padx = 10, pady = 25)
namelabel = tk.Label(second_frame, text="name:", font = ("Times New Roman", 10))
# namelabel.grid(row=14, column=0, padx = 10, pady = 25)
fiplabel = tk.Label(second_frame, text="fiPrefix:", font = ("Times New Roman", 10))
# fiplabel.grid(row=14, column=10, padx = 10, pady = 25)

# Combobox
disCombo = ttk.Combobox(second_frame, font = ("Times New Roman", 10), values=['False', 'True'])
disCombo.grid(row=12, column=15)
disCombo.current(0)

modeVar = tk.StringVar()
modeCombo = ttk.Combobox(second_frame, font = ("Times New Roman", 10), textvariable=modeVar, values=['Run', 'Debug'])
modeCombo.grid(row=13, column=5)
modeCombo.current(0)
modeVar.trace("w", on_trace_mode)

# Default to be 0
loglCombo = ttk.Combobox(second_frame, font = ("Times New Roman", 10), values=[10, 20, 30])
# loglCombo.grid(row=13, column=15)
loglCombo.current(0)

# Entry
nameEntry = tk.Entry(second_frame,bd=3)
# nameEntry.grid(row=14, column=5)
fipEntry = tk.Entry(second_frame,bd=3)
# fipEntry.grid(row=14, column=15)

# Button
fileButt = tk.Button(second_frame, font = ("Times New Roman", 10),text="Select file", command=browseFiles)
fileButt.grid(row=11, column=5)
fileConfButt = tk.Button(second_frame, font = ("Times New Roman", 10),text="Select YAML file", command=browseConfFiles)
fileConfButt.grid(row=11, column=15)
logdButt = tk.Button(second_frame, font = ("Times New Roman", 10),text="Select log directory", command=browseLogDir)
logdButt.grid(row=12, column=5)
fiButt = tk.Button(second_frame, font = ("Times New Roman", 10),text="Inject faults", command=injectFaults)
fiButt.grid(row=13, column=20)

# -------------------------------
# Statistics

# Generate feed_dict
Dict = {}
def addDict():
    key = feedKeyEntry.get()
    value = feedValEntry.get()
    Dict[key] = value
    feedLabel1 = tk.Label(second_frame, text='Successfully added!')
    feedLabel1.grid(row=17, column=25)
    feedLabel1.after(1000, feedLabel1.destroy)

def printt():
    print(Dict)

# Label
staTitleLabel = tk.Label(second_frame, text="Statistics", font = ("Times New Roman", 10)).grid(row=15, column=0, padx = 10, pady = 25)
corrPreLabel = tk.Label(second_frame, text="Correct Prediction: ", font = ("Times New Roman", 10)).grid(row=16, column=0, padx = 10, pady = 25)
feedKeyLabel = tk.Label(second_frame, text="Feed key: ", font = ("Times New Roman", 10))
feedKeyLabel.grid(row=17, column=0, padx = 10, pady = 25)
feedValLabel = tk.Label(second_frame, text="Feed value: ", font = ("Times New Roman", 10))
feedValLabel.grid(row=17, column=10, padx = 10, pady = 25)
testXLabel = tk.Label(second_frame, text="Test set (X): ", font = ("Times New Roman", 10))
testXLabel.grid(row=18, column=0, padx = 10, pady = 25)
testYLabel = tk.Label(second_frame, text="Test set (Y): ", font = ("Times New Roman", 10))
testYLabel.grid(row=18, column=10, padx = 10, pady = 25)


# Entry
correPreEntry = tk.Entry(second_frame,bd=3)
correPreEntry.grid(row=16, column=5)
feedKeyEntry = tk.Entry(second_frame,bd=3)
feedKeyEntry.grid(row=17, column=5)
feedValEntry = tk.Entry(second_frame,bd=3)
feedValEntry.grid(row=17, column=15)
testXEntry = tk.Entry(second_frame,bd=3)
testXEntry.grid(row=18, column=5)
testYEntry = tk.Entry(second_frame,bd=3)
testYEntry.grid(row=18, column=15)


#

# Button
feedDicButt = tk.Button(second_frame, font = ("Times New Roman", 10),text="Add feed Dictionary", command=addDict)
feedDicButt.grid(row=17, column=20)
# feeButt = tk.Button(second_frame, font = ("Times New Roman", 10),text="Print", command=printt)
# feeButt.grid(row=18, column=0)



root.mainloop()


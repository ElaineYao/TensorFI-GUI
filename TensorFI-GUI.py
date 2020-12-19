# -*- coding: utf-8 -*

# TODO: Package this GUI
import tkinter.filedialog
import Tkinter as tk
import ttk
import ruamel_yaml as yaml
import insertCode as inCd
import logging
import os


top = tk.Tk()
top.title('TensorFI')
top.geometry('1250x850')

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

    geneLabel1 = tk.Label(top, text='Successfully generated!')
    geneLabel1.grid(row=9, column=20)
    geneLabel1.after(1000, geneLabel1.destroy)

def addOp():
    opsEle = opsCombo.get() + ' = ' + opsEntry.get()
    opsList.append(opsEle)
    opsLabel1 = tk.Label(top, text='Successfully added!')
    opsLabel1.grid(row=6, column=25)
    opsLabel1.after(1000, opsLabel1.destroy)

def addIns():
    insEle = insCombo.get() + ' = ' + insEntry.get()
    insList.append(insEle)
    insLabel1 = tk.Label(top, text='Successfully added!')
    insLabel1.grid(row=6, column=25)
    insLabel1.after(1000, insLabel1.destroy)

#--------------
# Parameters Part
#Labels
# FIXME: How to align  'Parameters' with 'ScalarFaultType' - Beautify the GUI
paraTitlelabel = tk.Label(top, text="YAML File Parameters", font = ("Times New Roman", 10)).grid(row=0, column=0)


injectLabel = tk.Label(top, font = ("Times New Roman", 10), text="InjectMode: ")\
                    .grid(row = 5, column = 0, padx = 10, pady = 25)
scalarLabel = tk.Label(top, font = ("Times New Roman", 10), text="ScalarFaultType: ")\
                    .grid(row = 6, column = 0, padx = 10, pady = 25)
tensorLabel = tk.Label(top, font = ("Times New Roman", 10), text="TensorFaultType: ")\
                    .grid(row = 6, column = 10, padx = 10, pady = 25)
opsLabel = tk.Label(top, font = ("Times New Roman", 10), text="Ops: ")\
                    .grid(row = 7, column = 0, padx = 10, pady = 25)
ProbLabel = tk.Label(top, font = ("Times New Roman", 10), text="Probability: ")\
                    .grid(row = 7, column = 10, padx = 10, pady = 25)
insLabel = tk.Label(top, font = ("Times New Roman", 10), text="Instances: ")\
                    .grid(row = 8, column = 0, padx = 10, pady = 25)
numLabel = tk.Label(top, font = ("Times New Roman", 10), text="Number: ")\
                    .grid(row = 8, column = 10, padx = 10, pady = 25)
seedLabel = tk.Label(top, font = ("Times New Roman", 10), text="Seed: ")\
                    .grid(row = 9, column = 0, padx = 10, pady = 25)
skipLabel = tk.Label(top, font = ("Times New Roman", 10), text="SkipCount: ")\
                    .grid(row = 9, column = 10, padx = 10, pady = 25)

# Combobox
injectCombo = ttk.Combobox(top, font = ("Times New Roman", 10), values=['errorRate', 'dynamicInstance', 'oneFaultPerRun'])
injectCombo.grid(row=5, column=5)
injectCombo.current(0)

scalarCombo = ttk.Combobox(top, font = ("Times New Roman", 10), values=['None', 'Rand', 'Zero', 'Rand-element', 'bitFlip-element', 'bitFlip-tensor'])
scalarCombo.grid(row=6, column=5)
scalarCombo.current(0)

tensorCombo = ttk.Combobox(top, font = ("Times New Roman", 10), values=['None', 'Rand', 'Zero', 'Rand-element', 'bitFlip-element', 'bitFlip-tensor'])
tensorCombo.grid(row=6, column=15)
tensorCombo.current(4)

opsCombo = ttk.Combobox(top, font = ("Times New Roman", 10), values=['ABSOLUTE', 'ADD', 'ASSIGN', 'ALL', 'ARGMAX', 'ARGMIN', 'BIASADD', 'CAST', 'COUNT-NONZERO', 'CONV2D', 'ELU', 'END', 'EQUAL', 'EXPAND-DIMS',
                                                                        'FILL', 'FLOOR-MOD', 'GREATER-EQUAL', 'IDENTITY', 'LESS-EQUAL', 'LOG', 'LRN', 'MATMUL', 'MAX-POOL', 'MEAN', 'MINIMUM', 'MUL', 'NEGATIVE', 'NOT-EQUAL', 'NOOP',
                                                                        'ONE-HOT', 'PACK', 'POW', 'RANDOM_UNIFORM', 'RANK', 'RANGE', 'REALDIV', 'RELU', 'RESHAPE', 'RSQRT', 'SIGMOID', 'SIZE', 'SHAPE', 'SOFT-MAX', 'SQUARE', 'STRIDED-SLICE',
                                                                        'SUB',  'SUM', 'SWITCH', 'TANH', 'UNPACK'])
opsCombo.grid(row=7, column=5)
opsCombo.current(0)

insCombo = ttk.Combobox(top, font = ("Times New Roman", 10), values=['ABSOLUTE', 'ADD', 'ASSIGN', 'ALL', 'ARGMAX', 'ARGMIN', 'BIASADD', 'CAST', 'COUNT-NONZERO', 'CONV2D', 'ELU', 'END', 'EQUAL', 'EXPAND-DIMS',
                                                                        'FILL', 'FLOOR-MOD', 'GREATER-EQUAL', 'IDENTITY', 'LESS-EQUAL', 'LOG', 'LRN', 'MATMUL', 'MAX-POOL', 'MEAN', 'MINIMUM', 'MUL', 'NEGATIVE', 'NOT-EQUAL', 'NOOP',
                                                                        'ONE-HOT', 'PACK', 'POW', 'RANDOM_UNIFORM', 'RANK', 'RANGE', 'REALDIV', 'RELU', 'RESHAPE', 'RSQRT', 'SIGMOID', 'SIZE', 'SHAPE', 'SOFT-MAX', 'SQUARE', 'STRIDED-SLICE',
                                                                        'SUB',  'SUM', 'SWITCH', 'TANH', 'UNPACK'])
insCombo.grid(row=8, column=5)
insCombo.current(0)


# Entry - Enter the value
opsEntry = tk.Entry(top, bd=5)
opsEntry.grid(row=7, column = 15)
opsEntry.focus()
insEntry = tk.Entry(top, bd=5)
insEntry.grid(row=8, column = 15)
insEntry.focus()
seedText = tk.StringVar()
seedEntry = tk.Entry(top,bd=3,textvariable=seedText)
seedEntry.grid(row=9, column=5)
seedText.set(100000)
seedEntry.focus()
skipText = tk.StringVar()
skipEntry = tk.Entry(top,bd=3,textvariable=skipText)
skipEntry.grid(row=9, column=15)
skipText.set(1)
skipEntry.focus()

# Button - Click to generate default.yaml file
opButt = tk.Button(top, font = ("Times New Roman", 10),text="Add operation", command=addOp)
opButt.grid(row=7, column=20)
insButt = tk.Button(top, font = ("Times New Roman", 10),text="Add instance", command=addIns)
insButt.grid(row=8, column=20)
geneButt = tk.Button(top, font = ("Times New Roman", 10),text="Generate", command=generateYaml).grid(row=9, column=20)

#------------------------
# Fault injection

# BrowseFiles
def browseFiles():
    filename = tkinter.filedialog.askopenfilename(initialdir=os.path.dirname(os.path.abspath(__file__)),
                                          title="Select a File",
                                          filetypes=(("Python files",
                                                      "*.py*"),))
    # print(filename)
    if filename != '':
        fileButt.configure(text=filename)

def browseConfFiles():
    filename = tkinter.filedialog.askopenfilename(initialdir=os.path.dirname(os.path.abspath(__file__)),
                                                  title="Select a File",
                                                  filetypes=(("YAML files",
                                                              "*.yaml*"),))
    if filename != '':
        fileConfButt.configure(text=filename)
#TODO: Add browse logDir
def browseLogDir():


#TODO: Add exceptions
def injectFaults():
    filename = fileButt.cget('text')
    parse_src_import = inCd.addImport(filename)
    loglValue = eval(loglCombo.get())

    parse_src_fi = inCd.addFi(parse_src_import, fileConfButt.cget('text'), logdEntry.get(), loglValue, disCombo.get(), nameEntry.get(), fipEntry.get())
    # Execute the parsed code
    exec(compile(parse_src_fi, filename="<ast>", mode="exec"))


# Label
fiTitleLabel = tk.Label(top, text="Fault injection", font = ("Times New Roman", 10)).grid(row=10, column=0, padx = 10, pady = 25)
sourLabel = tk.Label(top, text="Source file: ", font = ("Times New Roman", 10)).grid(row=11, column=0, padx = 10, pady = 25)
confLabel = tk.Label(top, text="configFileName:", font = ("Times New Roman", 10)).grid(row=11, column=10, padx = 10, pady = 25)
logdLabel = tk.Label(top, text="logDir:", font = ("Times New Roman", 10)).grid(row=12, column=0, padx = 10, pady = 25)
disLabel = tk.Label(top, text="disableInjections:", font = ("Times New Roman", 10)).grid(row=12, column=10, padx = 10, pady = 25)
# Debugging mode
loglLabel = tk.Label(top, text="logLevel:", font = ("Times New Roman", 10)).grid(row=13, column=00, padx = 10, pady = 25)
namelabel = tk.Label(top, text="name:", font = ("Times New Roman", 10)).grid(row=13, column=10, padx = 10, pady = 25)
fiplabel = tk.Label(top, text="fiPrefix:", font = ("Times New Roman", 10)).grid(row=14, column=0, padx = 10, pady = 25)

# Combobox
disCombo = ttk.Combobox(top, font = ("Times New Roman", 10), values=['False', 'True'])
disCombo.grid(row=12, column=15)
disCombo.current(0)
loglCombo = ttk.Combobox(top, font = ("Times New Roman", 10), values=[10, 20, 30])
loglCombo.grid(row=13, column=5)
loglCombo.current(0)

# Entry
nameEntry = tk.Entry(top,bd=3)
nameEntry.grid(row=13, column=15)
nameEntry.focus()
fipEntry = tk.Entry(top,bd=3)
fipEntry.grid(row=14, column=5)
fipEntry.focus()

# Button
fileButt = tk.Button(top, font = ("Times New Roman", 10),text="Select file", command=browseFiles)
fileButt.grid(row=11, column=5)
fileConfButt = tk.Button(top, font = ("Times New Roman", 10),text="Select YAML file", command=browseConfFiles)
fileConfButt.grid(row=11, column=15)
logdButt = tk.Button(top, font = ("Times New Roman", 10),text="Select log directory ", command=browseLogDir)
logdButt.grid(row=12, column=15)
fiButt = tk.Button(top, font = ("Times New Roman", 10),text="Inject faults", command=injectFaults)
fiButt.grid(row=14, column=15)

# -------------------------------
# Statistics
# Label
staTitleLabel = tk.Label(top, text="Statistics", font = ("Times New Roman", 10)).grid(row=15, column=0, padx = 10, pady = 25)
finumLabel = tk.Label(top, text="Number of injections: ", font = ("Times New Roman", 10)).grid(row=16, column=0, padx = 10, pady = 25)

# Entry
finumEntry = tk.Entry(top,bd=3)
finumEntry.grid(row=16, column=5)
finumEntry.focus()

# Button
# Button is only available to certain InjectMode
# Bit flip/Random element
sdcvButt = tk.Button(top, font = ("Times New Roman", 10),text="Figure: SDC rates vs FI error rate", command=browseFiles)
sdcvButt.grid(row=17, column=0)
# One fault per run/ Dynamic instance
sdcoButt = tk.Button(top, font = ("Times New Roman", 10),text="Figure: SDC rates unber single bit-flip faults", command=browseFiles)
sdcoButt.grid(row=17, column=15)



top.mainloop()


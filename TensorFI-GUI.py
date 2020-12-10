# -*- coding: utf-8 -*
import Tkinter as tk
import ttk
import yaml

top = tk.Tk()
top.title('TensorFI')
top.geometry('800x350')

# Global variable
opsList = []
insList = []

# Code to add widgets

# Generate default.yaml file
# FIXME : try to realize generating the file before closing the window
def generateYaml():
    seed = seedEntry.get()
    scalarFaultType = scalarCombo.get()
    tensorFaultType = tensorCombo.get()
    skipCount = skipEntry.get()
    injectMode = injectCombo.get()

    paramsDict = {'ScalarFaultType': 'None', 'TensorFaultType': 'bitFlip-element', 'Ops': ['ALL = 1.0'],
              'Instances': ['CONV2D = 2', 'MAX-POOL = 2', 'RELU = 3', 'BIASADD = 2', 'RESHAPE = 1', 'ADD = 3',
                            'MATMUL = 3'], 'InjectMode': 'errorRate'}
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

    with open('default.yaml', 'w') as f:
        data = yaml.dump(paramsDict, f)

    geneLabel1 = tk.Label(top, text='Successfully generated!')
    geneLabel1.grid(row=9, column=20)
    geneLabel1.after(1000, geneLabel1.destroy)

# TODO: When click the button, a message will say "Successfully added!" and then restore the value
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


#Labels
# FIXME: How to align  'Parameters' with 'ScalarFaultType'
paraTitlelabel = tk.Label(top, text="Parameters", font = ("Times New Roman", 10)).grid(row=0, column=0)

scalarLabel = tk.Label(top, font = ("Times New Roman", 10), text="ScalarFaultType: ")\
                    .grid(row = 5, column = 0, padx = 10, pady = 25)
tensorLabel = tk.Label(top, font = ("Times New Roman", 10), text="TensorFaultFaultType: ")\
                    .grid(row = 5, column = 10, padx = 10, pady = 25)
opsLabel = tk.Label(top, font = ("Times New Roman", 10), text="Ops: ")\
                    .grid(row = 6, column = 0, padx = 10, pady = 25)
ProbLabel = tk.Label(top, font = ("Times New Roman", 10), text="Probability: ")\
                    .grid(row = 6, column = 10, padx = 10, pady = 25)
insLabel = tk.Label(top, font = ("Times New Roman", 10), text="Instances: ")\
                    .grid(row = 7, column = 0, padx = 10, pady = 25)
numLabel = tk.Label(top, font = ("Times New Roman", 10), text="Number: ")\
                    .grid(row = 7, column = 10, padx = 10, pady = 25)
injectLabel = tk.Label(top, font = ("Times New Roman", 10), text="InjectMode: ")\
                    .grid(row = 8, column = 0, padx = 10, pady = 25)
seedLabel = tk.Label(top, font = ("Times New Roman", 10), text="Seed: ")\
                    .grid(row = 8, column = 10, padx = 10, pady = 25)
skipLabel = tk.Label(top, font = ("Times New Roman", 10), text="SkipCount: ")\
                    .grid(row = 8, column = 20, padx = 10, pady = 25)

# Combobox
scalarCombo = ttk.Combobox(top, font = ("Times New Roman", 10), values=['None', 'Rand', 'Zero', 'Rand-element', 'bitFlip-element', 'bitFlip-tensor'])
scalarCombo.grid(row=5, column=5)
scalarCombo.current(0)

tensorCombo = ttk.Combobox(top, font = ("Times New Roman", 10), values=['None', 'Rand', 'Zero', 'Rand-element', 'bitFlip-element', 'bitFlip-tensor'])
tensorCombo.grid(row=5, column=15)
tensorCombo.current(4)

insCombo = ttk.Combobox(top, font = ("Times New Roman", 10), values=['ABSOLUTE', 'ADD', 'ASSIGN', 'ALL', 'ARGMAX', 'ARGMIN', 'BIASADD', 'CAST', 'COUNT-NONZERO', 'CONV2D', 'ELU', 'END', 'EQUAL', 'EXPAND-DIMS',
                                                                        'FILL', 'FLOOR-MOD', 'GREATER-EQUAL', 'IDENTITY', 'LESS-EQUAL', 'LOG', 'LRN', 'MATMUL', 'MAX-POOL', 'MEAN', 'MINIMUM', 'MUL', 'NEGATIVE', 'NOT-EQUAL', 'NOOP',
                                                                        'ONE-HOT', 'PACK', 'POW', 'RANDOM_UNIFORM', 'RANK', 'RANGE', 'REALDIV', 'RELU', 'RESHAPE', 'RSQRT', 'SIGMOID', 'SIZE', 'SHAPE', 'SOFT-MAX', 'SQUARE', 'STRIDED-SLICE',
                                                                        'SUB',  'SUM', 'SWITCH', 'TANH', 'UNPACK'])
insCombo.grid(row=6, column=5)
insCombo.current(0)
opsCombo = ttk.Combobox(top, font = ("Times New Roman", 10), values=['ABSOLUTE', 'ADD', 'ASSIGN', 'ALL', 'ARGMAX', 'ARGMIN', 'BIASADD', 'CAST', 'COUNT-NONZERO', 'CONV2D', 'ELU', 'END', 'EQUAL', 'EXPAND-DIMS',
                                                                        'FILL', 'FLOOR-MOD', 'GREATER-EQUAL', 'IDENTITY', 'LESS-EQUAL', 'LOG', 'LRN', 'MATMUL', 'MAX-POOL', 'MEAN', 'MINIMUM', 'MUL', 'NEGATIVE', 'NOT-EQUAL', 'NOOP',
                                                                        'ONE-HOT', 'PACK', 'POW', 'RANDOM_UNIFORM', 'RANK', 'RANGE', 'REALDIV', 'RELU', 'RESHAPE', 'RSQRT', 'SIGMOID', 'SIZE', 'SHAPE', 'SOFT-MAX', 'SQUARE', 'STRIDED-SLICE',
                                                                        'SUB',  'SUM', 'SWITCH', 'TANH', 'UNPACK'])
opsCombo.grid(row=7, column=5)
opsCombo.current(0)

injectCombo = ttk.Combobox(top, font = ("Times New Roman", 10), values=['errorRate', 'dynamicInstance', 'oneFaultPerRun'])
injectCombo.grid(row=8, column=5)
injectCombo.current(0)

# Entry - Enter the value
opsEntry = tk.Entry(top, bd=5)
opsEntry.grid(row=6, column = 15)
opsEntry.focus()
insEntry = tk.Entry(top, bd=5)
insEntry.grid(row=7, column = 15)
insEntry.focus()
seedEntry = tk.Entry(top,bd=3)
seedEntry.grid(row=8, column=15)
seedEntry.focus()
skipEntry = tk.Entry(top,bd=3)
skipEntry.grid(row=8, column=25)
seedEntry.focus()

# Button - Click to generate default.yaml file
opButt = tk.Button(top, font = ("Times New Roman", 10),text="Add operation", command=addOp)
opButt.grid(row=6, column=20)
insButt = tk.Button(top, font = ("Times New Roman", 10),text="Add instance", command=addIns)
insButt.grid(row=7, column=20)
geneButt = tk.Button(top, font = ("Times New Roman", 10),text="Generate", command=generateYaml).grid(row=9, column=15)


top.mainloop()


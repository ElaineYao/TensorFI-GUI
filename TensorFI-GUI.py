import Tkinter as tk
import ttk
import yaml

top = tk.Tk()
top.title('TensorFI')
top.geometry('500x250')
# Code to add widgets

# Generate default.yaml file
# FIXME : try to realize generating the file before closing the window
def generateYaml():
    params = {'InjectMode': 'errorRate',
              'Instances': ['CONV2D = 2', 'MAX-POOL = 2', 'RELU = 3', 'BIASADD = 2', 'RESHAPE = 1', 'ADD = 3',
                            'MATMUL = 3'],
              'ScalarFaultType': 'None', 'TensorFaultType': 'bitFlip-element', 'Ops': ['ALL = 1.0']}

    with open('default.yaml', 'w') as f:
        data = yaml.dump(params, f)

#Labels
# FIXME: How to align  'Parameters' with 'ScalarFaultType'
paraTitlelabel = tk.Label(top, text="Parameters", font = ("Times New Roman", 10)).grid(row=0, column=0)

scalarLabel = tk.Label(top, font = ("Times New Roman", 10), text="ScalarFaultType: ")\
                    .grid(row = 5, column = 0, padx = 10, pady = 25)
tensorLabel = tk.Label(top, font = ("Times New Roman", 10), text="TensorFaultFaultType: ")\
                    .grid(row = 5, column = 10, padx = 10, pady = 25)
# TODO: How to realize this multi choice with numbers
opsLabel = tk.Label(top, font = ("Times New Roman", 10), text="Ops: ")\
                    .grid(row = 6, column = 0, padx = 10, pady = 25)
# TODO: THe same with instance lable
insLabel = tk.Label(top, font = ("Times New Roman", 10), text="Instances: ")\
                    .grid(row = 6, column = 10, padx = 10, pady = 25)
injectLabel = tk.Label(top, font = ("Times New Roman", 10), text="InjectMode: ")\
                    .grid(row = 7, column = 0, padx = 10, pady = 25)

# Combobox
scalarCombo = ttk.Combobox(top, font = ("Times New Roman", 10), values=['None', 'Rand', 'Zero', 'Rand-element', 'bitFlip-element', 'bitFlip-tensor'])
scalarCombo.grid(row=5, column=5)
scalarCombo.current(0)

tensorCombo = ttk.Combobox(top, font = ("Times New Roman", 10), values=['None', 'Rand', 'Zero', 'Rand-element', 'bitFlip-element', 'bitFlip-tensor'])
tensorCombo.grid(row=5, column=15)
tensorCombo.current(4)
# TODO: How to realize this multi choice with numbers
opsBox = tk.Spinbox(top, from_=0, to=1).grid(row=6, column=5)

# TODO: THe same with instance lable
opsCombo = ttk.Combobox(top, font = ("Times New Roman", 10), values=['None', 'Rand', 'Zero', 'Rand-element', 'bitFlip-element', 'bitFlip-tensor'])
opsCombo.grid(row=6, column=15)
opsCombo.current(4)

injectCombo = ttk.Combobox(top, font = ("Times New Roman", 10), values=['errorRate', 'dynamicInstance', 'oneFaultPerRun'])
injectCombo.grid(row=7, column=5)
injectCombo.current(0)

# Button - Click to generate default.yaml file
btYaml = tk.Button(top, font = ("Times New Roman", 10),text="Generate", command=generateYaml).grid(row=7, column=10)


top.mainloop()
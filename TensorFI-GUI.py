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
# paraTitlelabel.pack(side=tk.LEFT)

paralabel = tk.Label(top, font = ("Times New Roman", 10), text="ScalarFaultType: ")\
                    .grid(row = 5, column = 0, padx = 10, pady = 25)

# Combobox
ScalarCombo = ttk.Combobox(top, font = ("Times New Roman", 10), values=['None', 'Rand', 'Zero', 'Rand-element', 'bitFlip-element', 'bitFlip-tensor'])
ScalarCombo.grid(row=5, column=1)
ScalarCombo.current(0)

# # Button - Click to generate default.yaml file
# btYaml = tk.Button(paraFrame3, font = ("Times New Roman", 10),text="Generate", command=generateYaml)
# btYaml.pack(side=tk.RIGHT)





top.mainloop()
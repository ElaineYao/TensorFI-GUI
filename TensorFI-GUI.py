# -*- coding: utf-8 -*
import Tkinter as tk
import ttk
import yaml

top = tk.Tk()
top.title('TensorFI')
top.geometry('800x350')
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

# TODO: When click the button, a message will say "Successfully added!" and then restore the value
def addOpIns():
    print('Added!')
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
ProbLabel = tk.Label(top, font = ("Times New Roman", 10), text="Probability: ")\
                    .grid(row = 6, column = 10, padx = 10, pady = 25)
# TODO: THe same with instance lable
insLabel = tk.Label(top, font = ("Times New Roman", 10), text="Instances: ")\
                    .grid(row = 7, column = 0, padx = 10, pady = 25)
numLabel = tk.Label(top, font = ("Times New Roman", 10), text="Number: ")\
                    .grid(row = 7, column = 10, padx = 10, pady = 25)
injectLabel = tk.Label(top, font = ("Times New Roman", 10), text="InjectMode: ")\
                    .grid(row = 8, column = 0, padx = 10, pady = 25)

# Combobox
scalarCombo = ttk.Combobox(top, font = ("Times New Roman", 10), values=['None', 'Rand', 'Zero', 'Rand-element', 'bitFlip-element', 'bitFlip-tensor'])
scalarCombo.grid(row=5, column=5)
scalarCombo.current(0)

tensorCombo = ttk.Combobox(top, font = ("Times New Roman", 10), values=['None', 'Rand', 'Zero', 'Rand-element', 'bitFlip-element', 'bitFlip-tensor'])
tensorCombo.grid(row=5, column=15)
tensorCombo.current(4)
# TODO: How to realize this multi choice with numbers
tensorCombo = ttk.Combobox(top, font = ("Times New Roman", 10), values=['ABSOLUTE', 'ADD', 'ASSIGN', 'ALL', 'ARGMAX', 'ARGMIN', 'BIASADD', 'CAST', 'COUNT-NONZERO', 'CONV2D', 'ELU', 'END', 'EQUAL', 'EXPAND-DIMS',
                                                                        'FILL', 'FLOOR-MOD', 'GREATER-EQUAL', 'IDENTITY', 'LESS-EQUAL', 'LOG', 'LRN', 'MATMUL', 'MAX-POOL', 'MEAN', 'MINIMUM', 'MUL', 'NEGATIVE', 'NOT-EQUAL', 'NOOP',
                                                                        'ONE-HOT', 'PACK', 'POW', 'RANDOM_UNIFORM', 'RANK', 'RANGE', 'REALDIV', 'RELU', 'RESHAPE', 'RSQRT', 'SIGMOID', 'SIZE', 'SHAPE', 'SOFT-MAX', 'SQUARE', 'STRIDED-SLICE',
                                                                        'SUB',  'SUM', 'SWITCH', 'TANH', 'UNPACK'])
tensorCombo.grid(row=6, column=5)
tensorCombo.current(0)
# TODO: THe same with instance lable
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
insEntry = tk.Entry(top, bd=5)
insEntry.grid(row=6, column = 15)
insEntry.focus()
opsEntry = tk.Entry(top, bd=5)
opsEntry.grid(row=7, column = 15)
opsEntry.focus()

# Button - Click to generate default.yaml file
btYaml = tk.Button(top, font = ("Times New Roman", 10),text="Generate", command=generateYaml).grid(row=8, column=10)
btYaml = tk.Button(top, font = ("Times New Roman", 10),text="Add operation", command=addOpIns()).grid(row=6, column=20)
btYaml = tk.Button(top, font = ("Times New Roman", 10),text="Add instance", command=addOpIns()).grid(row=7, column=20)


top.mainloop()

# import Tkinter as tk
# import ttk
# win = tk.Tk()
# win.title("Python GUI")
# ttk.Label(win, text="Chooes a number").grid(column=1, row=0) # 添加一个标签0
# ttk.Label(win, text="Enter a name:").grid(column=0, row=0) # 设置其在界面中出现的位置
# # button被点击之后会被执行
# def clickMe():  # 当acction被点击时,该函数则生效
#  action.configure(text='Hello ' + name.get() + ' ' + numberChosen.get())#设置button显示的内容
#  print('check3 is %d %s' % (chvarEn.get(), type(chvarUn.get())))
# action = ttk.Button(win, text="Click Me!", command=clickMe) # 创建一个按钮, text：显示按
# action.grid(column=2, row=1)  # 设置其在界面中出现的位置
# # 文本框
# name = tk.StringVar() # StringVar是Tk库内部定义的字符串变量类型，在这里用于管理
#         #部件上面的字符；不过一般用在按钮button上。改变StringVar，按钮上的文字也随之改变。
# nameEntered = ttk.Entry(win, width=12, textvariable=name) # 创建一个文本框，字符长度为12，
#      #内容绑定到name,方便clickMe调用
# nameEntered.grid(column=0, row=1) # 设置其在界面中出现的位置
# nameEntered.focus() # 当程序运行时,光标默认会出现在该文本框中
# # 一个下拉列表
# number = tk.StringVar()
# numberChosen = ttk.Combobox(win, width=12, textvariable=number, state='readonly')
# numberChosen['values'] = (1, 2, 4, 42, 100) # 设置下拉列表的值
# numberChosen.grid(column=1, row=1) # 设置其在界面中出现的位置 column代表列 row 代表行
# numberChosen.current(4) # 设置下拉列表默认显示的值，0为numberChosen['values'] 的下标值
# # 复选框
# chVarDis = tk.IntVar() # 用来获取复选框是否被勾选，通过chVarDis.get()来获取其的状态,
#            #其状态值为int类型 勾选为1 未勾选为0
# check1 = tk.Checkbutton(win, text="Disabled", variable=chVarDis, state='disabled') # text为复选框
#            #后面的名称,variable将该复选框的状态赋值给一个变量，当state='disabled'时，
#            #该复选框为灰色，不能点的状态
# check1.select() # 该复选框是否勾选,select为勾选, deselect为不勾选
# check1.grid(column=0, row=4, sticky=tk.W) # sticky=tk.W 当该列中其他行或该行中的其他列的
#           #某一个功能拉长这列的宽度或高度时，设定该值可以保证本行保持左对齐，
#           #N：北/上对齐 S：南/下对齐 W：西/左对齐 E：东/右对齐
# chvarUn = tk.IntVar()
# check2 = tk.Checkbutton(win, text="UnChecked", variable=chvarUn)
# check2.deselect()
# check2.grid(column=1, row=4, sticky=tk.W)
# chvarEn = tk.IntVar()
# check3 = tk.Checkbutton(win, text="Enabled", variable=chvarEn)
# check3.select()
# check3.grid(column=2, row=4, sticky=tk.W)
# win.mainloop() # 当调用mainloop()时,窗口才会显示出来

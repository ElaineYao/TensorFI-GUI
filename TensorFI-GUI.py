# -*- coding: utf-8 -*

# TODO: Package this GUI
import tkinter.filedialog
import Tkinter as tk
import ttk
import ruamel_yaml as yaml
import insertCode as inCd
import insertCodeAccu as inCdAc
import calStats as calS
import logging
import os
import csv
import numpy as np
import astor
import subprocess
import matplotlib
import matplotlib.pyplot as plt
import shutil
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import geneTable as geTable

root = tk.Tk()
root.title('TensorFI')
# FIXME
root.geometry('890x650')
root['bg'] = 'grey'
# root.geometry("+%d+%d" % (self.window_start_x, self.window_start_y))

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
    print(var.get())
    if var.get() == 1:
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

        # with open('test-0.yaml', 'w') as f:
        #     data = yaml.dump(paramsDict, f, Dumper=yaml.RoundTripDumper)

        yamldir = os.path.join(os.getcwd(), 'configYAML')
        if os.path.exists(yamldir):
            shutil.rmtree(yamldir)
            os.mkdir(yamldir)
        else:
            os.mkdir(yamldir)
        yamlFile = yamldir + '/0-conf.yaml'
        print(yamlFile)
        with open(yamlFile, 'w') as f:
            data = yaml.dump(paramsDict, f, Dumper=yaml.RoundTripDumper)

        geneLabel1 = tk.Label(second_frame, text='Successfully generated!')
        geneLabel1.grid(row=9, column=5)
        geneLabel1.after(1000, geneLabel1.destroy)
    else:
        totList = []
        numFile = 0
        for j in range(len(opsList)): # j - select each ops, e.g., All
            ops = list(opsList[j].keys())[0]
            probList = list(opsList[j].values())[0]
            eachList = []
            numFile = 0
            for i in np.arange(probList[0], probList[1]+0.0001, probList[2]):
                eachELe = ops + ' = ' + str(i)
                eachList.append(eachELe)
                numFile += 1
            totList.append(eachList)

        print('totList:')
        print(totList)

        # finList : [['All = 0.1', 'ADD = 0.1'], ['All = 0.2', 'ADD = 0.2']], finEaList = ['All = 0.1', 'ADD = 0.1']
        finList = []
        for i in range(numFile):
            finEaList = []
            for j in range(len(opsList)):
                col = totList[j]
                ele = col[i]
                finEaList.append(ele)
            finList.append(finEaList)

        yamldir = os.path.join(os.getcwd(), 'configYAML')
        if os.path.exists(yamldir):
            shutil.rmtree(yamldir)
            os.mkdir(yamldir)
        else:
            os.mkdir(yamldir)

        for i in range(numFile):
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
                paramsDict['Ops'] = finList[i]

            if insList != []:
                paramsDict['Instances'] = insList
            if seed != '':
                paramsDict['Seed'] = int(seed)
            if skipCount != '':
                paramsDict['SkipCount'] = int(skipCount)

            yamlFile = yamldir+'/'+str(i)+'-conf'+'.yaml'
            with open(yamlFile, 'w') as f:
                data = yaml.dump(paramsDict, f, Dumper=yaml.RoundTripDumper)


    geneLabel1 = tk.Label(second_frame, text='Successfully generated!')
    geneLabel1.grid(row=9, column=5)
    geneLabel1.after(1000, geneLabel1.destroy)

def addOp():
    if var.get() == 1:
        opsEle = opsCombo.get() + ' = ' + opsEntry.get()
        opsList.append(opsEle)

    else:
        opsDict = {}
        opsDList = [float(opsEntry.get()), float(opsEntry2.get()), float(opsEntry3.get())]
        opsEle = opsCombo.get()
        opsDict[opsEle] = opsDList
        opsList.append(opsDict)

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
# Callback function1

def sel():
    if var.get() == 2:
        opsEntry2.config(state="normal")
        opsEntry3.config(state="normal")
    else:
        opsEntry2.config(state="disabled")
        opsEntry3.config(state="disabled")

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
        # Both operations and Instances settings are enabled under dynamicInstance and oneFaultPerRun mode
        opsCombo.configure(state="normal")
        opsEntry.config(state='normal')
        opButt.config(state='normal')
        insCombo.configure(state='normal')
        insEntry.config(state='normal')
        insButt.config(state='normal')

# -------------------
# Callback function2
def on_trace_mode(name, index, mode):
    refresh_mode()
def refresh_mode( ):
    mode = modeCombo.get()
    if mode == 'Run':
        disLabel.grid_forget()
        disCombo.grid_forget()
        logdLabel.grid_forget()
        logdButt.grid_forget()
        loglLabel.grid_forget()
        loglCombo.grid_forget()
        namelabel.grid_forget()
        nameEntry.grid_forget()
        fiplabel.grid_forget()
        fipEntry.grid_forget()
        feedKeyLabel.grid_forget()
        feedKeyEntry.grid_forget()
        feedValLabel.grid_forget()
        feedValEntry.grid_forget()
        feedDicButt.grid_forget()
        corrPreLabel.grid_forget()
        correPreEntry.grid_forget()
    else:
        disLabel.grid(row=11,column=0,padx=5, pady=5,sticky='w')
        disCombo.grid(row=11, column=1, padx=5, pady=5, sticky='w')
        logdLabel.grid(row=12, column = 0, padx = 5, pady = 5, sticky = 'w')
        logdButt.grid(row=12, column=1, padx=5, pady=5, sticky='w')
        loglLabel.grid(row=11, column = 2, padx = 5, pady = 5, sticky = 'w')
        loglCombo.grid(row=11, column = 3, padx = 5, pady = 5, sticky = 'w')
        namelabel.grid(row=13, column = 0, padx = 5, pady = 5, sticky = 'w')
        nameEntry.grid(row=13, column = 1, padx = 5, pady = 5, sticky = 'w')
        fiplabel.grid(row=12, column = 2, padx = 5, pady = 5, sticky = 'w')
        fipEntry.grid(row=12, column = 3, padx = 5, pady = 5, sticky = 'w')
        feedKeyLabel.grid(row=14,column=0,padx=5, pady=5,sticky='w')
        feedKeyEntry.grid(row=14,column=1,padx=5, pady=5,sticky='w')
        feedValLabel.grid(row=14,column=2,padx=5, pady=5,sticky='w')
        feedValEntry.grid(row=14,column=3,padx=5, pady=5,sticky='w')
        feedDicButt.grid(row=14,column=4,padx=5, pady=5,sticky='w')
        corrPreLabel.grid(row=13, column = 2, padx = 5, pady = 5, sticky = 'w')
        correPreEntry.grid(row=13, column = 3, padx = 5, pady = 5, sticky = 'w')

# --------------------
# Callback function3 - formCombo


def formSel( ):
    choice = formVar.get()
    if choice == 2:
        # TODO
        # showfig
        statLabel.grid_forget()
        index = 0
        for i in range(total_rows):
            for j in range(total_columns):
                labels[index].grid_forget()
                index += 1

        fig = plt.figure(figsize=(6, 6), dpi=100)
        root2 = tk.Toplevel()
        canvas = FigureCanvasTkAgg(fig, master=root2)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.BOTTOM, fill=tkinter.NONE, expand=0)


        if var.get() == 1:
            t = np.arange(1, 1 + int(numFIEntry.get())).astype(dtype=np.str)

            labelData = tuple(t)
            labelpos = np.arange(len(labelData))
            y1 = np.loadtxt('./origin.csv', delimiter='\n', unpack=True)
            plt.bar(labelpos, y1, align='center', alpha=1.0)
            plt.xticks(labelpos, labelData)
            plt.ylabel("Accuracy")
            plt.xlabel("Index of fault injection")
            plt.tight_layout(pad=2.2, w_pad=5.5, h_pad=5.1)
            plt.title('Accuracy per fault injection')
            plt.xticks(rotation=38, horizontalalignment='center')

            for index, datapoints in enumerate(y1):
                plt.text(x=index, y=datapoints, s=" ", fontdict=dict(fontsize=18), ha='center',
                         va='bottom')
            # plt.show()

        else:
            y1 = []
            for i in range(len(lst)-1):
                tup = lst[i+1]
                y1.append(tup[1])
            t = np.arange(1, total_rows).astype(dtype=np.str)
            labelData = tuple(t)
            print(labelData)
            labelpos = np.arange(len(labelData))

            plt.bar(labelpos, y1, align='center', alpha=1.0)
            plt.xticks(labelpos, labelData)
            plt.ylabel("Accuracy")
            plt.xlabel("Index of setting")
            plt.tight_layout(pad=2.2, w_pad=5.5, h_pad=5.1)
            plt.title('Accuracy per setting')
            plt.xticks(rotation=38, horizontalalignment='center')

            for index, datapoints in enumerate(y1):
                plt.text(x=index, y=datapoints, s="", fontdict=dict(fontsize=18), ha='center', va='bottom')

            # plt.show()


        # forget data
        statLabel.grid_forget()
        # forget csv
        csvLabel.grid_forget()
        csvButt.grid_forget()
        csvEntry.grid_forget()
        csvdotLabel.grid_forget()



    elif choice == 1:
        # TODO
        # show data
        # if var.get() == 1:
        #     statLabel.grid(row=21, column=1, padx=5, pady=5, sticky='w')
        #     statLabel.configure(text='Mean: ' + str(calS.calAve('./origin.csv')) + ', Standard deviation: ' + str(calS.calmsd('./origin.csv')) + ', Min: ' + str(calS.calMin('./origin.csv')) + ', Max: ' + str(
        #         calS.calMax('./origin.csv')))
        #     index = 0
        #     for i in range(total_rows):
        #         for j in range(total_columns):
        #             labels[index].grid_forget()
        #             index += 1
        # else:
        index = 0
        for i in range(total_rows):
            for j in range(total_columns):
                labels[index].grid(row=i + 23, column=j)
                index += 1

        csvLabel.grid_forget()
        csvButt.grid_forget()
        csvEntry.grid_forget()
        csvdotLabel.grid_forget()

    else:

        # forget data

        # show csv
        # TODO - export the csv file
        csvLabel.grid(row=21,column=0,padx=5, pady=5,sticky='w')
        csvEntry.grid(row=21,column=1,padx=5, pady=5,sticky='w')
        csvdotLabel.grid(row=21,column=2,padx=5, pady=5,sticky='w')
        csvButt.grid(row=21, column=3, padx=5, pady=5, sticky='w')
        index = 0
        for i in range(total_rows):
            for j in range(total_columns):
                labels[index].grid_forget()
                index += 1


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

    # TODO: browse the files, if the number of files is 1, then ,

    yamldir = os.path.join(os.getcwd(), 'configYAML')
    global confiles
    confiles_unsorted = [os.path.join(root, name)
                 for root, dirs, files in os.walk(yamldir)
                 for name in files
                 if name.endswith((".yaml"))]
    confiles = sorted(confiles_unsorted)

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

# Generate feed_dict
Dict = {}
def addDict():
    key = feedKeyEntry.get()
    # value = check(feedValEntry)
    value = feedValEntry.get()
    Dict[key] = value
    feedLabel1 = tk.Label(second_frame, text='Successfully added!')
    feedLabel1.grid(row=17, column=20)
    feedLabel1.after(1000, feedLabel1.destroy)

# TODO: Export the csv file
def exportCSV():
    csvName = csvEntry.get() + '.csv'
    numFI = int(numFIEntry.get())
    y = np.loadtxt('./origin.csv', delimiter='\n', unpack=True)
    cols = numFI
    rows = len(y)/numFI
    csv_list = []
    for i in range(rows):
        per_list = []
        for j in range(cols):
            per_list.append(y[i*rows+j])
        csv_list.append(per_list)
    with open(csvName, 'wb') as file:
        writer = csv.writer(file)
        writer.writerows(csv_list)
    csvgLabel = tk.Label(second_frame, text='Successfully exported!')
    csvgLabel.grid(row=21, column=5)
    csvgLabel.after(1000, csvgLabel.destroy)

# ------------------------
# Fault injection
emptyTuple = ()


# TODO: Add exceptions
def injectFaults():
    fiButt.configure(text='Injecting')
    generateYaml()
    browseConfFiles()
    loglValue = 0
    writePattern = 'a'

    origConfFile = 'origin.csv'
    if os.path.exists(origConfFile):
        os.remove(origConfFile)

    if var.get() == 1:
        writePattern = 'w'

    if modeCombo.get() == 'Debug':
        loglValue = eval(loglCombo.get())
        parse_src_import = inCd.addImport(sourcefile)
        parse_src_fi = inCd.addFi(parse_src_import, correPreEntry.get(), Dict, 'sdcRates.csv', int(numFIEntry.get()),
                                  testXEntry.get(), testYEntry.get(), confiles[0], dirpath, loglValue, disCombo.get(),
                                  nameEntry.get(), fipEntry.get())
    else:
        dirpath = ' '
        parse_src_import = inCdAc.addImport(sourcefile)
        parse_src_fi = inCdAc.addFi(parse_src_import,
                                    testXEntry.get(), testYEntry.get(), accuEntry.get(),
                                    confiles[0], 'origin', int(numFIEntry.get()))

    # FIXME:
    if len(confiles) == 1:
        # exec (compile(parse_src_fi, filename="<ast>", mode="exec"), globals())
        with open("Injected-0" + ".py", "w") as f:
            f.write(astor.to_source(parse_src_fi))
        subprocess.call(["/home/elainey/backup/pycharmProjects/yamlTest/runFIfileAcc.sh"],
                        env={"PATH": "/home/elainey/anaconda/envs/tensorfi/bin/"})
    else:
        with open("Injected-0" + ".py", "w") as f:
            f.write(astor.to_source(parse_src_fi))
        arg1 = str(len(confiles))
        subprocess.check_call(['/home/elainey/backup/pycharmProjects/yamlTest/createFIfile.sh', arg1])
        subprocess.call(["/home/elainey/backup/pycharmProjects/yamlTest/runFIfile.sh", arg1],
                        env={"PATH": "/home/elainey/anaconda/envs/tensorfi/bin/"})

    # showRes()
    fiButt.configure(text='Injection completed!')
    global lst
    global total_rows
    global total_columns
    global labels
    lst = []
    lst = geTable.geneTable(int(numFIEntry.get()), './origin.csv')
    total_rows = len(lst)
    total_columns = len(lst[0])

    labels = []
    index = 0
    for i in range(total_rows):
        for j in range(total_columns):
            statLabel = tk.Label(second_frame, font=('Times New Roman', 10, 'bold'), text=lst[i][j])
            labels.append(statLabel)
        index += 1

    index = 0
    for i in range(total_rows):
        for j in range(total_columns):
            labels[index].grid(row=i + 23, column=j)
            index += 1

# FIXME: to be modified or deleted
def showRes():
    if modeCombo.get() == 'Debug':
        # Execute the parsed code
        sdc = np.loadtxt('sdcRates.csv', delimiter='\n', unpack=True)
        # FIXME: add sdcrates & accuracy in Debug settings
        sdcOnceLabel.configure(text='SDC rates: ' + str(sdc))

    else:
        # FIXME: add accuracy
        acc = np.loadtxt('accuracy.csv', delimiter='\n', unpack=True)
        formLable.configure(text='Accuracy with injections: ' + str(acc))


#--------------
# Parameters Part
#Labels
# FIXME: How to align  'Parameters' with 'ScalarFaultType' - Beautify the GUI
paraTitlelabel = tk.Label(second_frame, text="Configuration", font = ('Times New Roman', 12, 'bold')).grid(row=0, column=0, padx = 5, pady = 25, sticky = 'w')


injectLabel = tk.Label(second_frame, font = ("Times New Roman", 10), text="InjectMode: ")\
                    .grid(row = 5, column = 0, padx = 5, pady = 5, sticky = 'w')
modeLabel2 = tk.Label(second_frame, font = ("Times New Roman", 10), text="configMode: ")\
                    .grid(row = 5, column = 2, padx = 5, pady = 5, sticky = 'w')
scalarLabel = tk.Label(second_frame, font = ("Times New Roman", 10), text="ScalarFaultType: ")\
                    .grid(row = 6, column = 0, padx = 5, pady = 5, sticky = 'w')
tensorLabel = tk.Label(second_frame, font = ("Times New Roman", 10), text="TensorFaultType: ")\
                    .grid(row = 6, column = 2, padx = 5, pady = 5, sticky = 'w')
opsLabel = tk.Label(second_frame, font = ("Times New Roman", 10), text="Operations: ")\
                    .grid(row = 7, column = 0, padx = 5, pady = 5, sticky = 'w')
ProbLabel = tk.Label(second_frame, font = ("Times New Roman", 10), text="Probability: ")\
                    .grid(row = 7, column = 2, padx = 5, pady = 5, sticky = 'w')
ProbExpLable = tk.Label(second_frame, font = ("Times New Roman", 10), text="(Start:End:Step)")\
                    .grid(row = 7, column = 4, padx = 5, pady = 5, sticky = 'w')

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
sourLabel = tk.Label(second_frame, text="Source file: ", font = ("Times New Roman", 10)).grid(row = 10, column = 0, padx = 5, pady = 5, sticky = 'w')
modeLabel = tk.Label(second_frame, text="Mode:", font = ("Times New Roman", 10)).grid(row=10, column = 2, padx = 5, pady = 5, sticky = 'w')
accuLabel = tk.Label(second_frame, text="Accuracy function: ", font = ("Times New Roman", 10)).grid(row=15, column = 0, padx = 5, pady = 5, sticky = 'w')
corrPreLabel = tk.Label(second_frame, text="Correct Prediction: ", font = ("Times New Roman", 10))
testXLabel = tk.Label(second_frame, text="Input: ", font = ("Times New Roman", 10))
testXLabel.grid(row=16, column = 0, padx = 5, pady = 5, sticky = 'w')
testYLabel = tk.Label(second_frame, text="Output: ", font = ("Times New Roman", 10))
testYLabel.grid(row=16, column = 2, padx = 5, pady = 5, sticky = 'w')
# Debugging mode
disLabel = tk.Label(second_frame, text="disableInjections:", font = ("Times New Roman", 10))
logdLabel = tk.Label(second_frame, text="logDir:", font = ("Times New Roman", 10))
loglLabel = tk.Label(second_frame, text="logLevel:", font = ("Times New Roman", 10))
namelabel = tk.Label(second_frame, text="name:", font = ("Times New Roman", 10))
fiplabel = tk.Label(second_frame, text="fiPrefix:", font = ("Times New Roman", 10))
numFILabel = tk.Label(second_frame, text="Number of injections: ", font = ("Times New Roman", 10))
numFILabel.grid(row=15, column=2, padx=5, pady=5, sticky='w')
feedKeyLabel = tk.Label(second_frame, text="Feed key: ", font = ("Times New Roman", 10))
feedValLabel = tk.Label(second_frame, text="Feed value: ", font = ("Times New Roman", 10))


# Combobox
choiceVar = tk.StringVar()
injectCombo = ttk.Combobox(second_frame, width = 15, font = ("Times New Roman", 10), textvariable=choiceVar, values=['errorRate', 'dynamicInstance', 'oneFaultPerRun'])
injectCombo.grid(row=5, column=1, sticky = 'w')
injectCombo.current(0)
choiceVar.trace("w", on_trace_choice)

# modeCombo2 = ttk.Combobox(second_frame, width = 15, font = ("Times New Roman", 10), textvariable=choiceVar2, values=['Single', 'Multiple'])
# modeCombo2.grid(row=5, column=3, sticky = 'w')
# modeCombo2.current(0)
var = tk.IntVar(second_frame,1)
modeRadio1 = tk.Radiobutton(second_frame, width = 15, font = ("Times New Roman", 10), text='Single', value=1, variable = var, command = sel)
modeRadio1.grid(row=5, column=3, sticky = 'w')
modeRadio2 = tk.Radiobutton(second_frame, width = 15, font = ("Times New Roman", 10), text='Multiple', value=2, variable = var, command = sel)
modeRadio2.grid(row=5, column=4, sticky = 'w')
# choiceVar2.trace("w", on_trace_choice)


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

disCombo = ttk.Combobox(second_frame, font = ("Times New Roman", 10), values=['False', 'True'], width = 8)
# disCombo.grid(row=11, column = 1, padx = 5, pady = 5, sticky = 'w')
disCombo.current(0)

modeVar = tk.StringVar()
modeCombo = ttk.Combobox(second_frame, font = ("Times New Roman", 10), textvariable=modeVar, values=['Run', 'Debug'], width = 8)
modeCombo.grid(row=10, column = 3, padx = 5, pady = 5, sticky = 'w')
modeCombo.current(0)
modeVar.trace("w", on_trace_mode)

# Default to be 0
loglCombo = ttk.Combobox(second_frame, font = ("Times New Roman", 10), values=[10, 20, 30], width = 8)
# loglCombo.grid(row=13, column=15)
loglCombo.current(0)

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
seedText.set(1000)
skipText = tk.StringVar()
skipEntry = tk.Entry(second_frame,width = 8,bd=3,textvariable=skipText)
skipEntry.grid(row=9, column=3, sticky = 'w')
skipText.set(0)
nameText = tk.StringVar()
nameEntry = tk.Entry(second_frame,bd=3, width = 8,textvariable=nameText)
nameText.set('noname')
numFItext = tk.StringVar()
numFIEntry = tk.Entry(second_frame,bd=3, width = 15, textvariable=numFItext)
numFItext.set('5')
numFIEntry.grid(row=15,column=3,padx=5, pady=5,sticky='w')
fipText = tk.StringVar()
fipEntry = tk.Entry(second_frame,bd=3, width = 8, textvariable=fipText)
fipText.set('fi_')

accuEntry = tk.Entry(second_frame,bd=3, width = 15)
accuEntry.grid(row=15, column = 1, padx = 5, pady = 5, sticky = 'w')
correPreEntry = tk.Entry(second_frame,bd=3, width = 15)

testXEntry = tk.Entry(second_frame,bd=3, width = 15)
testXEntry.grid(row=16, column = 1, padx = 5, pady = 5, sticky = 'w')
testYEntry = tk.Entry(second_frame,bd=3, width = 15)
testYEntry.grid(row=16, column = 3, padx = 5, pady = 5, sticky = 'w')

# Debugging mode

feedKeyEntry = tk.Entry(second_frame,bd=3, width = 15)
feedValEntry = tk.Entry(second_frame,bd=3, width = 15)

# Button - Click to generate default.yaml file
opButt = tk.Button(second_frame, font = ("Times New Roman", 10),text="Add", command=addOp)
opButt.grid(row=7, column=5)
insButt = tk.Button(second_frame, font = ("Times New Roman", 10),text="Add", command=addIns, state="disabled")
insButt.grid(row=8, column=4)
fileButt = tk.Button(second_frame, font = ("Times New Roman", 10),text="Select", command=browseFiles)
fileButt.grid(row=10, column = 1, padx = 5, pady = 5, sticky = 'w')
logdButt = tk.Button(second_frame, font = ("Times New Roman", 10),text="Select", command=browseLogDir)
# Debugging mode
feedDicButt = tk.Button(second_frame, font = ("Times New Roman", 10),text="Add", command=addDict)

# fiButt = tk.Button(second_frame, font = ("Times New Roman", 10),text="Inject", command=injectFaults)
fiButt = tk.Button(second_frame, font = ("Times New Roman", 10),text="Inject", command=injectFaults)
fiButt.grid(row=16, column = 4, padx = 5, pady = 5, sticky = 'w')




#-------





# -------------------------------
# Statistics setting

# Check date type in Entry
def check(entry):
    try:
        int(entry.get())
        print(int(entry.get()))
        return int(entry.get())
    except ValueError:
        try:
            float(entry.get())
            print(float(entry.get()))
            return float(entry.get())
        except ValueError:
            try:
                str(entry.get())
                print(str(entry.get()))
                return str(entry.get())
            except ValueError:
                print('Data type not support.')




#-----------------
# Results
resTitleLabel = tk.Label(second_frame, text="Results", font = ('Times New Roman', 12, 'bold')).grid(row=19, column = 0, padx = 5, pady = 25, sticky = 'w')
formLable = tk.Label(second_frame, text="Output forms: ", font=('Times New Roman', 10))
formLable.grid(row=20, column = 0, padx = 5, pady = 5, sticky = 'w')

# formModeVar = tk.StringVar()
# formCombo = ttk.Combobox(second_frame, font = ("Times New Roman", 10), textvariable=formModeVar, values=['', 'Figures', 'Statistic data (accuracy)', 'Export to a CSV file'], width = 25)
# formCombo.grid(row=20, column = 1, padx = 5, pady = 5, sticky = 'w')
# formCombo.current(0)
# formModeVar.trace('w', on_trace_form)

formVar = tk.IntVar(second_frame,1)
formRadio1 = tk.Radiobutton(second_frame, width = 15, font = ("Times New Roman", 10), text='Statistics', value=1, variable = formVar, command = formSel)
formRadio1.grid(row=20, column=1, sticky = 'w')
formRadio2 = tk.Radiobutton(second_frame, width = 15, font = ("Times New Roman", 10), text='Graph', value=2, variable = formVar, command = formSel)
formRadio2.grid(row=20, column=2, sticky = 'w')
formRadio3 = tk.Radiobutton(second_frame, width = 15, font = ("Times New Roman", 10), text='Export to CSV', value=3, variable = formVar, command = formSel)
formRadio3.grid(row=20, column=3, sticky = 'w')

# Debugging mode

# Statistics option - Single
statLabel = tk.Label(second_frame, font = ("Times New Roman", 10))
# TODO: Calculate the data
mean = 2
std  = 2
mind = 1
maxd = 2
statLabel.configure(text='Mean: ' + str(mean) + ', Standard deviation: ' + str(std) + ', Min: ' + str(mind) + ', Max: ' + str(maxd))

# Statistics option - Multiple

# lst = geTable.geneTable(int(numFIEntry.get()), './origin.csv')

# total_rows = len(lst)
# total_columns = len(lst[0])
#
# labels = []
# index = 0
# for i in range(total_rows):
# 	for j in range(total_columns):
# 		statLabel = tk.Label(second_frame, font=('Times New Roman', 10, 'bold'), text=lst[i][j])
# 		labels.append(statLabel)
#         labels[index].grid(row=i + 23, column=j)
#         index +=1

# CSV option
csvLabel = tk.Label(second_frame, text="CSV filename: ", font = ("Times New Roman", 10))
csvdotLabel = tk.Label(second_frame, text=".csv ", font = ("Times New Roman", 10))
csvEntry = tk.Entry(second_frame,bd=3, width = 15)
csvButt = tk.Button(second_frame, font = ("Times New Roman", 10),text="Export", command=exportCSV)


# Add formCombo click function

root.mainloop()
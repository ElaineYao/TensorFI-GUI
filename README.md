# TensorFI-GUI: An automated fault-injection tool in TensorFlow based on [TensorFI](https://github.com/DependableSystemsLab/TensorFI).
## 1. Supported Platforms
UNIX platform with Tensorflow v1
## 2. Dependencies
You have to install [TensorFI](https://github.com/DependableSystemsLab/TensorFI) first. See **2. Dependencies** and **3. Installation Instructions** in TensorFI homepage.
## 3. Download

TODO

## 4. Usage Guide
TensorFI-GUI is shown as follows:

![image](https://github.com/ElaineYao/TensorFI-GUI/blob/master/Figures/TensorFI-GUI-interface.png)

### 4.1 Steps:

1. Have a trained ML program( as this saves time during injections). 
2. Fill in part 1 - **Configuration** for FI(fault injection) setting. 
3. Click the *Generate* button to get a(/some) YAML file(s) named with *test-x.yaml*, i.e., configFile. 
3. In part 2 - **Fault injection**, select the ML program and configFile(s), i.e., YAML file(s) generated in part 1. Two mode are provided, i.e., *Run* and *Debug*, and the latter allows user to get the FI log files. 
4. In part 3 - **Statistics settings**, provide the name of functions or variables in their ML program to help get the SDC rates in part 4 - ***Results**. 
5. Click *Inject* button, the whole FI process begins and SDC rates will appear in part 4 when all is done. 

*Note:* Part 1 is seperated from Part 2, which means the users can either select the *configFileName*(Part 2) right after clicking the *Generate* button in Part 1, or select the YAML file previously generated - now the user is leaving Part 1 blank.

Detailed explanation for each field is as follows:

### 4.2 Part 1 - Configuration
- **InjectMode:** 
  - errorRate: Uses the error rate specified in *Probability* to determine which operations are injected with faults
  - dynamicInstance: Injects each operation type in the program once
  - oneFaultPerRun: Perform one random injection per run
  
  *Note:* When InjectMode is *errorRate*, *Instances* and *Number* fields are disabled. When InjectMode is *dynamicInstance* or *oneFaultPerRun*, *Ops* and *Probability* fields are disabled.


- **Mode:**
  - Single: User only wants to generate one configuration file.
  - Multiple: User can set the range of *Probability* and get several YAML file. This is useful when user wants to generate a bunch of configfiles with different errorrate(*Probability*) in errorRate InjectMode to get statistic figure.
- **ScalarFaultType:**
  - None: Does not inject fault
  - Rand: Shuffle all the data items in the output of the target op into random values
  - Zero: Change the value into all zeros
  - Rand-element: Shuffle one of the data item in the output of the target op into random value
  - bitFlip-element: Single bit-flip over one data item in the output of the target op
  - bitFlip-tensor: Single bit-flip over all data items in the output of the target op
  
- **TensorFaultType:** Same as *ScalarFaultType*
- **Operations:** For now, the supported operations include: 

'ABSOLUTE', 'ADD', 'ASSIGN', 'ALL', 'ARGMAX', 'ARGMIN', 'BIASADD', 'CAST', 'COUNT-NONZERO', 'CONV2D', 'ELU', 'END', 'EQUAL', 'EXPAND-DIMS',
                                                                        'FILL', 'FLOOR-MOD', 'GREATER-EQUAL', 'IDENTITY', 'LESS-EQUAL', 'LOG', 'LRN', 'MATMUL', 'MAX-POOL', 'MEAN', 'MINIMUM', 'MUL', 'NEGATIVE', 'NOT-EQUAL', 'NOOP',
                                                                        'ONE-HOT', 'PACK', 'POW', 'RANDOM_UNIFORM', 'RANK', 'RANGE', 'REALDIV', 'RELU', 'RESHAPE', 'RSQRT', 'SIGMOID', 'SIZE', 'SHAPE', 'SOFT-MAX', 'SQUARE', 'STRIDED-SLICE',
                                                                        'SUB',  'SUM', 'SWITCH', 'TANH', 'UNPACK'

Each operation coincides with a probability. This is used for the errorRate inject mode, where the probability represents the probability that a fault will be injected into that particular operation. This is used when InjectMode is "errorRate".


- **Probability:** 
Represents the probability that a fault will be injected into that particular operation.
  - Only one blank available: This is when *Mode* is set Single. One Probability corresponds with one Operation.
  - Three blanks available: This is when *Mode* is set Multiple. One Operation corresponds with a list of Probability. The 1st blank(from left to right) is for start value, the 2nd blank is for end value and the 3rd blank is for step value.
  
  Example: 
  
  ![image](https://github.com/ElaineYao/TensorFI-GUI/blob/master/Figures/Ops%26Prob.png)
  
  Then user can get 6 YAML files named with *test-x.yaml*, in which the ABSOLUTE operation is 0.1, 0.2, 0.3, 0.4, 0.5, 0.6 respectively, so that the user can analyze the SDC rates under operations with increasing probability.
  
  *Note:* 
  1. For **each** operation with certain probability(ies), user must click *Add* button. 
  2. When *Mode* is *Multiple*, make sure for each operation, the number of Probability(i.e., the number of YAML files generated) must be the same.
  
  Example:
  
  If the user want to add ABSOLUTE operation and ADD operation.
  
   ![image](https://github.com/ElaineYao/TensorFI-GUI/blob/master/Figures/Ops%26Prob.png)
  
   ![image]()
   
   However, this following **doesn't work** as the range(0.1, 0.6, 0.1) will generate 6 YAML files, while the range(0.2, 0.6, 0.1) only generates 5 YAML files.
   
   ![image](https://github.com/ElaineYao/TensorFI-GUI/blob/master/Figures/Ops%26Prob.png)
   
   ![image]()
   
  
- **Instances:**
- **Number:**
- **Seed:**
- **SkipCount:**

### 4.3 Part 2 - Fault injection
- **Source file:**
- **configFileName:**
- **Mode:**
- **disableInjection:**
- **logDir:**
- **logLevel:**
- **name:**
- **fiPrefix:**

### 4.4 Part 3 - Statistics settings:
- **Correct Prediction:**
- **Number of injections:**
- **Feed key:**
- **Feed value:**
- **Test set(X):**
- **Test set(Y):**

### 4.5 Part 4 - Results
- **SDC rates:**


The project is still in progess.

# TensorFI-GUI: An automated fault-injection tool in TensorFlow based on [TensorFI](https://github.com/DependableSystemsLab/TensorFI).
## 1. Supported Platforms
UNIX platform with Tensorflow v1
## 2. Dependencies
You have to install [TensorFI](https://github.com/DependableSystemsLab/TensorFI) first. See **2. Dependencies** and **3. Installation Instructions** in TensorFI homepage.
## 3. Usage Guide
TensorFI-GUI is shown as follows:

![image](https://github.com/ElaineYao/TensorFI-GUI/blob/master/Figures/TensorFI-GUI-interface.png)

### Steps:

1. Have a trained ML program( as this saves time during injections). 
2. Fill in part 1 - **Configuration** for FI(fault injection) setting. 
3. Click the *Generate* button to get a(/some) YAML file(s) named with *test-x.yaml*, i.e., configFile. 
3. In part 2 - **Fault injection**, select the ML program and configFile(s), i.e., YAML file(s) generated in part 1. Two mode are provided, i.e., *Run* and *Debug*, and the latter allows user to get the FI log files. 
4. In part 3 - **Statistics settings**, provide the name of functions or variables in their ML program to help get the SDC rates in part 4 - ***Results**. 
5. Click *Inject* button, the whole FI process begins and SDC rates will appear in part 4 when all is done. 

*Note:* Part 1 is seperated from Part 2, which means the users can either select the *configFileName*(Part 2) right after clicking the *Generate* button in Part 1, or select the YAML file previously generated - now the user is leaving Part 1 blank.

Detailed explanation for each field is as follows:

### Part 1 - Configuration
- **InjectMode:**
- **Mode:**
- **ScalarFaultType:**
- **TensorFaultType:**
- **Ops:**
- **Probability:**
- **Instances:**
- **Number:**
- **Seed:**
- **SkipCount:**

### Part 2 - Fault injection
- **Source file:**
- **configFileName:**
- **Mode:**
- **disableInjection:**
- **logDir:**
- **logLevel:**
- **name:**
- **fiPrefix:**

### Part 3 - Statistics settings:
- **Correct Prediction:**
- **Number of injections:**
- **Feed key:**
- **Feed value:**
- **Test set(X):**
- **Test set(Y):**

### Part 4 - Results
- **SDC rates:**


The project is still in progess.

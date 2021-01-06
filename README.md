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
  
   ![image](https://github.com/ElaineYao/TensorFI-GUI/blob/master/Figures/Ops%26Prob_Right.png)
   
   The above setting works.
   
   However, this following **doesn't work** as the range(0.1, 0.6, 0.1) will generate 6 YAML files, while the range(0.2, 0.6, 0.1) only generates 5 YAML files.
   
   ![image](https://github.com/ElaineYao/TensorFI-GUI/blob/master/Figures/Ops%26Prob.png)
   
   ![image](https://github.com/ElaineYao/TensorFI-GUI/blob/master/Figures/Ops%26Prob_Wrong.png)
   
  
- **Instances:** Shares the same operations as *Operations*. Each operation coincides with a number representing the *Number* of instances it occurs in a given model. This is used when InjectMode is "dynamicInstance". The sum of all these numbers is used when InjectMode is "oneFaultPerRun".
- **Number:** Each operation coincides with a number representing the *Number* of instances it occurs in a given model. 
- **Seed:** Seed the randomness of the fault injection. Fault injection will be random if unspecified. The default value is 1000.
- **SkipCount:** Representing the number of operations to skip at the beginning of the program before beginning injecting fault. The default value is 0.
### 4.3 Part 2 - Fault injection
- **Source file:** The path of the ML program to be injected. User can choose it by *Select* button.
- **configFileName:** The path of the configuration file(s), i.e., `test-x.yaml`. User can choose it by *Select* button, which supports selecting multiple files by clicking with *Ctrl*.
- **Mode:**
  - Run: Choose it when user don't care about the logfiles.
  - Debug: This is helpful when user wants to get the logfiles for debugging. When in 'Debug' mode, four other fields have to be completed, i.e., *logDir*, *logLevel*, *name*, *fiPrefix*.
- **disableInjection:** 
  - True: Disable fault injections
  - False: The default value is False, and hence injections are enabled.
- **logDir:** Log directory for the Fault log. 
- **logLevel:** Logging level {DEBUG=10, INFO=20, ERROR=30}
- **name:** Each fault injector is optionally assigned a name string, which is used in debug logging. 
- **fiPrefix:** This is the prefix to attach to all fault injection nodes inserted by TensorFI, for easy identification in the graph (e.g., with TensorBoard). 

### 4.4 Part 3 - Statistics settings:
- **Correct Prediction:** Name of the array that records the boolean values by comparing the true label with the predicted label in test set. 

  Example: `correct_pred = tf.equal(tf.argmax(logits, 1), tf.argmax(one_hot_y, 1))`
  
  where `tf.argmax(logits, 1)` represents the index of label(i.e., value of handwriting number) with the greatest probability during prediction, while `tf.argmax(one_hot_y, 1)` is the index of true label.

  If the value of correct_pred is `(True, True, False, True, ....)`, then we know that the model correctly predicts the 1st, 2nd and 4th image but fails to predict the 3rd one. 

  Here we should fill `correct_pred` in **Correct Prediction**.

- **Number of injections:** *SDC rates* in Part 4 are reported after lots of repeated injections, say 1000 or even 10000 and more. *Note* that since we will randomly choose 10 inputs in test sets for injection, the **actual** number of injections is *10 times* as the user fill in. If the user want 10000 injections, they need to fill in 1000 in the blank.
- **Feed key:** Refers to the *key* of *feed_dict* required in variable of **Correct Prediction**. Each *Feed key* coincides with a *Feed value*. 

  Example: 
  ```
  # Neural network model
  ...
  # x is the input to NN, y is the gold standard data(correct output)
  one_hot_y = tf.one_hot(y, 10)
  logits = LeNet(x)
  ...
  correct_pred = tf.equal(tf.argmax(logits, 1), tf.argmax(one_hot_y, 1))
  ```
  If users want to call `correct_pred`, they should write `correct = sess.run(correct_pred, feed_dict={y: y_test, x: X_test})`.
  
  There are two keys in the dictionary, i.e., `x` and `y`. 
  
  *Note*: User has to click *Add* button *every time* they want to add a key-value pair, which is similar to add Operations-Probability pair.

- **Feed value:** In the above case, there are two corresponding values, i.e., `y_test` and `X_test`.

  Demo: 
  
  To add the above key-value pairs
  
  
  *Note*: The add order doesn't matter.
  
- **Test set(X):**
- **Test set(Y):**

### 4.5 Part 4 - Results
- **SDC rates:**


The project is still in progess.

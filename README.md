# Cyber Threat Intelligence (CTI) Reports_Report_Analyzer_UI

**Program Design Purpose**: This project is a sub project (visualization) of NCL “Towards Automated and Large-scale Cyber Attack Reconstruction with APT Reports” (CTI Report Analyzer) Project. The CTI Report Analyzer is aimed to provide an automated platform for researchers and analysts to expedite their understanding and significantly reduce their turnaround time in addressing cyberthreats.

[TOC]

### Introduction

Cyber Threat Intelligence (CTI) reports are valuable sources that researchers and analysts seek to have a deeper understanding of the current APT activities and the cyberthreat landscape. These reports are used to obtain insights of vulnerabilities and their associated attack techniques.

The CTI Report Analyzer Visualization will create App and Web based UI for NCL customer use and monitor the process to convert the rich details found in CTI reports to reconstruct a dynamic environment. It is a group programming project which aims to let National Cybersecurity R&D Laboratory (NCL) interns can pick up the knowledge about CTI report, API events, python UI development and webpage design. Then create a Application and Web which NCL user can use it to control and monitor their CTI report analysis process. (As shown below ) 

###### Program design purpose diagram

![](doc/img/design.png)

CTI Report Analyzer UI view: 

![](doc/img/CTI_rpt.gif)

`version 0.12`



------

### Program Design

The CTI report analyzer UI project is aimed to provide two kinds of user interface which also NCL customer can directly control and monitor their CTI report analysis progress. The program workflow is shown below:

![](doc/img/workflow.png)

The CTI report Analyzer UI contents 7 main modules

1. CTI Report Analyzer UI App Module: Main program running on user’s local computer to init other module with individual threading. 
2. Data Manger Module: Process all the input data checking, converting and pre-processing for the CTI report user uploaded. 
3. Application UI module: The main UI module user to upload the CTI report, Config the report analysis parameters, monitor report analysis process and check the result. 
4. Communication manager module: The communication module to handle the data updating and data transfer (such as report upload). 
5. Web page UI module: the Web page with the same function as the Application UI module. 
6. Web host module: The Web Host program to handle the user control on the UI and provide same function as the data manager.
7. Control Hub Adapter: The main control hub use to collect data from the CTI report analyzer and the data base. 

The main page for each module is shown below:

![](doc/img/userInterface.png)



------

### Program setup 

###### Development Environment : python 3.7.4

###### Additional Lib/Software Need

1. **wxPython** : https://docs.wxpython.org/index.html

   ```
   Install: pip install wxPython
   ```

2. Hardware Needed : None


###### Program Files List 

| Program File | Execution Env | Description   |
| ------------ | ------------- | ------------- |
| src/uiRun.py | python 3      | main UI frame |



------

#### Program Usage

###### Program Execution 

```
python uiRun.py
```

###### Load packets data from file 





------

#### Problem and Solution

Refer to `doc/ProblemAndSolution.md`



------

> Last edit by LiuYuancheng(liu_yuan_cheng@hotmail.com) at 14/01/2022


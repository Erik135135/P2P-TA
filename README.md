# P2P-TA
P2P-TA is an open-source P2P trading algorithm made in EU funded SENDER project. The primary purpose of operating a P2P electricity market for a prospective demonstration site. It is also designed to give participants an experience of how a decentralised P2P market can provide possible economic gains. Additionally, the design of the results is made end-user friendly to recruit more consumers or producers to the test areas.  


## Requirements

Download Anaconda

Download Python-IDE (example Pycharm, Spyder etc.)

## Setup

### Step 1 

Download the P2P-TA, by clicking on code up in the right corner and click download P2P-TA.zip

### Step 2

In the terminal go to the directory of the project, and create the P2P-TA enviroment by writing:

``` conda env create -f environment.yaml ```

Later, when the environment file is updated, e.g. changed or edited dependency, run:

``` conda env create -f environment.yaml --force ```

For development and running commands activate conda environment:

``` conda activate P2P-TA ```

### Step 3

Run the P2P-TA with standard settings

``` python app.py ```

## Input data

Go to the folder data and open Input_data.xlsx. In the sheet "Overview" one will have different fields to fill in. 

The two first columns are called "Energy data API adress PV" and "Energy data API adress demand" - In this fields one should put the http:// adress to the API, if one want to connect with API.
Format of API has to be: 

[{"date": "2022-08-22 10:00:00+00:00", "l1": 547.742, "l2": 639.216, "q05": 181.704, "q10": 232.255, "q15": 293.373, "q20": 319.562, "q25": 380.39, "q30": 440.164, "q35": 464.59, "q40": 491.484, "q45": 537.989, "q50": 547.742, "q55": 595.791, "q60": 610.801, "q65": 672.016, "q70": 759.91, "q75": 759.324, "q80": 893.444, "q85": 995.338, "q90": 1135.609, "q95": 1312.909}, {"date": "2022-08-22 10:05:00+00:00", "l1": 547.097, "l2": 609.17, "q05": 181.36, "q10": 231.613, "q15": 288.516, "q20": 315.206, "q25": 381.523, "q30": 422.154, "q35": 440.567, "q40": 471.667, "q45": 506.35, "q50": 547.097, "q55": 584.809, "q60": 610.241, "q65": 663.123, "q70": 748.486, "q75": 757.243, "q80": 896.829, "q85": 988.393, "q90": 1157.147, "q95": 1309.066}, {"date": "2022-08-22 10:10:00+00:00", "l1": 545.983, "l2": 567.927, "q05": 177.994, "q10": 237.219, "q15": 

In the third column one has to select the energy source of the your data "Energy data source (API/Excel)". In this case sett the column to API if you have your data in API, and Excel if one has it in the Excel format.

For excel format please insert the data 











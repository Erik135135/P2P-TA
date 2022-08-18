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

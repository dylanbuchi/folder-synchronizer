# folder-synchronizer

A program that synchronizes two folders in one-way: source and replica.


-------


## Installation

**1** Clone this repository or download the source code.

**2** Install the required dependencies by running `pip install -r requirements.txt` in the project directory.

---
## Usage

Run the program by executing `python src/main.py` in the project directory. You can also specify the source and replica folders, the synchronization interval (in minutes) and log file location using the command line arguments. If you don’t specify arguments, the program will run with its default values.

```
python src/main.py --source="/path/to/source" --replica="/path/to/replica" --sync_interval=5 --log="/path/to/log-file.log"

```

---

## Getting Help

To display a help message with information about the available options and arguments, run the program with the `-h` or `--help` option:

```
usage: 
main.py [-h] [--source SOURCE] [--replica REPLICA] [--sync_interval SYNC_INTERVAL]
               [--log LOG]

Sync two folders one-way: source and replica

options:
-h, --help                      show this help message and exit
--source SOURCE                 Path to the source folder
--replica REPLICA               Path to the replica folder
--sync_interval SYNC_INTERVAL
                                Interval between syncs in minutes
--log LOG                       Path to the log file
```

## Author

- Website - [Dylan Buchi](https://dylanbuchi.com/)
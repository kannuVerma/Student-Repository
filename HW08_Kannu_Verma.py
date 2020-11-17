""" Author: Kannu Verma """

from datetime import datetime, timedelta
from typing import Tuple, Iterator
import os
from prettytable import PrettyTable


""" return a tuple with three values """ 
def date_arithmetic() -> Tuple[datetime, datetime, int]:
    # calculate Date three days after Feb 27, 2020
    three_days_after_02272020:datetime = datetime.strptime("Feb 27, 2020", "%b %d, %Y") + timedelta(days=3)
     # calculate Date three days after Feb 27, 2019
    three_days_after_02272019:datetime = datetime.strptime("Feb 27, 2019", "%b %d, %Y") + timedelta(days=3)
   
    # calculate No. of days passed between Feb 1, 2019 and Sept 30, 2019
    #days_passed_09302019_02012019:int = datetime(2019, 9, 30) - datetime(2019, 2, 1)
    date2:datetime = datetime.strptime("Feb 1, 2019", "%b %d, %Y")
    date1:datetime = datetime.strptime("Sep 30, 2019", "%b %d, %Y")
    
    days_passed_09302019_02012019:int = date1 - date2

    return three_days_after_02272020, three_days_after_02272019, days_passed_09302019_02012019
    

""" Reading text files with a fixed number of fields, separated by a specific character """
def file_reader(path, fields, sep=',', header=False) -> Iterator[Tuple[str]]:
    # open file
    try:
        file = open(path)
    except FileNotFoundError:
        print("File does not exist", path)
    
    words:list = []
    line_num:int = 0
    
    # read file line by line
    for line in file.readlines():
        line_num += 1
        if header:
            header = False
            continue
        tuples = tuple(line.strip("\n").split(sep))
        if(len(tuples) != fields):
            raise ValueError(f"{path} has {len(tuples)} fields on line {line_num} but expected {fields}")
        yield tuples


""" scanning and summarizing the files """
class FileAnalyzer:
    
    def __init__(self, directory: str) -> None:
        self.directory: str = directory
        self.files_summary: Dict[str, Dict[str, int]] = dict() 
        self.analyze_files()

    """  populate the summarized data into self.files_summary """
    def analyze_files(self) -> None:
        # scanning directory for python files
        try:
            files = [file for file in os.listdir(self.directory) if file.endswith('.py')] # get all python files
            all_files_info = list() 
            # read all files
            for f in files:
                file_name = os.path.join(self.directory, f)
                try:
                    file = open(file_name)
                except FileNotFoundError:
                    print("File Not found: "+ file_name)

                # reading file
                with file:
                    file_read = file.read()
                    lines = file_read.strip("\n").split("\n")

                    num_classes = 0
                    num_functions = 0

                    for l in lines:
                        if l.strip(' ').startswith('class'):
                            num_classes += 1
                        elif l.strip(' ').startswith('def'):
                            num_functions += 1
            
                all_files_info.append([file_name, ('Classes',num_classes), ('Functions',num_functions), ('Lines', len(lines)), ('Characters', len(file_read))])
            self.files_summary = all_files_info

        except FileNotFoundError:
            print("Directory Not found: "+ self.directory)


    """ print out the pretty table from the data stored in the self.files_summary """ 
    def pretty_print(self) -> None:
        pt = PrettyTable(field_names=['File', 'Classes', 'Functions', 'Lines', 'Characters'])
        for file_name, num_classes, num_functions, lines, characters in self.files_summary:
            pt.add_row([file_name, num_classes[1], num_functions[1], lines[1], characters[1]])

        print(pt)


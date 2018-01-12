#!/usr/bin/env python3

import sys
import re


#purpose: process text file after table tag has been removed
#input:   text file and the current table number
#ouput:   csv fomratted text file

def processTable(table_result,table_number):

    tr_result = re.findall(r'<tr\s*>(.*?)</tr\s*>\s*', str(table_result), re.M|re.I|re.S)

    for idx,x in enumerate(tr_result):
        if x==" ":
            tr_result[idx] = "<td> </td>"



    td = []
    max_col = 0


    header = re.findall(r'<th\s*>(.*?)</th\s*>\s*', str(table_result), re.M|re.I|re.S)
    td.append(header)
    
    max_col = len(header)
    
    for each in tr_result:
        val = re.findall(r'<td[\w\s=";:-]*\s*>(.*?)</td\s*>', str(each), re.M|re.I|re.S)
        td.append(val)
        if len(val) > max_col:
            max_col = len(val)



    td_final = [x for x in td if x != []]
    
    #ensures all the rows have the maximum column number
    for idx, val in enumerate(td_final):
        if len(val) < max_col:
            difference = max_col - len(val)
            for x in range(0, difference):
                td_final[idx].append('')


    # removes extra spaces
    for x in td_final:
        for idx, y in enumerate(x):
            x[idx] = y.strip()
    

    final_data = ""

    for x in td_final:
        final_data += ",".join(x)
        final_data += "\n"


    data = ""
    if table_number >= 2:
        data +="\n"
    data += "TABLE " + str(table_number) + ":\n"
    
    data += final_data
    

    return data


#purpose: input the data through stdin and output the data through stdout

def main():
    
    
    file = ""
    for line in sys.stdin:
        file += line


    # removes uncessary newlines and extraspaces
    text = " ".join(file.split())

    table_res  = re.findall(r'<table>(.*?)</table>', str(text), re.IGNORECASE)

    output_data = ""
    for idx, x in enumerate(table_res):
        output_data += processTable(x,idx+1)

    sys.stdout.write(output_data)



if __name__ == '__main__':
    main();

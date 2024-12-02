import json
import sys
from xml.etree.ElementTree import iterparse
import pandas as pd
import os
from recordTypes import *

namesToRemove = ['HKQuantityTypeIdentifier', 'HKDataType', 'HKCategoryTypeIdentifier']

def generateCSV(output_dict):
    """Creates a new folder and moves specified CSV files into it."""
    folder_name = 'HealthKitExport'
    folder_path = os.path.dirname(os.path.abspath(__file__))+'/'

    # Create the new folder
    if not os.path.exists(folder_path+folder_name):
        os.makedirs(folder_path+folder_name)
        print(f"Folder '{folder_path+folder_name}' created successfully.")
    else:
        print(f"Folder '{folder_path+folder_name}' already exists.")

    # Move CSV files
    for recordType, df in output_dict.items():
        for names in namesToRemove:
            recordType = recordType.replace(names, "")
            recordType[:20]
        df.to_csv(folder_path+folder_name+'/'+f'{recordType}.csv', index=False)
        print(recordType+" created in "+folder_name)



def parseHealthKit(xmlFile='export.xml',output_type='csv', structure_type='grouped', filter=False, return_record_types=False):
    """
    This program takes a healthkit XML file and formats it into usable CSV files.

    First you can dictate the way that the CSV data is grouped:
    1. Get all of the XML data as a single large CSV by setting the structure_type to 'unprocessed'.
    2. Get each record type from the XML file as a seperate CSV by leaving the structure_type as the default 'grouped'.

    The data can also be filtered using the 'filter' variable. Either pass in a list of Record Types you would like to return
    or input the Record Types you need as a list of lists from the recordTypes.py file.
    For example:
        parseHealthKit(filter=[bodyMeasurmentRecordTypes,audioexposureRecordTypes])

    You can also get a printed list of each record type in your xml file by setting return_record_types equal to 'True'.

    This will simply print all of the record types and exit the script.

    Check gitlab for more info.
    """
    df = pd.DataFrame(columns=['type', 'sourceName','sourceVersion','unit','creationDate','startDate','endDate','value'])
    dict_list = []

    #This builds our DataFrame and handles some common errors.
    folder_path = os.path.dirname(os.path.abspath(__file__))+'/'
    for _, elem in iterparse(folder_path+xmlFile):
        if elem.tag == 'Record':
            if 'unit' not in elem.attrib:
                elem.attrib['unit'] = 'N/A'
            if 'sourceVersion' not in elem.attrib:
                elem.attrib['sourceVersion'] = 'N/A'
            try:
                dict_list.append({'type': elem.attrib['type'],
                                  'sourceName': elem.attrib['sourceName'],
                                  'sourceVersion': elem.attrib['sourceVersion'],
                                  'unit': elem.attrib['unit'],
                                  'creationDate': elem.attrib['creationDate'],
                                  'startDate': elem.attrib['startDate'],
                                  'endDate': elem.attrib['endDate'],
                                  'value': elem.attrib['value']
                                  })
            except KeyError:
                print("Could Not Parse: ",elem.attrib)
                pass

            elem.clear()
    df = pd.DataFrame(dict_list)

    #Returns a list of record types if the user selects this option.
    if return_record_types == True:
        grouped_df = df['type']
        grouped_df = df.groupby('type')

        for key, item in grouped_df:
            print(key)
        exit()
    else:
        pass
    
    #This section either bypasses the filter, or uses a list of lists to filter the dataframe.
    if filter == False:
        df = pd.DataFrame(dict_list)
    else:
        combinedlists = []
        for list in filter:
            combinedlists.extend(list)
        df = df[df['type'].isin(combinedlists)]



    
    #This section lets a user choose some different formats and output types.
    if structure_type == 'grouped':
        grouped_df = df['type']
        grouped_df = df.groupby('type')
        
        output_dict = {}
        for key,recordType in grouped_df:
            output_df = df[df['type'] == f'{key}']
            output_dict[f'{key}'] = output_df

        if output_type == 'csv':
            generateCSV(output_dict)
        elif output_type == 'df':
            return output_dict

    elif structure_type == 'unprocessed':
        if output_type == 'csv':
            output_dict = {}
            output_dict['export'] = df
            generateCSV(output_dict)
        elif output_type == 'df':
            return df

    else:
        print('Invalid value given for the structure_type.\nUse "grouped" or "unprocessed".')

def main():
    while True:
        xmlFile = input("What is the name of the XML file you are trying to parse?\nIf it is the default 'export.xml' you can just leave this blank.\n")
        folder_path = os.path.dirname(os.path.abspath(__file__))+'/'
        if xmlFile == '':
            xmlFile = 'export.xml'
        if os.path.exists(folder_path+xmlFile):
            print(f"{xmlFile} is a valid file.")
            break
        else:
            print(f"{xmlFile} is not a valid file. Please enter a valid file.")

    while True:
        structure_type = input("How do you want to load files?\nYour options are 'grouped' and 'unprocessed'.\n").strip()
        if structure_type in ['grouped','unprocessed']:
            break
        else:
            print("Unrecognized parameter. Please enter a valid parameter.")
    print("Success. Running script...")
    parseHealthKit(xmlFile=xmlFile,structure_type=structure_type)

if __name__ == "__main__":
    main()
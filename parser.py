import sys
import re
import json
from pathlib import Path


def read_file_arr(filename):
    with open(filename) as f:
        output_line = list(map(lambda line: line.rstrip(), f.readlines()))
    return output_line


def delete_space_in_arr(arr):
    return(list(map(lambda line: re.sub(r' ', '', line), arr)))


def get_ability_arr(arr):
    output_line = []
    for line in arr:
        if (re.search(r'^\t"', line)
           and not re.search(r'"Version"', line)
           and not re.search(r'"dota_base_ability"', line)
           and not re.search(r'"ability_base"', line)):
            output_line.append(line.strip().strip('"'))
    return output_line


def get_id_arr(arr):
    output_line = []
    for line in arr:
        if (re.search(r'"ID"', line)
           and not re.search(r'"0"', line)):
            splited_arr = re.sub(r'\t\t*', '\t', line.strip()).split('\t')
            ability_id = re.sub(r'//.*', '', splited_arr[1]).strip('"')
            output_line.append(ability_id)
    return output_line

def make_json(input_ability_arr, input_id_arr):
    output_json = {}
    sorted_output_json = {}
    for i, ability in enumerate(input_ability_arr):
        output_json[input_id_arr[i]] = ability
    sorted_tuple =  sorted(output_json.items(), key=lambda x:int(x[0]))
    for tuple in sorted_tuple:
        sorted_output_json[tuple[0]] = tuple[1]
    return sorted_output_json


def write_json(output_dict, output_file_name):
    with open(output_file_name, mode='w') as f:
        json.dump(output_dict, f, indent=2)

if __name__ == '__main__':
    print("---pars  start---")
    input_file_name = sys.argv[1]

    ## init erace space 
    line_arr = read_file_arr(input_file_name)
    line_not_space_arr = delete_space_in_arr(line_arr)

    ## get arr
    ability_arr = get_ability_arr(line_not_space_arr)
    id_arr = get_id_arr(line_not_space_arr)

    ## make json and sort
    ability_ids_dict = make_json(ability_arr, id_arr)

    ## write
    filepath = Path(__file__).resolve().parent / 'ability_ids.json'
    write_json(ability_ids_dict, filepath)

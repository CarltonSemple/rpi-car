import json

'''
dictionary: keys are arrays
'''
def save_dictionary_to_csv(dictionary, filepath):
    with open(filepath, 'wb') as file:
        line_arrays = [[]]
        for i in range(_get_longest_array_length(dictionary)):
            line_arrays.append([])

        for key,array in dictionary.items():
            for line_index in range(len(array)):
                line_arrays[line_index].append(array[line_index])
            # add empty spaces for the rest of the column
            for line_index in range(len(array), len(line_arrays)):
                line_arrays[line_index].append('_ _ _ _ _ _ _ _ _ _ _ _ _ _')
        print(json.dumps(line_arrays))

        for line_index in range(len(line_arrays)):
            file.write(bytes(_array_to_csv_line(line_arrays[line_index]), 'UTF-8'))
            file.write(bytes('\n', 'UTF-8'))

def _get_longest_array_length(arrays_dictionary):
    longest = 0
    for key,array in arrays_dictionary.items():
        if (len(array) > longest):
            longest = len(array)
    return longest

def _array_to_csv_line(input_array):
    return ','.join(input_array) 
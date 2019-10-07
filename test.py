import subprocess

#Configuration
read_set_of_Data_from_end = False
number_of_computercores = 4

# pfahltest.txt
#filename = 'pfahltest.txt'
#x_value_position_in_dataset, y_value_position_in_dataset = 0,1
#maximal_length_of_side = 4.0
#minimal_length_of_side = 0.5
#maximal_difference_between_comparable_sides_in_percent = 0.25

# newtest.dat
filename = 'newtest.dat'
id_position_in_dataset = 0
x_value_position_in_dataset, y_value_position_in_dataset = 1, 2
maximal_length_of_side = 45.0
minimal_length_of_side = 2.5
maximal_difference_between_comparable_sides_in_percent = 0.01

# zuerich_selected.txt
#filename = 'zuerich_selected.txt'
#x_value_position_in_dataset, y_value_position_in_dataset = 1,0
#read_set_of_Data_from_end = True
#maximal_length_of_side = 10.0
#minimal_length_of_side = 1.0
#maximal_difference_between_comparable_sides_in_percent = 0.05

transferfilename = "data.csv"
returnfilename = "rectangles_and_buildings.csv"


with open(transferfilename, 'w') as transferfile:
    with open(filename, 'r') as datafile:
        for line in datafile:
            data = line.split()
            if len(data) >= x_value_position_in_dataset and len(data) >= y_value_position_in_dataset:
                try:
                    if read_set_of_Data_from_end:
                        transferfile.write(data[id_position_in_dataset] + ' ' + data[len(data)-x_value_position_in_dataset-1] + ' ' + data[len(data)-y_value_position_in_dataset-1] + '\n')
                    else:
                        transferfile.write(data[id_position_in_dataset] + ' ' + data[x_value_position_in_dataset] + ' ' + data[y_value_position_in_dataset] + '\n')
                except ValueError:
                    pass

# Argumente: filename, returnfilename, maximal_length_of_side, minimal_length_of_side, maximal_difference_between_comparable_sides_in_percent, number_of_computercores
print(subprocess.call(["python", "postaar_algorithm.py", str(transferfilename), '-o', str(returnfilename), '-smax', str(maximal_length_of_side), '-smin', str(minimal_length_of_side), '-diff',str(maximal_difference_between_comparable_sides_in_percent), '-cores', str(number_of_computercores)]))



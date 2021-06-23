import csv

def export_to_csv(output_list, location):
    """
    Exports given move list to csv
    """
    file = open(location, 'w')

    with file:
        write = csv.writer(file, lineterminator = '\n')
        write.writerows(output_list)
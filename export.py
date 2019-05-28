import csv
import parser
import config

export_file = config.FILE_NAME
export_fields = config.CSV_FIELDS


def csv_dict_writer(path, fieldnames, data):
    with open(path, "w", newline='') as out_file:
        writer = csv.DictWriter(out_file, delimiter=',', fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


if __name__ == '__main__':
    csv_dict_writer(export_file, export_fields, parser.goods())


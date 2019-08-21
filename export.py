import csv
import parser
import config

import_file = config.IMPORT_FILE_NAME
export_file = config.EXPORT_FILE_NAME
export_fields = config.CSV_MAJOR_FIELDS


def csv_dict_writer(path, fieldnames, data):
    with open(path, "w", newline='') as out_file:
        writer = csv.DictWriter(out_file, delimiter=',', fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def csv_dict_reader(path):
    with open(path, "r", newline='') as in_file:
        reader = csv.DictReader(in_file, delimiter=',')
        return list(reader)


if __name__ == '__main__':

    # Read goods from chameleon
    chameleon_data = parser.goods()

    # Read goods from prom
    prom_data = csv_dict_reader(import_file)

    # Output csv
    export_data = []

    for chameleon_row in chameleon_data:
        for prom_row in prom_data:
            if chameleon_row[export_fields[1]] == prom_row[export_fields[1]]:


                name_goods = prom_row[export_fields[0]]
                id_goods = prom_row[export_fields[1]]
                price_goods = chameleon_row[export_fields[2]]
                rest_goods = chameleon_row[export_fields[4]]

                goods_availability = '+'
                if rest_goods == 0:
                    goods_availability = '3'

                row = dict.fromkeys(export_fields)
                row[export_fields[0]] = name_goods #name_goods
                row[export_fields[1]] = id_goods #id_goods

                row[export_fields[2]] = price_goods #price_goods
                row[export_fields[3]] = goods_availability #goods_availability
                row[export_fields[4]] = rest_goods #rest_goods

                # print(row)
                export_data.append(row)



    # Write goods from chameleon
    csv_dict_writer(export_file, export_fields, export_data)




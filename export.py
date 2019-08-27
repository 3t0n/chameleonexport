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
            if chameleon_row[export_fields[1]] == prom_row[export_fields[1]] and prom_row[export_fields[8]] != '':

                name_goods        = prom_row[export_fields[0]]
                id_goods          = prom_row[export_fields[1]]
                desc_goods        = prom_row[export_fields[2]]
                price_goods       = chameleon_row[export_fields[3]]
                currency_goods    = prom_row[export_fields[4]]
                unit_goods        = prom_row[export_fields[5]]
                goods_availability= chameleon_row[export_fields[6]]
                rest_goods        = chameleon_row[export_fields[7]]
                external_id_goods = prom_row[export_fields[8]]

                #print(chameleon_row)

                row = dict.fromkeys(export_fields)
                row[export_fields[0]] = name_goods
                row[export_fields[1]] = id_goods
                row[export_fields[2]] = desc_goods
                row[export_fields[3]] = price_goods
                row[export_fields[4]] = currency_goods
                row[export_fields[5]] = unit_goods
                row[export_fields[6]] = goods_availability
                row[export_fields[7]] = rest_goods
                row[export_fields[8]] = external_id_goods

                #print(row)
                export_data.append(row)



    # Write goods from chameleon
    csv_dict_writer(export_file, export_fields, export_data)




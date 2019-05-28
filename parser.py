import postgresql
import config
import json

connection_string = config.CONNECTION_STRING
export_fields = config.CSV_FIELDS


def goods():
    with postgresql.open(connection_string) as db:
        goods = []
        query = '''
        SELECT 
            name_goods, 
            id_goods, 
            (SELECT (price_new/100.0)::numeric(12,2) FROM spring.doc_reprice_table where id_goods = goods.id_goods 
                ORDER BY date_doc DESC LIMIT 1),
            (SELECT name_unit FROM front.unit WHERE is_default = true AND id_goods = goods.id_goods),
            (SELECT bar_code FROM front.bar_codes WHERE id_goods = goods.id_goods LIMIT 1), 
            type_goods,
            (SELECT rest::numeric(12,0) FROM front.rest where id_goods = goods.id_goods 
                ORDER BY time_rest DESC LIMIT 1),
            id_group,
            (SELECT name_group FROM front.group_goods WHERE id_group = goods.id_group)
        FROM front.goods 
        ORDER BY id_goods'''

        try:
            result = db.query(query)

            for line in result:
                name_goods = line[0].replace('"', '""')
                id_goods = line[1]
                goods_queries = name_goods + ', ' + name_goods.replace(' ', ',')

                price_goods = line[2]
                if price_goods is None or price_goods == 0:
                    # Skip if price unknown
                    continue

                name_unit = line[3]
                if name_unit == 'гр':
                    name_unit = 'г'

                bar_code = line[4]
                type_goods = line[5]

                rest_goods = line[6]
                if rest_goods is None:
                    rest_goods = 0

                id_group = line[7]
                name_group = line[8]

                goods_availability = '+'
                if rest_goods == 0:
                    goods_availability = '3'


                goods_description = ''

                goods_image = ''

                row = dict.fromkeys(export_fields)
                row[export_fields[0]] = name_goods
                row[export_fields[1]] = id_goods
                row[export_fields[2]] = goods_queries
                row[export_fields[3]] = goods_description
                row[export_fields[4]] = 'r'
                row[export_fields[5]] = price_goods
                row[export_fields[11]] = 'UAH'
                row[export_fields[15]] = name_unit
                row[export_fields[19]] = goods_image
                row[export_fields[20]] = goods_availability
                row[export_fields[21]] = rest_goods
                row[export_fields[22]] = name_group
                row[export_fields[24]] = id_group
                row[export_fields[33]] = id_goods

                goods.append(row)

                # break

        except Exception as e:
            print('goods(): {}'.format(e))

        print(goods)

        return goods

import postgresql
import config
import json

connection_string = config.CONNECTION_STRING
export_fields = config.CSV_MAJOR_FIELDS


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
            (SELECT SUM(rest)::numeric(12,0) FROM front.v_rest where id_goods = goods.id_goods) as rest,
            id_group,
            (SELECT name_group FROM front.group_goods WHERE id_group = goods.id_group)
        FROM front.goods 
        ORDER BY id_goods'''

        try:
            result = db.query(query)

            for line in result:
                name_goods = line[0].replace('"', '""')
                id_goods = str(line[1])
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
                # try:
                #     with open('/Users/skipper/Documents/Projects/python/googlesearch/' + name_goods + '.txt', 'r') as file:
                #         goods_description = file.read()
                # except IOError as e:
                #     print('description(): {}'.format(e))


                goods_image = ''
                # try:
                #     with open('/Users/skipper/Documents/Projects/python/googleimages/' + name_goods + '/Scrapper_1.json', 'r') as file:
                #         goods_image = json.loads(file.read())[5]
                # except IOError as e:
                #     print('image(): {}'.format(e))

                row = dict.fromkeys(export_fields)
                row[export_fields[0]] = name_goods
                row[export_fields[1]] = id_goods
                row[export_fields[2]] = goods_description
                row[export_fields[3]] = price_goods
                row[export_fields[4]] = 'UAH'
                row[export_fields[5]] = name_unit
                row[export_fields[6]] = goods_availability
                row[export_fields[7]] = rest_goods
                row[export_fields[8]] = id_goods

                #print(row)
                goods.append(row)

                # break

        except Exception as e:
            print('Exception: goods(): {}'.format(e))

        #print(goods)

        return goods

import postgresql
import config

from apscheduler.schedulers.background import BackgroundScheduler

export_template = config.CSV_TEMPLATE
export_line = config.CSV_LINE
connection_string = config.CONNECTION_STRING


def goods():
    with postgresql.open(connection_string) as db:
        goods = ''
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
                if price_goods is None:
                    price_goods = 0

                name_unit = line[3]
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

                goods += export_line.format(name_goods,
                                            id_goods,
                                            goods_queries,
                                            price_goods,
                                            name_unit,
                                            goods_availability,
                                            rest_goods,
                                            name_group,
                                            id_group,
                                            id_goods)
        except Exception as e:
            print('goods(): {}'.format(e))

        message = export_template.format(goods)
        print(message)

        return message

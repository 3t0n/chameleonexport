import parser
import config

export_file = config.FILE_NAME


if __name__ == '__main__':
    goods = parser.goods()

    file = open(export_file, 'w')
    file.write(goods)
    file.close()


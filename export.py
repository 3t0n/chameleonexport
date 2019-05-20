import parser
import config
import time

from apscheduler.schedulers.background import BackgroundScheduler

export_file = config.FILE_NAME
start = time.time()


def scheduler_handler():
    goods = parser.goods()

    file = open(export_file, 'w')
    file.write(goods)
    file.close()


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    # scheduler.add_job(scheduler_handler, 'interval', seconds=5)
    scheduler.add_job(scheduler_handler, 'cron', hour=21, minute=15, second=0)
    scheduler.start()

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

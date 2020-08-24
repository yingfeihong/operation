from tornado.ioloop import IOLoop
from tornado.options import define, options
from common.scheduler import scheduler_jobs
from core.init.cron import CronServerInit
from base.log.log_manager import LogManager as Log

define("CONFIG", default='local', help="Config Name", type=str)

if __name__ == '__main__':
    options.parse_command_line()
    CronServerInit.init(options.CONFIG)
    Log.logger.info("Cron Config:%s  listen.........", options.CONFIG)
    scheduler_jobs().start()
    IOLoop.instance().start()

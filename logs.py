import logging


logging.basicConfig(format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
                    # stream=sys.stdout,
                    level=logging.INFO,
                    filename='bot.log',
                    filemode="w"
                    )
main_logger = logging.getLogger('PB')

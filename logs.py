import logging


logging.basicConfig(format='[%(name)s] %(message)s',
                    # stream=sys.stdout,
                    level=logging.INFO,
                    filename='bot.log',
                    filemode="w"
                    )
main_logger = logging.getLogger('PB')

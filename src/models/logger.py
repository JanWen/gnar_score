import logging

logging.basicConfig(filename="model_log.txt",
                    filemode='w',
                    # format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

log = logging.getLogger('model')

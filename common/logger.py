import logging


logger = logging.getLogger(__name__)

logging.basicConfig(filename='my_log.txt', level=logging.DEBUG)

logger.setLevel(logging.DEBUG)



handler = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

handler.setFormatter(formatter)

logger.addHandler(handler)

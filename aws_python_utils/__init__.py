import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-10s %(levelname)-8s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging
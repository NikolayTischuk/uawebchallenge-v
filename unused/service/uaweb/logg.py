import logging

class Loggs:
    logger = None
    
    def __init__(self):
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler = logging.FileHandler('logger.log')
        handler.setFormatter(formatter)
        
        self.logger = logging.getLogger('parsing')
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
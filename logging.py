# 나중에 쓰기 위해 미리 저장

import os
import logging
import pathlib
from logging.handlers import TimedRotatingFileHandler

# 로그 파일 생성 위치 정해주기 -> 수정 필요!
file_path = pathlib.Path(__file__).parent.parent.absolute() / 'log' / '~~.log'
# 로그 폴더가 존재하는지 확인 후 없으면 생성
os.makedirs(file_path.parents[0], exist_ok=True)

# logger instance 생성
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler()
file_handler = TimedRotatingFileHandler(file_path, when="midnight", encoding='utf-8')

# formmater 생성
formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
file_handler.suffix = "%Y%m%d"

# logger instance에 handler 설정
logger.addHandler(stream_handler)
logger.addHandler(file_handler)


# logger.debug('debug')
# logger.info('info')
# logger.warning('warning')
# logger.error('error')
# logger.critical('critical')
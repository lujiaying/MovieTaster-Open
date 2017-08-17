# -*- coding: utf-8 -*-
'''
Easy and basic configure for print log
'''

__author__ = 'lujiaying@baidu.com'

import logging
from logging.handlers import RotatingFileHandler
import os

################################
# Conf to edit
################################
# To print into screen if DebugConf is True
DebugConf = True
#DebugConf = False


################################
# Init Loggers
################################
data_analysis_logger = logging.getLogger('data_analysis')
data_process_logger = logging.getLogger('data_process')
model_logger = logging.getLogger('model')


################################
# Init Handlers
################################
formatter = logging.Formatter('[%(asctime)s][pid:%(process)s] %(module)s.%(funcName)s: %(levelname)s: %(message)s')

# StreamHandler for print log to console
hdr = logging.StreamHandler()
hdr.setFormatter(formatter)
hdr.setLevel(logging.DEBUG)

# RotatingFileHandler
## Set log dir
abs_path = os.path.dirname(os.path.abspath(__file__))
abs_father_path = os.path.dirname(abs_path)
log_dir_path = abs_father_path + '/log'
#log_dir_path = abs_path + '/log'
if not os.path.exists(log_dir_path):
    os.makedirs(log_dir_path)

## Specific file handler
fhr_ana = RotatingFileHandler('%s/analysis.log'%(log_dir_path), maxBytes=10*1024*1024, backupCount=3)
fhr_ana.setFormatter(formatter)
fhr_ana.setLevel(logging.DEBUG)

## Specific file handler
fhr_pro = RotatingFileHandler('%s/process.log'%(log_dir_path), maxBytes=10*1024*1024, backupCount=3)
fhr_pro.setFormatter(formatter)
fhr_pro.setLevel(logging.DEBUG)

## Specific file handler
fhr_model = RotatingFileHandler('%s/model.log'%(log_dir_path), maxBytes=10*1024*1024, backupCount=3)
fhr_model.setFormatter(formatter)
fhr_model.setLevel(logging.DEBUG)


################################
# Add Handlers
################################
data_analysis_logger.addHandler(fhr_ana)
if DebugConf:
    data_analysis_logger.addHandler(hdr)
    data_analysis_logger.setLevel(logging.DEBUG) #lowest debug level for logger
else:
    data_analysis_logger.setLevel(logging.ERROR) #lowest debug level for logger

data_process_logger.addHandler(fhr_pro)
if DebugConf:
    data_process_logger.addHandler(hdr)
    data_process_logger.setLevel(logging.DEBUG)
else:
    data_process_logger.setLevel(logging.ERROR)

model_logger.addHandler(fhr_model)
if DebugConf:
    model_logger.addHandler(hdr)
    model_logger.setLevel(logging.DEBUG)
else:
    model_logger.setLevel(logging.ERROR)


if __name__ == '__main__':
    '''
    Usage:
    from tools.log_tools import data_process_logger as logger
    logger.debug('debug debug')
    '''
    data_analysis_logger.debug('My logger configure success')
    data_analysis_logger.info('My logger configure success')
    data_analysis_logger.error('analysis error test')

    data_process_logger.info('My logger configure success~~')
    data_process_logger.error('process error test test')

    model_logger.info('Ohhh model')
    model_logger.error('error model')

import datetime
import os
import sys

def log(exception, file='error_logs.txt'):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    log = '[{}] File "{}", line {}, {}\n'.format(str(datetime.datetime.now()), fname, str(exc_tb.tb_lineno), str(exc_type))
    open(file, 'w').write(log)
    print('Error Written to, '+file+', Log: '+log)

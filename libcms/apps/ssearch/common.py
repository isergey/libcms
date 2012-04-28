# -*- coding: utf-8 -*-
import re
date_full_main = re.compile(ur'^\d{8}$',re.UNICODE) # CCYYMMDD 19890314
date_full_main_ext = re.compile(ur'^\d{4}-\d{2}-\d{2}$',re.UNICODE) # CCYY-MM-DD 1989-03-14
date_low_main_1 = re.compile(ur'^\d{4}-\d{2}$',re.UNICODE) # CCYY-MM 1989-03
date_low_main_2 = re.compile(ur'^\d{4}$',re.UNICODE) # CCYY 1989
date_low_main_3 = re.compile(ur'^\d{2}$',re.UNICODE) # CC 19

date_short_main = re.compile(ur'^\d{6}$',re.UNICODE) # YYMMDD 890314
date_short_main_ext = re.compile(ur'^\d{2}-\d{2}-\d{2}$',re.UNICODE) # YY-MM-DD 89-03-14


date_short_main_1 = re.compile(ur'^-\d{4}$',re.UNICODE) # -YYMM -8903
date_short_main_ext_1 = re.compile(ur'^-\d{2}-\d{2}$',re.UNICODE) # YY-MM-DD 89-03-14

date_short_main_2 = re.compile(ur'^-\d{2}$',re.UNICODE) # -YY -89

date_short_main_3 = re.compile(ur'^--\d{4}$',re.UNICODE) # --MMDD --0314
date_short_main_ext_3 = re.compile(ur'^--\d{2}-\d{2}$',re.UNICODE) # --MM-DD --03-14

date_short_main_4 = re.compile(ur'^--\d{2}$',re.UNICODE) # --MM --03

date_short_main_5 = re.compile(ur'^---\d{2}$',re.UNICODE) # ---DD ---14


import datetime
def to_datetime(date):
    if date_full_main.match(date):
        #print date, u' - Основной формат (Полное)'
        date =  datetime.datetime.strptime(date, '%Y%m%d')
    elif date_full_main_ext.match(date):
        #print date, u' - Расширенный формат (Полное)'
        date =  datetime.datetime.strptime(date, '%Y-%m-%d')
    elif date_low_main_1.match(date):
        #print date, u' - Основной формат (c уменьшенной точноcтью)'
        date =  datetime.datetime.strptime(date, '%Y-%m')
    elif date_low_main_2.match(date):
        #print date, u' - Основной формат (с уменьшенной точноcтью)'
        date =  datetime.datetime.strptime(date, '%Y')
    elif date_low_main_3.match(date):
        date =  datetime.datetime(year=int(date +u'00'), month=1, day=1)
        #print date, u' - Основной формат (с уменьшенной точноcтью)'
    elif date_short_main.match(date):
        date =  datetime.datetime.strptime(date, '%y%m%d')
        #print date, u' - Основной формат (Сокращенное)'
    elif date_short_main_ext.match(date):
        date =  datetime.datetime.strptime(date, '%y-%m-%d')
        #print date, u' - Расширенный формат (Сокращенное)'

    elif date_short_main_1.match(date):
        date =  datetime.datetime.strptime(date, '-%y%m')
        #print date, u' - Основной формат (Сокращенное)'
    elif date_short_main_ext_1.match(date):
        date =  datetime.datetime.strptime(date, '-%y-%m')
        #print date, u' - Расширенный формат (Сокращенное)'

    elif date_short_main_2.match(date):
        date =  datetime.datetime.strptime(date, '-%y')
        #print date, u' - Основной формат (Сокращенное)'

    elif date_short_main_3.match(date):
        date =  datetime.datetime.strptime(date, '--%m%d')
        date = datetime.datetime(datetime.datetime.now().year, month=date.month, day=date.day)
        #print date, u' - Основной формат (Сокращенное)'
    elif date_short_main_ext_3.match(date):
        date =  datetime.datetime.strptime(date, '--%m-%d')
        date = datetime.datetime(datetime.datetime.now().year, month=date.month, day=date.day)
        #print date, u' - Расширенный формат (Сокращенное)'

    elif date_short_main_4.match(date):
        date =  datetime.datetime.strptime(date, '--%m')
        date = datetime.datetime(datetime.datetime.now().year, month=date.month, day=date.day)
        #print date, u' - Основной формат (Сокращенное)'
    elif date_short_main_5.match(date):
        date =  datetime.datetime.strptime(date, '---%d')
        date = datetime.datetime(datetime.datetime.now().year, month=date.month, day=date.day)
        #print date, u' - Основной формат (Сокращенное)'
    else:
        return None
    return date

def resolve_date(date):
    """
    Распознает даты и периоды в формате ГОСТ 7.64-90
    Период указывается так: [(дата начала)-] или [(дата начала)-(дата конца)]: [1989-2012], [19890314-]
    Возвращает datetime, кортеж (datetime,) - если указано только начало периода, или (datetime,datetime) - начало и конец
    test_dates = [
        u'18890314',
        u'1989-03-14',
        u'1989-03',
        u'1989',
        u'19',
        u'890314',
        u'89-03-14',
        u'-8903',
        u'-89-03',
        u'-89',
        u'--0314',
        u'--03-14',
        u'--03',
        u'---14',
        u'[1989]',
        u'[1989-]',
        u'[19890314-]',
        u'[1989-03-14-]',
        u'[1989-2012]',
        u'[---14----14]',
        u'[--03-14---03-14]',
    ]
    """
    try:
        year = int(date)
        return datetime.datetime(year=year, month=1, day=1)
    except ValueError:
        pass


    if date.startswith('[') and date.endswith(']'): # указан период или приблизительная дата
        date = date[1:-1]
        if  len(date) < 2:
            raise ValueError(u'Wong date field format: ' + date)

        result_date = to_datetime(date)
        if not result_date:

            if date[-1] == '-': # похоже на период без даты окончания
                result_date = to_datetime(date[:-1]) # может быть дата в одном из форматов?
                if not result_date:
                    raise ValueError(u'Wong date field format: ' + date)
                else:
                    return (result_date)
            else:
                tire_count = date.count(u'-') # количестов тире должно быть нечетным число, если указан период с началом и концом
                if not tire_count % 2: # количество тире четное, а это плохо
                    raise ValueError(u'Wong date field format: ' + date)
                # число тире нечетное. Значит указали диапозон с началом и концом
                else:
                    middle_tire_count = (tire_count / 2) + 1 # порядковый номер тире, находящегося посередине
                    tire_counter = 0 # cx

                    # ищем тире которая разделяет даты и добавляем в диапозон
                    for i, char in enumerate(date):
                        if char == '-': tire_counter += 1
                        if tire_counter == middle_tire_count:
                            start_date = to_datetime(date[:i])
                            end_date = to_datetime(date[i + 1:])
                            if start_date and end_date:
                                return (start_date, end_date)
                            else:
                                raise ValueError(u'Wong date field format: ' + date)
        else:
            return result_date
    else: # значит должна быть указана дата
        result_date = to_datetime(date)
        if not result_date:
            raise ValueError(u'Wong date field format: ' + date)
        else:
            return result_date

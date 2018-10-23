"""
    @Project : DB.py
    @Auther  : Kanrin
    @Date    : 2018/02/28
"""
# -*- coding=utf-8 -*-
import os
import pickle


class Database(object):
    def __init__(self, dbname):
        self.dbname = dbname
        try:
            self.db = pickle.load(open(os.path.join('data', self.dbname + '.bin'), 'rb+'))
        except:
            self.db = []
            self.__error('1100', '! init database')

    # write data when the class destory
    def __del__(self):
        self.__write()

    # insert the value
    # data   <class list>
    def insert(self, data):
        if(len(self.db) > 0):
            if not self.__check_value(data):
                self.db.append(data)
            else:
                self.__error('1002', data)
                return False
        else:
            self.__error('1003')
            return False

    # select the value where titles
    # titles   <class list>
    def select(self, titles):
        if not self.__check_args(titles):
            return False
        index_t = self.__check_title(titles)
        if len(index_t) == 0:
            # can't find the value
            self.__error('1004')
            return False
        else:
            r = {}
            for index in index_t:
                a = []
                for db in self.db:
                    a.append(db[index])
                a.remove(self.db[0][index])
                r[self.db[0][index]] = a
            return r

    # create a database
    # titles   <class list>
    def create(self, titles):
        if not self.__check_args(titles):
            return False
        if len(self.db) == 0:
            self.db.append(titles)
            return True
        else:
            self.__error('1001')
            return False

    # update a data
    # titles   <class list>
    # values   <class list>
    def update(self, titles, values, id):
        if not self.__check_args(titles):
            return False
        if not self.__check_args(values):
            return False
        realid = id + 1
        indexs = self.__check_title(titles)
        if len(titles) == len(values):
            for i in range(0, len(titles)):
                self.db[realid][indexs[i]] = values[i]
        else:
            self.__error('1005')
            return False

    # delete datas by id
    # ids   <class list>
    def delete(self, ids):
        if not self.__check_args(ids):
            return False
        for i in range(0, len(ids)):
            realid = int(ids[i]) + 1
            if len(self.db) > realid:
                del self.db[realid]
            else:
                self.__error('1008', str(realid))

    # wirte the db in *.bin file
    def __write(self):
        try:
            pickle.dump(self.db, open(os.path.join('data', self.dbname + '.bin'), 'wb+'))
        except IOError as e:
            self.__error('1101')
            print(e)

    # check the title in db frist line
    def __check_title(self, title):
        if isinstance(title, list):
            index_t = []
            for t in title:
                if t in self.db[0]:
                    index_t.append(self.db[0].index(t))
            return index_t
        elif isinstance(title, str):
            if title in self.db[0]:
                return self.db[0].index(title)
            else:
                self.__error('1006')
                return False
        else:
            self.__error('1006')
            return False

    def __check_value(self, data):
        if isinstance(data, list):
            return data in self.db
        else:
            for db in self.db:
                if data in db:
                    return True
            return False

    def __check_args(self, arg):
        return isinstance(arg, list)

    # print error msg
    def __error(self, code, info=''):
        infos = {
            '1001': 'database exsit',
            '1002': 'the repeat value',
            '1003': 'the database hasn\'t title',
            '1004': 'the value not found',
            '1005': 'value error',
            '1006': 'the title not found',
            '1007': 'error type',
            '1008': 'can\'t found the id',
            '1100': 'database load failed',
            '1101': 'database write failed'
        }
        print('\033[31m [ERROR]: Database [', self.dbname, '] ->',infos[code], info, '!\033[0m')

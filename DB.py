# -*- coding=utf-8 -*-
import os
import pickle

class Database:
    def __init__(self, dbname):
        self.dbname = dbname
        try:
            self.db = pickle.load(open(os.path.join('data', self.dbname + '.bin'), 'rb+'))
        except:
            self.db = []
            self.__error('1100', '! init database')

    def insert(self, data):
        if(len(self.db) > 0):
            if not self.__check_value(data):
                self.db.append(data)
                self.__write()
            else:
                self.__error('1002', data)
                return False
        else:
            self.__error('1003')
            return False

    def select(self, titles):
        title = titles.split(',')
        index_t = self.__check_title(title)
        if len(index_t) == 0:
            # 未找到值
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

    def create(self, titles):
        if len(self.db) == 0:
            self.db.append(titles)
            self.__write()
            return True
        else:
            self.__error('1001')
            return False

    def update(self, titles, values, id):
        title = titles.split(',')
        value = values.split(',')
        realid = id + 1
        indexs = self.__check_title(title)
        if len(title) == len(value):
            for i in range(0, len(title)):
                self.db[realid][indexs[i]] = value[i]
            self.__write()
        else:
            self.__error('1005')
            return False

    def delete(self, ids):
        id = ids.split(',')
        for i in range(0, len(id)):
            realid = int(i + 1)
            if len(self.db) > realid:
                del self.db[realid]
            else:
                self.__error('1008', str(realid))
        self.__write()

    def __write(self):
        try:
            pickle.dump(self.db, open(os.path.join('data', self.dbname + '.bin'), 'wb+'))
        except IOError as e:
            self.__error('1101')
            print(e)

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

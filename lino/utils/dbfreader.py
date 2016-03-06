# Copyright 2003-2009-2016 Luc Saffre
# License: BSD (see file COPYING for details)

# Based on original work by Lars Garshol
# http://www.garshol.priv.no/download/software/python/dbfreader.py

# modified by Luc Saffre who is interested in support for Clipper
# rather than FoxPro support.
"""
What's the format of a Clipper .dbf file?
http://www.the-oasis.net/clipper-12.html#ss12.4

http://www.clicketyclick.dk/databases/xbase/format/
"""
from __future__ import print_function
from builtins import hex
from builtins import str
from builtins import object

import datetime
from dateutil import parser as dateparser


import sys
import string

codepages = {
    '\x01': "cp437",
    '\x02': "cp850",
}

# --- Useful functions


def unpack_long(number):
    return ord(number[0]) + 256 * (ord(number[1]) + 256 * (ord(number[2]) +
                                                           256 * ord(number[3])))


def unpack_long_rev(number):
    return ord(number[3]) + 256 * (ord(number[2]) + 256 * (ord(number[1]) +
                                                           256 * ord(number[0])))


def unpack_int(number):
    return ord(number[0]) + 256 * ord(number[1])


def unpack_int_rev(number):
    return ord(number[1]) + 256 * ord(number[0])


def hex_analyze(number):
    for ch in number:
        print("%s\t%s\t%d" % (hex(ord(ch)), ch, ord(ch)))

# def sort_by_key(list,key_func):
# for ix in range(len(list)):
# list[ix]=(key_func(list[ix]),list[ix])

# list.sort()

# for ix in range(len(list)):
# list[ix]=list[ix][1]

# return list

# --- A class for the entire file


class DBFFile(object):

    "Represents a single DBF file."

    HAS_MEMO_FILE = 128  # "\x80"

    versionmap = {
        "\x03": "dBASE III",
        "\x83": "dBASE III+ with memo",
        "\x8B": "dBASE IV with memo",
        "\xF5": "FoxPro with memo"
    }

    def __init__(self, filename, codepage=None):
        self.filename = filename

        infile = open(self.filename, "rb")

        # Read header

        header = infile.read(32)

        self.version = header[0]
        year = ord(header[1]) + 2000
        month = ord(header[2])
        day = ord(header[3])
        self.lastUpdate = datetime.date(year, month, day)

        self.rec_num = unpack_long(header[4:8])

        self.first_rec = unpack_int(header[8:10])

        self.rec_len = unpack_int(header[10:12])

        self.codepage = codepage  # s[header[29]]

        # Read field defs

        self.fields = {}
        self.field_list = []
        while 1:
            ch = infile.read(1)
            if ch == "\x0D":
                break
            field = DBFField(ch + infile.read(31), self)
            self.fields[field.name] = field
            self.field_list.append(field)

        infile.close()
        if self.has_memo():
            if self.version == "\x83":
                self.blockfile = DBTFile(self)
            else:
                self.blockfile = FPTFile(self)

    def has_memo(self):
        if ord(self.version) & self.HAS_MEMO_FILE:
            return True
        return False

    def has_blocksize(self):
        # FoxPro : return True
        return False

    def get_version(self):
        return DBFFile.versionmap[self.version]

    def __len__(self):
        return self.get_record_count()

    def get_record_count(self):
        return self.rec_num

    def get_record_len(self):
        return self.rec_len

    def get_fields(self):
        # return self.fields.values()
        return self.field_list

    def get_field(self, name):
        return self.fields[name]

    # --- Record-reading methods

    def open(self, deleted=False):
        self.recno = 0
        self.deleted = deleted
        self.infile = open(self.filename, "rb")
        # self.infile.read(32+len(self.fields)*32+1)
        self.infile.seek(self.first_rec)
        # self.field_list=sort_by_key(self.get_fields(),DBFField.get_pos)

    def get_next_record(self):
        values = {}
        ch = self.infile.read(1)
        self.recno += 1
        if ch == "*":
            deleted = True
            # Skip the record
            # return self.get_next_record()
        elif ch == "\x1A" or ch == "":
            return None
        else:
            deleted = False

        for field in self.field_list:
            data = self.infile.read(field.get_len())
            values[field.get_name()] = field.interpret(data)
        if deleted and not self.deleted:
            return self.get_next_record()
        return DBFRecord(self, values, deleted)

    def close(self):
        self.infile.close()
        del self.infile
        del self.deleted

    def __iter__(self):
        return self

    def __next__(self):
        rec = self.get_next_record()
        if rec is None:
            raise StopIteration
        return rec

    def fetchall(self):
        self.open()
        l = [rec for rec in self]
        self.close()
        return l


class NOTGIVEN(object):
    pass


class DBFRecord(object):

    def __init__(self, dbf, values, deleted):
        self._recno = dbf.recno
        self._values = values
        self._deleted = deleted
        self._dbf = dbf

    def deleted(self):
        return self._deleted

    def recno(self):
        return self._recno

    def __getitem__(self, name):
        return self._values[name.upper()]

    def __getattr__(self, name, default=NOTGIVEN):
        name = name.upper()
        try:
            return self._values[name]
        except KeyError:
            if default is NOTGIVEN:
                raise AttributeError(
                    "No field named %r in %s" %
                    (name, list(self._values.keys())))
            return default

    def get(self, *args, **kw):
        return self._values.get(*args, **kw)

    def __repr__(self):
        return self._dbf.filename + "#" + str(self._recno)

# --- A class for a single field


class DBFField(object):

    "Represents a field in a DBF file."

    typemap = {
        "C": "Character", "N": "Numeric",
        "L": "Logical", "M": "Memo field",
        "G": "Object", "D": "Date",
        "F": "Float", "P": "Picture"}

    def __init__(self, buf, dbf):
        pos = string.find(buf, "\x00")
        if pos == -1 or pos > 11:
            pos = 11
        self.name = buf[:pos]
        self.field_type = buf[11]
        self.field_pos = unpack_long(buf[12:16])
        self.field_len = ord(buf[16])
        self.field_places = ord(buf[17])
        self.dbf = dbf

# if self.field_type=="M" or self.field_type=="P" or \
# self.field_type=="G" :
# self.blockfile=blockfile

    def get_name(self):
        return self.name

    def get_pos(self):
        return self.field_pos

    def get_type(self):
        return self.field_type

    def get_type_name(self):
        return DBFField.typemap[self.field_type]

    def get_len(self):
        return self.field_len

    def interpret(self, data):
        if self.field_type == "C":
            if not self.dbf.codepage is None:
                data = data.decode(self.dbf.codepage)
            data = data.strip()
            #~ if len(data) == 0: return None
            if len(data) == 0:
                return ''
            return data
        elif self.field_type == "L":
            return data == "Y" or data == "y" or data == "T" or data == "t"
        elif self.field_type == "M":
            try:
                num = string.atoi(data)
            except ValueError:
                if len(data.strip()) == 0:
                    #~ return None
                    return ''
                raise Exception("bad memo block number %s" % repr(data))
            return self.dbf.blockfile.get_block(num)

        elif self.field_type == "N":
            try:
                return string.atoi(data)
            except ValueError:
                return 0
        elif self.field_type == "D":
            data = data.strip()
            if not data:
                return None
            try:
                return dateparser.parse(data)
            except ValueError as e:
                raise ValueError("Invalid date value %r (%s)" % (data, e))
            # ~ return data # string "YYYYMMDD", use the time module or mxDateTime
        else:
            raise NotImplementedError("Unknown data type " + self.field_type)

# --- A class that represents a block file


class FPTFile(object):

    "Represents an FPT block file"

    def __init__(self, dbf):
        self.dbf = dbf
        self.filename = dbf.filename[:-4] + ".FPT"
        infile = open(self.filename, "rb")
        infile.read(6)
        self.blocksize = unpack_int_rev(infile.read(2))
        infile.close()

    def get_block(self, number):
        infile = open(self.filename, "rb")
        infile.seek(512 + self.blocksize * (number - 8))  # ?

        code = infile.read(4)
        if code != "\000\000\000\001":
            return "Block %d has invalid code %s" % (number, repr(code))

        length = infile.read(4)
        length = unpack_long_rev(length)
        data = infile.read(length)
        infile.close()

        data = data.strip()
        if len(data) == 0:
            return None
        return data


class DBTFile(object):

    "Represents a DBT block file"

    def __init__(self, dbf):
        self.dbf = dbf
        self.filename = dbf.filename[:-4] + ".DBT"
        # print "DBTFile", self.filename
        self.blocksize = 512

    def get_block(self, number):
        infile = open(self.filename, "rb")
        infile.seek(512 + self.blocksize * (number - 1))
        data = ""
        while True:
            buf = infile.read(self.blocksize)
# if len(buf) != self.blocksize:
# print str(number)+":"+str(len(buf))
##                 data += buf
# break
            data += buf
            pos = data.find("\x1A")
            #pos = data.find("\x1A\x1A")
            if pos != -1:
                data = data[:pos]
                break

        infile.close()
        if not self.dbf.codepage is None:
            data = data.decode(self.dbf.codepage)
        # clipper adds "soft CR's" to memo texts. we convert them to
        # simple spaces:
        data = data.replace(u"\xec\n", "")

        # convert CR/LF to simple LF:
        data = data.replace("\r\n", "\n")

        data = data.strip()
        if len(data) == 0:
            return None
        return data

# --- A class that stores the contents of a DBF file as a hash of the
#     primary key


class DBFHash(object):

    def __init__(self, file, key):
        self.file = DBFFile(file)
        self.hash = {}
        self.key = key

        self.file.open()
        while 1:
            rec = self.file.get_next_record()
            if rec is None:
                break
            self.hash[rec[self.key]] = rec

    def __getitem__(self, key):
        return self.hash[key]

# --- Utility functions


def display_info(f):
    print(f.get_version())
    print(f.get_record_count())
    print(f.get_record_len())

    for field in f.get_fields():
        print("%s: %s (%d)" % (field.get_name(), field.get_type_name(),
                               field.get_len()))


def make_html(f, out=sys.stdout, skiptypes="MOP"):
    out.write("<TABLE>\n")

    # Writing field names
    out.write("<TR>")
    for field in f.get_fields():
        out.write("<TH>" + field.get_name())

    f.open()
    while 1:
        rec = f.get_next_record()
        if rec is None:
            break

        out.write("<TR>")
        for field in f.get_fields():
            if not field.get_type() in skiptypes:
                out.write("<TD>" + str(rec[field.get_name()]))
            else:
                out.write("<TD>*skipped*")

    f.close()
    out.write("</TABLE>\n")

if __name__ == "__main__":
    make_html(DBFFile(sys.argv[1]))

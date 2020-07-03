# SCRIVERE SOLO CARATTERI NEL RANGE
# ASCII CLASSICO [0, 127], QUINDI
# NIENTE LETTERE ACCENTATE O
# CARATTERI STRANI
from struct import pack, unpack

def dtype_str_to_char(type_name):
    if not (type(type_name) is str):
        raise TypeError("You must insert a string.")
    if type_name == 'unsigned char':
        return 'B'
    elif type_name == 'char':
        return 'c'
    elif type_name == 'signed char':
        return 'b'
    elif type_name == '_Bool':
        return '?'
    elif type_name == 'short':
        return 'h'
    elif type_name == 'unsigned short':
        return 'H'
    elif type_name == 'int':
        return 'i'
    elif type_name == 'unsigned int':
        return 'I'
    elif type_name == 'long':
        return 'l'
    elif type_name == 'unsigned long':
        return 'L'
    elif type_name == 'long long':
        return 'q'
    elif type_name == 'unsigned long long':
        return 'Q'
    elif type_name == 'float':
        return 'f'
    elif type_name == 'double':
        return 'd'
    elif type_name == 'char[]':
        return 's'
    elif type_name == 'char *':
        return 'p'
    elif type_name == 'void *':
        return 'p'
    else :
        raise ValueError("Unknown type name: " + type_name)
 
def type_size(type_name):
    if not (type(type_name) is str):
        raise TypeError("You must insert a string.")
    if type_name == 'unsigned char':
        return 1
    elif type_name == 'char':
        return 1
    elif type_name == 'signed char':
        return 1
    elif type_name == '_Bool':
        return 1
    elif type_name == 'short':
        return 2
    elif type_name == 'unsigned short':
        return 2
    elif type_name == 'int':
        return 4
    elif type_name == 'unsigned int':
        return 4
    elif type_name == 'long':
        return 4
    elif type_name == 'unsigned long':
        return 4
    elif type_name == 'long long':
        return 8
    elif type_name == 'unsigned long long':
        return 8
    elif type_name == 'float':
        return 4
    elif type_name == 'double':
        return 8
    else :
        raise ValueError("Unknown type name: " + type_name)


class Bin:
    def __init__(self, filename, truncate = False, little_endian = True):
        try:
            self._f = open(filename, "r+" + "b")
        except:
            self._f = open(filename, "wb")
            self._f.close()
            self._f = open(filename, "r+" + "b")
        self._f.seek(0)
        self._endian_char = "<" if little_endian else ">"
        if truncate:
            self._f.truncate(0)

    # Vecchia versione. La tolgo per simmetria con le funzioni di lettura.
    # Voglio che il tipo (type_str) vada specificato alla fine perché
    # voglio che di default sia unsigned char. Non cancellare questa
    # vecchia versione
    # def write(self, type_str, *vals):
    #     self._f.write(pack(self._endian_char + dtype_str_to_char(type_str) * len(vals), *vals))
    
    def write(self, val, type_str = "unsigned char"):
        self._f.write(pack(self._endian_char + dtype_str_to_char(type_str), val))
        
    def write_many(self, vals, type_str = "unsigned char"):
        self._f.write(pack(self._endian_char + dtype_str_to_char(type_str) * len(vals), *vals))

    # Vecchia versione. Non cancellare
    # def write_at(self, point, type_str, *val):
    #     self.jump_to(point)
    #     self.write(type_str, *val)

    def write_at(self, point, val, type_str = "unsigned char"):
        self.jump_to(point)
        self.write(type_str, val)
        
    def write_namy_at(self, point, vals, type_str = "unsigned char"):
        self.jump_to(point)
        self.write_many(type_str, vals)

    def write_string(self, s):
        #self._f.write(pack(self._endian_char + "c" * len(s), *tuple(a for a in s)))
        self._f.write(s.encode("ascii"))
        
    def write_string_at(self, point, s):
        self.jump_to(point)
        self.write_string(s)

    # Prima "get_value" (e tutti gli altri getters) avevano type_str come
    # penultimo argomento. Lo ho messo per ultimo di modo da evere
    # unsigned char come argomento di default. Di conseguenza ho modificato
    # anche tutti gli "write"
    def get_value(self, type_str = "unsigned char"):
        return unpack(self._endian_char + dtype_str_to_char(type_str), self._f.read(type_size(type_str)))[0]

    def get_values(self, num, type_str = "unsigned char"):
        return unpack(self._endian_char + dtype_str_to_char(type_str) * num, self._f.read(num * type_size(type_str)))

    def get_value_at(self, point, type_str = "unsigned char"):
        self.jump_to(point)
        return self.get_value(type_str)

    def get_values_at(self, point, num, type_str = "unsigned char"):
        self.jump_to(point)
        return self.get_values(num, type_str)

    def get_string(self, sz):
        ret = str()
        s = unpack(self._endian_char + "c" * sz, self._f.read(sz))
        for a in s:
            ret += str(a)[2:-1]
        return ret
        
    def get_string_at(self, point, sz):
        self.jump_to(point)
        return self.get_string(sz)

    def jump_to(self, point):
        self._f.seek(point)

    def pos(self):
        return self._f.tell()
        
    def move_by(self, size, type_str = "char"):
        self.jump_to(self.pos() + size * type_size(type_str))
    
    def size(self):
        p = self.pos()
        self._f.seek(0, 2)
        ret = self.pos()
        self.jump_to(p)
        return ret
        
    def flush(self):
        self._f.flush()
        
    def close(self):
        self._f.close()

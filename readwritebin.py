from struct import pack, unpack


def dtype_str_to_char(type_name):
    '''
    Convert the name of the type to a character code
    to be interpreted by the "struct" library.
    '''
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
    '''
    Get the size of a type in bytes.
    '''
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
    '''
    The class that manages a binary file.
    '''
    def __init__(self, filename, truncate = False, little_endian = True):
        try:
            # Does the file already exist?
            self._f = open(filename, "r+" + "b")
        except:
            # If it doesn't exist craete it.
            self._f = open(filename, "wb")
            self._f.close()
            self._f = open(filename, "r+" + "b")
        self._f.seek(0)
        self._endian_char = "<" if little_endian else ">"
        self._filename = filename
        if truncate:
            self._f.truncate(0)

    def write(self, val, type_str = "unsigned char"):
        '''
        Write a value in the current position.
        param: val
            The value you want to write
        param: type_str
            The type of the value        
        '''
        self._f.write(pack(self._endian_char + dtype_str_to_char(type_str), val))
        
    def write_many(self, vals, type_str = "unsigned char"):
        '''
        Write multiple values in the current position.
        param: vals
            The container containing the values you want to write.
            E.g.: bin_instance.write_many((6, 8, -1), "int")
        param: type_str
            The type of the values        
        '''
        self._f.write(pack(self._endian_char + dtype_str_to_char(type_str) * len(vals), *vals))

    def write_at(self, point, val, type_str = "unsigned char"):
        '''
        Write a value in the specified position.
        param: point
            The point where to write. It must be espressed in bytes.
        param: val
            The value you want to write
        param: type_str
            The type of the value        
        '''
        self.jump_to(point)
        self.write(type_str, val)
        
    def write_many_at(self, point, vals, type_str = "unsigned char"):
        '''
        Write multiple values in the current position.
        param: point
            The point where to write. It must be espressed in bytes.
        param: vals
            The container containing the values you want to write.
            E.g.: bin_instance.write_many((6, 8, -1), "int")
        param: type_str
            The type of the values        
        '''
        self.jump_to(point)
        self.write_many(type_str, vals)

    def write_string(self, s):
        '''
        Write a string in the current position.
        param: s
            The string you want to write
        '''
        self._f.write(s.encode("ascii"))
        
    def write_string_at(self, point, s):
        '''
        Write a string in the current position.
        param: point
            The point where to write. It must be espressed in bytes.
        param: s
            The string you want to write
        '''
        self.jump_to(point)
        self.write_string(s)

    def get_value(self, type_str = "unsigned char"):
        '''
        Get the value in the current position.
        param: type_str
            The type of the value
        '''
        return unpack(self._endian_char + dtype_str_to_char(type_str), self._f.read(type_size(type_str)))[0]

    def get_values(self, num, type_str = "unsigned char"):
        '''
        Get multiple values starting from the current position.
        param: num
            The number of values you want to read
        param: type_str
            The type of the value
        '''
        return unpack(self._endian_char + dtype_str_to_char(type_str) * num, self._f.read(num * type_size(type_str)))

    def get_value_at(self, point, type_str = "unsigned char"):
        '''
        Get the value in the specified position.
        param: point
            The point from where to read. It must be expressed in bytes.
        param: type_str
            The type of the value
        '''
        self.jump_to(point)
        return self.get_value(type_str)

    def get_values_at(self, point, num, type_str = "unsigned char"):
        '''
        Get multiple values starting from the specified position.
        param: point
            The point from where to read. It must be expressed in bytes.
        param: num
            The number of values you want to read
        param: type_str
            The type of the value
        '''
        self.jump_to(point)
        return self.get_values(num, type_str)

    def get_string(self, sz):
        '''
        Read a string from the current position.
        param: sz
            The size of the string
        '''
        ret = str()
        s = unpack(self._endian_char + "c" * sz, self._f.read(sz))
        for a in s:
            ret += str(a)[2:-1]
        return ret
        
    def get_string_at(self, point, sz):
        '''
        Read a string from the specified position.
        param: point
            The point from where to read. It must be expressed in bytes.
        param: sz
            The size of the string
        '''
        self.jump_to(point)
        return self.get_string(sz)

    def jump_to(self, point):
        '''
        Move the current position.
        param: point
            The point where to move. It must be expressed in bytes.
        '''
        self._f.seek(point)

    def pos(self):
        '''
        Get the position you are currently on. It is expressed in bytes.
        '''
        return self._f.tell()
        
    def move_by(self, size, type_str = "char"):
        '''
        Move from your current position by a certain quantity.
        E.g: You have just written 3 integers and you want to move back
             to the first one:
             bin_instance.move_by(-3, "int")
             or
             bin_instance.move_by(-12)
             since the size of "int" is 4 bytes.
        param: size
            The number of steps
        param: type_str
            The type to deduce the size of the step
        '''
        self.jump_to(self.pos() + size * type_size(type_str))
    
    def size(self):
        '''
        Get the size of the file in bytes
        '''
        p = self.pos()
        self._f.seek(0, 2)
        ret = self.pos()
        self.jump_to(p)
        return ret
        
    def flush(self):
        '''
        Flush the buffer
        '''
        self._f.flush()
        
    def close(self):
        '''
        Close the file
        '''
        self._f.close()

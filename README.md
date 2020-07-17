# read_write_binary_python_dummies
A simple, intuitive and very little library to read and write binary files.

It allows to manage binary files in a high-level way.

# Usage
```python
from readwritebin import Bin

binfile = Bin("myfile.bin", truncate=False, little_endian=True)

binfile.write_many((0, 2, 5, 9), "int")
binfile.move_by(-3, "int")

values = binfile.get_values(3, "int")

print(values)
```

Output:
```
(2, 5, 9)
```

---
layout: versioned
version: master
title: Storage format
---

## Storage format

**(Experimental in 1.2.0-dev)**

ds-format implements a native format "ds" (file extension ".ds") in addition to
other standard formats. This format is compatible with the most commonly used
features of NetCDF. Over NetCDF, this format has an advantage of being much
simpler and faster (up to 10 times), especially when reading or writing many
small files. Unlike NetCDF, which is editable, the ds format is inteded to be
written only once (the copy-on-write paradigm). This greatly simplifies the
format and implementation, and improves performance. The ds format can be used
by reading or writing files an extension ".ds". Existing NetCDF files can be
converted to ds with `ds select input.nc output.ds`, where `input.nc` is the
input NetCDF files and `output.ds` is the output ds file.

The format is composed of a version string, header and body, separated by a
newline character (`\n`). The version string is `ds-<x>.<y>`, where `x` and `y`
are a major and minor format version numbers. The header consists of one line
containing JSON of the metadata. In addition to the [standard
structure](../../Description), the metadata contains a number of special fields
describing where to find and how to decode the variable data.  The body is a
block of binary data directly following the header. The header and body are
separated by a single newline character (`\n`).  The body contains raw bindary
data of the variables in a sequential order. Schematically, the structure of
the format is:

```
# Three lines of the format version string, header and body.
ds = ds-<x>.<y>\n<header>\n<body>

# JSON header describing variable metadata.
header = { "<var>": <var-metadata> ... ".": <dataset-metadata> }

# Body composed of binary data.
body = <var-data>...

var-data = [<missing-bitmask>]<data>
```

where `var` is a variable name, `var-metadata` is variable metadata,
`dataset-metadata` is dataset metadata, `missing-bitmask` is a missing value
bitmask (described below) and `data` are binary variable data.

In addition to the standard variable metadata, the ds native format uses the
following properties:

| Property | Description |
| --- | --- |
| `.offset` | Data offset in bytes relative to the start of the body. |
| `.len` | Length of data in bytes, including a missing data bitmask or string lengths, if present. |
| `.type` | Data type of the variable. One of: `float32` and `float64` (32-bit and 64-bit floating-point number, resp.), `int8` `int16`, `int32` and `int64` (8-bit, 16-bit, 32-bit and 64-bit integer, resp.), `uint8`, `uint16`, `uint32` and `uint64` (8-bit, 16-bit, 32-bit and 64-bit unsigned integer, resp.), `bool` (boolean), `str` (byte string) and `unicode` (Unicode). |
| `.endian` | Endianness. `b` for big endian, `l` for little endian. |
| `.missing` | A boolean value signifying if the data array is a masked array. A bitmask of missing data is stored directly after the variable data, and is bitpacked. |

If missing values are allowed (`.missing` is true), a missing value bitmask is
stored at the variable offset. The bitmask is bitpacked, and at the end it is
padded with zeros to occupy an integer number of bytes. Bit ordering of
bitpacked values is alwyas big endian, regardless of `.endian` of the variable.

The variable data are stored directly after missing value bitmask, or at
variable offset if missing values are not allowed. They are stored as a flat
sequence of binary values in bit ordering as in `.endian`. Multi-dimensional
arrays are stored in the "C ordering" of rows and columns. Missing values are
not written.

Boolean values (type `bool`) are bitpacked, and at the end are padded with
zeros to occupy an integer number of bytes. Bit ordering of bitpacked values is
alwyas big endian, and `.endian` of boolean variables should be `b`.

Data of string arrays (type `str` and `unicode`) are stored as an array of
string lengths, followed by a sequence of the strings, encoded as UTF-8 if the
original strings are Unicode. The array of lengths is a flat array of 64-bit
unsigned integers in bit ordering as in `.endian`. The strings are stored
directly following this array as a sequence of bytes, with no separators between
the strings.

### Performance

The ds format is up 10 times faster than NetCDF, while taking the same or less
space (uncompressed). It is especially faster for reading and writing small
files. Below are results of a set of performance tests which write and read
NetCDF and ds files:

- **tiny**: one int64 variable of size 1

  `{'x': 1}`

- **small**: one int64 variable of size 1000

  `{'x': np.arange(1000)}`

- **large**: one float64 variable of size 100×1000×1000

  `{'x': np.ones(100, 1000, 1000)}`

| Test             | Time NetCDF (s) | Time ds (s) | Speed factor | Size NetCDF (MB) | Size ds (MB) | Size factor |
| ---------------- | --------------- | ----------- | ------------ | ---------------- | ------------ | ----------- |
| write tiny 100k  | 56              | 11          | 5            | 394              | 394          | 1           |
| write small 100k | 82              | 12          | 7            | 1566             | 785          | 2           |
| write large 10   | 11              | 11          | 1            | 7633             | 7633         | 1           |
| read tiny 100k   | 60              | 6           | 10           |                  |              |             |
| read small 100k  | 70              | 8           | 9            |                  |              |             |
| read large 10    | 3.3             | 2.5         | 1.3          |                  |              |             |

The factors are NetCDF realtive to ds.

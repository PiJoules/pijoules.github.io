Title: Adding Custom Builtin Functions to the Python Interpreter
Date: 2016-06-14 14:03
Category: Python
Tags: Python, Builtin Functions, C, Extension
Authors: Lenard Chan

When I have a few minutes of spare time, like if I’m on the bus heading to work or waiting for class to start, one of the things I like to do is explore the cpython source code. I want to learn how the Python interpreter works as a way to become a better Python programmer (or just a better programmer in general), and perhaps someday contribute to the development of Python in later releases.

# Objective
One of the first things I did to get more familiar with the source is add my own custom builtin functions to the interpreter. I’m not talking about making a new function in python like `def func(args)`. I’m also not talking about making an extension module in C that can be imported in python like `from my_c_module import my_c_func`. I’m talking about adding a new one of [these functions](https://docs.python.org/3/library/functions.html): functions like `sum()`, `abs()`, and `range()` that are automatically built into the langauge and do not require manually importing anything to use. I figured this would be a good way to learn more about the source since I’d be learning how the core functions, which are part of the source, are implemented and used.

The function I will be adding for this example is a simple product function which will take the product of a list of numbers, similar to sum, but with multiplying instead of adding and a starting value of 1. Now, I know the idea of a product function has been [proposed before and rejected due to low demand for the function](http://bugs.python.org/issue1093), and there are [many existing ways to impliment this function in python](http://stackoverflow.com/questions/595374/whats-the-python-function-like-sum-but-for-multiplication-prod), but this is just for learning purposes.

## Python Version
The version of python I am also working with is the first alpha version of Python 3.6.0 (more specifically, [3.6.0a1](https://docs.python.org/dev/)). The reason I am working with python 2 instead of 3 is because nearly all active development is in python 3, and the latest version of python 2 at the time (2.7.11) is only receiving bug fixes and backporting from python 3. [There is a whole PEP dedicated to why Python 2.8 will never be a thing](https://www.python.org/dev/peps/pep-0404/). You know it’s serious because the PEP number is 404. The reason I am also working with an alpha version of python 3 instead of the latest release at the time (3.5.1) is because I accidentally cloned the cpython repo from github without asserting first that the master branch contained the latest release version instead of development version.
¯\\\_(ツ)\_/¯

# How it works
Now, I kind of lied when I mentioned not making a C extension. It turns out that adding a builtin function is a lot like making a C extension for python. There are already lots of articles and documentation on the internet about making C extensions, especially [this one](http://dan.iel.fm/posts/python-c-extensions/), so I will not go into great detail about making one from scratch, just how it gets added and what changes I made to the source.

When you normally make a C extension, you add a `PyMethodDef` struct to an array of PyMethodDef structs which represent the functions you would like to expose in python space. These PyMethodDef structs is given as:

```C
struct PyMethodDef {
    const char *ml_name; /* The name of the built-in function/method */
    PyCFunction ml_meth; /* The C function that implements it */
    int ml_flags; /* Combination of METH_xxx flags, which mostly describe the args expected by the C func */
    const char *ml_doc; /* The __doc__ attribute, or NULL */
};
```

Hopefully the comments in this code, taken straight from the source, are enough to explain the individual members of the struct.

Inside `Python/bltinmodule.c`, the array of PyMethodDef structs this gets added to is:

```C
static PyMethodDef builtin_methods[] = {
    {"__build_class__", (PyCFunction)builtin___build_class__, METH_VARARGS | METH_KEYWORDS, build_class_doc},
    {"__import__", (PyCFunction)builtin___import__, METH_VARARGS | METH_KEYWORDS, import_doc},
    BUILTIN_ABS_METHODDEF
    BUILTIN_ALL_METHODDEF
    …
    {"vars",            builtin_vars,       METH_VARARGS, vars_doc},
    {NULL, NULL},
};
```

In the source, some of the array elements are given as literal structs while others like `BUILTIN_ABS_METHODDEF` are implemented as macros. You may notice that this array does not contain all builtin functions. The remaining functions like `bytearray()`, `int()`, or `str()` are actually constructors located in the `_PyBuiltin_Init`method also in `Python/bltinmodule.c`. (I don’t like using the word constructor when referencing these in python, but that’s another story.)

So, in order to add my custom builtin method, I just need to add a PyMethodDef to this array containing my function name, implementation, argument flags, and docstring.

# Implementation
All changes implemented are in my copy of the source on [Github](https://github.com/PiJoules/cpython-modified).

I decided to try and isolate my additions as much as possible from the existing source so that it would be easier to reference later by making my changes stand out. The actual implementation of my builtin product function is pretty much an exact copy of the builtin sum function with a few minor changes.

## [Custom/custom.c](https://github.com/PiJoules/cpython-modified/blob/master/Custom/custom.c)
This file contains the implementation of my product function and the wrapper for it.

The implementation (builtin_prod_impl) does the exact same stuff as builtin_sum_impl, but with the default value changed from 0 to 1, the actual addition done by PyNumber_Add changed to PyNumber_Multiply for multiplication, and Fast Addition was removed. This Fast Addition was a way to speed up addition by storing the temporary sum in C space instead of Python space. The downside of this is that you always need to check for overflow since you’re working with data types that have a limited range of values. Now this can easily, and quickly, be done by comparing the sign bit of your result against the sign bit of your two numbers that you’re adding (which the interpreter does in this fast addition). However, for multiplication, I cannot find a quick way for checking if overflow occurred that does not involve dividing the product by one of the two numbers to get the other. Regardless, I ended up just using python’s builtin objects for multiplication since they handle overflow and large numbers already.

I have not profiled this, but I am curious to see if multiplying in C and dividing to check for overflow will still outperform PyNumber_Multiply.

The wrapper (builtin_prod) essentially unpacks the arguments into the iterable and starting value for the implementation.

## [Custom/custom.h](https://github.com/PiJoules/cpython-modified/blob/master/Custom/custom.h)
This file just contains the declarations for builtin_prod_impl and builtin_prod, the docstring, and the final macro to be included in the original `builtin_methods` array.

## [Python/bltinmodule.c](https://github.com/PiJoules/cpython-modified/blob/master/Python/bltinmodule.c)
To actually my `prod()` function to the builtin functions, I just needed to add my macro to the array of builtin functions.

```C
static PyMethodDef builtin_methods[] = {
    {"__build_class__", (PyCFunction)builtin___build_class__, METH_VARARGS | METH_KEYWORDS, build_class_doc},
    {"__import__", (PyCFunction)builtin___import__, METH_VARARGS | METH_KEYWORDS, import_doc},
    BUILTIN_ABS_METHODDEF
    BUILTIN_ALL_METHODDEF
    …
    {"vars",            builtin_vars,       METH_VARARGS, vars_doc},
#ifdef USE_CUSTOM_BUILTINS
    BUILTIN_PROD_METHODDEF
#endif
    {NULL, NULL},
};
```

The `USE_CUSTOM_BUILTINS` is just a flag I can pass to the compiler that says whether or not I want to include whatever custom builtin functions I had.

## Makefile
The last thing to do was just adjust the Makefile such that it accepted this flag, and compiled the product function. Nothing big.

# Usage
After re-building python from source, I am able to use `prod()` in both the shell and from a python script.

```python
>>> prod(range(1, 6))
120
>>> prod([])  # Empty iterable, default starting value of 1
1
>>> prod(range(5))  # Zero included
0
>>> prod(range(-3, 4, 2))  # Negative numbers, positive result
9
>>> prod(range(-5, 4, 2))  # Negative numbers, negative result
-45
>>> prod((1, 2), 10)  # New starting value
20
>>> prod([2, 2**64]) == 2**65
True
```

# Conclusions
Hopefully, this serves as a nice introduction into how new builtin functions are added. Feel free to send me an email if there’s anything blatantly wrong in this article.

# Resources
[Source](https://github.com/PiJoules/cpython-modified)


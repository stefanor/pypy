"""Built-in functions, exceptions, and other objects.

Noteworthy: None is the `nil' object; Ellipsis represents `...' in slices.
"""

__builtins__['None']       = __interplevel__eval('space.w_None')
__builtins__['False']      = __interplevel__eval('space.w_False')
__builtins__['True']       = __interplevel__eval('space.w_True')
__builtins__['type']       = __interplevel__eval('space.w_type')
__builtins__['__debug__']  = True

object = __interplevel__eval('space.w_object')


# TODO Fix this later to show Ctrl-D on Unix
quit = exit = "Use Ctrl-Z (i.e. EOF) to exit."

def execfile(filename, glob=None, loc=None):
    if glob is None:
        glob = _caller_globals()
        if loc is None:
            loc = _caller_locals()
    elif loc is None:
        loc = glob
    f = file(filename)
    try:
        source = f.read()
    finally:
        f.close()
    #Don't exec the source directly, as this loses the filename info
    co = compile(source, filename, 'exec')
    exec co in glob, loc

def raw_input():
    import sys
    return sys.stdin.readline()   # XXX review

def input():
    return eval(raw_input())


def sum(sequence, total=0):
    # must forbid "summing" strings, per specs of built-in 'sum'
    if isinstance(total, str): raise TypeError
    for item in sequence:
        total = total + item
    return total

def _iter_generator(callable_, sentinel):
    """ This generator implements the __iter__(callable,sentinel) protocol """
    while 1:
        result = callable_()
        if result == sentinel:
            return
        yield result

def enumerate(collection):
    'Generates an indexed series:  (0,coll[0]), (1,coll[1]) ...'     
    i = 0
    it = iter(collection)
    while 1:
        yield (i, it.next())
        i += 1

def apply(function, args, kwds={}):
    """call a function (or other callable object) and return its result"""
    return function(*args, **kwds)

def map(function, *collections):
    """does 3 separate things, hence this enormous docstring.
       1.  if function is None, return a list of tuples, each with one
           item from each collection.  If the collections have different
           lengths,  shorter ones are padded with None.

       2.  if function is not None, and there is only one collection,
           apply function to every item in the collection and return a
           list of the results.

       3.  if function is not None, and there are several collections,
           repeatedly call the function with one argument from each
           collection.  If the collections have different lengths,
           shorter ones are padded with None
    """

    if len(collections) == 0:
        raise TypeError, "map() requires at least one sequence"

    elif len(collections) == 1:
        #it's the most common case, so make it faster
        if function is None:
            return list(collections[0])
        else:
            return [function(x) for x in collections[0]]
    else:
       res = []
       idx = 0   
       while 1:
          cont = 0     #is any collection not empty?
          args = []
          for collection in collections:
              try:
                 elem = collection[idx]
                 cont = cont + 1
              except IndexError:
                 elem = None
              args.append(elem)
          if cont:
              if function is None:
                 res.append(tuple(args))
              else:
                 res.append(function(*args))
          else:
              return res
          idx = idx + 1

def filter(function, collection):
    """construct a list of those elements of collection for which function
       is True.  If function is None, then return the items in the sequence
       which are True."""

    if function is None:
        res = [item for item in collection if item]
    else:
        res = [item for item in collection if function(item)]

    if type(collection) is tuple:
       return tuple(res)
    elif type(collection) is str:
       return "".join(res)
    else:
       return res

def zip(*collections):
    """return a list of tuples, where the nth tuple contains every
       nth item of each collection.  If the collections have different
       lengths, zip returns a list as long as the shortest collection,
       ignoring the trailing items in the other collections."""

    if len(collections) == 0:
        raise TypeError, "zip() requires at least one sequence"
    res = []
    idx = 0
    while 1:
        try:
            elems = []
            for collection in collections:
                elems.append(collection[idx])
            res.append(tuple(elems))
        except IndexError:
            break
        idx = idx + 1
    return res

def reduce(function, l, *initialt):
    """ Apply function of two arguments cumulatively to the items of
        sequence, from left to right, so as to reduce the sequence to a
        single value.  Optionally begin with an initial value."""

    if initialt:
       initial, = initialt
       idx = 0
    else:
       try:
          initial = l[0]
       except IndexError:
          raise TypeError, "reduce() of empty sequence with no initial value"
       idx = 1
    while 1:
       try:
         initial = function(initial, l[idx])
         idx = idx + 1
       except IndexError:
         break
    return initial

def isinstance(obj, klass_or_tuple):
    try:
        objcls = obj.__class__
    except AttributeError:
        objcls = type(obj)
    if issubclass(klass_or_tuple.__class__, tuple):
       for klass in klass_or_tuple:
           if issubclass(objcls, klass):
              return 1
       return 0
    else:
       try:
           return issubclass(objcls, klass_or_tuple)
       except TypeError:
           raise TypeError, "isinstance() arg 2 must be a class or type"

def range(x, y=None, step=1):
    """ returns a list of integers in arithmetic position from start (defaults
        to zero) to stop - 1 by step (defaults to 1).  Use a negative step to
        get a list in decending order."""

    if y is None: 
            start = 0
            stop = x
    else:
            start = x
            stop = y

    if step == 0:
        raise ValueError, 'range() arg 3 must not be zero'

    elif step > 0:
        if stop <= start: # no work for us
            return []
        howmany = (stop - start + step - 1)/step

    else:  # step must be < 0, or we would have raised ValueError
        if stop >= start: # no work for us
            return []
        howmany = (start - stop - step  - 1)/-step

    arr = [None] * howmany  # this is to avoid using append.

    i = start
    n = 0
    while n < howmany:
        arr[n] = i
        i += step
        n += 1

    return arr

# min and max could be one function if we had operator.__gt__ and
# operator.__lt__  Perhaps later when we have operator.

def min(*arr):
    """return the smallest number in a list"""

    if not arr:
        raise TypeError, 'min() takes at least one argument'

    if len(arr) == 1:
        arr = arr[0]

    iterator = iter(arr)
    try:
        min = iterator.next()
    except StopIteration:
        raise ValueError, 'min() arg is an empty sequence'

    for i in iterator:
        if min > i:
            min = i
    return min

def max(*arr):
    """return the largest number in a list"""

    if not arr:
        raise TypeError, 'max() takes at least one argument'

    if len(arr) == 1:
        arr = arr[0]

    iterator = iter(arr)
    try:
        max = iterator.next()
    except StopIteration:
        raise ValueError, 'max() arg is an empty sequence'

    for i in iterator:
        if max < i:
            max = i
    return max

def divmod(x, y):
    return x//y, x%y

def cmp(x, y):
    """return 0 when x == y, -1 when x < y and 1 when x > y """
    if x < y:
        return -1
    elif x == y:
        return 0
    else:
        return 1

def vars(*obj):
    """return a dictionary of all the attributes currently bound in obj.  If
    called with no argument, return the variables bound in local scope."""

    if len(obj) == 0:
        return _caller_locals()
    elif len(obj) != 1:
        raise TypeError, "vars() takes at most 1 argument."
    else:
        try:
            return obj[0].__dict__
        except AttributeError:
            raise TypeError, "vars() argument must have __dict__ attribute"

def hasattr(ob, attr):
    try:
        getattr(ob, attr)
        return True
    except AttributeError:
        return False

def callable(ob):
    for c in type(ob).__mro__:
        if '__call__' in c.__dict__:
            return True
    else:
        return False

def dir(*args):
    """dir([object]) -> list of strings

    Return an alphabetized list of names comprising (some of) the attributes
    of the given object, and of attributes reachable from it:

    No argument:  the names in the current scope.
    Module object:  the module attributes.
    Type or class object:  its attributes, and recursively the attributes of
        its bases.
    Otherwise:  its attributes, its class's attributes, and recursively the
        attributes of its class's base classes.
    """
    if len(args) > 1:
        raise TypeError("dir expected at most 1 arguments, got %d"
                        % len(args))
    if len(args) == 0:
        local_names = _caller_locals().keys() # 2 stackframes away
        local_names.sort()
        return local_names

    import types
    def _classdir(klass):
        """Return a dict of the accessible attributes of class/type klass.

        This includes all attributes of klass and all of the
        base classes recursively.

        The values of this dict have no meaning - only the keys have
        meaning.  
        """
        Dict = {}
        try:
            Dict.update(klass.__dict__)
        except AttributeError: pass 
        try:
            # XXX - Use of .__mro__ would be suggested, if the existance
            #   of that attribute could be guarranted.
            bases = klass.__bases__
        except AttributeError: pass
        else:
            try:
                #Note that since we are only interested in the keys,
                #  the order we merge classes is unimportant
                for base in bases:
                    Dict.update(_classdir(base))
            except TypeError: pass
        return Dict
    #End _classdir

    obj = args[0]

    if isinstance(obj, types.ModuleType):
        try:
            result = obj.__dict__.keys()
            result.sort()
            return result
        except AttributeError:
            return []

    elif isinstance(obj, (types.TypeType, types.ClassType)):
        #Don't look at __class__, as metaclass methods would be confusing.
        result = _classdir(obj).keys()
        result.sort()
        return result

    else: #(regular item)
        Dict = {}
        try:
            Dict.update(obj.__dict__)
        except AttributeError: pass
        try:
            Dict.update(_classdir(obj.__class__))
        except AttributeError: pass

        ## Comment from object.c:
        ## /* Merge in __members__ and __methods__ (if any).
        ## XXX Would like this to go away someday; for now, it's
        ## XXX needed to get at im_self etc of method objects. */
        for attr in ['__members__','__methods__']:
            try:
                for item in getattr(obj, attr):
                    if isinstance(item, types.StringTypes):
                        Dict[item] = None
            except (AttributeError, TypeError): pass

        result = Dict.keys()
        result.sort()
        return result

_stringtable = {}
def intern(s):
    # XXX CPython has also non-immortal interned strings
    if not isinstance(s, str):
        raise TypeError("intern() argument 1 must be string.")
    return _stringtable.setdefault(s,s)

def copyright():
    print 'Copyright 2003-2004 Pypy development team.\nAll rights reserved.\nFor further information see http://www.codespaek.net/pypy.\nSome materials may have a different copyright.\nIn these cases, this is explicitly noted in the source code file.'

def license():
    print \
"""
Copyright (c) <2003-2004> <Pypy development team>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

def help():
    print "You must be joking."


# ______________________________________________________________________
#
#   Interpreter-level function definitions
#

__interplevel__execfile('__builtin__interp.py')

from __interplevel__ import abs, chr, len, ord, pow, repr
from __interplevel__ import hash, oct, hex, round
from __interplevel__ import getattr, setattr, delattr, iter, hash, id
from __interplevel__ import issubclass, _pypy_get
from __interplevel__ import compile, eval
from __interplevel__ import globals, locals, _caller_globals, _caller_locals

from __interplevel__ import file
from __interplevel__ import file as open

# The following must be the last import from __interplevel__ because it
# overwrites the special __import__ hook with the normal one.
from __interplevel__ import __import__


# ________________________________________________________________________

class xrange:
    def __init__(self, start, stop=None, step=1):
        if stop is None: 
            self.start = 0
            self.stop = start
        else:
            self.start = start
            self.stop = stop
        if step == 0:
            raise ValueError, 'xrange() step-argument (arg 3) must not be zero'
        self.step = step

    def __len__(self):
        if not hasattr(self, '_len'):
            slicelength = self.stop - self.start
            lengthsign = cmp(slicelength, 0)
            stepsign = cmp(self.step, 0)
            if stepsign == lengthsign:
                self._len = (slicelength - lengthsign) // self.step + 1
            else:
                self._len = 0
        return self._len

    def __getitem__(self, index):
        # xrange does NOT support slicing
        if not isinstance(index, int):
            raise TypeError, "sequence index must be integer"
        len = self.__len__()
        if index<0:
            index += len
        if 0 <= index < len:
            return self.start + index * self.step
        raise IndexError, "xrange object index out of range"

    def __iter__(self):
        start, stop, step = self.start, self.stop, self.step
        i = start
        if step > 0:
            while i < stop:
                yield i
                i+=step
        else:
            while i > stop:
                yield i
                i+=step


# Descriptor code, shamelessly stolen to Raymond Hettinger:
#    http://users.rcn.com/python/download/Descriptor.htm
class property(object):

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc or ""   # XXX why:  or ""  ?

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self         
        if self.fget is None:
            raise AttributeError, "unreadable attribute"
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError, "can't set attribute"
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError, "can't delete attribute"
        self.fdel(obj, value)


class staticmethod(object):

    def __init__(self, f):
        self.f = f

    def __get__(self, obj, objtype=None):
        return self.f


class classmethod(object):

    def __init__(self, f):
        self.f = f

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        def newfunc(*args):
            return self.f(klass, *args)
        return newfunc

if not hasattr(dict, 'fromkeys'):
    def _fromkeys(cls, seq, value=None):
        r = cls()
        for s in seq:
            r[s] = value
        return r

    dict.fromkeys = classmethod(_fromkeys)

    del _fromkeys


# super is a modified version from Guido's tutorial
#     http://www.python.org/2.2.3/descrintro.html
# it exposes the same special attributes as CPython's.
class super(object):
    def __init__(self, type, obj=None):
        self.__thisclass__ = type
        self.__self__ = obj
        if obj is not None and isinstance(obj, type):
            self.__self_class__ = obj.__class__
        else:
            self.__self_class__ = obj
    def __get__(self, obj, type=None):
        if self.__self__ is None and obj is not None:
            return super(self.__thisclass__, obj)
        else:
            return self
    def __getattr__(self, attr):
        mro = iter(self.__self_class__.__mro__)
        for cls in mro:
            if cls is self.__thisclass__:
                break
        # Note: mro is an iterator, so the second loop
        # picks up where the first one left off!
        for cls in mro:
            try:                
                x = cls.__dict__[attr]
            except KeyError:
                continue
            if hasattr(x, '__get__'):
                x = x.__get__(self.__self__, type(self.__self__))
            return x
        raise AttributeError, attr

class complex(object):
    """complex(real[, imag]) -> complex number

    Create a complex number from a real part and an optional imaginary part.
    This is equivalent to (real + imag*1j) where imag defaults to 0."""
    PREC_REPR = 0 # 17
    PREC_STR = 0 # 12
    
    def __init__(self, real=0.0, imag=None):
        if isinstance(real, str) and imag is not None:
            msg = "complex() can't take second arg if first is a string"
            raise TypeError, msg

        if isinstance(imag, str): 
            msg = "complex() second arg can't be a string"
            raise TypeError, msg

        if isinstance(real, str): 
            real, imag = self._makeComplexFromString(real)
            self.__dict__['real'] = real
            self.__dict__['imag'] = imag
        else:
            if imag is None:
               imag = 0.
            self.__dict__['real'] = float(real)
            self.__dict__['imag'] = float(imag)
        

    def __setattr__(self, name, value):
        if name in ('real', 'imag'):
            raise TypeError, "readonly attribute"
        else:
            raise TypeError, "'complex' object has no attribute %s" % name 

    def _makeComplexFromString(self, string):
        import re
        pat = re.compile(" *([\+\-]?\d*\.?\d*)([\+\-]?\d*\.?\d*)[jJ] *")
        m = pat.match(string)
        x, y = m.groups()
        if len(y) == 1 and y in '+-':
            y = y + '1.0'
        x, y = map(float, [x, y])
        return x, y


    def __description(self, precision):
        sign = '+'
        if self.imag < 0.:
            sign = ''
        if self.real != 0.:
            format = "(%%%02dg%%s%%%02dgj)" % (precision, precision)
            args = (self.real, sign, self.imag)
        else:
            format = "%%%02dgj" % precision
            args = self.imag
        return format % args


    def __repr__(self):
        return self.__description(self.PREC_REPR)


    def __str__(self):
        return self.__description(self.PREC_STR)

        
    def __hash__(self):
        hashreal = hash(self.real)
        hashimag = hash(self.imag)

        # Note:  if the imaginary part is 0, hashimag is 0 now,
        # so the following returns hashreal unchanged.  This is
        # important because numbers of different types that
        # compare equal must have the same hash value, so that
        # hash(x + 0*j) must equal hash(x).

        combined = hashreal + 1000003 * hashimag
        if combined == -1:
            combined = -2

        return combined


    def __add__(self, other):
        self, other = self.__coerce__(other)
        real = self.real + other.real
        imag = self.imag + other.imag
        return complex(real, imag)


    def __sub__(self, other):
        self, other = self.__coerce__(other)
        real = self.real - other.real
        imag = self.imag - other.imag
        return complex(real, imag)


    def __mul__(self, other):
        if other.__class__ != complex:
            return complex(other*self.real, other*self.imag)

        real = self.real*other.real - self.imag*other.imag
        imag = self.real*other.imag + self.imag*other.real
        return complex(real, imag)


    def __div__(self, other):
        if other.__class__ != complex:
            return complex(self.real/other, self.imag/other)

        if other.real < 0:
            abs_breal = -other.real
        else: 
            abs_breal = other.real
      
        if other.imag < 0:
            abs_bimag = -other.imag
        else:
            abs_bimag = other.imag

        if abs_breal >= abs_bimag:
            # divide tops and bottom by other.real
            if abs_breal == 0.0:
                real = imag = 0.0
            else:
                ratio = other.imag / other.real
                denom = other.real + other.imag * ratio
                real = (self.real + self.imag * ratio) / denom
                imag = (self.imag - self.real * ratio) / denom
        else:
            # divide tops and bottom by other.imag
            ratio = other.real / other.imag
            denom = other.real * ratio + other.imag
            assert other.imag != 0.0
            real = (self.real * ratio + self.imag) / denom
            imag = (self.imag * ratio - self.real) / denom

        return complex(real, imag)


    def __floordiv__(self, other):
        return self / other
        
        
    def __truediv__(self, other):
        return self / other
        

    def __mod__(self, other):
        import warnings, math 
        warnings.warn("complex divmod(), // and % are deprecated", DeprecationWarning)

        if other.real == 0. and other.imag == 0.:
            raise ZeroDivisionError, "complex remainder"

        div = self/other # The raw divisor value.
        div = complex(math.floor(div.real), 0.0)
        mod = self - div*other

        if mod.__class__ == complex:
            return mod
        else:
            return complex(mod)


    def __divmod__(self, other):
        import warnings, math
        warnings.warn("complex divmod(), // and % are deprecated", DeprecationWarning)

        if other.real == 0. and other.imag == 0.:
            raise ZeroDivisionError, "complex remainder"

        div = self/other # The raw divisor value.
        div = complex(math.floor(div.real), 0.0)
        mod = self - div*other
        return div, mod


    def __pow__(self, other):
        import math
        if other.__class__ != complex:
            other = complex(other, 0)
                    
        a, b = self, other

        if b.real == 0. and b.imag == 0.:
            real = 1.
            imag = 0.
        elif a.real == 0. and a.imag == 0.:
            real = 0.
            imag = 0.
        else:
            vabs = math.hypot(a.real,a.imag)
            len = math.pow(vabs,b.real)
            at = math.atan2(a.imag, a.real)
            phase = at*b.real
            if b.imag != 0.0:
                len /= math.exp(at*b.imag)
                phase += b.imag*math.log(vabs)
            real = len*math.cos(phase)
            imag = len*math.sin(phase)

        return complex(real, imag)


    def __neg__(self):
        return complex(-self.real, -self.imag)


    def __pos__(self):
        return complex(self.real, self.imag)


    def __abs__(self):
        import math
        result = math.hypot(self.real, self.imag)
        return float(result)


    def __nonzero__(self):
        return self.real != 0.0 or self.imag != 0.0


    def __coerce__(self, other):
        typ = type(other)
        
        if typ is int: 
            return self, complex(float(other))
        elif typ is long: 
            return self, complex(float(other))
        elif typ is float: 
            return self, complex(other)
        elif other.__class__ == complex:
            return self, other
        elif typ is complex: 
            return self, complex(other.real, other.imag)
            
        raise TypeError, "number %r coercion failed" % typ


    def conjugate(self):
        return complex(self.real, -self.imag)

    def __eq__(self, other):
        self, other = self.__coerce__(other)
        return self.real == other.real and self.imag == other.imag

    def __ne__(self, other):
        self, other = self.__coerce__(other)
        return self.real != other.real or self.imag != other.imag


    # unsupported operations
    
    def __lt__(self, other):
        raise TypeError, "cannot compare complex numbers using <, <=, >, >="

        
    def __le__(self, other):
        raise TypeError, "cannot compare complex numbers using <, <=, >, >="

        
    def __gt__(self, other):
        raise TypeError, "cannot compare complex numbers using <, <=, >, >="

        
    def __ge__(self, other):
        raise TypeError, "cannot compare complex numbers using <, <=, >, >="


    def __int__(self):
        raise TypeError, "can't convert complex to int; use e.g. int(abs(z))"


    def __long__(self):
        raise TypeError, "can't convert complex to long; use e.g. long(abs(z))"


    def __float__(self):
        raise TypeError, "can't convert complex to float; use e.g. float(abs(z))"


    def _unsupportedOp(self, other, op):
        selfTypeName = type(self).__name__
        otherTypeName = type(other).__name__
        args = (op, selfTypeName, otherTypeName)
        msg = "unsupported operand type(s) for %s: '%s' and '%s'" % args
        raise TypeError, msg


    def __and__(self, other):
        self._unsupportedOp(self, other, "&")


    def __or__(self, other):
        self._unsupportedOp(self, other, "|")


    def __xor__(self, other):
        self._unsupportedOp(self, other, "^")


    def __rshift__(self, other):
        self._unsupportedOp(self, other, ">>")


    def __lshift__(self, other):
        self._unsupportedOp(self, other, "<<")


    def __iand__(self, other):
        self._unsupportedOp(self, other, "&=")


    def __ior__(self, other):
        self._unsupportedOp(self, other, "|=")


    def __ixor__(self, other):
        self._unsupportedOp(self, other, "^=")


    def __irshift__(self, other):
        self._unsupportedOp(self, other, ">>=")


    def __ilshift__(self, other):
        self._unsupportedOp(self, other, "<<=")


    # augmented assignment operations
    
    def __iadd__(self, other):
        return self + other
    

    def __isub__(self, other):
        return self - other
    

    def __imul__(self, other):
        return self * other
    

    def __idiv__(self, other):
        return self / other
    

#    def __new__(self, ...):
#        pass


# test mod, divmod

# add radd, rsub, rmul, rdiv...


# ________________________________________________________________________
##    def app___import__(*args):
##        # NOTE: No import statements can be done in this function,
##        # as that would involve a recursive call to this function ...
##
##        # args => (name[, globals[, locals[, fromlist]]])
##        
##        l = len(args)
##        if l >= 1:
##            modulename = args[0]
##        else:
##            raise TypeError('__import__() takes at least 1 argument (0 given)')
##        if l >= 2:
##            globals = args[1]
##            try:
##                local_context = self.imp_dirname(globals['__file__'])
##            except KeyError:
##                local_context = ''
##        else:
##            local_context = ''
##        if l >= 4:
##            fromlist = args[3]
##        else:
##            fromlist = []
##        if l > 4:
##            raise TypeError('__import__() takes at most 4 arguments (%i given)' % l)
##            
##        def inner_load(f, fullname):
##            """Load module from file `f` with canonical name `fullname`.
##            """
##            mod = self.imp_module(fullname) # XXX - add in docstring
##            self.imp_modules[fullname] = mod
##            mod.__file__ = f
##            dict = mod.__dict__
##            execfile(f, dict, dict)
##            return mod
##
##        def load(path, modulename, fullname):
##            """Create a module.
##
##            Create a mnodule with canonical name `fullname` from file
##            `modulename`+'.py' in path `path`, if it exist.
##            Or alternatively from the package
##            `path`/`modulename`/'__init__.py'.
##            If neither are found, return None.
##            """
##                
##            f = self.imp_join(path, modulename + '.py')
##            if self.imp_exists(f):
##                return inner_load(f, fullname)
##            f = self.imp_join(path, modulename, '__init__.py')
##            if self.imp_exists(f):
##                return inner_load(f, fullname)
##            else:
##                return None
##
##        names = modulename.split('.')
##
##        if not names:
##            raise ValueError("Cannot import an empty module name.")
##        if len(names) == 1:
##            if self.imp_modules.has_key(modulename):
##                return self.imp_modules[modulename]
##            #Relative Import
##            if local_context:
##                #Regular Module
##                module = load(local_context, modulename, modulename)
##                if module:
##                    return module
##            #Standard Library Module Import
##            for path in self.imp_path:
##                #Regular Module
##                module = load(path, modulename, modulename)
##                if module:
##                    return module                
##            #Module Not Found
##            raise ImportError(modulename)
##        else:
##            #Find most specific module already imported.
##            for i in range(len(names),0,-1):
##                base_name = '.'.join(names[0:i])
##                if self.imp_modules.has_key(base_name):
##                    break
##            #Top level package not imported - import it.
##            else:
##                base_name = names[0]
##                i = 1
##                #Relative Import
##                if ((not local_context) or
##                    not load(local_context, base_name, base_name)):
##                     #Standard Module Import
##                    for path in self.imp_path:
##                        if load(path, base_name, base_name):
##                            break
##                    else:
##                        #Module Not Found
##                        raise ImportError(base_name)                
##            path = self.imp_dirname(self.imp_modules[base_name].__file__)
##            full_name = base_name
##            for j in range(i,len(names)):
##                path = self.imp_join(path, names[j])
##                full_name = '.'.join((full_name, names[j]))
##                if not load(path, '__init__', full_name):
##                    raise ImportError(full_name)
##                ### load module from path
##            if fromlist:
##                return self.imp_modules[modulename]
##            else:
##                return self.imp_modules[names[0]]
##            
##    # Interpreter level helpers for app level import
##    def imp_dirname(*args_w):
##        return self.space.wrap(os.path.dirname(*self.space.unwrap(args_w)))
##
##    def imp_join(*args_w):
##        return self.space.wrap(os.path.join(*self.space.unwrap(args_w)))
##
##    def imp_exists(*args_w):
##        return self.space.wrap(os.path.exists(*self.space.unwrap(args_w)))
##    
##    def imp_module(w_name):
##        return self.space.wrap(Module(self.space, w_name))

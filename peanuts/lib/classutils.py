"""Utilities for class interaction.

    The diferences between `property`, `classproperty`, and `instantiableclassproperty`
    can be illustrated as follows:

    ```
        >>> class Foo( object ):
        ...     bar=0
        ...     def __init__( self, bar ): self.bar=bar
        ...     @property
        ...     def a( self ): return self.bar
        ...     @classproperty
        ...     def b( cls ): return cls.bar
        ...     @instantiableclassproperty
        ...     def c( cls_or_self ): return cls_or_self.bar
        ... 
        >>> Foo.a
        <property object at 0x7f497d307158>
        >>> Foo.b
        0
        >>> Foo.c
        0
        >>> foo = Foo(1)
        >>> foo.a
        1
        >>> foo.b
        0
        >>> foo.c
        1
    ```

    `instantiableclassmethod` works very similarly.
"""


class classproperty(object):
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, obj, cls):
        return self.getter(cls)


class instantiableclassproperty(object):
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, obj, cls):
        if obj is not None:
            return self.getter(obj)
        else:
            return self.getter(cls)


class instantiableclassmethod(object):
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, obj, cls):
        if obj is not None:
            def wrapper(*args, **kargs):
                return self.getter(obj, *args, **kargs)
        else:
            def wrapper(*args, **kargs):
                return self.getter(cls, *args, **kargs)

        return wrapper
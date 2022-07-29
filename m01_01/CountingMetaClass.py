class Meta(type):
    """
    Metaclass that assigns a number to each class,
    which is using Meta, as its metaclass
    """

    def __new__(mcs, *args, **kwargs):
        print(mcs, "__new__ of the counting Meta Class is called")
        instance = super().__new__(mcs, *args, **kwargs)
        instance.class_number = mcs.children_number
        mcs.children_number += 1
        return instance

Meta.children_number = 0


class Cls1(metaclass=Meta):
    def __init__(self, data):
        self.data = data
        print(self.data)


class Cls2(metaclass=Meta):
    def __init__(self, data):
        self.data = data

class Cls3(metaclass=Meta):
    def __init__(self, data):
        self.data = data

if __name__ == '__main__':
    print("Assigned numbers of Cls1(), Cls2() and Cls3():")
    assert (Cls1.class_number, Cls2.class_number, Cls3.class_number) == (0, 1, 2)
    print(Cls1.class_number)
    print(Cls2.class_number)
    print(Cls3.class_number)
    a, b, c = Cls1(''), Cls2(''), Cls3(''),
    assert (a.class_number, b.class_number, c.class_number) == (0, 1, 2)
    print(a.class_number, b.class_number, c.class_number)

class Person:
    age = 1
    color = 2


class MagicList:
    def __init__(self, cls_type=None):
        """
        constructor
        :param cls_type: class_type name
        """
        self.class_type = cls_type
        self.list = []

    def __setitem__(self, key, value):
        """
        This method is being called when an assignment is called. example : a[2]=5.
        Important note - In the condition we support list continuity. So we don't allow lists no accept larger indexes
        Than their length. For instance-  a[0]=1 , a[2]=5 will raise an exception .
        """
        if key == len(self.list):  # extending the list
            self.list.append(value)
        elif 0 <= key < len(self.list):

            self.list[key] = value
        else:
            raise IndexError("list assignment index out of range")

    def __getitem__(self, item):
        """
        This this method we generate an object if we get referenced by the last index (should be extended) and class
        type is not None.
        :param item: int
        :return:
        """
        if self.class_type is not None and len(self.list) == item:
            custom_object = self.class_type()
            self.list.append(custom_object)
        return self.list[item]


a = MagicList()
a[0] = 5
a[1] = 7
a[1] = 9
a[3] = 6
ohad = "ohad"

b = MagicList(cls_type=Person)
b[0].age = 7
b[0].color = "blue"

c = MagicList(cls_type=Person)
c[1].age = 5

import pytest

from monkey.object import Object
from monkey.object import ObjectType
from monkey.object import IntegerObject
from monkey.object import BooleanObject
from monkey.object import NullObject


def test_integer_object():
    int_obj = IntegerObject(5)

    assert int_obj.data_type() == ObjectType.INTEGER
    assert int_obj.inspect() == "5"
    assert int_obj.inspect() == str(int_obj)
    assert int_obj == IntegerObject(5)
    assert int_obj != 5


@pytest.mark.parametrize("bool_value", [True, False])
def test_boolean_object(bool_value):
    bool_obj = BooleanObject(bool_value)

    assert bool_obj.data_type() == ObjectType.BOOLEAN
    assert bool_obj.inspect() == str(bool_value)
    assert bool_obj.inspect() == str(bool_obj)
    assert bool_obj == BooleanObject(bool_value)
    assert bool_obj != bool_value


def test_null_object():
    null_obj = NullObject()

    assert null_obj.data_type() == ObjectType.NULL
    assert null_obj.inspect() == "NULL"
    assert null_obj.inspect() == str(null_obj)
    assert null_obj == NullObject()
    assert null_obj != "NULL"

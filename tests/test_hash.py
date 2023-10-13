import pytest

import monkey.object as objs


class TestHash:
    def test_integers_equal(self):
        int0 = objs.IntegerObject(5)
        int1 = objs.IntegerObject(5)

        assert objs.create_object_hash(int0) == objs.create_object_hash(int1)

    def test_integers_not_equal(self):
        int0 = objs.IntegerObject(5)
        int1 = objs.IntegerObject(7)

        assert objs.create_object_hash(int0) != objs.create_object_hash(int1)

    def test_strings_equal(self):
        string0 = objs.StringObject("hello")
        string1 = objs.StringObject("hello")

        assert objs.create_object_hash(string0) == objs.create_object_hash(string1)

    def test_strings_not_equal(self):
        string0 = objs.StringObject("hello")
        string1 = objs.StringObject("world")

        assert objs.create_object_hash(string0) != objs.create_object_hash(string1)

    def test_booleans_equal(self):
        bool0 = objs.BooleanObject(True)
        bool1 = objs.BooleanObject(True)

        assert objs.create_object_hash(bool0) == objs.create_object_hash(bool1)

    def test_booleans_not_equal(self):
        bool0 = objs.BooleanObject(True)
        bool1 = objs.BooleanObject(False)

        assert objs.create_object_hash(bool0) != objs.create_object_hash(bool1)

    @pytest.mark.parametrize(
        "obj",
        [
            objs.ArrayObject([]),
        ],
    )
    def test_no_hash_exists(self, obj):
        hash_key = objs.create_object_hash(obj)
        assert hash_key.data_type == objs.ObjectType.ERROR

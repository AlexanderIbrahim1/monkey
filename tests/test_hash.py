import pytest

import monkey.object as objs


class TestHash:
    def test_integers_equal(self):
        int0 = objs.IntegerObject(5)
        int1 = objs.IntegerObject(5)

        assert objs.create_hash_key(int0) == objs.create_hash_key(int1)

    def test_integers_not_equal(self):
        int0 = objs.IntegerObject(5)
        int1 = objs.IntegerObject(7)

        assert objs.create_hash_key(int0) != objs.create_hash_key(int1)

    def test_strings_equal(self):
        string0 = objs.StringObject("hello")
        string1 = objs.StringObject("hello")

        assert objs.create_hash_key(string0) == objs.create_hash_key(string1)

    def test_strings_not_equal(self):
        string0 = objs.StringObject("hello")
        string1 = objs.StringObject("world")

        assert objs.create_hash_key(string0) != objs.create_hash_key(string1)

    def test_booleans_equal(self):
        bool0 = objs.BooleanObject(True)
        bool1 = objs.BooleanObject(True)

        assert objs.create_hash_key(bool0) == objs.create_hash_key(bool1)

    def test_booleans_not_equal(self):
        bool0 = objs.BooleanObject(True)
        bool1 = objs.BooleanObject(False)

        assert objs.create_hash_key(bool0) != objs.create_hash_key(bool1)

    @pytest.mark.parametrize(
        "obj",
        [
            objs.ArrayObject([]),
        ],
    )
    def test_no_hash_exists(self, obj):
        hash_key = objs.create_hash_key(obj)
        assert hash_key.data_type == objs.ObjectType.ERROR

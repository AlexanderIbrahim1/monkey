import monkey.object as objs


class TestEnvironment:
    def test_basic(self):
        env = objs.Environment()

        name0 = "x"
        obj0 = objs.IntegerObject(5)

        env.set(name0, obj0)
        assert env.get(name0) == obj0

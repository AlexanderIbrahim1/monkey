import monkey.object as objs


class TestEnvironment:
    def test_basic(self):
        env = objs.Environment()

        name0 = "x"
        obj0 = objs.IntegerObject(5)

        env.set(name0, obj0)
        assert env.get(name0) == obj0


def test_enclosed_environment():
    outer_env = objs.Environment()

    name0 = "x"
    obj0 = objs.IntegerObject(5)
    outer_env.set(name0, obj0)

    inner_env = objs.new_enclosed_environment(outer_env)
    assert inner_env.get(name0) == obj0
    assert inner_env.get("name_that_isnt_there").data_type() == objs.ObjectType.ERROR

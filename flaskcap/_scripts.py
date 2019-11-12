__index__ = ["get_user", "save_user"]


def get_scripts():
    scripts = dict()

    for script in __index__:
        scripts[script] = globals()["__%s__" % script]

    return scripts


__get_user__ = """
if
redis.call("HGET", "id_to_username", KEYS[1])
then
    username = redis.call("HGET", "id_to_username", KEYS[1])
    password_hash = redis.call("HGET", "id_to_password_hash")
    redis.call("HSET", "id_to_last_accessed", KEYS[1], KEYS[2])
    return ("\"" .. username .. "\",\"" .. password_hash)
else
    return nil
end
                            """
__save_user__ = """
if not
    redis.call("HGET", "username_to_id", KEYS[1])
then
    redis.call("HSET", "username_to_id", KEYS[1], KEYS[2])
    redis.call("HSET", "id_to_username", KEYS[2], KEYS[1])
    redis.call("HSET", "id_to_password_hash", KEYS[2], KEYS[3])
    redis.call("HSET", "id_to_created_time", KEYS[2], KEYS[4])
    redis.call("HSET", "id_to_edit_time", KEYS[2], KEYS[4])
else
    redis.call("HSET", 'id_to_password_hash', KEYS[2], KEYS[3])
    redis.call("HSET", "id_to_edit_time", KEYS[2], KEYS[4])
end
                            """

x = get_scripts()
print(type(x))

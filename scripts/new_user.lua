redis.call("HSET", "username_to_id", KEYS[1], KEYS[2])
redis.call("HSET", "id_to_username", KEYS[2], KEYS[1])
redis.call("HSET", "id_to_password_hash", KEYS[2], KEYS[3])
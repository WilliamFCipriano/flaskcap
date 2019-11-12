--[[
save_user

Retrieves a users details from the database by id

KEYS[1]: id
KEYS[2]: current timestamp
]]
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
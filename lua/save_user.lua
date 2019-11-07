--[[
save_user

Saves a user, creates that user if the user does
not yet exist

KEYS[1]: username
KEYS[2]: id
KEYS[3]: password_hash
KEYS[4]: utc timestamp
]]
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
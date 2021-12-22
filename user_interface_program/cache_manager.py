import json, os

# Create cache file
def create_cache():
    if not os.path.exists("cache.json"):
        with open("cache.json", "w+") as cache:
            cache.write('{ \n }')

# Delete cache
def delete_cache():
    # Create database file
    if os.path.exists("cache.json"):
        os.remove("cache.json")

# Delete & create database
def recreate_cache():
    delete_cache()
    create_cache()

# Write content to database file
def write_cache(cache):
    with open("cache.json", "w") as file:
        json.dump(cache, file, indent=4, sort_keys=True)

# Read contents of database file
def read_cache():

    cache = None
    try_count = 0

    # Try to read cache 10 times
    while cache is None and try_count < 10:
        try:
            # Read cache file
            with open("cache.json", "r") as file:
                cache = json.load(file)
                return cache
        except:
            try_count += 1

    # Otherwise recreate database and read again
    recreate_cache()
    read_cache()

# Update cache
def update_cache(topic, value):
    cache = read_cache()
    cache[topic] = value
    write_cache(cache)

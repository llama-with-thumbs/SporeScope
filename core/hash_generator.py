import hashlib
import time

def unix_time_to_6_digit_string():
    # Get the current Unix timestamp
    current_timestamp = int(time.time())

    # Convert the timestamp to a string
    timestamp_str = str(current_timestamp)

    # Calculate the MD5 hash of the timestamp
    hash_object = hashlib.md5(timestamp_str.encode())

    # Take the first 6 characters of the hash and convert them to uppercase
    hash_str = hash_object.hexdigest()[:6].upper()

    return hash_str

# Example usage:
six_digit_string = unix_time_to_6_digit_string()
print(six_digit_string)

import string
import os
from math import ceil

def calculate_mersenne_primes():

    mersenne_prime_exponents = [
        2, 3, 5, 7, 13, 17, 19, 31, 61, 89, 107, 127, 521, 607, 1279
    ]
    primes = []
    for exp in mersenne_prime_exponents:
        prime = long(1)
        for i in range(exp):
            prime *= 2
        prime -= 1
        primes.append(prime)
    return primes

SMALLEST_257BIT_PRIME = (2**256 + 297)
SMALLEST_321BIT_PRIME = (2**320 + 27)
SMALLEST_385BIT_PRIME = (2**384 + 231)
STANDARD_PRIMES = calculate_mersenne_primes() + [
    SMALLEST_257BIT_PRIME, SMALLEST_321BIT_PRIME, SMALLEST_385BIT_PRIME
]
STANDARD_PRIMES.sort()

def get_large_enough_prime(batch):
    """ Returns a prime number that is greater all the numbers in the batch.
    """
    # build a list of primes
    primes = STANDARD_PRIMES
    # find a prime that is greater than all the numbers in the batch
    for prime in primes:
        numbers_greater_than_prime = [i for i in batch if i > prime]
        if len(numbers_greater_than_prime) == 0:
            return prime
    return None


def dev_random_entropy(numbytes):
    return open("/dev/random", "rb").read(numbytes)

def dev_urandom_entropy(numbytes):
    return open("/dev/urandom", "rb").read(numbytes)

def get_entropy(numbytes):
    if os.name == 'nt':
        return os.urandom(numbytes)
    else:
        return dev_random_entropy(numbytes)

def randint(min_value, max_value):

    if not (isinstance(min_value, int) and isinstance(min_value, int)):
        raise ValueError('min and max must be integers')

    value_range = (max_value - min_value) + 1
    numbytes_of_entropy = int(ceil(value_range.bit_length()/8.0)) + 1
    entropy_value_range = 2**(numbytes_of_entropy*8)
    acceptable_sample_range = entropy_value_range - (entropy_value_range % value_range)
    while True:
        byte_from_entropy = get_entropy(numbytes_of_entropy)
        int_from_entropy = int(byte_from_entropy.encode('hex'), 16)
        if int_from_entropy <= acceptable_sample_range:
            break
    rand_int = min_value + (int_from_entropy % value_range)
    return rand_int

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def mod_inverse(k, prime):
    k = k % prime
    if k < 0:
        r = egcd(prime, -k)[2]
    else:
        r = egcd(prime, k)[2]
    return (prime + r) % prime

def random_polynomial(degree, intercept, upper_bound):
    if degree < 0:
        raise ValueError('Degree must be a non-negative number.')
    coefficients = [intercept]
    for i in range(degree):
        random_coeff = randint(0, upper_bound-1)
        coefficients.append(random_coeff)
    return coefficients

def get_polynomial_points(coefficients, num_points, prime):
    points = []
    for x in range(1, num_points+1):
        y = coefficients[0]
        for i in range(1, len(coefficients)):
            exponentiation = (long(x)**i) % prime
            term = (coefficients[i] * exponentiation) % prime
            y = (y + term) % prime
        points.append((x, y))
    return points

def modular_lagrange_interpolation(x, points, prime):
    x_values, y_values = zip(*points)
    f_x = long(0)
    for i in range(len(points)):
        numerator, denominator = 1, 1
        for j in range(len(points)):
            if i == j: continue
            numerator = (numerator * (x - x_values[j])) % prime
            denominator = (denominator * (x_values[i] - x_values[j])) % prime
        lagrange_polynomial = numerator * mod_inverse(denominator, prime)
        f_x = (prime + f_x + (y_values[i] * lagrange_polynomial)) % prime
    return f_x

def charset_to_int(s, charset):
    if not isinstance(s, (str)):
        raise ValueError("s must be a string.")
    if (set(s) - set(charset)):
        raise ValueError("s has chars that aren't in the charset.")
    output = 0
    for char in s:
        output = output * len(charset) + charset.index(char)
    return output

def change_charset(s, original_charset, target_charset):
    intermediate_integer = charset_to_int(s, original_charset)
    output_string = int_to_charset(intermediate_integer, target_charset)
    return output_string

base16_chars = string.hexdigits[0:16]

base58_chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

base32_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"

zbase32_chars = "ybndrfg8ejkmcpqxot1uwisza345h769"

base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def secret_int_to_points(secret_int, point_threshold, num_points):
    if point_threshold < 2:
        raise ValueError("Threshold must be >= 2.")
    if point_threshold > num_points:
        raise ValueError("Threshold must be < the total number of points.")
    #prime = get_large_enough_prime([secret_int, num_points])
    prime = 6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574028291115057151
    #if not prime:
    #raise ValueError("Error! Secret is too long for share calculation!")
    #coefficients = random_polynomial(point_threshold-1, secret_int, prime)
    #points = get_polynomial_points(coefficients, num_points, prime)
    
    #Your y's in format:
    #y1 = int1_
    #y2 = int2_ and etc.
    #points in format: points = [(int1_,y1),(int2_,y3),...]
    return points

def point_to_share_string(point, charset):
    # point should be in the format (1, 4938573982723...)
    if '-' in charset:
        raise ValueError('The character "-" cannot be in the supplied charset.')
    if not isinstance(point, tuple) and len(point) == 2 and \
        isinstance(point[0], (int, long)) and isinstance(point[1], (int, long)):
        raise ValueError('Point format is invalid. Must be a pair of integers.')
    x,y = point
    x_string = int_to_charset(x, charset)
    y_string = int_to_charset(y, charset)
    share_string = x_string + '-' + y_string
    return share_string

def share_string_to_point(share_string, charset):
    # share should be in the format "01-d051080de7..."
    if '-' in charset:
        raise ValueError('The character "-" cannot be in the supplied charset.')
    if not isinstance(share_string, str) and share_string.count('-') == 1:
        raise ValueError('Share format is invalid.')    
    x_string, y_string = share_string.split('-')
    if (set(x_string) - set(charset)) or (set(y_string) - set(charset)):
        raise ValueError("Share has characters that aren't in the charset.")
    x = charset_to_int(x_string, charset)
    y = charset_to_int(y_string, charset)
    return (x, y)

class SecretSharer():
    secret_charset = string.hexdigits[0:16]
    share_charset = string.hexdigits[0:16]

    def __init__(self):
        pass

    @classmethod
    def split_secret(cls, secret_string, share_threshold, num_shares):
        secret_int = charset_to_int(secret_string, cls.secret_charset)
        points = secret_int_to_points(secret_int, share_threshold, num_shares)
        shares = []
        for point in points:
            shares.append(point_to_share_string(point, cls.share_charset))
        return shares

    @classmethod
    def recover_secret(cls, shares):
        points = []
        for share in shares:
            points.append(share_string_to_point(share, cls.share_charset))
        secret_int = points_to_secret_int(points)
        secret_string = int_to_charset(secret_int, cls.secret_charset)
        return secret_string
    
def points_to_secret_int(points):
    if not isinstance(points, list):
        raise ValueError("Points must be in list form.")
    for point in points:
        if not isinstance(point, tuple) and len(point) == 2:
            raise ValueError("Each point must be a tuple of two values.")
        if not isinstance(point[0], (int, long)) and \
            isinstance(point[1], (int, long)):
            raise ValueError("Each value in the point must be an int.")
    x_values, y_values = zip(*points)
    prime = get_large_enough_prime(y_values)
    free_coefficient = modular_lagrange_interpolation(0, points, prime)
    secret_int = free_coefficient # the secret int is the free coefficient
    return secret_int

def int_to_charset(x, charset):
    if not (isinstance(x, (int, long)) and x >= 0):
        raise ValueError("x must be a non-negative integer.")
    if x == 0:
        return charset[0]
    output = ""
    while x > 0:
        x, digit = divmod(x, len(charset))
        output += charset[digit]
    # reverse the characters in the output and return
    return output[::-1]


def main():
    #Your y's in format:
    #y1 = int1_
    #y2 = int2_ and etc.
    #points in format: points = [(int1_,y1),(int2_,y3),...]
    secret_int = points_to_secret_int(points)
    secret_charset = base58_chars
    secret_string = int_to_charset(secret_int, secret_charset)
    print(secret_string)
    
if __name__ == '__main__':
    main()

    


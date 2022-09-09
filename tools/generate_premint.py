import time
from starkware.crypto.signature.fast_pedersen_hash import pedersen_hash

basicAlphabet = "abcdefghijklmnopqrstuvwxyz0123456789-"
bigAlphabet = "这来"
small_size_plus = len(basicAlphabet) + 1
big_size_plus = len(bigAlphabet) + 1

def encode(decoded):
    encoded = 0
    multiplier = 1
    for i in range(len(decoded)):
        char = decoded[i]
        try:
            index = basicAlphabet.index(char)
            if i == len(decoded) - 1 and decoded[i] == basicAlphabet[0]:
                encoded += multiplier * len(basicAlphabet)
                multiplier *= small_size_plus**2  # like adding 0
            else:
                encoded += multiplier * index
                multiplier *= small_size_plus
        except ValueError:
            encoded += multiplier * len(basicAlphabet)
            multiplier *= small_size_plus
            newid = int(i == len(decoded) - 1) + bigAlphabet.index(char)
            encoded += multiplier * newid
            multiplier *= len(bigAlphabet)
    return encoded

# domain -> (token_id, target_address)
expiry = int(time.time()) + 3600*24*365*10
to_airdrop = { "th0rgal" : [ 1, 0x048F24D0D0618fa31813DB91a45d8be6c50749e5E19ec699092CE29aBe809294 ] }

for domain, [token_id, address ] in to_airdrop.items():
    encoded_domain = encode(domain)
    hashed_domain = pedersen_hash(encoded_domain, 0)
    print(f"mint_domain({expiry}, {address}, {hashed_domain}, Uint256({token_id}, 0), {encoded_domain})")

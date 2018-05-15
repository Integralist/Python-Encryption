# Python Encryption

This library provides three functions:

1. `generate_digest`
2. `decrypt_digest`
3. `validate_digest`

### generate_digest

This is a multi-arity function that will generate a digest using either a password-based key derivation function ([KDF](https://en.wikipedia.org/wiki/Key_derivation_function)) or a [PBKDF2](https://en.wikipedia.org/wiki/PBKDF2) depending on the input given.

If a `password` argument is provided, then KDF will be used (along with a random salt) to generate a _non-deterministic_ digest.

If a `salt` is provided, then a PBKDF2 will be used to generate a _deterministic_ digest.

> Note: salts should be a minimum of 128bits (~16 characters) in length.

### KDF or PBKDF2 ?

It's recommended you use KDF (i.e. provide a `password` argument to the `generate_digest` function), this is because they're designed to be more computationally intensive than standard hashing functions and so are harder to use dictionary or rainbow table style attacks (as they would require a lot of extra memory resources and become more unfeasible as an attack vector).

By default the KDF will have a maximum computational time of `0.5`, but this can be overridden using the `maxtime` argument.

A PBKDF2 is able to provide deterministic output (and the ability to specify an explicit salt value). The internal implementation will repeat its process multiple times, thus reducing the feasibility of automated password cracking attempts.

> Note: when specifying a maxtime with `generate_digest`, ensure you include that same value when decrypting with `decrypt_digest` or validating via `validate_digest`.

### decrypt_digest and validate_digest

The `decrypt_digest` and `validate_digest` functions only apply to digests that have been generated using a password (i.e. KDF). Given the right password `decrypt_digest` will return the original message, and thus is considered more a form of symmetrical encryption than a straight one-way hash function. The `validate_digest` function will return a boolean true or false if the given password was able to decrypt the message.

## Usage

See the [tests](tests/test_interface.py) for examples of how to use these functions.

## Tests

See [tests](tests/test_interface.py).

## Dependencies

We have two dependency files:

* `requirements.txt`
* `requirements-to-freeze.txt`

The latter should contain both 'explicit' versions (i.e. versions of dependencies our service is known to support) and 'non-explicit' versions (e.g. no versions defined), where as the former (`requirements.txt`) simply acts as a lockfile.

If we execute `pip freeze` the output will include dependencies that have the explicit versions we requested and the _latest_ version for those dependencies where we defined no explicit version. We can direct that output to a new file called `requirements.txt`.

"""gets checksums from file"""

# TODO: Move to C or C++ in the future...
# external 
import click

# standard
import hashlib
from typing import TYPE_CHECKING, NamedTuple


if TYPE_CHECKING:
    def hash_file(file:str, algo:hashlib._Hash) -> str:...
else:
    def hash_file(file:str, algo) -> str: 
        with open(file, "rb") as r:
            while buff := r.read(10240):
                algo.update(buff)
        return algo.hexdigest()


def md5_checksum(file:str):
    return hash_file(file, hashlib.md5())

def sha1_checksum(file:str):
    return hash_file(file, hashlib.sha1())

def sha256_checksum(file:str):
    return hash_file(file, hashlib.sha256())

def sha384_checksum(file:str):
    return hash_file(file, hashlib.sha384())

def sha512_checksum(file:str):
    return hash_file(file, hashlib.sha512())


class CheckSums(NamedTuple):
    md5:str 
    sha1:str 
    sha256:str 
    sha384:str
    sha512:str

    @classmethod
    def generate(cls, file:str):
        return cls(
            md5 =  md5_checksum(file),
            sha1 = sha1_checksum(file),
            sha256 = sha256_checksum(file),
            sha384 = sha384_checksum(file),
            sha512 = sha512_checksum(file)
        )

    if TYPE_CHECKING:
        def __eq__(self, __value: "CheckSums") -> TYPE_CHECKING:...
    else:
        def __eq__(self, __value):
            return (
                (self.md5 == __value.md5) and
                (self.sha1 ==  __value.sha1) and 
                (self.sha256 == __value.sha256) and 
                (self.sha384 == __value.sha384) and
                (self.sha512 == __value.sha512)
            )

@click.group()
def cli():
    """Used for generating or verifying files"""
    pass

@cli.command
@click.argument("file", type=click.Path())
def generate(file:str):
    s = CheckSums.generate(file)
    print("[md5]: ", s.md5)
    print("[sha1]: ", s.sha1)
    print("[sha256]: ", s.sha256)
    print("[sha384]: ", s.sha384)
    print("[sha512]: ", s.sha512)

@cli.command
@click.argument("a", type=click.Path())
@click.argument("b", type=click.Path())
def verify(a:str, b:str):
    """verifies between 2 files"""
    cs_a = CheckSums.generate(a)
    cs_b = CheckSums.generate(b)
    if cs_a == cs_b:
        print("Correct")
    else:
        print("Incorrect")

if __name__ == "__main__":
    cli()


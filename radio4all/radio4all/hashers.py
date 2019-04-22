from django.contrib.auth.hashers import BasePasswordHasher

def mysql_hash_password(password):
    nr = 1345345333
    add = 7
    nr2 = 0x12345671

    for c in (ord(x) for x in password if x not in (' ', '\t')):
        nr^= (((nr & 63)+add)*c)+ (nr << 8) & 0xFFFFFFFF
        nr2= (nr2 + ((nr2 << 8) ^ nr)) & 0xFFFFFFFF
        add= (add + c) & 0xFFFFFFFF

    return "%08x%08x" % (nr & 0x7FFFFFFF,nr2 & 0x7FFFFFFF)

class OldMySQLPasswordHasher(BasePasswordHasher):
    algorithm = "old_mysql_hasher"

    def salt(self):
        return 'my_salt'

    def encode(self, password):
        return mysql_hash_password(password)

    def verify(self, password, encoded):
        encoded_2 = self.encode(password, '')
        return constant_time_compare(encoded, encoded_2)

    def safe_summary(self, encoded):
        return SortedDict([
            (_('algorithm'), self.algorithm),
            (_('hash'), mask_hash(encoded, show=3)),
        ])
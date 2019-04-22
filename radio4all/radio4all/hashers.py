from django.contrib.auth.hashers import BasePasswordHasher, mask_hash

from collections import OrderedDict as SortedDict

from django.utils.crypto import constant_time_compare
from django.utils.translation import ugettext_noop as _

class MySQLOldPasswordHasher:

    algorithm =" mysql_old_password "

    def salt (self):
        return ''

    def encode (self, password, salt):
        nr = 1345345333
        add = 7
        nr2 = 0x12345671

        for c in (ord (x) for x in password if x not in ('', '\ t')):
            nr ^= (((nr & 63) + add) * c) + (nr << 8) & 0xFFFFFFFF
            nr2 = (nr2 + ((nr2 << 8) ^ nr)) & 0xFFFFFFFF
            add = (add + c) & 0xFFFFFFFF

        password = "% 08x% 08x"% (nr & 0x7FFFFFFF, nr2 & 0x7FFFFFFF)
        return "% $ s% s "% (self.algorithm, password)

    def verify (self, password, encoded):
        encoded_2 = self.encode (password, '')
        return constant_time_compare (encoded, encoded_2)

    def safe_summary (self, encoded):
        return SortedDict ([
            (_ ('algorithm'), self.algorithm),
            (_ ('hash'),mask_hash (encoded, show = 3)),
        ])
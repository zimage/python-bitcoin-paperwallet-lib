#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import paperwallet
import paperwallet.util

from bitcoin.key import CKey

k = CKey()
k.generate()
k.set_compressed(False)

public_key = paperwallet.util.public_key_to_bc_address(k.get_pubkey())
private_key = \
    paperwallet.util.private_key_to_wallet_import_format(k.get_privkey())

pw = paperwallet.PaperWallet(sys.argv[1], sys.argv[2], public_key,
                             private_key)
pw.save('bar.png')

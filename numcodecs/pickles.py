# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division


import numpy as np


from numcodecs.abc import Codec
from numcodecs.compat import ndarray_from_buffer, buffer_copy
try:
    import cPickle as pickle
except ImportError:
    import pickle


class Pickle(Codec):
    """Codec to encode data as as pickled bytes. Useful for encoding python
    strings.

    Parameters
    ----------
    protocol : int, defaults to pickle.HIGHEST_PROTOCOL
        the protocol used to pickle data

    Raises
    ------
    encoding a non-object dtyped ndarray will raise ValueError

    Examples
    --------
    >>> import numcodecs as codecs
    >>> import numpy as np
    >>> x = np.array(['foo', 'bar', 'baz'], dtype='object')
    >>> f = codecs.Pickle()
    >>> f.decode(f.encode(x))
    array(['foo', 'bar', 'baz'], dtype=object)

    """  # flake8: noqa

    codec_id = 'pickle'

    def __init__(self, protocol=pickle.HIGHEST_PROTOCOL):
        self.protocol = protocol

    def encode(self, buf):
        if hasattr(buf, 'dtype') and buf.dtype != 'object':
            raise ValueError("cannot encode non-object ndarrays, %s "
                             "dtype was passed" % buf.dtype)
        return pickle.dumps(buf, protocol=self.protocol)

    def decode(self, buf, out=None):
        dec = pickle.loads(buf)
        if out is not None:
            np.copyto(out, dec)
            return out
        else:
            return dec

    def get_config(self):
        return dict(id=self.codec_id,
                    protocol=self.protocol)

    def __repr__(self):
        return 'Pickle(protocol=%s)' % self.protocol

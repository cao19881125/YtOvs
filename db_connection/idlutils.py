import collections
import os
import time
import uuid

from ovs.db import idl
from ovs import jsonrpc
from ovs import poller
from ovs import stream

_NO_DEFAULT = object()

def wait_for_change(_idl, timeout, seqno=None):
    if seqno is None:
        seqno = _idl.change_seqno
    stop = time.time() + timeout
    while _idl.change_seqno == seqno and not _idl.run():
        ovs_poller = poller.Poller()
        _idl.wait(ovs_poller)
        ovs_poller.timer_wait(timeout * 1000)
        ovs_poller.block()
        if time.time() > stop:
            raise Exception(_("Timeout"))


def _get_schema_helper(connection, schema_name):
    err, strm = stream.Stream.open_block(
        stream.Stream.open(connection))
    if err:
        raise Exception(_("Could not connect to %s") % connection)
    rpc = jsonrpc.Connection(strm)
    req = jsonrpc.Message.create_request('get_schema', [schema_name])
    err, resp = rpc.transact_block(req)
    rpc.close()
    if err:
        raise Exception(_("Could not retrieve schema from %(conn)s: "
                          "%(err)s") % {'conn': connection,
                                        'err': os.strerror(err)})
    elif resp.error:
        raise Exception(resp.error)
    return idl.SchemaHelper(None, resp.result)

def get_schema_helper(connection, schema_name, retry=True):
    try:
        return _get_schema_helper(connection, schema_name)
    except Exception:
        print 'get_schema_helper'



def row_by_value(idl_, table, column, match, default=_NO_DEFAULT):
    """Lookup an IDL row in a table by column/value"""
    tab = idl_.tables[table]
    for r in tab.rows.values():
        if getattr(r, column) == match:
            return r
    if default is not _NO_DEFAULT:
        return default
    raise None

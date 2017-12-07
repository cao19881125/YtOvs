from cmd_executer import CmdExecuter

class DumpTableCmd(CmdExecuter):
    def __init__(self, connection, table_name):
        CmdExecuter.__init__(self, connection)
        self.table_name = table_name

    def execute(self):
        result = []
        for key in self.con.idl.tables[self.table_name].rows:
            ret_row = {}
            ret_row['uuid'] = str(key)
            values = self.con.idl.tables[self.table_name].rows[key]._data
            for d in values:
                ret_row[d] = str(values[d])
            result.append(ret_row)

        return result


'''
[
{u'direction': 'to-lport', 
u'name': '[]', 
u'priority': '100', 
u'log': 'true', 
u'action': 'drop', 
u'external_ids': '{"neutron:lport"="5fb77332-2035-4f72-8e57-7415b02489c9"}', 
u'match': '"outport==\\"inside-vm2\\""', 
u'severity': '[]',
'uuid': '2890a832-1c83-4b8e-8b40-2928817012cc'}]

'''

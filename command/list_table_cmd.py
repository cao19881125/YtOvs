from cmd_executer import CmdExecuter

class ListTableCmd(CmdExecuter):
    def __init__(self, connection):
        CmdExecuter.__init__(self, connection)

    def execute(self):
        result = []

        for t in self.con.idl.tables:
            result.append(t)

        return result
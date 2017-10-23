from cmd_executer import CmdExecuter


class GetTableStructureCmd(CmdExecuter):
    def __init__(self, connection, table_name):
        CmdExecuter.__init__(self, connection)
        self.__table_name = table_name

    def execute(self):
        result = self.con.idl.tables[self.__table_name].to_json()

        return result['columns']



'''
result like this:
    {
        u'direction': {
            'type': {
                'key': {
                    'enum': [
                        'set',
                        [
                            u'from-lport',
                            u'to-lport'
                        ]
                    ],
                    'type': 'string'
                }
            }
        },
        u'name': {
            'type': {
                'key': {
                    'type': 'string',
                    'maxLength': 63
                },
                'min': 0
            }
        },
        u'severity': {
            'type': {
                'key': {
                    'enum': [
                        'set',
                        [
                            u'alert',
                            u'debug',
                            u'info',
                            u'notice',
                            u'warning'
                        ]
                    ],
                    'type': 'string'
                },
                'min': 0
            }
        },
        u'priority': {
            'type': {
                'key': {
                    'minInteger': 0,
                    'maxInteger': 32767,
                    'type': 'integer'
                }
            }
        },
        u'action': {
            'type': {
                'key': {
                    'enum': [
                        'set',
                        [
                            u'allow',
                            u'allow-related',
                            u'drop',
                            u'reject'
                        ]
                    ],
                    'type': 'string'
                }
            }
        },
        u'external_ids': {
            'type': {
                'max': 'unlimited',
                'value': 'string',
                'key': 'string',
                'min': 0
            }
        },
        u'match': {
            'type': 'string'
        },
        u'log': {
            'type': 'boolean'
        }
    }
'''
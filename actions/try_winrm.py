from winrm.protocol import Protocol

from st2common.runners.base_action import Action

__all__ = [
    'TryWinRMAction'
]


class TryWinRMAction(Action):
    def run(self, host, password, username='Administrator',
            port=5732, secure=True):
        proto = 'https' if secure else 'http'
        p = Protocol(
            endpoint='%s://%s:%i/wsman' % (proto, host, port),  # RFC 2732?
            transport='ntlm',
            username=username,
            password=password,
            server_cert_validation='ignore')
        shell_id = p.open_shell()
        command_id = p.run_command(shell_id, 'ipconfig', ['/all'])
        std_out, std_err, status_code = p.get_command_output(shell_id,
                                                             command_id)
        p.cleanup_command(shell_id, command_id)
        p.close_shell(shell_id)
        return {'stdout': std_out, 'stderr': std_err}

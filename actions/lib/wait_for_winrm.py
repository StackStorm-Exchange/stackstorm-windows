#!/usr/bin/env python

import time

from st2common.runners.base_action import Action
from winrm import Session

WINRM_HTTP_PORT = 5985


class BaseAction(Action):
    def run(self, host, port, username, password, transport, scheme, verify_ssl_cert,
            winrm_timeout, sleep_delay, retries):

        # read_timeout must be > operation_timeout (winrm_timeout)
        read_timeout = winrm_timeout + 1
        # if connecting to the HTTP port then we must use "http" as the scheme
        # in the URL
        if port == WINRM_HTTP_PORT:
            scheme = "http"

        # construct the URL for connecting to WinRM on the host
        winrm_url = "{}://{}:{}/wsman".format(scheme, host, port)

        # convert boolean into text required by winrm library
        server_cert_validation = "validate" if verify_ssl_cert else "ignore"

        # create our session object, this doesn't actually connect
        # it just sets up all of the information into a reusable object
        session = Session(winrm_url,
                          auth=(username, password),
                          transport=transport,
                          server_cert_validation=server_cert_validation,
                          operation_timeout_sec=winrm_timeout,
                          read_timeout_sec=read_timeout)

        # loop for the given number of retries
        for index in range(retries):
            attempt = index + 1
            shell_id = None
            try:
                self.logger.debug('WinRM connection attempt: %s' % (attempt))
                # openning up a shell is how WinRM connects, this way we do not
                # need to invoke a command and incur that overhead
                shell_id = session.protocol.open_shell()
                return True
            except Exception as e:
                self.logger.info('Attempt %s failed (%s), sleeping for %s seconds...' %
                                 (attempt, str(e), sleep_delay))
                time.sleep(sleep_delay)
            finally:
                if shell_id:
                    session.protocol.close_shell(shell_id)

        raise Exception('Exceeded max retries (%s)' % (retries))

# Windows Integration Pack

Pack which allows integration with Windows systems.

## Actions

### WMIQueryAction

Action which runs a provided WQL query on a specified host and returns the
result.

For this action to work, WMI client for Linux (wmic) needs to be installed on
the host where this action is running. Packages for Ubuntu and other systems
are available at [https://www.orvant.com/packages/](https://www.orvant.com/packages/).

#### Parameters

* ``host`` - Host of a Window machine to run the query on.
* ``username`` - Account username (defaults to ``Administrator``).
* ``password`` - Account password.
* ``query`` - WQL query to run.

For information on how to enable and configure WMI, please see the following
page - [Enable WMI (Windows Management Instrumentation)](http://www.poweradmin.com/help/enablewmi.aspx).

#### Sample Queries

1. Retrieve process id for all the running processes

```sql
Select ProcessId from Win32_Process Where CommandLine like '%java.exe%'
```

2. Retrieve all the information for a particular process

```sql
Select * from Win32_Process Where CommandLine like '%java.exe%'
```

3. Retrieve information about Windows services

```sql
Select * From Win32_Service
```

4. Retrieve information about free memory

```sql
Select FreePhysicalMemory from Win32_OperatingSystem
```

## winexe (RPC) commands

These require `winexe` to be installed and available in the path.

For debian this is available by:
```
wget http://download.opensuse.org/repositories/home:/uibmz:/opsi:/opsi40-testing/xUbuntu_12.04/amd64/winexe_1.00.1-1_amd64.deb
sudo dpkg --install winexe_1.00.1-1_amd64.deb
```

## winrm commands

The WinRM commands require WinRM to be configured to allow non-domain joined connections (untrusted).
2 actions are provided to set this up via RPC, `setup_winrm` and `lockdown_winrm`. If you have finished using WinRM, it is recommended to run
the lockdown action.

For more examples, see [WMI Query Language by Example](http://www.codeproject.com/Articles/46390/WMI-Query-Language-by-Example).

### wait_for_winrm

This action behaves similar to the core `linux.wait_for_ssh` action. It allows a workflow
to wait for a WinRM connection to become available on a Windows host.


#### Common parameters

* `host` - Hostname / IP address to connect to
* `username` - Username used to authenticate.
* `password` - Password used to authenticate.
* `verify_ssl_cert` - Should SSL certs on the remote host be validated?
* `winrm_timeout` - Timeout of each connection attempt (seconds).
* `sleep_delay` - Time to sleep between connection attempts (seconds).
* `retries` - Maximum number of retries before failing.
* `timeout` - Total timeout for the action
      Note: timeout needs to be `>= ((winrm_timeout + sleep_delay) * retries)` so we override a
      default Python runner action timeout with a larger value


#### Example

``` shell
st2 run windows.wait_for_winrm host="hostname.domain.tld" username="user@domain.tld" password="xxx" verify_ssl_cert=false
```

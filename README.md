# ReadWriteMemory

### Description
This ReadWriteMemory Module is made on Python for reading and writing to the memory of any process. This module does not required any extra modules only uses standard Python lib’s like ctypes.

---

### Requirements
Python 3.4+
OS: Windows 7, 8 and 10

---

#### Windows API’s in this module:<br />
[EnumProcesses](https://docs.microsoft.com/en-us/windows/win32/api/psapi/nf-psapi-enumprocesses)<br />
[GetProcessImageFileName](https://docs.microsoft.com/en-us/windows/win32/api/psapi/nf-psapi-getprocessimagefilenamea)<br />
[OpenProcess](https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocess)<br />
[Process Security and Access Rights](https://docs.microsoft.com/en-us/windows/win32/procthread/process-security-and-access-rights)<br />
[CloseHandle](https://docs.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-closehandle)<br />
[GetLastError](https://docs.microsoft.com/en-us/windows/win32/api/errhandlingapi/nf-errhandlingapi-getlasterror)<br />
[ReadProcessMemory](https://docs.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-readprocessmemory)<br />
[WriteProcessMemory](https://docs.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-writeprocessmemory)<br />

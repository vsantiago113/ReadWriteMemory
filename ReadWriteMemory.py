import os.path
import ctypes
import ctypes.wintypes

# Process Permissions
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_OPERATION = 0x0008
PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020

MAX_PATH = 260


class ReadWriteMemory:

    def GetProcessIdByName(self, pName):
        if pName.endswith('.exe'):
            pass
        else:
            pName = pName+'.exe'
            
        ProcessIds, BytesReturned = self.EnumProcesses()

        for index in list(range(int(BytesReturned / ctypes.sizeof(ctypes.wintypes.DWORD)))):
            ProcessId = ProcessIds[index]
            hProcess = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, False, ProcessId)
            if hProcess:
                ImageFileName = (ctypes.c_char*MAX_PATH)()
                if ctypes.windll.psapi.GetProcessImageFileNameA(hProcess, ImageFileName, MAX_PATH) > 0:
                    filename = os.path.basename(ImageFileName.value)
                    if filename.decode('utf-8') == pName:
                        return ProcessId
                self.CloseHandle(hProcess)

    def EnumProcesses(self):
        count = 32
        while True:
            ProcessIds = (ctypes.wintypes.DWORD*count)()
            cb = ctypes.sizeof(ProcessIds)
            BytesReturned = ctypes.wintypes.DWORD()
            if ctypes.windll.Psapi.EnumProcesses(ctypes.byref(ProcessIds), cb, ctypes.byref(BytesReturned)):
                if BytesReturned.value < cb:
                    return ProcessIds, BytesReturned.value
                else:
                    count *= 2
            else:
                return None

    def OpenProcess(self, dwProcessId):
        dwDesiredAccess = (PROCESS_QUERY_INFORMATION |
                           PROCESS_VM_OPERATION |
                           PROCESS_VM_READ | PROCESS_VM_WRITE)
        bInheritHandle = False
        hProcess = ctypes.windll.kernel32.OpenProcess(
                                                    dwDesiredAccess,
                                                    bInheritHandle,
                                                    dwProcessId
                                                    )
        if hProcess:
            return hProcess
        else:
            return None

    def CloseHandle(self, hProcess):
        ctypes.windll.kernel32.CloseHandle(hProcess)
        return self.GetLastError()

    def GetLastError(self):
        return ctypes.windll.kernel32.GetLastError()

    def getPointer(self, hProcess, lpBaseAddress, offsets):
        pointer = self.ReadProcessMemory2(hProcess, lpBaseAddress)
        if offsets == None:
            return lpBaseAddress
        elif len(offsets) == 1:
            temp = int(str(pointer), 0) + int(str(offsets[0]), 0)
            return temp
        else:
            count = len(offsets)
            for i in offsets:
                count -= 1
                temp = int(str(pointer), 0) + int(str(i), 0)
                pointer = self.ReadProcessMemory2(hProcess, temp)
                if count == 1:
                    break
            return pointer

    def ReadProcessMemory(self, hProcess, lpBaseAddress):
        try:
            lpBaseAddress = lpBaseAddress
            ReadBuffer = ctypes.c_uint()
            lpBuffer = ctypes.byref(ReadBuffer)
            nSize = ctypes.sizeof(ReadBuffer)
            lpNumberOfBytesRead = ctypes.c_ulong(0)

            ctypes.windll.kernel32.ReadProcessMemory(
                                                    hProcess,
                                                    lpBaseAddress,
                                                    lpBuffer,
                                                    nSize,
                                                    lpNumberOfBytesRead
                                                    )
            return ReadBuffer.value
        except (BufferError, ValueError, TypeError):
            self.CloseHandle(hProcess)
            e = 'Handle Closed, Error', hProcess, self.GetLastError()
            return e

    def ReadProcessMemory2(self, hProcess, lpBaseAddress):
        try:
            lpBaseAddress = lpBaseAddress
            ReadBuffer = ctypes.c_uint()
            lpBuffer = ctypes.byref(ReadBuffer)
            nSize = ctypes.sizeof(ReadBuffer)
            lpNumberOfBytesRead = ctypes.c_ulong(0)

            ctypes.windll.kernel32.ReadProcessMemory(
                                                    hProcess,
                                                    lpBaseAddress,
                                                    lpBuffer,
                                                    nSize,
                                                    lpNumberOfBytesRead
                                                    )
            return ReadBuffer.value
        except (BufferError, ValueError, TypeError):
            self.CloseHandle(hProcess)
            e = 'Handle Closed, Error', hProcess, self.GetLastError()
            return e

    def WriteProcessMemory(self, hProcess, lpBaseAddress, Value):
        try:
            lpBaseAddress = lpBaseAddress
            Value = Value
            WriteBuffer = ctypes.c_uint(Value)
            lpBuffer = ctypes.byref(WriteBuffer)
            nSize = ctypes.sizeof(WriteBuffer)
            lpNumberOfBytesWritten = ctypes.c_ulong(0)

            ctypes.windll.kernel32.WriteProcessMemory(
                                                    hProcess,
                                                    lpBaseAddress,
                                                    lpBuffer,
                                                    nSize,
                                                    lpNumberOfBytesWritten
                                                    )
        except (BufferError, ValueError, TypeError):
            self.CloseHandle(hProcess)
            e = 'Handle Closed, Error', hProcess, self.GetLastError()
            return e


rwm = ReadWriteMemory()

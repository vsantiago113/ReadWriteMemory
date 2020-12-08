from typing import Any,  List
import os.path
import ctypes
import ctypes.wintypes

# Process Permissions
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_OPERATION = 0x0008
PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020
PROCESS_ALL_ACCESS = 0x1f0fff

MAX_PATH = 260


class ReadWriteMemoryError(Exception):
    pass


class Process(object):
    """
    The Process class holds the information about the requested process.
    """
    def __init__(self, name: [str, bytes] = '', pid: int = -1, handle: int = -1, error_code: [str, bytes] = None):
        """
        :param name: The name of the executable file for the specified process.
        :param pid: The process ID.
        :param handle: The process handle.
        :param error_code: The error code from a process failure.
        """
        self.name = name
        self.pid = pid
        self.handle = handle
        self.error_code = error_code

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}: "{self.name}"'

    def open(self):
        """
        Open the process with the Query, Operation, Read and Write permissions and return the process handle.

        :return: True if the handle exists if not return False
        """
        dw_desired_access = (PROCESS_QUERY_INFORMATION | PROCESS_VM_OPERATION | PROCESS_VM_READ | PROCESS_VM_WRITE)
        b_inherit_handle = True
        self.handle = ctypes.windll.kernel32.OpenProcess(dw_desired_access, b_inherit_handle, self.pid)
        if not self.handle:
            raise ReadWriteMemoryError(f'Unable to open process <{self.name}>')

    def close(self) -> int:
        """
        Closes the handle of the process.

        :return: The last error code from the result after an attempt to close the handle.
        """
        ctypes.windll.kernel32.CloseHandle(self.handle)
        return self.get_last_error()
   
    def get_all_access_handle(self):
        """
        Gets full access handle of the process.

        :return: handle of the process
        """
        b_inherit_handle = True
        self.handle = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, b_inherit_handle, self.pid)
    
    @staticmethod
    def get_last_error() -> int:
        """
        Get the last error code.

        :return: The last error code.
        """
        return ctypes.windll.kernel32.GetLastError()

    def get_pointer(self, lp_base_address: hex, offsets: List[hex] = ()) -> int:
        """
        Get the pointer of a given address.

        :param lp_base_address: The address from where you want to get the pointer.
        :param offsets: a list of offets.

        :return: The pointer of a give address.
        """
        temp_address = self.read(lp_base_address)
        pointer = 0x0
        if not offsets:
            return lp_base_address
        else:
            for offset in offsets:
                pointer = int(str(temp_address), 0) + int(str(offset), 0)
                temp_address = self.read(pointer)
            return pointer

    def read(self, lp_base_address: int) -> Any:
        """
        Read data from the process's memory.

        :param lp_base_address: The process's pointer

        :return: The data from the process's memory if succeed if not raises an exception.
        """
        try:
            read_buffer = ctypes.c_uint()
            lp_buffer = ctypes.byref(read_buffer)
            n_size = ctypes.sizeof(read_buffer)
            lp_number_of_bytes_read = ctypes.c_ulong(0)
            ctypes.windll.kernel32.ReadProcessMemory(self.handle, ctypes.c_void_p(lp_base_address), lp_buffer,
                                                     n_size, lp_number_of_bytes_read)
            return read_buffer.value
        except (BufferError, ValueError, TypeError) as error:
            if self.handle:
                self.close()
            self.error_code = self.get_last_error()
            error = {'msg': str(error), 'Handle': self.handle, 'PID': self.pid,
                     'Name': self.name, 'ErrorCode': self.error_code}
            ReadWriteMemoryError(error)

    def write(self, lp_base_address: int, value: int) -> bool:
        """
        Write data to the process's memory.

        :param lp_base_address: The process' pointer.
        :param value: The data to be written to the process's memory

        :return: It returns True if succeed if not it raises an exception.
        """
        try:
            write_buffer = ctypes.c_uint(value)
            lp_buffer = ctypes.byref(write_buffer)
            n_size = ctypes.sizeof(write_buffer)
            lp_number_of_bytes_written = ctypes.c_ulong(0)
            ctypes.windll.kernel32.WriteProcessMemory(self.handle, ctypes.c_void_p(lp_base_address), lp_buffer,
                                                      n_size, lp_number_of_bytes_written)
            return True
        except (BufferError, ValueError, TypeError) as error:
            if self.handle:
                self.close()
            self.error_code = self.get_last_error()
            error = {'msg': str(error), 'Handle': self.handle, 'PID': self.pid,
                     'Name': self.name, 'ErrorCode': self.error_code}
            ReadWriteMemoryError(error)


class ReadWriteMemory:
    """
    The ReadWriteMemory Class is used to read and write to the memory of a running process.
    """
    def __init__(self):
        self.process = Process()

    def get_process_by_name(self, process_name: [str, bytes]) -> "Process":
        """
        :description: Get the process by the process executabe\'s name and return a Process object.

        :param process_name: The name of the executable file for the specified process for example, my_program.exe.

        :return: A Process object containing the information from the requested Process.
        """
        if not process_name.endswith('.exe'):
            self.process.name = process_name + '.exe'

        process_ids = self.enumerate_processes()

        for process_id in process_ids:
            self.process.handle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, False, process_id)
            if self.process.handle:
                image_file_name = (ctypes.c_char * MAX_PATH)()
                if ctypes.windll.psapi.GetProcessImageFileNameA(self.process.handle, image_file_name, MAX_PATH) > 0:
                    filename = os.path.basename(image_file_name.value)
                    if filename.decode('utf-8') == process_name:
                        self.process.pid = process_id
                        self.process.name = process_name
                        return self.process
                self.process.close()

        raise ReadWriteMemoryError(f'Process "{self.process.name}" not found!')

    def get_process_by_id(self, process_id: int) -> "Process":
        """
        :description: Get the process by the process ID and return a Process object.

        :param process_id: The process ID.

        :return: A Process object containing the information from the requested Process.
        """

        self.process.handle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, False, process_id)
        if self.process.handle:
            image_file_name = (ctypes.c_char * MAX_PATH)()
            if ctypes.windll.psapi.GetProcessImageFileNameA(self.process.handle, image_file_name, MAX_PATH) > 0:
                filename = os.path.basename(image_file_name.value)
                self.process.pid = process_id
                self.process.name = filename.decode('utf-8')
                self.process.close()
                return self.process
            else:
                raise ReadWriteMemoryError(f'Unable to get the executable\'s name for PID={self.process.pid}!')

        raise ReadWriteMemoryError(f'Process "{self.process.pid}" not found!')

    @staticmethod
    def enumerate_processes() -> list:
        """
        Get the list of running processes ID's from the current system.

        :return: A list of processes ID's
        """
        count = 32
        while True:
            process_ids = (ctypes.wintypes.DWORD * count)()
            cb = ctypes.sizeof(process_ids)
            bytes_returned = ctypes.wintypes.DWORD()
            if ctypes.windll.Psapi.EnumProcesses(ctypes.byref(process_ids), cb, ctypes.byref(bytes_returned)):
                if bytes_returned.value < cb:
                    return list(set(process_ids))
                else:
                    count *= 2

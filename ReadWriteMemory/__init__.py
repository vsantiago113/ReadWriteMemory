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
    def __init__(self):
        self.process_id = None
        self.process_name = None
        self.handle_process = None

    def get_process_id_by_name(self, process_name):
        if not process_name.endswith('.exe'):
            process_name = process_name + '.exe'

        process_ids, bytes_returned = self.enumerate_processes()

        for index in range(int(bytes_returned / ctypes.sizeof(ctypes.wintypes.DWORD)))[:-1]:
            process_id = process_ids[index]
            handle_process = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, False, process_id)
            if handle_process:
                image_file_name = (ctypes.c_char * MAX_PATH)()
                if ctypes.windll.psapi.GetProcessImageFileNameA(handle_process, image_file_name, MAX_PATH) > 0:
                    filename = os.path.basename(image_file_name.value)
                    if filename.decode('utf-8') == process_name:
                        self.process_id = process_id
                        self.process_name = process_name
                        return process_id
                self.close()

    @staticmethod
    def enumerate_processes():
        count = 32
        while True:
            process_ids = (ctypes.wintypes.DWORD * count)()
            cb = ctypes.sizeof(process_ids)
            bytes_returned = ctypes.wintypes.DWORD()
            if ctypes.windll.Psapi.EnumProcesses(ctypes.byref(process_ids), cb, ctypes.byref(bytes_returned)):
                if bytes_returned.value < cb:
                    return process_ids, bytes_returned.value
                else:
                    count *= 2

    def open(self):
        dw_desired_access = (PROCESS_QUERY_INFORMATION | PROCESS_VM_OPERATION | PROCESS_VM_READ | PROCESS_VM_WRITE)
        b_inherit_handle = False
        handle_process = ctypes.windll.kernel32.OpenProcess(dw_desired_access, b_inherit_handle, self.process_id)
        self.handle_process = handle_process
        return handle_process

    def close(self):
        ctypes.windll.kernel32.CloseHandle(self.handle_process)
        return self.get_last_error()

    @staticmethod
    def get_last_error():
        return ctypes.windll.kernel32.GetLastError()

    def get_pointer(self, lp_base_address, offsets=None):
        temp_address = self.read(lp_base_address)
        pointer = 0x0
        if not offsets:
            return lp_base_address
        else:
            for offset in offsets:
                pointer = int(str(temp_address), 0) + int(str(offset), 0)
                temp_address = self.read(pointer)
            return pointer

    def read(self, lp_base_address):
        try:
            read_buffer = ctypes.c_uint()
            lp_buffer = ctypes.byref(read_buffer)
            n_size = ctypes.sizeof(read_buffer)
            lp_number_of_bytes_read = ctypes.c_ulong(0)
            ctypes.windll.kernel32.ReadProcessMemory(self.handle_process, lp_base_address, lp_buffer,
                                                     n_size, lp_number_of_bytes_read)
            return read_buffer.value
        except (BufferError, ValueError, TypeError):
            self.close()
            error = 'Handle Closed, Error', self.handle_process, self.get_last_error()
            return error

    def write(self, lp_base_address, value):
        try:
            write_buffer = ctypes.c_uint(value)
            lp_buffer = ctypes.byref(write_buffer)
            n_size = ctypes.sizeof(write_buffer)
            lp_number_of_bytes_written = ctypes.c_ulong(0)
            ctypes.windll.kernel32.WriteProcessMemory(self.handle_process, lp_base_address, lp_buffer,
                                                      n_size, lp_number_of_bytes_written)
        except (BufferError, ValueError, TypeError):
            self.close()
            error = 'Handle Closed, Error', self.handle_process, self.get_last_error()
            return error

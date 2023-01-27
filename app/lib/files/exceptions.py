class FileNotExist(Exception):
    def __init__(self, msg: str = "No arguments bytes_buffer or filename") -> None:
        super().__init__(msg)

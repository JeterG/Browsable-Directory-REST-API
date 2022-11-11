from pathlib import Path
import os
import shutil


class Helper:
    def __init__(self, ROOT_DIRECTORY) -> None:
        self.ROOT_DIRECTORY = ROOT_DIRECTORY

    def get_json_body(self, name: str, path: str) -> dict:
        """Helper method to generate the JSON body with standard fields.

        Args:
            name (str): the name of the file/directory
            path (str): the rest of the file/directory path.

        Returns:
            (dict): the resulting json body with populated data fields about the file/directory
        """
        if path != "/":
            full_path = path + "/" + name if name not in path else path
        else:
            full_path = name
        file = Path(full_path)
        if file.exists():
            file_stat = file.stat()
            return {
                "File_Name": name,
                "Owner": file.owner(),
                "Size": file_stat.st_size,
                "Permissions": oct(file_stat.st_mode)[-3:],
                "Type": "file" if file.is_file() else "directory",
            }
        else:
            return {"File_Name": name, "Permissions": "DENIED"}

    def create_directory(self, directory_path: str) -> None:
        """Creates directories in directory_path recursively if they do not already exist.

        Args:
            directory_path (str): the "/" separated directories
        """
        os.makedirs(directory_path, exist_ok=True)

    def _write_to_file(self, file_path: str, content: str, mode: str) -> None:
        """_summary_

        Args:
            file_path (str): the "/" separated path to file
            content (str): the content to write to file
            mode (str): one of ["x","w","a"] for creating, overwriting, extending file content
        """

        if "/" in file_path:
            directory_paths = file_path.rsplit("/", 1)[0]
            self.create_directory(self.ROOT_DIRECTORY + directory_paths)
        file = open(self.ROOT_DIRECTORY + file_path, mode)
        file.write(content)
        file.close()

    def create_new_file(self, file_path: str, content: str) -> None:
        """
            Creates a new file populated by `content` in the path ROOT_DIRECTORY+file_path

        Args:
            file_path (str): the "/" separated path to file
            content (str): the content to write to file
        """
        self._write_to_file(file_path, content, "x")

    def overwrite_existing_file(self, file_path: str, content: str) -> None:
        """
            Overwrites file content with `content` in the path ROOT_DIRECTORY+file_path

        Args:
            file_path (str): the "/" separated path to file
            content (str): the content to write to file
        """
        self._write_to_file(file_path, content, "w")

    def extend_existing_file(self, file_path: str, content: str):
        """
            Appends `content` to existing file at ROOT_DIRECTORY+file_path

        Args:
            file_path (str): the "/" separated path to file
            content (str): the content to write to file
        """

        self._write_to_file(file_path, "\n" + content, "a")

    def delete_file_or_directory(self, path: str) -> bool:
        """
            Deletes file/directory if it exists
        Args:
            path (str): the "/" separated path to delete
        Returns:
            (bool): whether a deletion occured.
        """
        pointer = Path(path)
        if pointer.exists():
            if pointer.is_dir():
                shutil.rmtree(path)
            if pointer.is_file():
                os.remove(path)
            return True
        return False

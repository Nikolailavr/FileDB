import json
from dataclasses import dataclass
import xmltodict

from filedb.models import File, FileType
from misc.constants import REQUIRED_FIELDS


@dataclass
class Result:
    status: bool
    error: bool = False
    err_message: str = ''


class UploadedFile:

    def __init__(self, file):
        self.file = file

    def __check_file_type(self):
        extension = self.file.name.split('.')[-1].lower()
        if extension == 'xml':
            self.__load_data_from_xml()
        elif extension == 'json':
            self.__load_data_from_json()

    def __load_data_from_xml(self):
        """Загрузка данных из файла XML"""
        try:
            data = xmltodict.parse(self.file)
            for value in data.values():
                if len(value) > 2:
                    self.data = value
        except Exception as ex:
            raise ex

    def __load_data_from_json(self):
        """Загрузка данных из файла JSON"""
        try:
            self.data = json.load(self.file)
        except json.JSONDecodeError:
            raise json.JSONDecodeError

    def is_valid(self, required_fields: list[str] = REQUIRED_FIELDS) -> Result:
        """Проверка на наличие требуемых полей"""
        try:
            self.__check_file_type()
        except Exception as ex:
            return Result(
                status=False,
                error=True,
                err_message=ex.__str__()
            )
        else:
            return self.__check_file_fields(required_fields)

    def __check_file_fields(self, required_fields) -> Result:
        """Проверочные условия"""
        # Наличие требуемых полей
        if not all(field in self.data for field in required_fields):
            return Result(
                status=False,
                error=True,
                err_message='Required fields are missing in the File'
            )
        # Тип совпадает с предложенными
        if all(self.data.get('type') != member.value for member in FileType):
            return Result(
                status=False,
                error=True,
                err_message=f'{self.data.get("type")} is not a valid FileType'
            )
        return Result(True)

    def save(self, required_fields: list[str] = REQUIRED_FIELDS):
        file_instance = File(
            type=FileType(self.data.get('type')),
            vendor=self.data.get('vendor'),
            date_revision=self.data.get('date_revision'),
            extra_field=json.dumps(
                {
                    key: value
                    for key, value in self.data.items()
                    if key not in required_fields
                }
            )
        )
        file_instance.save()
        return file_instance

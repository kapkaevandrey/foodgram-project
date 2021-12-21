import csv
import os
import pathlib

from chardet import detect
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from recipes.models import IngredientType


User = get_user_model()


class Command(BaseCommand):
    FILES_AND_MODELS_NAME = {
        'ingredients.csv': {'model_obj': IngredientType},
    }

    help = "This script update rating in DB models Title."

    def check_that_all_files_exists(self) -> None:
        """Проверяет наличие необходимых файлов в директории."""
        for file in Command.FILES_AND_MODELS_NAME:
            if not os.path.exists(file):
                raise CommandError(f'"{file}" not exist in dir {os.getcwd()} ')
            self.stdout.write(self.style.SUCCESS(f'File {file} is exists.'))

    @staticmethod
    def go_to_dir_with_data_files(path: str) -> None:
        """Переходит в директорию где должны хранится файлы для заполнения из БД.
        По умолчанию: ~/static/data"""
        if path is None:
            os.chdir(settings.BASE_DIR)
            os.chdir("..")
            os.chdir(pathlib.Path.cwd() / 'data')
            print(os.getcwd())
        elif os.path.exists(path):
            os.chdir(path)
        else:
            raise CommandError(f"Path {path} is not exist")

    @staticmethod
    def detect_encoding(file) -> dict:
        with open(file, "rb") as f:
            return detect(f.read())

    @staticmethod
    def get_file_reader(file: str):
        encoding_info = Command.detect_encoding(file)
        with open(file, "r", encoding=encoding_info["encoding"]) as f:
            reader = list(csv.DictReader(f))
            if len(reader) == 0:
                raise CommandError("File is empty")
            return reader

    @staticmethod
    def load_data_from_csv():
        for file_name, data in Command.FILES_AND_MODELS_NAME.items():
            reader = Command.get_file_reader(file_name)
            model_object = data['model_obj']
            for row in reader:
                model_object.objects.create(**row)

    def add_arguments(self, parser):
        parser.add_argument(
            'path_to_dir',
            type=str,
            help='Abs path to dir with files',
            nargs="?")

    def handle(self, *args, **options):
        path = options['path_to_dir']
        Command.go_to_dir_with_data_files(path=path)
        self.check_that_all_files_exists()
        try:
            Command.load_data_from_csv()
        except Exception as error:
            raise CommandError("Objects can create", error)
        self.stdout.write(self.style.SUCCESS('Date Base Update.'))

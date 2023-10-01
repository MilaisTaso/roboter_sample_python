import configparser
import os
import csv
import collections

import my_conf

# 扱うcsvファイルの名称とキー
DEFAULT_CSV_FILE_PATH = 'restaurant.csv'
DEFAULT_COLUMN_NAME = 'NAME'
DEFAULT_COLUMN_COUNT = 'COUNT'


class CsvModel(object):
    """csvファイルを利用するベースクラス"""

    def __init__(
            self,
            csv_file_name: str = None,
            field_names: dict[str] | None = None,
    ) -> None:
        """クラス内で扱うcsvファイルの指定、なければ作成する

        Argus:
            csv_file_name (str): csvファイルの名称
            filed_name (dict[str]) csvファイルのキー

        Returns:
            None:
        """
        self.csv_dir_path = my_conf.read_config_file()['default'].get('csv_dir')
        self.csv_file_name: str = csv_file_name
        if not self.csv_file_name:
            self.csv_file_name: str = DEFAULT_CSV_FILE_PATH
        self.csv_file_path = self.find_csv_file_path(self.csv_file_name)

        self.field_names: list[str] | None = field_names
        if not field_names:
            self.field_names: list[str] | None = [
                DEFAULT_COLUMN_NAME,
                DEFAULT_COLUMN_COUNT
            ]

        self.data = collections.defaultdict(int)
        self.store_csv_file()

    def find_csv_file_path(self, csv_file_name: str | None = None) -> str:
        """csvファイルの保存先を取得する

        設定ファイルからパスを取得する
        ない場合はディレクトリを２つ遡ってからパスを作成

        Argus:
            csv_file_name (str | None): csvファイルの名称

        Returns:
            str: 読み書きを行うcsvファイルの絶対パス
        """
        if not self.csv_dir_path:
            base_dir = os.path.dirname(os.path.dirname(
                os.path.abspath(__file__)))
            csv_dir_path = os.path.join(base_dir, 'csv')
        csv_file_path = os.path.join(self.csv_dir_path, csv_file_name)

        return csv_file_path

    def store_csv_file(self) -> None:
        """指定のカラムを書き込んだcsvファイルと保存先のディレクトリを作成する

        Argus:
            csv_file_name (str): 読み書きするcsvファイルの絶対パス

        Returns:
            None: csvファイルを作成するだけで値を返さない
        """
        if not os.path.exists(self.csv_dir_path):
            os.makedirs(self.csv_dir_path, exist_ok=True)
        if not os.path.isfile(self.csv_file_path):
            with open(self.csv_file_path, 'w') as csv_file:
                columns = csv.DictWriter(csv_file, fieldnames=self.field_names)
                columns.writeheader()

    def load_data(self):
        pass


class RestaurantModel(CsvModel):
    def __init__(
            self,
            csv_file_name: str = None,
            field_names: dict[str] | None = None,
            *args,
            **kwargs
    ):
        super().__init__(csv_file_name, *args, **kwargs)
        self.load_data()

    def load_data(self) -> dict[str, int]:
        """csvファイルからレストランモデル用のデータを取得する

        Returns:
            dict[str, int]: csvファイルのデータ
        """
        with open(self.csv_file_path, 'r+') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                self.data[row[DEFAULT_COLUMN_NAME]] = int(
                    row[DEFAULT_COLUMN_COUNT])
        return self.data

    def save(self, restaurant_name: str) -> None:
        """csvファイルに新しいレストランを追加する ある場合はCOUNTを増やす

        Args:
            restaurant_name (str): レストランの名称

        :return:
            None: csvファイルのデータを更新するだけ返却なし
        """
        if restaurant_name in self.data:
            self.data[restaurant_name] += 1
        else:
            self.data[restaurant_name] = 1

        with open(self.csv_file_path, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file,
                                    fieldnames=self.field_names)
            writer.writeheader()
            for key, value in self.data.items():
                writer.writerow({self.field_names[0]: key,
                                 self.field_names[1]: value})

    @property
    def sort_restaurant_by_count(self) -> list:
        """csvファイル内のデータをCOUNTが多い順に並び替える

        Returns：
            dict: 並び替え後おデータ
        """
        sorted_restaurants = sorted(
            self.data.items(), key=lambda item: item[1], reverse=True)
        return [item[0] for item in sorted_restaurants]
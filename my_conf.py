import os
import sys
import configparser


def read_config_file(
        config_file_name: str = 'config.ini') -> configparser.ConfigParser:
    """設定ファイルを読み込む

    Args:
        config_file_name (str): 設定ファイルのパス

    Returns:
        ConfigParser: 設定ファイルの内容

    Exceptions:
        OSError, PermissionError: ファイルの読込み or 書込みに失敗した際のエラー
        configparser.Error: 設定ファイルの定義に問題があった際のエラー
    """
    try:
        if not os.path.isfile(config_file_name):
            config = store_config_file(config_file_name)
        else:
            config = configparser.ConfigParser()
            config.read(config_file_name)
        return config
    except (OSError, PermissionError) as err:
        print(f"Error occurred when reading/writing config file: {err}")
        sys.exit(1)
    except configparser.Error as err:
        print(f"Error occurred when parsing config file: {err}")
        sys.exit(1)


def store_config_file(
        config_file_name: str = 'config.ini') -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config['default'] = {
        'robot_name': 'roboko',
        'template_dir': 'roboter/templates',
        'csv_dir': 'roboter/csv'
    }
    with open(config_file_name, 'w') as config_file:
        config.write(config_file)
    return config

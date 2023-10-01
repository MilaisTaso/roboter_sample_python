import os
import string

import my_conf


def get_template_dir_path(config_file_name='config.ini'):
    """設定ファイル or デフォルトのテンプレートがあるディレクトリを返す

    Returns:
        str: templateディレクトリの絶対パス
    Raises:
        importError: 設定ファイルの呼び出し失敗時のエラー
    """
    config = my_conf.read_config_file()
    template_dir_path = config['default'].get('template_dir')

    if not template_dir_path:
        default_dir = os.path.dirname(os.path.dirname(
            os.path.abspath(__file__)))
        template_dir_path = os.path.join(default_dir, 'templates')

    return template_dir_path


def find_template(file_name: str) -> str:
    """引数で渡されたファルが存在するか検索する

    Args:
        file_name (str): 検索するファイルの名称

    Returns:
        str: ファイルの絶対パス

    Raises:
        NoTemplateError: テンプレートとなるファイルが存在しないエラー
    """
    template_dir_path = get_template_dir_path()
    template_file_path = os.path.join(template_dir_path, file_name)
    if not os.path.exists(template_file_path):
        raise NoTemplateError(f"Could not find {file_name}")
    return template_file_path


def get_template(file_name: str) -> string.Template:
    """引数で指定されたファイルをテンプレート文字列にする

    Args:
        file_name (str): ファイルの名称 別メソッドで存在するかチェックを行う

    Returns:
        string.templates: 読み込みでファイルを開いてテンプレートとする
    """
    file_path = find_template(file_name)
    with open(file_path, 'r') as template_file:
        template = template_file.read()
    return string.Template(template)


class NoTemplateError(Exception):
    pass

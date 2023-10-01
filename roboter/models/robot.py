from typing import Any

import my_conf
from roboter.views import console
from roboter.models import restaurant


class Robot(object):
    """コンソール対話ロボットのベースクラス"""

    def __init__(self, user_name=None):
        config = my_conf.read_config_file()
        self.name = config['default'].get('robot_name')
        self.user_name = user_name

    def hello(self) -> str:
        """挨拶をし、user_nameを取得する
        愛達文はhello.txt参照

        Returns:
            str 利用者の名前
        """
        self.speak('hello.txt', robot=self.name)
        while True:
            self.user_name: str = input('名前を入力してください:')
            if self.user_name: break
        return self.user_name

    def speak(
            self,
            file_name: str,
            **kwargs: Any
    ) -> str:
        """テンプレートにキーワードを渡して表示する

        Args:
            file_name (str): テンプレートファイルの名称
            **kwargs Any: テンプレート文字列へ埋め込む値

        Returns:
            str: コンソールへ表示後、表示した文字列を返す
        """
        template_file = console.get_template(file_name)
        contents = template_file.substitute(**kwargs)
        print(contents)
        return contents


class RestaurantRobot(Robot):
    """お気に入りのレストランを取得する会話ロボット"""
    def __init__(self):
        super().__init__()
        self.restaurant_model = restaurant.RestaurantModel()

    def ask_recommend_restaurant(self) -> str | None:
        sorted_restaurants = self.restaurant_model.sort_restaurant_by_count
        if not sorted_restaurants:
            user_recommend_restaurant = self.question_recommend_restaurant()
            return user_recommend_restaurant
        user_recommend_restaurant = None
        complete = False

        for sorted_restaurant in sorted_restaurants:
            while not complete:
                self.speak(
                    'recommend_restaurant.txt',
                    restaurant=sorted_restaurant,
                    name=self.user_name
                )
                answer = input('YesかNoでお答えください')
                capital_answer = answer.capitalize()
                if capital_answer == 'Y' or capital_answer == 'Yes':
                    user_recommend_restaurant = sorted_restaurant
                    self.restaurant_model.save(user_recommend_restaurant)
                    complete = True
                    break
                elif capital_answer == 'N' or capital_answer == 'No':
                    break

        if not user_recommend_restaurant:
            user_recommend_restaurant = self.question_recommend_restaurant()
        return user_recommend_restaurant

    def question_recommend_restaurant(self) -> str:
        """テンプレートを呼び出しユーザーからオススメのラストランを取得する

        Returns:
            str: ユーザーがお勧めするレストラン
        """
        self.speak('question_restaurant.txt', name=self.user_name)
        user_recommend_restaurant = input('オススメのレストラン:')
        self.restaurant_model.save(user_recommend_restaurant)
        return user_recommend_restaurant

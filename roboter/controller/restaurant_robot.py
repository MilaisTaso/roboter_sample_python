"""挨拶からオススメのレストランを訪ねる対話ロボット"""
from roboter.models import robot


def talk_about_restaurant():
    restaurant_robot = robot.RestaurantRobot()
    user_name = restaurant_robot.hello()
    user_recommend_restaurant = restaurant_robot.ask_recommend_restaurant()
    restaurant_robot.speak(
        'thanks.txt',
        name=user_name,
        restaurant=user_recommend_restaurant
    )
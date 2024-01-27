from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class ActionSetDishName(Action):
    def name(self) -> Text:
        return "action_set_dish_name"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the value of the 'recipe' entity from the user message
        recipe_entity = next(tracker.get_latest_entity_values("recipe"), None)

        # Define a list of valid recipes
        valid_recipes = [
            "spaghetti aglio e olio", "caprese salad", "chicken stir-fry",
            "vegetarian quesadillas", "pasta primavera", "omelette",
            "tomato basil bruschetta", "mushroom risotto",
            "honey mustard baked chicken", "tuna salad wrap"
        ]

        if recipe_entity.lower() in valid_recipes:
            # User directly mentions the dish in the current turn
            dispatcher.utter_message(f"Great choice! I've identified the dish as {recipe_entity}. How can I assist you with {recipe_entity} today?")
            # Set the 'recipe' slot with the recognized dish name
            return [SlotSet("recipe", recipe_entity)]

        else:
            # Handle the case where neither the entity nor the slot is available
            dispatcher.utter_message("I couldn't identify the dish name. Can you please specify the recipe?")
            return [SlotSet("recipe", None)]


class ActionGetRecipeCalories(Action):
    def name(self) -> Text:
        return "action_get_recipe_calories"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the value of the 'recipe' entity from the current user message
        recipe_entity = next(tracker.get_latest_entity_values("recipe"), None)

        # Check if the slot 'recipe' has been set in previous turns
        recipe_slot = tracker.get_slot("recipe")

        if recipe_entity:
            # User directly mentions the dish in the current turn
            response = self.get_calorie_response(recipe_entity)
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_calorie_response(recipe_slot)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"

        dispatcher.utter_message(response)
        return []

    @staticmethod
    def get_calorie_response(recipe_name: Text) -> Text:
        if recipe_name.lower() == "spaghetti aglio e olio":
            return "The calorie count for Spaghetti Aglio e Olio is approximately 400 calories per serving."
        elif recipe_name.lower() == "caprese salad":
            return "The calorie count for Caprese Salad is approximately 150 calories per serving."
        elif recipe_name.lower() == "chicken stir-fry":
            return "The calorie count for Chicken Stir-Fry is approximately 300 calories per serving."
        elif recipe_name.lower() == "vegetarian quesadillas":
            return "The calorie count for Vegetarian Quesadillas is approximately 250 calories per serving."
        elif recipe_name.lower() == "pasta primavera":
            return "The calorie count for Pasta Primavera is approximately 350 calories per serving."
        elif recipe_name.lower() == "omelette":
            return "The calorie count for Omelette is approximately 200 calories per serving."
        elif recipe_name.lower() == "tomato basil bruschetta":
            return "The calorie count for Tomato Basil Bruschetta is approximately 120 calories per serving."
        elif recipe_name.lower() == "mushroom risotto":
            return "The calorie count for Mushroom Risotto is approximately 400 calories per serving."
        elif recipe_name.lower() == "honey mustard baked chicken":
            return "The calorie count for Honey Mustard Baked Chicken is approximately 250 calories per serving."
        elif recipe_name.lower() == "tuna salad wrap":
            return "The calorie count for Tuna Salad Wrap is approximately 300 calories per serving."
        else:
            return f"I'm sorry, I don't have information on the calorie count for {recipe_name}."


class ActionGetRecipeVegetarianVersion(Action):
    def name(self) -> Text:
        return "action_get_recipe_vegetarian_version"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the value of the 'recipe' entity from the current user message
        recipe_entity = next(tracker.get_latest_entity_values("recipe"), None)

        # Check if the slot 'recipe' has been set in previous turns
        recipe_slot = tracker.get_slot("recipe")

        if recipe_entity:
            # User directly mentions the dish in the current turn
            response = self.get_vegetarian_version_response(recipe_entity)
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_vegetarian_version_response(recipe_slot)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"

        dispatcher.utter_message(response)
        return []

    @staticmethod
    def get_vegetarian_version_response(recipe_name: Text) -> Text:
        vegetarian_versions = {
            "spaghetti aglio e olio": "Yes, there is a vegetarian version of Spaghetti Aglio e Olio.",
            "caprese salad": "Caprese Salad is naturally vegetarian.",
            "chicken stir-fry": "A vegetarian version of Chicken Stir-Fry can be made using tofu or vegetables.",
            "vegetarian quesadillas": "Vegetarian Quesadillas are already meat-free.",
            "pasta primavera": "Pasta Primavera is a vegetarian dish with a variety of vegetables.",
            "omelette": "For a vegetarian omelette, you can use alternatives like tofu or mushrooms.",
            "tomato basil bruschetta": "Tomato Basil Bruschetta is a vegetarian appetizer.",
            "mushroom risotto": "Mushroom Risotto is a vegetarian dish.",
            "honey mustard baked chicken": "You can make a vegetarian version of Honey Mustard Baked Chicken using plant-based alternatives.",
            "tuna salad wrap": "A vegetarian version of Tuna Salad Wrap can be made using chickpeas or tofu."
        }

        if recipe_name.lower() in vegetarian_versions:
            return vegetarian_versions[recipe_name.lower()]
        else:
            return f"I'm sorry, I don't have information on the vegetarian version of {recipe_name}."


class ActionGetRecipePreparationTime(Action):
    def name(self) -> Text:
        return "action_get_recipe_preparation_time"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the value of the 'recipe' entity from the current user message
        recipe_entity = next(tracker.get_latest_entity_values("recipe"), None)

        # Check if the slot 'recipe' has been set in previous turns
        recipe_slot = tracker.get_slot("recipe")

        if recipe_entity:
            # User directly mentions the dish in the current turn
            response = self.get_preparation_time_response(recipe_entity)
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_preparation_time_response(recipe_slot)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"

        dispatcher.utter_message(response)
        return []

    @staticmethod
    def get_preparation_time_response(recipe_name: Text) -> Text:
        preparation_times = {
            "spaghetti aglio e olio": "The preparation time for Spaghetti Aglio e Olio is approximately 20 minutes.",
            "caprese salad": "The preparation time for Caprese Salad is approximately 10 minutes.",
            "chicken stir-fry": "The preparation time for Chicken Stir-Fry is approximately 15 minutes.",
            "vegetarian quesadillas": "The preparation time for Vegetarian Quesadillas is approximately 20 minutes.",
            "pasta primavera": "The preparation time for Pasta Primavera is approximately 30 minutes.",
            "omelette": "The preparation time for Omelette is approximately 10 minutes.",
            "tomato basil bruschetta": "The preparation time for Tomato Basil Bruschetta is approximately 15 minutes.",
            "mushroom risotto": "The preparation time for Mushroom Risotto is approximately 25 minutes.",
            "honey mustard baked chicken": "The preparation time for Honey Mustard Baked Chicken is approximately 20 minutes.",
            "tuna salad wrap": "The preparation time for Tuna Salad Wrap is approximately 15 minutes."
        }

        if recipe_name.lower() in preparation_times:
            return preparation_times[recipe_name.lower()]
        else:
            return f"I'm sorry, I don't have information on the preparation time for {recipe_name}."
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

        if recipe_entity:
            dispatcher.utter_message(f"Great choice! I've identified the dish as {recipe_entity}. How can I assist you with {recipe_entity} today?")
            # Set the 'recipe' slot with the recognized dish name
            return [SlotSet("recipe", recipe_entity)]
        else:
            # If no 'recipe' entity is found, inform the user
            dispatcher.utter_message("I couldn't identify the dish name. Can you please specify the recipe?")
            return []


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

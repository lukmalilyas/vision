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
            "spaghetti aglio e olio": "Yes, you can make a delightful vegetarian version of Spaghetti Aglio e Olio by using roasted vegetables such as cherry tomatoes, zucchini, and bell peppers.",
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


class ActionGetRecipeRequiredEquipment(Action):
    def name(self) -> Text:
        return "action_get_recipe_required_equipment"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the value of the 'recipe' entity from the current user message
        recipe_entity = next(tracker.get_latest_entity_values("recipe"), None)

        # Check if the slot 'recipe' has been set in previous turns
        recipe_slot = tracker.get_slot("recipe")

        if recipe_entity:
            # User directly mentions the dish in the current turn
            response = self.get_required_equipment_response(recipe_entity)
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_required_equipment_response(recipe_slot)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"

        dispatcher.utter_message(response)
        return []

    @staticmethod
    def get_required_equipment_response(recipe_name: Text) -> Text:
        equipment_info = {
            "spaghetti aglio e olio": "To prepare Spaghetti Aglio e Olio, you'll need a pot for boiling pasta, a pan for sautéing garlic, and tongs for tossing the pasta.",
            "caprese salad": "Caprese Salad is a simple dish that requires a cutting board, a knife, and a serving plate.",
            "chicken stir-fry": "For Chicken Stir-Fry, you'll need a wok or a large skillet, a cutting board, and a sharp knife.",
            "vegetarian quesadillas": "Vegetarian Quesadillas can be made with a skillet, a spatula, and a cutting board.",
            "pasta primavera": "To prepare Pasta Primavera, you'll need a pot for boiling pasta, a pan for sautéing vegetables, and tongs for tossing the pasta.",
            "omelette": "For making an Omelette, you'll need a non-stick skillet, a spatula, and a mixing bowl.",
            "tomato basil bruschetta": "Tomato Basil Bruschetta requires a toaster or an oven, a cutting board, and a knife.",
            "mushroom risotto": "To prepare Mushroom Risotto, you'll need a saucepan, a ladle, and a stirring spoon.",
            "honey mustard baked chicken": "Honey Mustard Baked Chicken can be made with a baking dish, a basting brush, and an oven.",
            "tuna salad wrap": "For Tuna Salad Wrap, you'll need a mixing bowl, a spoon, and a tortilla or wrap.",
        }

        if recipe_name.lower() in equipment_info:
            return equipment_info[recipe_name.lower()]
        else:
            return f"I'm sorry, I don't have information on the required equipment for {recipe_name}."


class ActionGetRecipeAllergens(Action):
    def name(self) -> Text:
        return "action_get_recipe_allergens"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the value of the 'recipe' entity from the current user message
        recipe_entity = next(tracker.get_latest_entity_values("recipe"), None)

        # Check if the slot 'recipe' has been set in previous turns
        recipe_slot = tracker.get_slot("recipe")

        if recipe_entity:
            # User directly mentions the dish in the current turn
            response = self.get_allergens_response(recipe_entity)
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_allergens_response(recipe_slot)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"

        dispatcher.utter_message(response)
        return []

    @staticmethod
    def get_allergens_response(recipe_name: Text) -> Text:
        allergens_info = {
            "spaghetti aglio e olio": "Spaghetti Aglio e Olio may contain wheat in the form of pasta.",
            "caprese salad": "Caprese Salad is generally allergen-free.",
            "chicken stir-fry": "Chicken Stir-Fry may contain soy sauce, which has soy and wheat.",
            "vegetarian quesadillas": "Vegetarian Quesadillas can include ingredients like cheese and wheat tortillas.",
            "pasta primavera": "Pasta Primavera may contain wheat in pasta.",
            "omelette": "Omelette ingredients vary, but common allergens include eggs and milk.",
            "tomato basil bruschetta": "Tomato Basil Bruschetta is generally allergen-free.",
            "mushroom risotto": "Mushroom Risotto may contain dairy.",
            "honey mustard baked chicken": "Honey Mustard Baked Chicken may contain mustard and honey.",
            "tuna salad wrap": "Tuna Salad Wrap may contain fish and other potential allergens."
        }

        if recipe_name.lower() in allergens_info:
            return allergens_info[recipe_name.lower()]
        else:
            return f"I'm sorry, I don't have information on the allergens for {recipe_name}."


class ActionGetRecipeDifficultyLevel(Action):
    def name(self) -> Text:
        return "action_get_recipe_difficulty_level"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the value of the 'recipe' entity from the current user message
        recipe_entity = next(tracker.get_latest_entity_values("recipe"), None)

        # Check if the slot 'recipe' has been set in previous turns
        recipe_slot = tracker.get_slot("recipe")

        if recipe_entity:
            # User directly mentions the dish in the current turn
            response = self.get_difficulty_level_response(recipe_entity)
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_difficulty_level_response(recipe_slot)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"

        dispatcher.utter_message(response)
        return []

    @staticmethod
    def get_difficulty_level_response(recipe_name: Text) -> Text:
        difficulty_levels = {
            "spaghetti aglio e olio": {
                "beginner": True,
                "difficulty": "Easy",
                "skill_level": "Basic",
            },
            "caprese salad": {
                "beginner": True,
                "difficulty": "Very Easy",
                "skill_level": "Basic",
            },
            "chicken stir-fry": {
                "beginner": False,
                "difficulty": "Moderate",
                "skill_level": "Intermediate",
            },
            "vegetarian quesadillas": {
                "beginner": True,
                "difficulty": "Easy",
                "skill_level": "Basic",
            },
            "pasta primavera": {
                "beginner": True,
                "difficulty": "Easy",
                "skill_level": "Basic",
            },
            "omelette": {
                "beginner": True,
                "difficulty": "Easy",
                "skill_level": "Basic",
            },
            "tomato basil bruschetta": {
                "beginner": True,
                "difficulty": "Very Easy",
                "skill_level": "Basic",
            },
            "mushroom risotto": {
                "beginner": False,
                "difficulty": "Moderate",
                "skill_level": "Intermediate",
            },
            "honey mustard baked chicken": {
                "beginner": False,
                "difficulty": "Moderate",
                "skill_level": "Intermediate",
            },
            "tuna salad wrap": {
                "beginner": False,
                "difficulty": "Moderate",
                "skill_level": "Intermediate",
            }
        }

        if recipe_name.lower() in difficulty_levels:
            info = difficulty_levels[recipe_name.lower()]
            return f"The recipe for {recipe_name} is {'suitable for beginners' if info['beginner'] else 'not recommended for beginners'}. " \
                   f"It has a difficulty level of {info['difficulty']} and requires a skill level of {info['skill_level']}."
        else:
            return f"I'm sorry, I don't have information on the difficulty level of {recipe_name}."


class ActionGetRecipeSideDishRecommendation(Action):
    def name(self) -> Text:
        return "action_get_recipe_side_dish_recommendation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the value of the 'recipe' entity from the current user message
        recipe_entity = next(tracker.get_latest_entity_values("recipe"), None)

        # Check if the slot 'recipe' has been set in previous turns
        recipe_slot = tracker.get_slot("recipe")

        if recipe_entity:
            # User directly mentions the dish in the current turn
            response = self.get_side_dish_recommendation_response(recipe_entity)
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_side_dish_recommendation_response(recipe_slot)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"

        dispatcher.utter_message(response)
        return []

    @staticmethod
    def get_side_dish_recommendation_response(recipe_name: Text) -> Text:
        side_dish_recommendations = {
            "spaghetti aglio e olio": "A classic side dish for Spaghetti Aglio e Olio is a simple green salad with a lemon vinaigrette.",
            "caprese salad": "Caprese Salad pairs well with a side of garlic bread or a light soup.",
            "chicken stir-fry": "For Chicken Stir-Fry, consider serving it with steamed rice or vegetable spring rolls.",
            "vegetarian quesadillas": "Vegetarian Quesadillas go well with guacamole, salsa, and sour cream for dipping.",
            "pasta primavera": "Pasta Primavera is delicious with a side of crusty bread or a fresh garden salad.",
            "omelette": "An Omelette is versatile, but you can pair it with a side of mixed greens or hash browns.",
            "tomato basil bruschetta": "Tomato Basil Bruschetta is fantastic with a side of balsamic-glazed roasted vegetables.",
            "mushroom risotto": "Mushroom Risotto can be complemented with a side of sautéed spinach or a simple green salad.",
            "honey mustard baked chicken": "Honey Mustard Baked Chicken pairs well with roasted sweet potatoes or steamed broccoli.",
            "tuna salad wrap": "Tuna Salad Wraps are great with a side of coleslaw or a refreshing fruit salad."
        }
        if recipe_name.lower() in side_dish_recommendations:
            return side_dish_recommendations[recipe_name.lower()]
        else:
            return f"I'm sorry, I don't have information on side dish recommendations for {recipe_name}."


class ActionGetRecipeHazards(Action):
    def name(self) -> Text:
        return "action_get_recipe_hazards"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the value of the 'recipe' entity from the current user message
        recipe_entity = next(tracker.get_latest_entity_values("recipe"), None)

        # Check if the slot 'recipe' has been set in previous turns
        recipe_slot = tracker.get_slot("recipe")

        if recipe_entity:
            # User directly mentions the dish in the current turn
            response = self.get_recipe_hazards_response(recipe_entity)
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_recipe_hazards_response(recipe_slot)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"

        dispatcher.utter_message(response)
        return []

    @staticmethod
    def get_recipe_hazards_response(recipe_name: Text) -> Text:
        recipe_hazards_info = {
            "spaghetti aglio e olio": "When making Spaghetti Aglio e Olio, be cautious of hot oil splatter while sautéing garlic. Additionally, be mindful of boiling water when cooking the pasta.",
            "caprese salad": "Caprese Salad is generally safe to prepare. However, exercise caution when using knives to slice tomatoes and mozzarella.",
            "chicken stir-fry": "When making Chicken Stir-Fry, be careful with the hot wok or pan. Use proper utensils to avoid burns and ensure the chicken is cooked thoroughly.",
            "vegetarian quesadillas": "When preparing Vegetarian Quesadillas, be cautious when flipping them to avoid hot filling spills. Use oven mitts or tongs.",
            "pasta primavera": "Pasta Primavera involves boiling pasta; take care to avoid burns from hot water. Be cautious when handling sharp knives for chopping vegetables.",
            "omelette": "When cooking an Omelette, use caution with the stove and hot pans. Be mindful of potential allergens if adding cheese or other ingredients.",
            "tomato basil bruschetta": "Tomato Basil Bruschetta is generally safe to make. Exercise caution with sharp knives when chopping tomatoes and basil.",
            "mushroom risotto": "When making Mushroom Risotto, be cautious of hot liquids and steam. Stir carefully to prevent burns, and ensure the mushrooms are properly cooked.",
            "honey mustard baked chicken": "When preparing Honey Mustard Baked Chicken, be cautious of cross-contamination with raw chicken. Ensure the chicken reaches a safe internal temperature.",
            "tuna salad wrap": "When assembling Tuna Salad Wraps, be cautious if using a knife to chop ingredients. Ensure the tuna is properly refrigerated and fresh."
        }
        if recipe_name.lower() in recipe_hazards_info:
            return recipe_hazards_info[recipe_name.lower()]
        else:
            return f"I'm sorry, I don't have information on the safety hazards of {recipe_name}."

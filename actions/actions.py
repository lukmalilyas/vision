from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


valid_recipes = [
    "Spaghetti Aglio e Olio",
    "Caprese Salad",
    "Chicken Stir-Fry",
    "Vegetarian Quesadillas",
    "Pasta Primaver",
    "Omelette",
    "Tomato Basil Bruschetta",
    "Mushroom Risotto",
    "Honey Mustard Baked Chicken",
    "Tuna Salad Wrap"
]


class ActionSetDishName(Action):
    def name(self) -> Text:
        return "action_set_dish_name"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the value of the 'recipe' entity from the user message
        recipe_entity = next(tracker.get_latest_entity_values("recipe"), None)

        if recipe_entity in valid_recipes:
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

        if recipe_entity in valid_recipes:
            # User directly mentions the dish in the current turn
            response = self.get_calorie_response(recipe_entity)
            dispatcher.utter_message(response)
            return [SlotSet("recipe", recipe_entity)]
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_calorie_response(recipe_slot)
            dispatcher.utter_message(response)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"
            dispatcher.utter_message(response)
            return [SlotSet("recipe", None)]

        return []

    @staticmethod
    def get_calorie_response(recipe_name: Text) -> Text:
        recipe_calories_info = {
            "spaghetti aglio e olio": "The calorie count for Spaghetti Aglio e Olio is approximately 400 calories per serving.",
            "caprese salad": "The calorie count for Caprese Salad is approximately 150 calories per serving.",
            "chicken stir-fry": "The calorie count for Chicken Stir-Fry is approximately 300 calories per serving.",
            "vegetarian quesadillas": "The calorie count for Vegetarian Quesadillas is approximately 250 calories per serving.",
            "pasta primavera": "The calorie count for Pasta Primavera is approximately 350 calories per serving.",
            "omelette": "The calorie count for Omelette is approximately 200 calories per serving.",
            "tomato basil bruschetta": "The calorie count for Tomato Basil Bruschetta is approximately 120 calories per serving.",
            "mushroom risotto": "The calorie count for Mushroom Risotto is approximately 400 calories per serving.",
            "honey mustard baked chicken": "The calorie count for Honey Mustard Baked Chicken is approximately 250 calories per serving.",
            "tuna salad wrap": "The calorie count for Tuna Salad Wrap is approximately 300 calories per serving."
        }

        # Check if the recognized dish is in the recipe_calories_info dictionary
        if recipe_name.lower() in recipe_calories_info:
            return recipe_calories_info[recipe_name.lower()]
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

        if recipe_entity in valid_recipes:
            # User directly mentions the dish in the current turn
            response = self.get_vegetarian_version_response(recipe_entity)
            dispatcher.utter_message(response)
            return [SlotSet("recipe", recipe_entity)]
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_vegetarian_version_response(recipe_slot)
            dispatcher.utter_message(response)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"
            dispatcher.utter_message(response)
            return [SlotSet("recipe", None)]

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

        # Check if the recognized dish is in the vegetarian_versions dictionary
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

        if recipe_entity in valid_recipes:
            # User directly mentions the dish in the current turn
            response = self.get_preparation_time_response(recipe_entity)
            dispatcher.utter_message(response)
            return [SlotSet("recipe", recipe_entity)]
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_preparation_time_response(recipe_slot)
            dispatcher.utter_message(response)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"
            dispatcher.utter_message(response)
            return [SlotSet("recipe", None)]

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

        # Check if the recognized dish is in the preparation_times dictionary
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

        if recipe_entity in valid_recipes:
            # User directly mentions the dish in the current turn
            response = self.get_required_equipment_response(recipe_entity)
            dispatcher.utter_message(response)
            return [SlotSet("recipe", recipe_entity)]
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_required_equipment_response(recipe_slot)
            dispatcher.utter_message(response)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"
            dispatcher.utter_message(response)
            return [SlotSet("recipe", None)]

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

        if recipe_entity in valid_recipes:
            # User directly mentions the dish in the current turn
            response = self.get_allergens_response(recipe_entity)
            dispatcher.utter_message(response)
            return [SlotSet("recipe", recipe_entity)]
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_allergens_response(recipe_slot)
            dispatcher.utter_message(response)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"
            dispatcher.utter_message(response)
            return [SlotSet("recipe", None)]

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

        if recipe_entity in valid_recipes:
            # User directly mentions the dish in the current turn
            response = self.get_difficulty_level_response(recipe_entity)
            dispatcher.utter_message(response)
            return [SlotSet("recipe", recipe_entity)]
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_difficulty_level_response(recipe_slot)
            dispatcher.utter_message(response)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"
            dispatcher.utter_message(response)
            return [SlotSet("recipe", None)]

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

        if recipe_entity in valid_recipes:
            # User directly mentions the dish in the current turn
            response = self.get_side_dish_recommendation_response(recipe_entity)
            dispatcher.utter_message(response)
            return [SlotSet("recipe", recipe_entity)]
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_side_dish_recommendation_response(recipe_slot)
            dispatcher.utter_message(response)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"
            dispatcher.utter_message(response)
            return [SlotSet("recipe", None)]

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

        if recipe_entity in valid_recipes:
            # User directly mentions the dish in the current turn
            response = self.get_recipe_hazards_response(recipe_entity)
            dispatcher.utter_message(response)
            return [SlotSet("recipe", recipe_entity)]
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_recipe_hazards_response(recipe_slot)
            dispatcher.utter_message(response)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"
            dispatcher.utter_message(response)
            return [SlotSet("recipe", None)]

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


class ActionBakingTimeAndTemperature(Action):
    def name(self) -> Text:
        return "action_baking_time_and_temperature"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the value of the 'recipe' entity from the current user message
        recipe_entity = next(tracker.get_latest_entity_values("recipe"), None)

        # Check if the slot 'recipe' has been set in previous turns
        recipe_slot = tracker.get_slot("recipe")

        if recipe_entity in valid_recipes:
            # User directly mentions the dish in the current turn
            response = self.get_baking_time_and_temperature_response(recipe_entity)
            dispatcher.utter_message(response)
            return [SlotSet("recipe", recipe_entity)]
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_baking_time_and_temperature_response(recipe_slot)
            dispatcher.utter_message(response)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"
            dispatcher.utter_message(response)
            return [SlotSet("recipe", None)]

        return []

    @staticmethod
    def get_baking_time_and_temperature_response(recipe_name: Text) -> Text:
        baking_info = {
            "spaghetti aglio e olio": None,  # Example: This dish doesn't require baking
            "caprese salad": None,  # Example: This dish doesn't require baking
            "chicken stir-fry": None,  # Example: This dish doesn't require baking
            "vegetarian quesadillas": None,  # Example: This dish doesn't require baking
            "pasta primavera": {
                "temperature": "350°F",
                "duration": "20 minutes",
                "tips": "Preheat the oven, bake until pasta is golden and bubbling.",
            },
            "omelette": None,  # Example: This dish doesn't require baking
            "tomato basil bruschetta": None,  # Example: This dish doesn't require baking
            "mushroom risotto": None,  # Example: This dish doesn't require baking
            "honey mustard baked chicken": {
                "temperature": "375°F",
                "duration": "30 minutes",
                "tips": "Preheat the oven, bake until chicken is cooked through and golden.",
            },
            "tuna salad wrap": None,  # Example: This dish doesn't require baking
        }

        if recipe_name.lower() in baking_info:
            info = baking_info[recipe_name.lower()]

            if info is None:
                # This dish doesn't require baking
                response = f"{recipe_name} doesn't require baking. It's ready to enjoy!"
            else:
                # Provide baking information
                response = f"For {recipe_name}, I recommend baking at {info['temperature']} for {info['duration']}. {info['tips']}"
            return response
        else:
            return f"I'm sorry, I don't have information on the baking time and temperature of {recipe_name}."


class ActionGrillingTechniques(Action):
    def name(self) -> Text:
        return "action_grilling_techniques"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the value of the 'recipe' entity from the current user message
        recipe_entity = next(tracker.get_latest_entity_values("recipe"), None)

        # Check if the slot 'recipe' has been set in previous turns
        recipe_slot = tracker.get_slot("recipe")

        if recipe_entity in valid_recipes:
            # User directly mentions the dish in the current turn
            response = self.get_grilling_techniques_response(recipe_entity)
            dispatcher.utter_message(response)
            return [SlotSet("recipe", recipe_entity)]
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_grilling_techniques_response(recipe_slot)
            dispatcher.utter_message(response)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"
            dispatcher.utter_message(response)
            return [SlotSet("recipe", None)]

        return []

    @staticmethod
    def get_grilling_techniques_response(recipe_name: Text) -> Text:
        grilling_info = {
            "spaghetti aglio e olio": None,  # Example: This dish doesn't require grilling
            "caprese salad": None,  # Example: This dish doesn't require grilling
            "chicken stir-fry": None,  # Example: This dish doesn't require grilling
            "vegetarian quesadillas": None,  # Example: This dish doesn't require grilling
            "pasta primavera": None,  # Example: This dish doesn't require grilling
            "omelette": None,  # Example: This dish doesn't require grilling
            "tomato basil bruschetta": None,  # Example: This dish doesn't require grilling
            "mushroom risotto": None,  # Example: This dish doesn't require grilling
            "honey mustard baked chicken": None,  # Example: This dish doesn't require grilling
            "tuna salad wrap": {
                "grilling_time": "3 minutes per side",
                "tips": "Preheat the grill, grill each side until the tuna is cooked through.",
            },
        }
        if recipe_name.lower() in grilling_info:
            info = grilling_info[recipe_name.lower()]

            if info is None:
                # This dish doesn't require grilling
                response = f"{recipe_name} doesn't require grilling. It's ready to enjoy!"
            else:
                # Provide grilling information
                response = f"For {recipe_name}, I recommend grilling for approximately {info['grilling_time']}. {info['tips']}"
            return response
        else:
            return f"I'm sorry, I don't have information on grilling techniques for {recipe_name}."


class ActionSauteingAndPanFrying(Action):
    def name(self) -> Text:
        return "action_sauteing_and_pan_frying"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the value of the 'recipe' entity from the current user message
        recipe_entity = next(tracker.get_latest_entity_values("recipe"), None)

        # Check if the slot 'recipe' has been set in previous turns
        recipe_slot = tracker.get_slot("recipe")

        if recipe_entity in valid_recipes:
            # User directly mentions the dish in the current turn
            response = self.get_sauteing_and_pan_frying_response(recipe_entity)
            dispatcher.utter_message(response)
            return [SlotSet("recipe", recipe_entity)]
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_sauteing_and_pan_frying_response(recipe_slot)
            dispatcher.utter_message(response)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"
            dispatcher.utter_message(response)
            return [SlotSet("recipe", None)]

        return []

    @staticmethod
    def get_sauteing_and_pan_frying_response(recipe_name: Text) -> Text:
        cooking_info = {
            "spaghetti aglio e olio": {
                "time": "5 minutes",
                "tips": "Heat olive oil in a pan, sauté garlic until golden, and toss with cooked pasta."
            },
            "caprese salad": None,  # Example: This dish doesn't involve sautéing or pan-frying
            "chicken stir-fry": {
                "time": "10 minutes",
                "tips": "Cut chicken into small pieces, stir-fry in a hot pan with vegetables, and season with sauce."
            },
            "vegetarian quesadillas": {
                "time": "7 minutes",
                "tips": "Fill tortillas with veggies and cheese, pan-fry until crispy, and serve with salsa."
            },
            "pasta primavera": {
                "time": "8 minutes",
                "tips": "Sauté a mix of fresh vegetables in olive oil, toss with cooked pasta, and season to taste."
            },
            "omelette": {
                "time": "5 minutes",
                "tips": "Beat eggs, pour into a hot pan, add desired fillings, and cook until the edges are set."
            },
            "tomato basil bruschetta": None,  # Example: This dish doesn't involve sautéing or pan-frying
            "mushroom risotto": None,  # Example: This dish doesn't involve sautéing or pan-frying
            "honey mustard baked chicken": None,  # Example: This dish doesn't involve sautéing or pan-frying
            "tuna salad wrap": None  # Example: This dish doesn't involve sautéing or pan-frying
        }

        if recipe_name.lower() in cooking_info:
            info = cooking_info[recipe_name.lower()]

            if info is None:
                # This dish doesn't involve sautéing or pan-frying
                response = f"{recipe_name} doesn't involve sautéing or pan-frying. Enjoy preparing it!"
            else:
                # Provide sautéing and pan-frying information
                response = f"For {recipe_name}, I recommend sautéing or pan-frying for approximately {info['time']}. {info['tips']}"
            return response
        else:
            return f"I'm sorry, I don't have information on sautéing or pan-frying for {recipe_name}."


class ActionBoilingAndSimmering(Action):
    def name(self) -> Text:
        return "action_boiling_and_simmering"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the value of the 'recipe' entity from the current user message
        recipe_entity = next(tracker.get_latest_entity_values("recipe"), None)

        # Check if the slot 'recipe' has been set in previous turns
        recipe_slot = tracker.get_slot("recipe")

        if recipe_entity in valid_recipes:
            # User directly mentions the dish in the current turn
            response = self.get_boiling_and_simmering_info(recipe_entity)
            dispatcher.utter_message(response)
            return [SlotSet("recipe", recipe_entity)]
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_boiling_and_simmering_info(recipe_slot)
            dispatcher.utter_message(response)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"
            dispatcher.utter_message(response)
            return [SlotSet("recipe", None)]

        return []

    @staticmethod
    def get_boiling_and_simmering_info(recipe_name: Text) -> Text:
        boiling_and_simmering_info = {
            "spaghetti aglio e olio": {
                "boiling_time": "8-10 minutes",
                "simmering_time": None,
                "tips": "Boil the pasta until al dente. No simmering required for this dish."
            },
            "caprese salad": None,  # Example: This dish doesn't require boiling or simmering
            "chicken stir-fry": None,  # Example: This dish doesn't require boiling or simmering
            "vegetarian quesadillas": None,  # Example: This dish doesn't require boiling or simmering
            "pasta primavera": {
                "boiling_time": "8-10 minutes",
                "simmering_time": "15 minutes",
                "tips": "Boil the pasta until al dente. Simmer the vegetables in the sauce for added flavor."
            },
            "omelette": None,  # Example: This dish doesn't require boiling or simmering
            "tomato basil bruschetta": None,  # Example: This dish doesn't require boiling or simmering
            "mushroom risotto": {
                "boiling_time": "18-20 minutes",
                "simmering_time": "15 minutes",
                "tips": "Boil the rice until tender. Simmer the rice with mushrooms and broth for a creamy texture."
            },
            "honey mustard baked chicken": None,  # Example: This dish doesn't require boiling or simmering
            "tuna salad wrap": None,  # Example: This dish doesn't require boiling or simmering
        }

        if recipe_name.lower() in boiling_and_simmering_info:
            info = boiling_and_simmering_info[recipe_name.lower()]

            if info is None:
                # This dish doesn't require boiling or simmering
                response = f"{recipe_name} doesn't require boiling or simmering. It's ready to enjoy!"
            else:
                # Provide boiling and simmering information
                response = f"For {recipe_name}, I recommend boiling for {info['boiling_time']}."
                if info['simmering_time']:
                    response += f" Simmer for {info['simmering_time']} for optimal flavor. {info['tips']}"
                else:
                    response += f" {info['tips']}"
            return response
        else:
            return f"I'm sorry, I don't have information on the boiling and simmering details for {recipe_name}."


class ActionRoastingTechniques(Action):
    def name(self) -> Text:
        return "action_roasting_techniques"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the value of the 'recipe' entity from the current user message
        recipe_entity = next(tracker.get_latest_entity_values("recipe"), None)

        # Check if the slot 'recipe' has been set in previous turns
        recipe_slot = tracker.get_slot("recipe")

        if recipe_entity in valid_recipes:
            # User directly mentions the dish in the current turn
            response = self.get_roasting_techniques_info(recipe_entity)
            dispatcher.utter_message(response)
            return [SlotSet("recipe", recipe_entity)]
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_roasting_techniques_info(recipe_slot)
            dispatcher.utter_message(response)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"
            dispatcher.utter_message(response)
            return [SlotSet("recipe", None)]

        return []

    @staticmethod
    def get_roasting_techniques_info(recipe_name: Text) -> Text:
        roasting_techniques_info = {
            "spaghetti aglio e olio": None,  # Example: This dish doesn't require roasting
            "caprese salad": None,  # Example: This dish doesn't require roasting
            "chicken stir-fry": None,  # Example: This dish doesn't require roasting
            "vegetarian quesadillas": None,  # Example: This dish doesn't require roasting
            "pasta primavera": None,  # Example: This dish doesn't require roasting
            "omelette": None,  # Example: This dish doesn't require roasting
            "tomato basil bruschetta": None,  # Example: This dish doesn't require roasting
            "mushroom risotto": None,  # Example: This dish doesn't require roasting
            "honey mustard baked chicken": {
                "roasting_time": "40-45 minutes",
                "tips": "Preheat the oven, roast until the chicken is cooked through and the skin is golden."
            },
            "tuna salad wrap": None,  # Example: This dish doesn't require roasting
        }

        if recipe_name.lower() in roasting_techniques_info:
            info = roasting_techniques_info[recipe_name.lower()]

            if info is None:
                # This dish doesn't require roasting
                response = f"{recipe_name} doesn't require roasting. It's ready to enjoy!"
            else:
                # Provide roasting information
                response = f"For {recipe_name}, I recommend roasting for approximately {info['roasting_time']}. {info['tips']}"
            return response
        else:
            return f"I'm sorry, I don't have information on the roasting techniques for {recipe_name}."


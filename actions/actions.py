from typing import Any, Text, Dict, List, Tuple
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

valid_ingredients = [
    "spaghetti",
    "olive oil",
    "garlic",
    "red pepper flakes",
    "parsley",
    "tomatoes",
    "fresh mozzarella",
    "fresh basil leaves",
    "balsamic glaze",
    "mixed vegetables",
    "bell peppers",
    "broccoli",
    "carrots",
    "soy sauce",
    "ginger",
    "flour tortillas",
    "black beans",
    "corn",
    "cheese",
    "salsa",
    "penne pasta",
    "zucchini",
    "cherry tomatoes",
    "parmesan cheese",
    "eggs",
    "milk",
    "fillings",
    "diced ham",
    "vegetables",
    "baguette slices",
    "onion",
    "chicken or vegetable broth",
    "arborio rice",
    "chicken thighs",
    "dijon mustard",
    "honey",
    "garlic powder",
    "salt",
    "pepper",
    "canned tuna",
    "mayonnaise",
    "celery",
    "lettuce",
    "tortillas"
]


class ActionSetDishName(Action):
    def name(self) -> Text:
        return "action_set_dish_name"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the value of the 'recipe' entity from the user message
        recipe_entity = next(tracker.get_latest_entity_values("recipe"), None)

        if recipe_entity in valid_recipes:
            # User directly mentions the dish in the current turn
            dispatcher.utter_message(f"Great choice! I've identified the dish as {recipe_entity}.")
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


class ActionAlternativeIngredients(Action):
    def name(self) -> Text:
        return "action_alternative_ingredients"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the value of the 'ingredient' entity from the current user message
        ingredient_entity = next(tracker.get_latest_entity_values("ingredient"), None)

        if ingredient_entity in valid_ingredients:
            # User directly mentions the ingredient in the current turn
            alternatives = self.get_alternatives(ingredient_entity)
            if alternatives:
                response = f"Here are some alternatives for {ingredient_entity}: {', '.join(alternatives)}"
            else:
                response = f"Sorry, I couldn't find any alternatives for {ingredient_entity}."
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the ingredient. Can you please specify which ingredient you're asking about?"
        dispatcher.utter_message(response)
        return []

    @staticmethod
    def get_alternatives(ingredient: Text) -> List[Text]:
        # Define your dictionary of alternative ingredients here
        alternative_dict = {
            "spaghetti": ["linguine", "fettuccine", "penne"],
            "olive oil": ["avocado oil", "coconut oil", "vegetable oil"],
            "garlic": ["garlic powder", "shallots", "onion"],
            "red pepper flakes": ["cayenne pepper", "crushed red pepper", "paprika"],
            "parsley": ["cilantro", "basil", "chives"],
            "tomatoes": ["cherry tomatoes", "roma tomatoes", "heirloom tomatoes"],
            "fresh mozzarella": ["buffalo mozzarella", "burrata", "ricotta"],
            "fresh basil leaves": ["dried basil", "parsley", "oregano"],
            "balsamic glaze": ["balsamic vinegar", "balsamic reduction", "balsamic syrup"],
            "mixed vegetables": ["broccoli", "bell peppers", "snap peas"],
            "bell peppers": ["red bell peppers", "green bell peppers", "yellow bell peppers"],
            "broccoli": ["cauliflower", "asparagus", "green beans"],
            "carrots": ["celery", "parsnips", "sweet potatoes"],
            "soy sauce": ["tamari", "coconut aminos", "fish sauce"],
            "ginger": ["ground ginger", "ginger paste", "ginger powder"],
            "flour tortillas": ["corn tortillas", "whole wheat tortillas", "lettuce wraps"],
            "black beans": ["pinto beans", "kidney beans", "chickpeas"],
            "corn": ["peas", "edamame", "green beans"],
            "cheese": ["cheddar cheese", "mozzarella cheese", "pepper jack cheese"],
            "salsa": ["pico de gallo", "guacamole", "queso dip"],
            "penne pasta": ["spaghetti", "fettuccine", "farfalle"],
            "zucchini": ["yellow squash", "cucumber", "eggplant"],
            "cherry tomatoes": ["grape tomatoes", "plum tomatoes", "sun-dried tomatoes"],
            "parmesan cheese": ["pecorino romano", "asiago cheese", "gruyere cheese"],
            "eggs": ["egg whites", "tofu", "egg replacer"],
            "milk": ["almond milk", "soy milk", "coconut milk"],
            "fillings": ["cheese", "ham", "spinach"],
            "diced ham": ["cooked bacon", "sausage", "smoked turkey"],
            "vegetables": ["bell peppers", "zucchini", "mushrooms"],
            "baguette slices": ["sourdough slices", "ciabatta slices", "French bread slices"],
            "onion": ["shallots", "leeks", "scallions"],
            "chicken or vegetable broth": ["beef broth", "mushroom broth", "vegetable stock"],
            "arborio rice": ["carnaroli rice", "vialone nano rice", "jasmine rice"],
            "chicken thighs": ["chicken drumsticks", "chicken wings", "tofu"],
            "dijon mustard": ["yellow mustard", "whole grain mustard", "honey mustard"],
            "honey": ["maple syrup", "agave nectar", "brown rice syrup"],
            "garlic powder": ["onion powder", "paprika", "cayenne pepper"],
            "salt": ["sea salt", "kosher salt", "pink Himalayan salt"],
            "pepper": ["black pepper", "white pepper", "cayenne pepper"],
            "canned tuna": ["canned salmon", "canned sardines", "canned mackerel"],
            "mayonnaise": ["Greek yogurt", "avocado", "hummus"],
            "celery": ["bell peppers", "cucumber", "carrots"],
            "lettuce": ["spinach", "arugula", "kale"],
            "tortillas": ["lettuce wraps", "collard green wraps", "rice paper wraps"]
        }

        return alternative_dict.get(ingredient, [])


class ActionRecipeStorageRecommendation(Action):
    def name(self) -> Text:
        return "action_recipe_storage_recommendation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        recipe_entity = next(tracker.get_latest_entity_values("recipe"), None)
        recipe_slot = tracker.get_slot("recipe")

        if recipe_entity in valid_recipes:
            response = self.get_recipe_storage_recommendation(recipe_entity)
            dispatcher.utter_message(response)
            return [SlotSet("recipe", recipe_entity)]
        elif recipe_slot:
            response = self.get_recipe_storage_recommendation(recipe_slot)
            dispatcher.utter_message(response)
        else:
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"
            dispatcher.utter_message(response)
            return [SlotSet("recipe", None)]

        return []

    @staticmethod
    def get_recipe_storage_recommendation(recipe_name: Text) -> Text:
        recipe_storage_info = {
            "spaghetti aglio e olio": "Store leftover Spaghetti Aglio e Olio in an airtight container in the refrigerator for up to 3 days. Reheat before consuming.",
            "caprese salad": "Caprese Salad is best served fresh. Store any leftovers in an airtight container in the refrigerator and consume within 1-2 days.",
            "chicken stir-fry": "Store leftover Chicken Stir-Fry in an airtight container in the refrigerator for up to 3 days. Reheat thoroughly before consuming.",
            "vegetarian quesadillas": "Store leftover Vegetarian Quesadillas in an airtight container in the refrigerator for up to 2 days. Reheat before serving.",
            "pasta primavera": "Store leftover Pasta Primavera in an airtight container in the refrigerator for up to 3 days. Reheat gently before consuming.",
            "omelette": "Store leftover Omelette in an airtight container in the refrigerator for up to 2 days. Reheat before consuming.",
            "tomato basil bruschetta": "Bruschetta is best enjoyed fresh. However, you can store any leftovers in the refrigerator for up to 1 day, but note that the bread may become soggy.",
            "mushroom risotto": "Store leftover Mushroom Risotto in an airtight container in the refrigerator for up to 3 days. Reheat gently on the stovetop or in the microwave before consuming.",
            "honey mustard baked chicken": "Store leftover Honey Mustard Baked Chicken in an airtight container in the refrigerator for up to 3 days. Reheat thoroughly before consuming.",
            "tuna salad wrap": "Store leftover Tuna Salad Wrap in an airtight container in the refrigerator for up to 1 day. Enjoy chilled."
        }
        if recipe_name.lower() in recipe_storage_info:
            return recipe_storage_info[recipe_name.lower()]
        else:
            return f"I'm sorry, I don't have storage recommendations for {recipe_name}."


class ActionRecipeTasteAdjustment(Action):
    def name(self) -> Text:
        return "action_recipe_taste_adjustment"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the value of the 'recipe' entity from the current user message
        recipe_entity = next(tracker.get_latest_entity_values("recipe"), None)

        # Check if the slot 'recipe' has been set in previous turns
        recipe_slot = tracker.get_slot("recipe")

        if recipe_entity in valid_recipes:
            # User directly mentions the dish in the current turn
            response = self.get_recipe_taste_adjustment_response(recipe_entity)
            dispatcher.utter_message(response)
            return [SlotSet("recipe", recipe_entity)]
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_recipe_taste_adjustment_response(recipe_slot)
            dispatcher.utter_message(response)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"
            dispatcher.utter_message(response)
            return [SlotSet("recipe", None)]

        return []

    @staticmethod
    def get_recipe_taste_adjustment_response(recipe_name: Text) -> Text:
        recipe_taste_info = {
            "spaghetti aglio e olio": "To adjust the taste of Spaghetti Aglio e Olio, you can increase the amount of garlic for a stronger flavor or add more red pepper flakes for extra heat. If you prefer it sweeter, you can add a pinch of sugar to balance the acidity of the tomatoes.",
            "caprese salad": "Caprese Salad's flavor is primarily influenced by the freshness of its ingredients. You can enhance its taste by using high-quality tomatoes, fresh basil, and a drizzle of aged balsamic vinegar. If you want to make it less spicy, you can omit the black pepper or reduce the amount of red pepper flakes.",
            "chicken stir-fry": "For Chicken Stir-Fry, you can balance the flavors by adding a touch of sweetness with honey or brown sugar, or reduce the spiciness by using less chili sauce or omitting it altogether. To enhance the flavor, you can add more ginger and garlic, or a splash of lime juice for tanginess.",
            "vegetarian quesadillas": "To adjust the taste of Vegetarian Quesadillas, consider adding more cheese for creaminess or incorporating sliced jalapenos for extra spice. You can also experiment with different types of salsa for added flavor. If you want to make it less salty, use low-sodium beans and cheese.",
            "pasta primavera": "To enhance the flavor of Pasta Primavera, try adding freshly grated Parmesan cheese or a squeeze of lemon juice for brightness. You can also sauté the vegetables with garlic and herbs for extra aroma. If you find it too tangy, reduce the amount of lemon juice or use a sweeter variety of tomatoes.",
            "omelette": "To adjust the taste of the Omelette, you can add more herbs like parsley or chives for freshness, or diced bell peppers and onions for sweetness. If it's too salty, use less salt in the egg mixture or add more vegetables to balance the flavors.",
            "tomato basil bruschetta": "To enhance the flavor of Tomato Basil Bruschetta, use ripe, flavorful tomatoes and fresh basil leaves. You can also drizzle balsamic glaze for sweetness or sprinkle with a pinch of salt and pepper for extra seasoning. If you want to make it less tangy, reduce the amount of balsamic vinegar.",
            "mushroom risotto": "For Mushroom Risotto, you can enhance the flavor by using a variety of mushrooms like porcini or shiitake for depth. Adding a splash of white wine or a sprinkle of nutritional yeast can also boost the umami taste. If it's too rich, add a squeeze of lemon juice for acidity.",
            "honey mustard baked chicken": "To adjust the taste of Honey Mustard Baked Chicken, you can add more honey for sweetness or reduce the amount of mustard for a milder flavor. You can also season with herbs like thyme or rosemary for added aroma. If it's too sweet, balance it with a splash of vinegar.",
            "tuna salad wrap": "For Tuna Salad Wraps, you can enhance the flavor by adding diced apples or grapes for sweetness, or chopped celery and red onions for crunch. You can also season with herbs like dill or parsley for freshness. If it's too bland, add a dollop of Greek yogurt or a squeeze of lemon juice.",
        }
        if recipe_name.lower() in recipe_taste_info:
            return recipe_taste_info[recipe_name.lower()]
        else:
            return f"I'm sorry, I don't have information on adjusting the taste of {recipe_name}."


class ActionRecipeHealthInfo(Action):
    def name(self) -> Text:
        return "action_recipe_health_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the value of the 'recipe' entity from the current user message
        recipe_entity = next(tracker.get_latest_entity_values("recipe"), None)

        # Check if the slot 'recipe' has been set in previous turns
        recipe_slot = tracker.get_slot("recipe")

        if recipe_entity in valid_recipes:
            # User directly mentions the dish in the current turn
            response = self.get_recipe_health_info_response(recipe_entity)
            dispatcher.utter_message(response)
            return [SlotSet("recipe", recipe_entity)]
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_recipe_health_info_response(recipe_slot)
            dispatcher.utter_message(response)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"
            dispatcher.utter_message(response)
            return [SlotSet("recipe", None)]

        return []

    @staticmethod
    def get_recipe_health_info_response(recipe_name: Text) -> Text:
        recipe_health_info = {
            "spaghetti aglio e olio": "Spaghetti Aglio e Olio is a relatively simple dish primarily made of pasta, olive oil, garlic, and parsley. While it's not inherently unhealthy, the nutritional value can vary based on portion size and ingredient ratios. It's a carb-heavy dish due to the pasta, but you can make it healthier by using whole wheat pasta and incorporating more vegetables.",
            "caprese salad": "Caprese Salad is a light and refreshing dish made with tomatoes, fresh mozzarella, basil, and balsamic glaze. It's low in calories and carbohydrates, making it a suitable option for those following a low-carb diet. Additionally, it's rich in vitamins, minerals, and antioxidants, providing various health benefits.",
            "chicken stir-fry": "Chicken Stir-Fry is a nutritious meal consisting of lean protein from chicken breast and an assortment of vegetables. It's low in carbs and can be tailored to fit different dietary preferences, such as low-carb or low-calorie diets. However, the healthiness of the dish depends on the cooking method and added sauces, so opt for minimal oil and use low-sodium soy sauce for a healthier option.",
            "vegetarian quesadillas": "Vegetarian Quesadillas can be a healthy meal option when made with whole wheat tortillas, black beans, vegetables, and a moderate amount of cheese. They provide plant-based protein, fiber, and essential nutrients. To make them even healthier, use a small amount of cheese and load up on vegetables for added vitamins and minerals.",
            "pasta primavera": "Pasta Primavera is a pasta dish loaded with vegetables, making it a nutritious option. However, the healthiness of the dish can vary based on the type of pasta used and the amount of cheese added. Opt for whole wheat pasta for added fiber and choose a light sauce to keep the dish lower in calories.",
            "omelette": "An Omelette can be a healthy meal choice, especially when loaded with vegetables and made with minimal oil. Eggs are a good source of protein and essential nutrients, but be mindful of added ingredients like cheese and high-fat meats.",
            "tomato basil bruschetta": "Tomato Basil Bruschetta is a light and flavorful appetizer made with fresh tomatoes, basil, garlic, and olive oil. It's low in calories and can be a healthy option when served in moderation. Avoid adding excessive amounts of oil or cheese to keep it nutritious.",
            "mushroom risotto": "Mushroom Risotto is a creamy rice dish flavored with mushrooms, onions, and Parmesan cheese. While it's delicious, it can be high in calories and fat due to the cheese and butter traditionally used. Opt for a lighter version by using less cheese and incorporating more vegetables.",
            "honey mustard baked chicken": "Honey Mustard Baked Chicken can be a healthy protein option when prepared with lean chicken breast and a moderate amount of honey mustard sauce. Be cautious of added sugars in store-bought sauces and consider making your own with natural sweeteners.",
            "tuna salad wrap": "Tuna Salad Wraps are a convenient and nutritious meal choice, especially when made with canned tuna, Greek yogurt, and plenty of vegetables. Be mindful of the type of wrap used and opt for whole grain or lettuce wraps for added fiber and nutrients.",
        }
        if recipe_name.lower() in recipe_health_info:
            return recipe_health_info[recipe_name.lower()]
        else:
            return f"I'm sorry, I don't have information on the health benefits of {recipe_name}."


class ActionRecipeOrigin(Action):
    def name(self) -> Text:
        return "action_recipe_origin"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the value of the 'recipe' entity from the current user message
        recipe_entity = next(tracker.get_latest_entity_values("recipe"), None)

        # Check if the slot 'recipe' has been set in previous turns
        recipe_slot = tracker.get_slot("recipe")

        if recipe_entity in valid_recipes:
            # User directly mentions the dish in the current turn
            response = self.get_recipe_origin_response(recipe_entity)
            dispatcher.utter_message(response)
            return [SlotSet("recipe", recipe_entity)]
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_recipe_origin_response(recipe_slot)
            dispatcher.utter_message(response)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"
            dispatcher.utter_message(response)
            return [SlotSet("recipe", None)]

        return []

    @staticmethod
    def get_recipe_origin_response(recipe_name: Text) -> Text:
        recipe_origin_info = {
            "spaghetti aglio e olio": "Spaghetti Aglio e Olio originates from Italy, specifically from the region of Naples. It's a traditional Italian pasta dish known for its simplicity and use of olive oil, garlic, and red pepper flakes.",
            "caprese salad": "Caprese Salad is a classic Italian dish originating from the island of Capri. It's a staple of Italian cuisine, featuring fresh tomatoes, mozzarella cheese, basil, and a drizzle of balsamic glaze or olive oil.",
            "chicken stir-fry": "Chicken Stir-Fry is a popular dish in Asian cuisine, particularly in Chinese cooking. It's characterized by quickly cooking bite-sized pieces of chicken and mixed vegetables in a wok over high heat.",
            "vegetarian quesadillas": "Quesadillas are a traditional Mexican dish, but the vegetarian version has become popular worldwide. While the exact origin of vegetarian quesadillas is unclear, they are inspired by Mexican cuisine and often feature ingredients like beans, cheese, and vegetables.",
            "pasta primavera": "Pasta Primavera is an Italian-American dish that originated in the United States. It was created in the 1970s in New York City and is characterized by pasta tossed with fresh vegetables and a light sauce.",
            "omelette": "Omelette is a versatile dish enjoyed worldwide, but it has roots in French cuisine. The French omelette is known for its creamy texture and can be filled with various ingredients such as cheese, vegetables, or ham.",
            "tomato basil bruschetta": "Bruschetta is an Italian appetizer that dates back to ancient Rome. Tomato Basil Bruschetta, in particular, is a modern variation featuring diced tomatoes, fresh basil, garlic, and olive oil served on toasted bread slices.",
            "mushroom risotto": "Risotto is a traditional Italian rice dish, and Mushroom Risotto is a popular variation. While risotto originates from Northern Italy, Mushroom Risotto has been adapted and enjoyed in various regions around the world.",
            "honey mustard baked chicken": "Honey Mustard Baked Chicken is a classic dish enjoyed in many parts of the world. While its exact origin is unclear, it's often associated with American cuisine and is a favorite for its sweet and tangy flavor.",
            "tuna salad wrap": "Tuna Salad Wraps are a modern dish inspired by various culinary influences. While tuna salad itself is not tied to a specific region, wraps are popular in many cultures, and this variation offers a convenient and healthy meal option.",
        }
        if recipe_name.lower() in recipe_origin_info:
            return recipe_origin_info[recipe_name.lower()]
        else:
            return f"I'm sorry, I don't have information on the origin of {recipe_name}."


class ActionGetRecipeNutrition(Action):
    def name(self) -> Text:
        return "action_get_recipe_nutrition"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the value of the 'recipe' entity from the current user message
        recipe_entity = next(tracker.get_latest_entity_values("recipe"), None)

        # Check if the slot 'recipe' has been set in previous turns
        recipe_slot = tracker.get_slot("recipe")

        if recipe_entity in valid_recipes:
            # User directly mentions the dish in the current turn
            response = self.get_recipe_nutrition_response(recipe_entity)
            dispatcher.utter_message(response)
            return [SlotSet("recipe", recipe_entity)]
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_recipe_nutrition_response(recipe_slot)
            dispatcher.utter_message(response)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"
            dispatcher.utter_message(response)
            return [SlotSet("recipe", None)]

        return []

    @staticmethod
    def get_recipe_nutrition_response(recipe_name: Text) -> Text:
        recipe_nutrition_info = {
            "spaghetti aglio e olio": "Spaghetti Aglio e Olio is a relatively simple dish primarily made of pasta, olive oil, garlic, and parsley. While it's not inherently unhealthy, the nutritional value can vary based on portion size and ingredient ratios. It's a carb-heavy dish due to the pasta, but you can make it healthier by using whole wheat pasta and incorporating more vegetables. Nutrition information per serving: Carbohydrates: 45g, Proteins: 8g, Fats: 15g, Vitamins: Vitamin C, Vitamin K, Minerals: Iron, Manganese",
            "caprese salad": "Caprese Salad is a light and refreshing dish made with tomatoes, fresh mozzarella, basil, and balsamic glaze. It's low in calories and carbohydrates, making it a suitable option for those following a low-carb diet. Additionally, it's rich in vitamins, minerals, and antioxidants, providing various health benefits. Nutrition information per serving: Carbohydrates: 5g, Proteins: 10g, Fats: 10g, Vitamins: Vitamin A, Vitamin C, Minerals: Calcium, Potassium",
            "chicken stir-fry": "Chicken Stir-Fry is a nutritious meal consisting of lean protein from chicken breast and an assortment of vegetables. It's low in carbs and can be tailored to fit different dietary preferences, such as low-carb or low-calorie diets. However, the healthiness of the dish depends on the cooking method and added sauces, so opt for minimal oil and use low-sodium soy sauce for a healthier option. Nutrition information per serving: Carbohydrates: 15g, Proteins: 20g, Fats: 10g, Vitamins: Vitamin B6, Vitamin C, Minerals: Potassium, Magnesium",
            "vegetarian quesadillas": "Vegetarian Quesadillas can be a healthy meal option when made with whole wheat tortillas, black beans, vegetables, and a moderate amount of cheese. They provide plant-based protein, fiber, and essential nutrients. To make them even healthier, use a small amount of cheese and load up on vegetables for added vitamins and minerals. Nutrition information per serving: Carbohydrates: 25g, Proteins: 12g, Fats: 15g, Vitamins: Vitamin A, Vitamin K, Minerals: Iron, Zinc",
            "pasta primavera": "Pasta Primavera is a pasta dish loaded with vegetables, making it a nutritious option. However, the healthiness of the dish can vary based on the type of pasta used and the amount of cheese added. Opt for whole wheat pasta for added fiber and choose a light sauce to keep the dish lower in calories. Nutrition information per serving: Carbohydrates: 40g, Proteins: 10g, Fats: 10g, Vitamins: Vitamin A, Vitamin C, Minerals: Potassium, Magnesium",
            "omelette": "An Omelette can be a healthy meal choice, especially when loaded with vegetables and made with minimal oil. Eggs are a good source of protein and essential nutrients, but be mindful of added ingredients like cheese and high-fat meats. Nutrition information per serving: Carbohydrates: 2g, Proteins: 15g, Fats: 15g, Vitamins: Vitamin D, Vitamin B12, Minerals: Iron, Phosphorus",
            "tomato basil bruschetta": "Tomato Basil Bruschetta is a light and flavorful appetizer made with fresh tomatoes, basil, garlic, and olive oil. It's low in calories and can be a healthy option when served in moderation. Avoid adding excessive amounts of oil or cheese to keep it nutritious. Nutrition information per serving: Carbohydrates: 10g, Proteins: 2g, Fats: 5g, Vitamins: Vitamin C, Vitamin K, Minerals: Calcium, Manganese",
            "mushroom risotto": "Mushroom Risotto is a creamy rice dish flavored with mushrooms, onions, and Parmesan cheese. While it's delicious, it can be high in calories and fat due to the cheese and butter traditionally used. Opt for a lighter version by using less cheese and incorporating more vegetables. Nutrition information per serving: Carbohydrates: 50g, Proteins: 8g, Fats: 20g, Vitamins: Vitamin D, Vitamin B6, Minerals: Iron, Selenium",
            "honey mustard baked chicken": "Honey Mustard Baked Chicken can be a healthy protein option when prepared with lean chicken breast and a moderate amount of honey mustard sauce. Be cautious of added sugars in store-bought sauces and consider making your own with natural sweeteners. Nutrition information per serving: Carbohydrates: 10g, Proteins: 25g, Fats: 15g, Vitamins: Vitamin B3, Vitamin B6, Minerals: Zinc, Potassium",
            "tuna salad wrap": "Tuna Salad Wraps are a convenient and nutritious meal choice, especially when made with canned tuna, Greek yogurt, and plenty of vegetables. Be mindful of the type of wrap used and opt for whole grain or lettuce wraps for added fiber and nutrients. Nutrition information per serving: Carbohydrates: 20g, Proteins: 20g, Fats: 10g, Vitamins: Vitamin D, Vitamin B12, Minerals: Selenium, Phosphorus",
        }
        if recipe_name.lower() in recipe_nutrition_info:
            return recipe_nutrition_info[recipe_name.lower()]
        else:
            return f"I'm sorry, I don't have information on the nutritional value of {recipe_name}."


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


class ActionMarinatingDuration(Action):
    def name(self) -> Text:
        return "action_marinating_duration"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the value of the 'recipe' entity from the current user message
        recipe_entity = next(tracker.get_latest_entity_values("recipe"), None)

        # Check if the slot 'recipe' has been set in previous turns
        recipe_slot = tracker.get_slot("recipe")

        if recipe_entity in valid_recipes:
            # User directly mentions the dish in the current turn
            response = self.get_marinating_duration_info(recipe_entity)
            dispatcher.utter_message(response)
            return [SlotSet("recipe", recipe_entity)]
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_marinating_duration_info(recipe_slot)
            dispatcher.utter_message(response)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"
            dispatcher.utter_message(response)
            return [SlotSet("recipe", None)]

        return []

    @staticmethod
    def get_marinating_duration_info(recipe_name: Text) -> Text:
        marinating_duration_info = {
            "spaghetti aglio e olio": None,  # Example: This dish doesn't require marinating
            "caprese salad": None,  # Example: This dish doesn't require marinating
            "chicken stir-fry": {
                "marinating_time": "30 minutes to 1 hour",
                "tips": "Marinate the chicken for at least 30 minutes to enhance flavor. For a deeper flavor, marinate for up to 1 hour."
            },
            "vegetarian quesadillas": None,  # Example: This dish doesn't require marinating
            "pasta primavera": None,  # Example: This dish doesn't require marinating
            "omelette": None,  # Example: This dish doesn't require marinating
            "tomato basil bruschetta": None,  # Example: This dish doesn't require marinating
            "mushroom risotto": None,  # Example: This dish doesn't require marinating
            "honey mustard baked chicken": {
                "marinating_time": "2 to 24 hours",
                "tips": "Marinate the chicken for at least 2 hours, but for the best flavor, marinate it overnight for up to 24 hours."
            },
            "tuna salad wrap": None,  # Example: This dish doesn't require marinating
        }

        if recipe_name.lower() in marinating_duration_info:
            info = marinating_duration_info[recipe_name.lower()]

            if info is None:
                # This dish doesn't require marinating
                response = f"{recipe_name} doesn't require marinating. You can proceed with the recipe!"
            else:
                # Provide marinating information
                response = f"For {recipe_name}, I recommend marinating for {info['marinating_time']}. {info['tips']}"
            return response
        else:
            return f"I'm sorry, I don't have information on the marinating duration for {recipe_name}."


class ActionChoppingCuttingTechniques(Action):
    def name(self) -> Text:
        return "action_chopping_cutting_techniques"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the value of the 'recipe' entity from the current user message
        recipe_entity = next(tracker.get_latest_entity_values("recipe"), None)

        # Check if the slot 'recipe' has been set in previous turns
        recipe_slot = tracker.get_slot("recipe")

        if recipe_entity in valid_recipes:
            # User directly mentions the dish in the current turn
            response = self.get_chopping_cutting_techniques_info(recipe_entity)
            dispatcher.utter_message(response)
            return [SlotSet("recipe", recipe_entity)]
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_chopping_cutting_techniques_info(recipe_slot)
            dispatcher.utter_message(response)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"
            dispatcher.utter_message(response)
            return [SlotSet("recipe", None)]

        return []

    @staticmethod
    def get_chopping_cutting_techniques_info(recipe_name: Text) -> Text:
        chopping_cutting_techniques_info = {
            "spaghetti aglio e olio": None,  # Example: This dish doesn't involve chopping or cutting
            "caprese salad": {
                "technique": "slicing",
                "tips": "Use a sharp knife to slice the tomatoes and mozzarella cheese evenly."
            },
            "chicken stir-fry": {
                "technique": "dicing",
                "tips": "Dice the chicken into uniform pieces to ensure even cooking."
            },
            "vegetarian quesadillas": {
                "technique": "chopping",
                "tips": "Chop the vegetables finely for a better texture in the quesadillas."
            },
            "pasta primavera": {
                "technique": "slicing",
                "tips": "Slice the vegetables thinly for a quick cooking time."
            },
            "omelette": {
                "technique": "beating",
                "tips": "Beat the eggs until they are well mixed before cooking the omelette."
            },
            "tomato basil bruschetta": {
                "technique": "slicing",
                "tips": "Slice the tomatoes and basil leaves thinly for easy topping on the bread."
            },
            "mushroom risotto": {
                "technique": "slicing",
                "tips": "Slice the mushrooms evenly to distribute their flavor throughout the risotto."
            },
            "honey mustard baked chicken": {
                "technique": "marinating",
                "tips": "Marinate the chicken pieces before baking for added flavor."
            },
            "tuna salad wrap": {
                "technique": "flaking",
                "tips": "Flake the canned tuna with a fork before mixing it with other ingredients."
            },
        }

        if recipe_name.lower() in chopping_cutting_techniques_info:
            info = chopping_cutting_techniques_info[recipe_name.lower()]

            if info is None:
                # This dish doesn't involve chopping or cutting
                response = f"{recipe_name} doesn't involve chopping or cutting. You can proceed with the recipe!"
            else:
                # Provide chopping/cutting information
                response = f"For {recipe_name}, the recommended cutting technique is {info['technique']}. {info['tips']}"
            return response
        else:
            return f"I'm sorry, I don't have information on the chopping and cutting techniques for {recipe_name}."


class ActionSeasoningAndSpices(Action):
    def name(self) -> Text:
        return "action_seasoning_and_spices"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the value of the 'recipe' entity from the current user message
        recipe_entity = next(tracker.get_latest_entity_values("recipe"), None)

        # Check if the slot 'recipe' has been set in previous turns
        recipe_slot = tracker.get_slot("recipe")

        if recipe_entity in valid_recipes:
            # User directly mentions the dish in the current turn
            response = self.get_seasoning_and_spices_info(recipe_entity)
            dispatcher.utter_message(response)
            return [SlotSet("recipe", recipe_entity)]
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_seasoning_and_spices_info(recipe_slot)
            dispatcher.utter_message(response)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"
            dispatcher.utter_message(response)
            return [SlotSet("recipe", None)]

        return []

    @staticmethod
    def get_seasoning_and_spices_info(recipe_name: Text) -> Text:
        seasoning_and_spices_info = {
            "spaghetti aglio e olio": {
                "spices": ["crushed red pepper flakes", "salt"],
                "salt_and_pepper_amount": "to taste",
                "tips": "Be cautious with salt as the dish might already have salt from the pasta water."
            },
            "caprese salad": {
                "spices": ["salt", "black pepper"],
                "salt_and_pepper_amount": "to taste",
                "tips": "Use freshly ground black pepper for enhanced flavor."
            },
            "chicken stir-fry": {
                "spices": ["soy sauce", "garlic powder", "ginger powder"],
                "salt_and_pepper_amount": "to taste",
                "tips": "Adjust soy sauce according to your preference for saltiness."
            },
            "vegetarian quesadillas": {
                "spices": ["cumin", "chili powder", "paprika"],
                "salt_and_pepper_amount": "to taste",
                "tips": "Add spices gradually and taste as you go to achieve the desired flavor."
            },
            "pasta primavera": {
                "spices": ["Italian seasoning", "garlic powder"],
                "salt_and_pepper_amount": "to taste",
                "tips": "Italian seasoning blend typically contains a mix of herbs like basil, oregano, and thyme."
            },
            "omelette": {
                "spices": ["salt", "black pepper"],
                "salt_and_pepper_amount": "to taste",
                "tips": "Sprinkle salt and pepper evenly over the beaten eggs before cooking."
            },
            "tomato basil bruschetta": {
                "spices": ["salt", "black pepper"],
                "salt_and_pepper_amount": "to taste",
                "tips": "Freshly chopped basil leaves add a burst of flavor to the bruschetta."
            },
            "mushroom risotto": {
                "spices": ["salt", "black pepper"],
                "salt_and_pepper_amount": "to taste",
                "tips": "A sprinkle of freshly grated Parmesan cheese on top adds a savory touch."
            },
            "honey mustard baked chicken": {
                "spices": ["paprika", "garlic powder", "onion powder"],
                "salt_and_pepper_amount": "to taste",
                "tips": "Coat the chicken evenly with the honey mustard mixture for maximum flavor."
            },
            "tuna salad wrap": {
                "spices": ["dill", "lemon pepper"],
                "salt_and_pepper_amount": "to taste",
                "tips": "Lemon pepper seasoning adds a zesty twist to the tuna salad."
            },
        }

        if recipe_name.lower() in seasoning_and_spices_info:
            info = seasoning_and_spices_info[recipe_name.lower()]

            spices_list = ", ".join(info["spices"])
            salt_and_pepper_amount = info["salt_and_pepper_amount"]
            tips = info["tips"]

            response = f"For {recipe_name}, you can use {spices_list} for seasoning. Salt and pepper should be added {salt_and_pepper_amount}. {tips}"
            return response
        else:
            return f"I'm sorry, I don't have information on the seasoning and spices for {recipe_name}."


class ActionGarnishingAndPresentation(Action):
    def name(self) -> Text:
        return "action_garnishing_and_presentation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the value of the 'recipe' entity from the current user message
        recipe_entity = next(tracker.get_latest_entity_values("recipe"), None)

        # Check if the slot 'recipe' has been set in previous turns
        recipe_slot = tracker.get_slot("recipe")

        if recipe_entity in valid_recipes:
            # User directly mentions the dish in the current turn
            response = self.get_garnishing_and_presentation_info(recipe_entity)
            dispatcher.utter_message(response)
            return [SlotSet("recipe", recipe_entity)]
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_garnishing_and_presentation_info(recipe_slot)
            dispatcher.utter_message(response)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"
            dispatcher.utter_message(response)
            return [SlotSet("recipe", None)]

        return []

    @staticmethod
    def get_garnishing_and_presentation_info(recipe_name: Text) -> Text:
        garnishing_and_presentation_info = {
            "spaghetti aglio e olio": {
                "garnish": "Freshly chopped parsley",
                "presentation": "Serve the spaghetti in individual bowls, garnish each portion with chopped parsley, and drizzle with extra olive oil."
            },
            "caprese salad": {
                "garnish": "Fresh basil leaves",
                "presentation": "Arrange alternating slices of tomatoes and mozzarella cheese on a serving platter, garnish with basil leaves, and drizzle with balsamic glaze."
            },
            "chicken stir-fry": {
                "garnish": "Sesame seeds",
                "presentation": "Serve the chicken stir-fry on a large plate or bowl, sprinkle with sesame seeds for garnish, and serve with steamed rice or noodles on the side."
            },
            "vegetarian quesadillas": {
                "garnish": "Chopped cilantro",
                "presentation": "Cut the quesadillas into wedges, arrange on a serving platter, garnish with chopped cilantro, and serve with salsa and sour cream on the side."
            },
            "pasta primavera": {
                "garnish": "Grated Parmesan cheese",
                "presentation": "Serve the pasta primavera in individual bowls, sprinkle with grated Parmesan cheese for garnish, and garnish with a sprig of fresh basil."
            },
            "omelette": {
                "garnish": "Chopped chives",
                "presentation": "Slide the omelette onto a plate, sprinkle with chopped chives for garnish, and serve hot with toast or a side salad."
            },
            "tomato basil bruschetta": {
                "garnish": "Balsamic glaze",
                "presentation": "Arrange the tomato basil bruschetta on a platter, drizzle with balsamic glaze for garnish, and serve immediately as an appetizer."
            },
            "mushroom risotto": {
                "garnish": "Freshly chopped parsley",
                "presentation": "Spoon the mushroom risotto onto plates, sprinkle with freshly chopped parsley for garnish, and serve hot with a side of garlic bread."
            },
            "honey mustard baked chicken": {
                "garnish": "Fresh rosemary sprigs",
                "presentation": "Arrange the honey mustard baked chicken on a serving platter, garnish with fresh rosemary sprigs, and serve with roasted vegetables on the side."
            },
            "tuna salad wrap": {
                "garnish": "Lemon wedges",
                "presentation": "Wrap the tuna salad in tortillas, arrange on a platter, garnish with lemon wedges, and serve with potato chips or a side salad."
            },
        }

        if recipe_name.lower() in garnishing_and_presentation_info:
            info = garnishing_and_presentation_info[recipe_name.lower()]

            garnish = info["garnish"]
            presentation = info["presentation"]

            response = f"For {recipe_name}, the best garnish is {garnish}. To plate for presentation, {presentation}."
            return response
        else:
            return f"I'm sorry, I don't have information on garnishing and presentation for {recipe_name}."


class ActionRestingAndServing(Action):
    def name(self) -> Text:
        return "action_resting_and_serving"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the value of the 'recipe' entity from the current user message
        recipe_entity = next(tracker.get_latest_entity_values("recipe"), None)

        # Check if the slot 'recipe' has been set in previous turns
        recipe_slot = tracker.get_slot("recipe")

        if recipe_entity in valid_recipes:
            # User directly mentions the dish in the current turn
            response = self.get_resting_and_serving_info(recipe_entity)
            dispatcher.utter_message(response)
            return [SlotSet("recipe", recipe_entity)]
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_resting_and_serving_info(recipe_slot)
            dispatcher.utter_message(response)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"
            dispatcher.utter_message(response)
            return [SlotSet("recipe", None)]

        return []

    @staticmethod
    def get_resting_and_serving_info(recipe_name: Text) -> Text:
        resting_and_serving_info = {
            "spaghetti aglio e olio": {
                "resting_time": None,  # Example: This dish doesn't require resting
                "serving_time": "Immediately",  # Example: Best served immediately after cooking
                "guidance": "Serve the spaghetti aglio e olio immediately after tossing with the sauce to enjoy it at its best."
            },
            "caprese salad": {
                "resting_time": None,  # Example: This dish doesn't require resting
                "serving_time": "Immediately",  # Example: Best served immediately after assembling
                "guidance": "Serve the caprese salad immediately after assembling to prevent the tomatoes from becoming too soggy."
            },
            "chicken stir-fry": {
                "resting_time": None,  # Example: This dish doesn't require resting
                "serving_time": "Immediately",  # Example: Best served immediately after cooking
                "guidance": "Serve the chicken stir-fry immediately after cooking while it's still hot and flavorful."
            },
            "vegetarian quesadillas": {
                "resting_time": None,  # Example: This dish doesn't require resting
                "serving_time": "Immediately",  # Example: Best served immediately after cooking
                "guidance": "Serve the vegetarian quesadillas immediately after cooking to enjoy them while they're hot and crispy."
            },
            "pasta primavera": {
                "resting_time": None,  # Example: This dish doesn't require resting
                "serving_time": "Immediately",  # Example: Best served immediately after tossing with the sauce
                "guidance": "Serve the pasta primavera immediately after tossing with the sauce to prevent it from becoming dry."
            },
            "omelette": {
                "resting_time": None,  # Example: This dish doesn't require resting
                "serving_time": "Immediately",  # Example: Best served immediately after cooking
                "guidance": "Serve the omelette immediately after cooking while it's still fluffy and hot."
            },
            "tomato basil bruschetta": {
                "resting_time": None,  # Example: This dish doesn't require resting
                "serving_time": "Immediately",  # Example: Best served immediately after assembling
                "guidance": "Serve the tomato basil bruschetta immediately after assembling to enjoy the crispiness of the bread."
            },
            "mushroom risotto": {
                "resting_time": "5 minutes",  # Example: Let the risotto rest for 5 minutes before serving
                "serving_time": "Immediately",  # Example: Best served immediately after cooking
                "guidance": "Let the mushroom risotto rest for 5 minutes before serving to allow the flavors to meld together."
            },
            "honey mustard baked chicken": {
                "resting_time": "5 minutes",  # Example: Let the chicken rest for 5 minutes before serving
                "serving_time": "Immediately",  # Example: Best served immediately after cooking
                "guidance": "Let the honey mustard baked chicken rest for 5 minutes before serving to retain its juices."
            },
            "tuna salad wrap": {
                "resting_time": None,  # Example: This dish doesn't require resting
                "serving_time": "Immediately",  # Example: Best served immediately after assembling
                "guidance": "Serve the tuna salad wrap immediately after assembling to prevent the tortillas from becoming soggy."
            },
        }

        if recipe_name.lower() in resting_and_serving_info:
            info = resting_and_serving_info[recipe_name.lower()]

            resting_time = info["resting_time"]
            serving_time = info["serving_time"]
            guidance = info["guidance"]

            if resting_time:
                response = f"For {recipe_name}, it's recommended to let it rest for {resting_time} before serving. "
            else:
                response = ""

            response += f"Best time to serve {recipe_name} is {serving_time}. {guidance}"
            return response
        else:
            return f"I'm sorry, I don't have information on resting and serving for {recipe_name}."


class ActionSauceAndDressing(Action):
    def name(self) -> Text:
        return "action_sauce_and_dressing"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the value of the 'recipe' entity from the current user message
        recipe_entity = next(tracker.get_latest_entity_values("recipe"), None)

        # Check if the slot 'recipe' has been set in previous turns
        recipe_slot = tracker.get_slot("recipe")

        if recipe_entity in valid_recipes:
            # User directly mentions the dish in the current turn
            response = self.get_sauce_and_dressing_info(recipe_entity)
            dispatcher.utter_message(response)
            return [SlotSet("recipe", recipe_entity)]
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            response = self.get_sauce_and_dressing_info(recipe_slot)
            dispatcher.utter_message(response)
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"
            dispatcher.utter_message(response)
            return [SlotSet("recipe", None)]

        return []

    @staticmethod
    def get_sauce_and_dressing_info(recipe_name: Text) -> Text:
        sauce_and_dressing_info = {
            "spaghetti aglio e olio": {
                "sauce": "No sauce needed",  # Example: This dish doesn't require sauce
                "dressing": None  # Example: This dish doesn't require dressing
            },
            "caprese salad": {
                "sauce": "Balsamic glaze",  # Example: Balsamic glaze pairs well with caprese salad
                "dressing": "Extra virgin olive oil, balsamic vinegar, salt, and pepper"  # Example: Classic dressing for caprese salad
            },
            "chicken stir-fry": {
                "sauce": "Teriyaki sauce",  # Example: Teriyaki sauce pairs well with chicken stir-fry
                "dressing": None  # Example: This dish doesn't require dressing
            },
            "vegetarian quesadillas": {
                "sauce": "Salsa",  # Example: Salsa pairs well with vegetarian quesadillas
                "dressing": None  # Example: This dish doesn't require dressing
            },
            "pasta primavera": {
                "sauce": "Alfredo sauce",  # Example: Alfredo sauce complements pasta primavera
                "dressing": None  # Example: This dish doesn't require dressing
            },
            "omelette": {
                "sauce": "Hot sauce",  # Example: Hot sauce adds a kick to omelette
                "dressing": None  # Example: This dish doesn't require dressing
            },
            "tomato basil bruschetta": {
                "sauce": None,  # Example: This dish doesn't require sauce
                "dressing": "Extra virgin olive oil, balsamic vinegar, salt, and pepper"  # Example: Classic dressing for bruschetta
            },
            "mushroom risotto": {
                "sauce": None,  # Example: This dish doesn't require sauce
                "dressing": None  # Example: This dish doesn't require dressing
            },
            "honey mustard baked chicken": {
                "sauce": "Honey mustard sauce",  # Example: Honey mustard sauce complements baked chicken
                "dressing": None  # Example: This dish doesn't require dressing
            },
            "tuna salad wrap": {
                "sauce": "Mayonnaise",  # Example: Mayonnaise adds creaminess to tuna salad wrap
                "dressing": None  # Example: This dish doesn't require dressing
            },
        }

        if recipe_name.lower() in sauce_and_dressing_info:
            info = sauce_and_dressing_info[recipe_name.lower()]

            sauce = info["sauce"]
            dressing = info["dressing"]

            response = f"For {recipe_name}:"
            if sauce:
                response += f"\n- Sauce: {sauce}"
            else:
                response += f"\n- Sauce: {recipe_name} doesn't require a sauce."
            if dressing:
                response += f"\n- Dressing: {dressing}"
            else:
                response += f"\n- Dressing: {recipe_name} doesn't require a dressing."

            return response
        else:
            return f"I'm sorry, I don't have information on sauce and dressing for {recipe_name}."


class ActionRetrieveRecipeInfo(Action):
    def name(self) -> Text:
        return "action_retrieve_recipe_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the value of the 'recipe' entity from the current user message
        recipe_entity = next(tracker.get_latest_entity_values("recipe"), None)

        # Check if the slot 'recipe' has been set in previous turns
        recipe_slot = tracker.get_slot("recipe")

        if recipe_entity in valid_recipes:
            # User directly mentions the dish in the current turn
            ingredients, instructions, response = self.retrieve_ingredients_and_instructions(recipe_entity)
            dispatcher.utter_message(response)
            if ingredients:
                dispatcher.utter_message(f"The ingredients for {recipe_entity} are: {', '.join(ingredients)}")
            if instructions:
                dispatcher.utter_message(f"Here are the instructions for {recipe_entity}:\n" + "\n".join(instructions))
            return [SlotSet("recipe", recipe_entity)]
        elif recipe_slot:
            # User has mentioned the dish in previous turns
            ingredients, instructions, response = self.retrieve_ingredients_and_instructions(recipe_slot)
            dispatcher.utter_message(response)
            if ingredients:
                dispatcher.utter_message(f"The ingredients for {recipe_slot} are: {', '.join(ingredients)}")
            if instructions:
                dispatcher.utter_message(f"Here are the instructions for {recipe_slot}:\n" + "\n".join(instructions))
        else:
            # Handle the case where neither the entity nor the slot is available
            response = "I didn't catch the name of the recipe. Can you please specify which recipe you're asking about?"
            dispatcher.utter_message(response)
            return [SlotSet("recipe", None)]

        return []

    @staticmethod
    def retrieve_ingredients_and_instructions(recipe_name: Text) -> Tuple[List[Text], List[Text], Text]:
        recipe_info = {
            "Spaghetti Aglio e Olio": {
                "ingredients": ["spaghetti", "olive oil", "garlic", "red pepper flakes", "parsley"],
                "instructions": ["1. Cook spaghetti according to package instructions.",
                                 "2. Heat olive oil in a large skillet over medium heat.",
                                 "3. Add minced garlic and red pepper flakes, cook until garlic is golden but not browned.",
                                 "4. Toss cooked spaghetti with the garlic oil mixture.",
                                 "5. Season with salt, pepper, and chopped parsley before serving."]
            },
            "Caprese Salad": {
                "ingredients": ["tomatoes", "fresh mozzarella", "fresh basil", "balsamic glaze", "olive oil"],
                "instructions": ["1. Slice tomatoes and fresh mozzarella into rounds.",
                                 "2. Arrange tomato and mozzarella slices on a plate, alternating them.",
                                 "3. Drizzle with balsamic glaze and olive oil before serving."]
            },
            "Chicken Stir-Fry": {
                "ingredients": ["chicken breast", "mixed vegetables (bell peppers, broccoli, carrots)", "soy sauce",
                                "ginger", "garlic"],
                "instructions": ["1. Stir-fry chicken in a pan until cooked.",
                                 "2. Add minced ginger and garlic.",
                                 "3. Add mixed vegetables and cook until tender.",
                                 "4. Pour soy sauce over the mixture and toss."]
            },
            "Vegetarian Quesadillas": {
                "ingredients": ["flour tortillas", "black beans", "corn", "cheese (cheddar or Mexican blend)", "salsa"],
                "instructions": ["1. Spread black beans and corn on half of a tortilla.",
                                 "2. Sprinkle cheese over the beans and corn.",
                                 "3. Fold the tortilla in half and cook on a griddle until cheese is melted.",
                                 "4. Serve with salsa."]
            },
            "Pasta Primavera": {
                "ingredients": ["penne pasta", "assorted vegetables (zucchini, cherry tomatoes, bell peppers)",
                                "olive oil", "Parmesan cheese"],
                "instructions": ["1. Cook penne pasta according to package instructions.",
                                 "2. Sauté vegetables in olive oil until tender.",
                                 "3. Toss cooked pasta with the sautéed vegetables.",
                                 "4. Sprinkle with Parmesan cheese before serving."]
            },
            "Omelette": {
                "ingredients": ["eggs", "milk", "salt and pepper", "fillings (cheese, diced ham, vegetables)"],
                "instructions": ["1. Whisk eggs with milk, salt, and pepper.",
                                 "2. Pour the mixture into a heated, greased pan.",
                                 "3. Add fillings on one side and fold the omelette when the edges set."]
            },
            "Tomato Basil Bruschetta": {
                "ingredients": ["baguette slices", "tomatoes (diced)", "fresh basil (chopped)", "garlic (minced)",
                                "olive oil"],
                "instructions": ["1. Toast baguette slices.",
                                 "2. Mix diced tomatoes, basil, minced garlic, and olive oil.",
                                 "3. Spoon the tomato mixture onto the toasted bread."]
            },
            "Mushroom Risotto": {
                "ingredients": ["Arborio rice", "mushrooms (sliced)", "onion (chopped)", "chicken or vegetable broth",
                                "Parmesan cheese"],
                "instructions": ["1. Sauté onions and mushrooms until tender.",
                                 "2. Add Arborio rice and cook for a minute.",
                                 "3. Gradually add broth, stirring until absorbed.",
                                 "4. Stir in Parmesan cheese before serving."]
            },
            "Honey Mustard Baked Chicken": {
                "ingredients": ["chicken thighs", "Dijon mustard", "honey", "garlic powder", "salt and pepper"],
                "instructions": ["1. Mix Dijon mustard, honey, garlic powder, salt, and pepper.",
                                 "2. Coat chicken thighs in the mixture.",
                                 "3. Bake in the oven until fully cooked."]
            },
            "Tuna Salad Wrap": {
                "ingredients": ["canned tuna", "mayonnaise", "celery (chopped)", "lettuce", "tortillas"],
                "instructions": ["1. Mix canned tuna with mayonnaise and chopped celery.",
                                 "2. Lay out a tortilla, add tuna mixture and lettuce.",
                                 "3. Roll the tortilla into a wrap."]
            }
        }

        # Retrieve the ingredients and instructions for the specified recipe
        recipe_data = recipe_info.get(recipe_name, None)

        if recipe_data:
            ingredients = recipe_data["ingredients"]
            instructions = recipe_data["instructions"]
            response = f"Found the recipe information for {recipe_name}."
        else:
            ingredients = []
            instructions = []
            response = f"I'm sorry, I don't have the recipe information for {recipe_name}."

        return ingredients, instructions, response

import pandas as pd #For data manipulation
import spacy #For natural language processing
import string #For string manipulation
import gensim #For topic modeling
import operator #For sorting
import re #For text cleaning

# Loading spaCy English model
spacy_nlp = spacy.load('en_core_web_sm')
#Tokenization and all that- essential for various natural language processing tasks
# like text cleaning, feature extraction, and information retrieval.

# Loading dataset
df_recipes = pd.read_csv('C:/Users/Acer/Desktop/New folder/New_recipe_similar_words.csv')

# Function for data cleaning and processing
def spacy_tokenizer(sentence):
    sentence = re.sub('\'', '', sentence)
    sentence = re.sub('\w*\d\w*', '', sentence)
    sentence = re.sub(' +', ' ', sentence)
    sentence = re.sub(r'\n: \'\'.*', '', sentence)
    sentence = re.sub(r'\n!.*', '', sentence)              #Text cleaning using regular expressions
    sentence = re.sub(r'^:\'\'.*', '', sentence)
    sentence = re.sub(r'\n', ' ', sentence)
    sentence = re.sub(r'[^\w\s]', ' ', sentence)

    tokens = spacy_nlp(sentence)
    tokens = [word.lemma_.strip() if word.lemma_ != "-PRON-" else word for word in tokens]
    tokens = [word for word in tokens if           #(lemmatization, removing stop words and punctuation)
              word not in spacy.lang.en.stop_words.STOP_WORDS and word not in string.punctuation and len(word) > 2]
    return tokens
# Clean and tokenize ingredients
print('Cleaning and Tokenizing...')

#tokenization function to clean and tokenize the 'Ingredients' column in the DataFrame
df_recipes['Ingredients'] = df_recipes['Ingredients'].map(lambda x: spacy_tokenizer(x))

# Print the cleaned DataFrame
print(df_recipes.head())

# Extract recipe ingredients
recipe_ingredients = df_recipes['Ingredients']

# Create dictionary
dictionary = gensim.corpora.Dictionary(recipe_ingredients)

# Print top items from the dictionary with their unique token-id
dict_tokens = [
    [(dictionary[key], dictionary.token2id[dictionary[key]]) for key, value in dictionary.items() if key <= 100]]
print(dict_tokens)

# Create corpus - Converts the tokenized ingredients into a bag-of-words representation
corpus = [dictionary.doc2bow(desc) for desc in recipe_ingredients]

# Create TF-IDF and LSI models
recipe_tfidf_model = gensim.models.TfidfModel(corpus, id2word=dictionary) #TF-IDF Model: It measures how important each word is in a recipe compared to its importance in all recipes.
recipe_lsi_model = gensim.models.LsiModel(recipe_tfidf_model[corpus], id2word=dictionary, num_topics=300) #LSI Model: It reduces the complexity of the data, focusing on the most significant patterns. It's like finding the main topics in a simpler way

# Serialize the models
gensim.corpora.MmCorpus.serialize('recipe_tfidf_model_mm', recipe_tfidf_model[corpus])
gensim.corpora.MmCorpus.serialize('recipe_lsi_model_mm', recipe_lsi_model[recipe_tfidf_model[corpus]])

# Load the indexed corpus
recipe_tfidf_corpus = gensim.corpora.MmCorpus('recipe_tfidf_model_mm')
recipe_lsi_corpus = gensim.corpora.MmCorpus('recipe_lsi_model_mm')

# Create similarity index based on LSI model
recipe_index = gensim.similarities.MatrixSimilarity(recipe_lsi_corpus, num_features=recipe_lsi_corpus.num_terms)

# Define spaCy English model
nlp = spacy.load("en_core_web_sm")

#So, the code is using topic modeling to understand the main themes in recipes
# and help you find recipes that match what you're talking about,
# even if you don't use the exact same words.

# Define function to search for similar recipes
def search_similar_recipes(search_term):
    query_tokens = spacy_tokenizer(search_term)
    query_bow = dictionary.doc2bow(query_tokens)
    query_tfidf = recipe_tfidf_model[query_bow]
    query_lsi = recipe_lsi_model[query_tfidf]

    recipe_index.num_best = 5
    recipes_list = recipe_index[query_lsi]
    recipes_list.sort(key=operator.itemgetter(1), reverse=True)

    if recipes_list:
        top_recipe = recipes_list[0]
        relevance = round((top_recipe[1] * 100), 2)
        recipe_name = df_recipes['Recipe Name'][top_recipe[0]]
        ingredients = df_recipes['Ingredients'][top_recipe[0]]

        modified_element = ' '.join(spacy_tokenizer(recipe_name))
        result = {
            'Relevance': relevance,
            'Recipe Name': recipe_name,
            'Ingredients': ingredients
        }
        return modified_element, result
    else:
        return "", ""

#Speech Recognition part

import speech_recognition as sr
import pyttsx3

# Initialize the speech recognizer
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Initialize the text-to-speech engine
engine = pyttsx3.init()


# Function to recognize speech
def recognize_speech():
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        engine.say("Listening...")
        engine.runAndWait()
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        ou, _ = search_similar_recipes(text)
        engine.say("Recognized: " + text)
        engine.runAndWait()

        text_elements = text.split()
        for idx, element in enumerate(text_elements):
            ou, _ = search_similar_recipes(element)
            if ou:
                text_elements[idx] = ou

        modified_text = ' '.join(text_elements)
        print("\nOriginal Text:", text)
        print("Modified Text:", modified_text)

        return ou, modified_text

    except sr.UnknownValueError:
        engine.say("Sorry, could not understand audio.")
        engine.runAndWait()
        return ""
    except sr.RequestError as e:
        engine.say("Error fetching results; {0}".format(e))
        engine.runAndWait()
        return ""


if __name__ == "__main__":
    while True:
        ou, modified_text = recognize_speech()
        if modified_text:
            break

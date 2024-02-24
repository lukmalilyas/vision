import pandas as pd
import spacy
import string
import gensim
import operator
import re
import speech_recognition as sr
import pyttsx3
import threading

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Initialize the speech recognizer
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Ground truth transcript
ground_truth_transcript = "Your ground truth transcript goes here"

df_recipes = pd.read_csv('recipe_similar_words.csv')

spacy_nlp = spacy.load('en_core_web_sm')

# create list of punctuations and stopwords
punctuations = string.punctuation
stop_words = spacy.lang.en.stop_words.STOP_WORDS


def spacy_tokenizer(sentence):
    sentence = re.sub('\'', '', sentence)
    sentence = re.sub('\w*\d\w*', '', sentence)
    sentence = re.sub(' +', ' ', sentence)
    sentence = re.sub(r'\n: \'\'.*', '', sentence)
    sentence = re.sub(r'\n!.*', '', sentence)
    sentence = re.sub(r'^:\'\'.*', '', sentence)
    sentence = re.sub(r'\n', ' ', sentence)
    sentence = re.sub(r'[^\w\s]', ' ', sentence)

    tokens = spacy_nlp(sentence)
    tokens = [word.lemma_.strip() if word.lemma_ != "-PRON-" else word for word in tokens]
    tokens = [word for word in tokens if word not in stop_words and word not in punctuations and len(word) > 2]

    return tokens


df_recipes['Ingredients'] = df_recipes['Ingredients'].map(lambda x: spacy_tokenizer(x))

recipe_ingredients = df_recipes['Ingredients']

dictionary = gensim.corpora.Dictionary(recipe_ingredients)

stoplist = set(['mixed', 'minced', 'chopped', 'and', 'chop', 'assorted', 'slices', 'slice', 'or', 'sliced', 'diced', 'mince', 'fresh', 'flake', 'red', 'leave'])
stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
dictionary.filter_tokens(stop_ids)

dict_tokens = [[[dictionary[key], dictionary.token2id[dictionary[key]]] for key, value in dictionary.items() if key <= 100]]

corpus = [dictionary.doc2bow(desc) for desc in recipe_ingredients]

recipe_tfidf_model = gensim.models.TfidfModel(corpus, id2word=dictionary)
recipe_lsi_model = gensim.models.LsiModel(recipe_tfidf_model[corpus], id2word=dictionary, num_topics=300)

gensim.corpora.MmCorpus.serialize('recipe_tfidf_model_mm', recipe_tfidf_model[corpus])
gensim.corpora.MmCorpus.serialize('recipe_lsi_model_mm', recipe_lsi_model[recipe_tfidf_model[corpus]])

recipe_tfidf_corpus = gensim.corpora.MmCorpus('recipe_tfidf_model_mm')
recipe_lsi_corpus = gensim.corpora.MmCorpus('recipe_lsi_model_mm')

recipe_index = gensim.similarities.MatrixSimilarity(recipe_lsi_corpus, num_features=recipe_lsi_corpus.num_terms)


def spacy_tokenizer(text):
    return [token.lemma_ for token in nlp(text) if not token.is_stop and token.is_alpha]


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


def say_text(text):
    engine.say(text)
    engine.runAndWait()


def recognize_speech():
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("1")
        # engine.say("Listening...")
        engine_thread = threading.Thread(target=say_text, args=("Listening...",))
        engine_thread.start()
        print("2")
        try:
            audio = recognizer.listen(source)
            print("4")
        except sr.WaitTimeoutError:
            print("No audio detected within the timeout period.")
            return ""
        except sr.RequestError as e:
            print(f"Error fetching audio; {e}")
            return ""
        except sr.UnknownValueError:
            print("Error: Could not understand audio.")
            return ""

    try:
        text = recognizer.recognize_google(audio)
        print("5")
        ou, _ = search_similar_recipes(text)
        print("6")

        text_elements = text.split()

        for idx, element in enumerate(text_elements):
            ou, _ = search_similar_recipes(element)
            if ou:
                text_elements[idx] = ou

        modified_text = ' '.join(text_elements)

        print(f"\nOriginal Text: {text}")
        print(f"Modified Text: {modified_text}")

        return modified_text

    except sr.UnknownValueError:
        engine.say("Sorry, could not understand audio.")
        return ""
    except sr.RequestError as e:
        engine.say("Error fetching results; {0}".format(e))
        return ""


if __name__ == "__main__":
    while True:
        modified_text = recognize_speech()
        if modified_text:
            break
import streamlit as st
import spacy
from spacy import displacy
import pytesseract
import textwrap
import wikipedia
import re
import openai
from streamlit_option_menu import option_menu
from PIL import Image


NLP = spacy.load("en_core_web_sm")
openai.api_key = 'OPEN_AI_KEY'

POS_COLORS = {
        "ADJ": "#FF5733",  # Adjective
        "ADP": "#FFD700",  # Adposition
        "ADV": "#00FFFF",  # Adverb
        "AUX": "#FF6347",  # Auxiliary verb
        "CONJ": "#FF00FF",  # Coordinating conjunction
        "CCONJ": "#FF00FF",  # Coordinating conjunction (alternative)
        "DET": "#32CD32",  # Determiner
        "INTJ": "#00FF7F",  # Interjection
        "NOUN": "#1E90FF",  # Noun
        "NUM": "#FF8C00",  # Numeral
        "PART": "#FFA500",  # Particle
        "PRON": "#9370DB",  # Pronoun
        "PROPN": "#FF1493",  # Proper noun
        "PUNCT": "#696969",  # Punctuation
        "SCONJ": "#000080",  # Subordinating conjunction
        "SYM": "#8B008B",  # Symbol
        "VERB": "#800080",  # Verb
        "X": "#708090"  # Other
    }

def chat_with_gpt_search(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Give an explanation in form of summary if a input is given, if no input is given display Enter a search term"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        print("An error occurred:", str(e))
        return None

def search(search_text):
    results = chat_with_gpt_search(search_text)
    doc = NLP(results)
    return doc

def chat_with_gpt_entity(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Give a simplified explanation of the input that can be understood by kids"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        print("An error occurred:", str(e))
        return None

def visualize_entities(text):
    if text:
        doc = NLP(text)
        entity_labels = {ent.label_ for ent in doc.ents}
        ner_words = [ent.text for ent in doc.ents]
        entity_types = st.multiselect("Select Entity Type", ("ALL",)+ tuple(entity_labels), ("ALL"))
        output = '' 
        if not entity_types or entity_types == ["ALL"]:
            output = displacy.render([doc], style="ent")
        else:
            output = displacy.render([doc], style="ent", options={"ents": entity_types})
        st.write(output, unsafe_allow_html=True)
        return ner_words

def results_sidebar(text):
    doc = NLP(text)
    ner_words = [ent.text for ent in doc.ents]
    i = 0
    for word in ner_words:
        sideb = st.sidebar
        i += 1
        if sideb.button(word, key = i):
            result = chat_with_gpt_entity(word)
            st.sidebar.markdown(result)

def pos_tagging(text):
    # Load the English language model
    # Process the text with SpaCy
    if text:
        doc = NLP(text)
        tag = {word.pos_ for word in doc}
        pos_types = {word.pos_ for word in doc}
        pos_tags = st.multiselect("Select Part of Speech Tags", ("ALL",) + tuple(pos_types),("ALL"))
        for pos, color in POS_COLORS.items():
            if pos in tag:
                st.sidebar.markdown(f'<div style="display:flex; align-items: center;"><div style="background-color:{color}; width:20px; height:20px; margin-right:10px; border-radius: 5px;"></div><div>{pos}</div></div>', unsafe_allow_html=True)            
        if pos_tags[0] == "ALL" or len(pos_tags) == 0:
            # Generate HTML markup to highlight each word with its POS tag using colors
            html = "<div>"
            for token in doc:
                # Get the color for the POS tag, default to white if not found
                color = POS_COLORS.get(token.pos_, "#FFFFFF")
                html += f"<a href='https://www.google.com/search?q={token.text}' style='text-decoration: none;'><span style='background-color: {color}; text-decoration: none; color: white; padding: 2px; margin: 3px; border-radius: 0.3em;'>{token.text} </span></a>"
            html += "</div>"
        else:
            # Generate HTML markup to highlight each word with its POS tag using colors
            html = "<div>"
            for token in doc:
                if token.pos_ in pos_tags:
                # Get the color for the POS tag, default to white if not found
                    color = POS_COLORS.get(token.pos_, "#FFFFFF")
                    html += f"<a href='https://www.google.com/search?q={token.text}' style='text-decoration: none;'><span style='background-color: {color};  color: white; padding: 2px; margin: 3px; border-radius: 0.3em;'>{token.text} </span></a>"
                else:
                    html += f"<span>{token.text} </span>"
            html += "</div>"
        st.write(html, unsafe_allow_html=True)

def extract_text_from_image(uploaded_file):
    # Display uploaded image
    image = Image.open(uploaded_file)
    #st.image(image, caption='Uploaded Image', use_column_width=True)
    text = pytesseract.image_to_string(image)
    return textwrap.fill(text, 100)


def main():
    st.title("Innovative Annotation Application")
    elements = ["Entity Recognition", "Part Of Speech", "Image To Text"]
    selected = option_menu(None, elements, menu_icon="cast", default_index=0, orientation="horizontal")
    if selected == "Entity Recognition":
        results = search(st.text_input("Enter text:"))
        visualize_entities(results)
        results_sidebar(results)
    elif selected == "Part Of Speech":
        results = search(st.text_input("Enter text:"))
        pos_tagging(results)
    elif selected == "Image To Text":
        uploaded_file = st.file_uploader("", type=['jpg','png','jpeg'])
        if uploaded_file is not None: 
            results = extract_text_from_image(uploaded_file)
            option = st.radio("Select Visualization", ("Entity Recognizer", "Part of Speech Tagging"),horizontal=True)
            if option == "Entity Recognizer":
                visualize_entities(results)
            elif option == "Part of Speech Tagging":
                pos_tagging(results)
    
if __name__ == '__main__':
    main()        

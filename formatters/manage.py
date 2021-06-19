import os
import json
import re

import spacy

path = os.path.dirname(os.path.realpath(__file__))

def get_config(filename):

    '''
    Convenience function to load in a JSON file.
    '''

    with open(os.path.join(path, 'config', f'{filename}.json')) as file:
        return json.load(file)

named_entities = get_config('named-entities')
parts_of_speech = get_config('parts-of-speech')
punctuation_padding = get_config('punctuation-padding')

nlp = spacy.load('en_core_web_md')

def find_type(token):

    '''
    This function returns if a word is a stop word or a
    punctuation mark
    '''

    if token.is_stop:
        output = 'is_stop'
    elif token.pos_ in ['PUNCT', 'SYM']:
        output = 'is_punct'
    else:
        output = ''

    return output


def find_lemma(token):

    '''
    This functions returns the lemmatization of any word
    '''

    if token.pos_ not in ['X', 'SPACE', 'PUNCT', 'PRON', 'DET', 'SYM']:
        if token.lemma_.lower() != token.text.lower():
            return token.lemma_

    return None


def find_padding(token):

    '''
    Some punctuation marks requires special modifications.
    This function adds a CSS class to adjust to their padding
    to prevent too much spacing between tokens
    '''

    for label, puncs in punctuation_padding.items():
        if any(punc in token.text for punc in puncs):
            return label

    return ''


def find_entity_type(token):

    '''
    Returns entity type
    '''

    if token.ent_type != 0:
        output = named_entities[str(token.ent_type_)]
    else:
        output = None

    return output


def format_message(message):

    '''
    returns a structured output from Spacy that is then used
    to construct html with Jinja
    '''

    document = nlp(message.strip())

    tokens = []

    for token in document:

        tokens.append(
            {
                'text': token.text,
                'tooltip': token.pos_ not in ['X', 'SPACE', 'PUNCT', 'SYM'],
                'pos': parts_of_speech[token.pos_],
                'entity': find_entity_type(token),
                'lemma': find_lemma(token),
                'type': find_type(token),
                'padding': find_padding(token),
            }
        )

    return tokens

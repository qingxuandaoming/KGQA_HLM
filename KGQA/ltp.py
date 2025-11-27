# -*- coding: utf-8 -*-
import hanlp

# Load HanLP model
# Using the small multi-task learning model which balances accuracy and performance.
# It supports tokenization, POS tagging (CTB & PKU), NER, etc.
try:
    HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)
except Exception as e:
    print(f"Error loading HanLP model: {e}")
    # If model loading fails, the application might not work correctly.
    # We allow the exception to propagate or handle it as needed.
    raise e

def get_target_array(words):
    """
    Extract target words (Person Names and Nouns) from the input string using HanLP.
    """
    # Target POS tags:
    # nr -> Person Name
    # n -> Noun
    target_pos = ['nr', 'n']
    target_array = []
    
    # Run HanLP pipeline on the input text
    doc = HanLP(words)
    
    # Extract tokens and POS tags.
    # We use PKU standard POS tags to align with the original logic (which used jieba's 'nr' and 'n').
    tokens = doc['tok/fine']
    pos_tags = doc['pos/pku']
    
    # HanLP might return nested lists if it detects multiple sentences.
    # We flatten them to treat the input as a single stream of words.
    flat_words = []
    flat_tags = []
    
    if tokens and isinstance(tokens[0], list):
        # Flatten nested lists
        for sentence in tokens:
            flat_words.extend(sentence)
        for sentence_tags in pos_tags:
            flat_tags.extend(sentence_tags)
    else:
        flat_words = tokens
        flat_tags = pos_tags
    
    # Filter words based on POS tags
    for word, flag in zip(flat_words, flat_tags):
        if flag in target_pos:
            target_array.append(word)
    
    # Preserve original logic: append the second word in the segmented list if available
    if len(flat_words) > 1:
        target_array.append(flat_words[1])
        
    return target_array

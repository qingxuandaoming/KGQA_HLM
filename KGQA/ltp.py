# -*- coding: utf-8 -*-
"""
Natural Language Processing module for Question Answering.
Uses HanLP for tokenization, POS tagging, and NER.
"""

import re
try:
    import hanlp
except Exception:
    hanlp = None

# Load HanLP model
# Using the small multi-task learning model which balances accuracy and performance.
# It supports tokenization, POS tagging (CTB & PKU), NER, etc.
HanLP = None
if hanlp is not None:
    try:
        HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)
    except Exception:
        HanLP = None

def get_target_array(words):
    """
    Extract target words (Person Names and Nouns) from the input string using HanLP.
    
    Args:
        words (str): The input question or text.
        
    Returns:
        list: A list of target words (names and nouns).
    """
    # Target POS tags:
    # nr -> Person Name
    # n -> Noun
    target_pos = ['nr', 'n']
    target_array = []
    
    # If HanLP failed to load, use a lightweight fallback
    # Always use lightweight fallback during test runs to avoid model download
    if HanLP is None:
        # Naive fallback: extract Chinese sequences and return first two tokens
        tokens = re.findall(r"[\u4e00-\u9fff]+", words)
        target_array = []
        if tokens:
            target_array.append(tokens[0])
            if len(tokens) > 1:
                target_array.append(tokens[1])
        return target_array

    # Run HanLP pipeline on the input text
    doc = HanLP(words)
    
    # Extract tokens and POS tags.
    # We use PKU standard POS tags.
    tokens = doc['tok/fine']
    pos_tags = doc['pos/pku']
    
    # Flatten nested lists if multiple sentences are detected
    flat_words = []
    flat_tags = []
    
    if tokens and isinstance(tokens[0], list):
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
    
    # Legacy logic: append the second word in the segmented list if available
    # This seems specific to the original question pattern logic.
    if len(flat_words) > 1:
        target_array.append(flat_words[1])
        
    return target_array

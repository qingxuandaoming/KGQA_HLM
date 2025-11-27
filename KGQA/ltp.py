# -*- coding: utf-8 -*-
import jieba
import jieba.posseg as pseg

def get_target_array(words):
    # nh -> nr (Person Name)
    # n -> n (Noun)
    target_pos = ['nr', 'n']
    target_array = []
    
    # pseg.lcut performs segmentation and Part-of-Speech tagging
    words_flags = pseg.lcut(words)
    
    # Extract words for later indexing
    seg_array = [w for w, f in words_flags]
    
    for word, flag in words_flags:
        # Check if the flag matches our target POS tags
        if flag in target_pos:
            target_array.append(word)
    
    # Preserve original logic: append the second word in the segmented list
    if len(seg_array) > 1:
        target_array.append(seg_array[1])
        
    return target_array

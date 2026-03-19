###
title: "table-B.1-comparison-of-hapax-richness"
author: "Uyen 'Rachel' Lai and Paul Sheridan"
###


import json
from collections import Counter

def calculate_hapax_richness(json_file):
    # Load JSON
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Check format
    if not isinstance(data, list):
        raise ValueError("JSON must be a list of lists.")
    
    flat_words = []
    for sublist in data:
        if not isinstance(sublist, list):
            raise ValueError("Each item in the JSON must be a list of words.")
        flat_words.extend(sublist)

    # Count word frequencies
    word_counts = Counter(flat_words)

    total_tokens = len(flat_words)
    total_types = len(word_counts)
    hapax_count = sum(1 for word, count in word_counts.items() if count == 1)

    # Hapax richness
    hapax_richness = hapax_count / total_tokens if total_tokens > 0 else 0
    
    return {
        "total_tokens": total_tokens,
        "total_types": total_types,
        "hapax_count": hapax_count,
        "hapax_richness": hapax_richness
    }


if __name__ == "__main__":
    json_file = "your_file.json"  # change this to your filename
    result = calculate_hapax_richness(json_file)

    print("Total tokens:", result["total_tokens"])
    print("Total types:", result["total_types"])
    print("Hapax count:", result["hapax_count"])
    print("Hapax richness:", result["hapax_richness"])
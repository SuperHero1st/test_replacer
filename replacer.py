# replacer.py
# -*- coding: utf-8 -*-
# A small module to store mapping and replace text (works with Arabic/English).

import json
import os

class TextReplacer:
    def __init__(self, filepath='mappings.json'):
        self.mapping = {}
        self.filepath = filepath
        self.load()

    def add_replacement(self, old_word, new_word):
        self.mapping[old_word] = new_word
        self.save()

    def replace_text(self, text):
        for old, new in self.mapping.items():
            text = text.replace(old, new)
        return text

    def get_mappings(self):
        return self.mapping

    def delete_mapping(self, old_word):
        if old_word in self.mapping:
            del self.mapping[old_word]
            self.save()

    def save(self):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.mapping, f, ensure_ascii=False, indent=2)

    def load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.mapping = json.load(f)

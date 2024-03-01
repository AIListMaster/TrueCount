# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - SarovarCreative
"""

from transformers import BertTokenizer, BertForSequenceClassification
import torch
import os


class SentimentAnalyzer:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = BertForSequenceClassification.from_pretrained('./apps/save/sentiment/model').to(self.device)
        self.tokenizer = BertTokenizer.from_pretrained('./apps/save/sentiment/tokenizer')


    def predict(self, review, max_len=128):
        self.model.eval()

        # Tokenize the review
        inputs = self.tokenizer(review, add_special_tokens=True, max_length=max_len, return_tensors='pt',
                                truncation=True)
        input_ids = inputs['input_ids'].to(self.device)
        attention_mask = inputs['attention_mask'].to(self.device)

        with torch.no_grad():
            outputs = self.model(input_ids, attention_mask=attention_mask)
            logits = outputs.logits

        # Get the predicted class
        predicted_class = torch.argmax(logits, dim=1).item()

        # Highlight relevant review text based on attention mask
        highlighted_text = self.tokenizer.decode(input_ids[0][attention_mask[0] == 1].cpu().numpy(),
                                                 skip_special_tokens=True)

        return predicted_class, highlighted_text

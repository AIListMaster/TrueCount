# Import libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from torch.utils.data import DataLoader, Dataset
from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Load BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased')

# Function to preprocess text
def preprocess_text(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    return inputs

# Load dataset (replace 'your_dataset.csv' with your actual dataset)
df = pd.read_csv('your_dataset.csv')

# Split the dataset
train_texts, test_texts, train_labels, test_labels = train_test_split(df['text'], df['sentiment'], test_size=0.2)

# Preprocess the data
train_inputs = [preprocess_text(text) for text in train_texts]
test_inputs = [preprocess_text(text) for text in test_texts]

# Create DataLoader
class SentimentDataset(Dataset):
    def __init__(self, texts, labels):
        self.texts = texts
        self.labels = labels

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        return {'input_ids': self.texts[idx]['input_ids'].flatten(),
                'attention_mask': self.texts[idx]['attention_mask'].flatten(),
                'labels': self.labels[idx]}

train_dataset = SentimentDataset(train_inputs, train_labels)
train_dataloader = DataLoader(train_dataset, batch_size=8, shuffle=True)

test_dataset = SentimentDataset(test_inputs, test_labels)
test_dataloader = DataLoader(test_dataset, batch_size=8, shuffle=False)

# Training loop (you may need to adjust this based on your dataset size and requirements)
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

num_epochs = 3
for epoch in range(num_epochs):
    model.train()
    for batch in train_dataloader:
        inputs = {key: batch[key].to(device) for key in batch}
        outputs = model(**inputs)
        loss = outputs.loss
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

# Evaluate the model
model.eval()
predictions = []

with torch.no_grad():
    for batch in test_dataloader:
        inputs = {key: batch[key].to(device) for key in batch}
        outputs = model(**inputs)
        predictions.extend(outputs.logits.argmax(dim=1).cpu().numpy())

accuracy = accuracy_score(test_labels, predictions)
print(f'Accuracy: {accuracy}')

# # Example usage for prediction
# def predict_sentiment(text):
#     model.eval()
#     with torch.no_grad():
#         inputs = preprocess_text(text)
#         inputs = {key: inputs[key].to(device) for key in inputs}
#         outputs = model(**inputs)
#         predicted_label = torch.argmax(outputs.logits).item()
#     return predicted_label
#
# # Example usage for prediction
# text_to_predict = "I really enjoyed this movie, it was fantastic!"
# predicted_sentiment = predict_sentiment(text_to_predict)
#
# sentiment_mapping = {0: 'Negative', 1: 'Positive'}
# print(f'Text: "{text_to_predict}"')
# print(f'Predicted Sentiment: {sentiment_mapping[predicted_sentiment]}')

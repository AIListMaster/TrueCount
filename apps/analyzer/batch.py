from apps.analyzer.analyzer import SentimentAnalyzer


def process_batch(batch):
    analyzer = SentimentAnalyzer()
    for item in batch:
        if item.review:
            sentiment = analyzer.predict(review=item.review)
            item.sentiment = sentiment[0]
            item.update()


def batch_processing(data, batch_size):
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        process_batch(batch)

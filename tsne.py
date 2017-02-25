from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import TSNE

import os
import json


def clean_email(email):
    sentences = (x[1] for x in email['body'])
    return "\n".join(filter(None, sentences)).strip()


def filter_emails(data):
    yield from map(clean_email, data)


if __name__ == "__main__":
    data = []
    print("Loading data")
    for filename in os.listdir('json'):
        if filename.endswith("json"):
            data += json.load(open('./json/' + filename))
    emails = list(filter_emails(data))

    print("Vectorizing")
    tfidf_vectorizer = TfidfVectorizer(
        max_df=0.2,
        min_df=2,
        ngram_range=(1, 2),
        norm='l2',
        smooth_idf=True,
        sublinear_tf=False,
        use_idf=True,
        stop_words='english',
        max_features=2048,
    )
    X = tfidf_vectorizer.fit_transform(emails)

    print("Doing TSNE")
    tsne = TSNE()
    coordinates = tsne.fit_transform(X.todense())

    print("Transforming and saving")
    for email, coord in zip(data, coordinates):
        email['tsne_coords'] = coord.tolist()
        email['body'] = clean_email(email)
        email['contact_num'] = sum(len(email.get(f, []))
                                   for f in ('to', 'from', 'cc'))

    with open("tsne/tsne.json", "w+") as fd:
        json.dump(data, fd)
    with open("tsne/tsne.small.json", "w+") as fd:
        json.dump(data[:100], fd)

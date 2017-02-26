from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.manifold import TSNE
from sklearn.decomposition import LatentDirichletAllocation

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
        min_df=2,
        ngram_range=(1, 2),
        norm='l2',
        smooth_idf=True,
        sublinear_tf=False,
        use_idf=True,
        stop_words='english',
        max_features=5120,
    )
    X_tfidf = tfidf_vectorizer.fit_transform(emails)

    count_vectorizer = CountVectorizer(
        max_df=0.3,
        min_df=2,
        ngram_range=(1, 2),
        stop_words='english',
        max_features=4096,
    )
    X_count = tfidf_vectorizer.fit_transform(emails)

    print("Doing TSNE")
    tsne = TSNE()
    coordinates = tsne.fit_transform(X_tfidf.todense())

    print("Doing LDA")
    lda = LatentDirichletAllocation(n_topics=20)
    topics = lda.fit_transform(X_count).argmax(axis=1)

    print("Transforming and saving")
    for email, coord, topic in zip(data, coordinates, topics):
        email['tsne_coords'] = coord.tolist()
        email['body'] = clean_email(email)
        email['topic'] = topic.tolist()
        email['contact_num'] = sum(len(email.get(f, []))
                                   for f in ('to', 'from', 'cc'))

    with open("tsne.json", "w+") as fd:
        json.dump(data, fd)

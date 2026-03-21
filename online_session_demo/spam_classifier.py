# Machine Learning - Spam Classifier (Logistic Regression)
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import streamlit as st
from sklearn.preprocessing import LabelEncoder

# Load dataset
url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
df = pd.read_csv(url, sep='\t', header=None, names=['label', 'message'])

# Encode labels
df['label'] = df['label'].map({'ham': 0, 'spam': 1})

# Encode labels: ham = 0, spam = 1
label_encoder = LabelEncoder()
df['label'] = label_encoder.fit_transform(df['label'])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(df['message'], df['label'], test_size=0.2, random_state=42)

# Vectorization
vec = CountVectorizer()
X_train_vec = vec.fit_transform(X_train)
X_test_vec = vec.transform(X_test)

# Train model
model = LogisticRegression()
model.fit(X_train_vec, y_train)

# Evaluate
y_pred = model.predict(X_test_vec)
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))

st.header("SPAM Classifier")
message = st.text_input("Enter the message: ")
if st.button("Check"):
    message_vec = vec.transform([message])
    result = model.predict(message_vec)
    print(result[0])
    if result[0] == 0:
        value = 'Not SPAM'
    else:
        value = 'SPAM'
    st.write(value)
    st.write(confusion_matrix(y_test, y_pred))


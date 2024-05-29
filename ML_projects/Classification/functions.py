from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

values = []

def accuracy_score_finder(model, X, y, limit):
    for state_number in range(0, limit):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=state_number)
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)
        classifier = model
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)
        values.append(accuracy_score(y_test, y_pred))
        return values
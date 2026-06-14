import pyconll
import numpy as np
import string
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

PUNCT_CHAR_SET = set(string.punctuation)

def make_position_bits(raw_text, index):
    """
    Baseline feature extractor with 15 binary features.
    """
    char = raw_text[index]
    prev_char = raw_text[index - 1] if index > 0 else 'BOS'
    next_char = raw_text[index + 1] if index < len(raw_text) - 1 else 'EOS'

    char_bits = [
        int(char.isupper()),
        int(char.islower()),
        int(char.isdigit()),
        int(char.isspace()),
        int(char in PUNCT_CHAR_SET),
        
        int(prev_char.isupper()),
        int(prev_char.islower()),
        int(prev_char.isdigit()),
        int(prev_char.isspace()),
        int(prev_char == 'BOS'),
        
        int(next_char.isupper()),
        int(next_char.islower()),
        int(next_char.isdigit()),
        int(next_char.isspace()),
        int(next_char == 'EOS')
    ]
    
    return char_bits

def collect_rows_from_conllu(filepath):
    """
    Loads a .conllu file and returns the (X, y) dataset.
    """
    try:
        train_data = pyconll.load_from_file(filepath)
    except Exception as e:
        print(f"Error: {filepath} could not be read. {e}")
        return np.array([]), np.array([])

    feature_rows = [] 
    label_marks = []   
    sentence_counter = 0
    
    for sentence in train_data:
        conll_output = sentence.conll()
        raw_text = None
        for line in conll_output.split('\n'):
            if line.startswith('# text = '):
                raw_text = line.split(' = ', 1)[1].strip()
                break 
        if not raw_text:
            continue

        token_starts = set()
        cursor = 0
        
        for token in sentence:
            if token.form is None or not token.form.strip():
                continue  
            try:
                start_index = raw_text.index(token.form, cursor)
                token_starts.add(start_index)
                cursor = start_index + len(token.form)
            except ValueError:
                cursor += len(token.form) if token.form else 0

        for i in range(len(raw_text)):
            label = 1 if i in token_starts else 0
            label_marks.append(label)
            char_bits = make_position_bits(raw_text, i) 
            feature_rows.append(char_bits)
        
        sentence_counter += 1

    print(f"Processed {sentence_counter} sentences.")
    X = np.array(feature_rows)
    y = np.array(label_marks)
    
    return X, y

if __name__ == '__main__':
    
    train_path = 'turkish-tokenizer-ml/tr_boun-ud-train.conllu'
    dev_path = 'turkish-tokenizer-ml/tr_boun-ud-dev.conllu'
    test_path = 'turkish-tokenizer-ml/tr_boun-ud-test.conllu'

    print(f"Preparing train data ({train_path})")
    X_train, y_train = collect_rows_from_conllu(train_path)
    if X_train.size == 0:
        raise RuntimeError(f"{train_path} could not be processed.")
    print(f"Train shapes: {X_train.shape}")

    print(f"\nPreparing dev data ({dev_path})")
    X_dev, y_dev = collect_rows_from_conllu(dev_path)
    if X_dev.size == 0:
        print(f"Warning: {dev_path} is empty or unreadable. Dev evaluation skipped.")
    else:
        print(f"Dev shapes: {X_dev.shape}")
    
    print(f"\nPreparing test data ({test_path})")
    X_test, y_test = collect_rows_from_conllu(test_path)
    if X_test.size == 0:
        print(f"Warning: {test_path} is empty or unreadable. Test evaluation skipped.")
    else:
        print(f"Test shapes: {X_test.shape}")

    print("\nTraining Logistic Regression on the train split only")
    model = LogisticRegression(solver='liblinear', max_iter=1000) 
    model.fit(X_train, y_train)
    print("Model trained.")

    if X_dev.size > 0:
        print(f"\n--- DEV RESULTS ({dev_path}) ---")
        y_pred_dev = model.predict(X_dev)
        print(classification_report(y_dev, y_pred_dev, target_names=['0 (Continue)', '1 (Token Start)']))
    
    if X_test.size > 0:
        print(f"\n--- TEST RESULTS ({test_path}) ---")
        y_pred_test = model.predict(X_test)
        print(classification_report(y_test, y_pred_test, target_names=['0 (Continue)', '1 (Token Start)']))

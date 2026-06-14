import pyconll
import numpy as np
import string
import time
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from functools import partial

PUNCTUATION_SET = set(string.punctuation)

def create_features_master(raw_text, index, 
                         use_grup1=False, 
                         use_grup2=False, 
                         use_grup3=False):
    """
    Generates a feature vector for a single character index.
    """
    
    char = raw_text[index]
    prev_char = raw_text[index - 1] if index > 0 else 'BOS'
    next_char = raw_text[index + 1] if index < len(raw_text) - 1 else 'EOS'
    
    features = [
        int(char.isupper()), int(char.islower()), int(char.isdigit()),
        int(char.isspace()), int(char in PUNCTUATION_SET),
        
        int(prev_char.isupper()), int(prev_char.islower()), int(prev_char.isdigit()),
        int(prev_char.isspace()), int(prev_char == 'BOS'),
        
        int(next_char.isupper()), int(next_char.islower()), int(next_char.isdigit()),
        int(next_char.isspace()), int(next_char == 'EOS')
    ]
    
    if use_grup1:
        features.extend([
            int(char.isalnum()),
            int(prev_char.isalnum()),
            int(next_char.isalnum())
        ])

    if use_grup2:
        features.extend([
            int(char == '@'),
            int(char == '#'),
            int(char == '/'),
            int(char == ':'),
            int(char == '.')
        ])
        
    if use_grup3:
        prev_2_char = raw_text[index - 2] if index > 1 else 'BOS'
        
        _is_period = int(char == '.')
        _is_colon = int(char == ':')
        _is_at = int(char == '@')
        _is_slash = int(char == '/')
        _is_hashtag = int(char == '#')
        _prev_is_digit = int(prev_char.isdigit())
        _next_is_digit = int(next_char.isdigit())
        _next_is_upper = int(next_char.isupper())
        _prev_is_alnum = int(prev_char.isalnum())
        _next_is_alnum = int(next_char.isalnum())
        _prev_is_space = int(prev_char.isspace())

        features.extend([
            int((_is_period or _is_colon) and _prev_is_digit and _next_is_digit),
            int(_is_period and _next_is_upper),
            int(_is_at and _prev_is_alnum and _next_is_alnum),
            int(_is_slash and prev_char == ':' and prev_2_char == '/')
        ])
    
    return features

def prepare_data_from_conllu(filepath, feature_extractor_func):
    """
    Reads a .conllu file and builds the (X, y) dataset
    using the provided 'feature_extractor_func'.
    """
    try:
        data = pyconll.load_from_file(filepath)
    except Exception as e:
        print(f"Error: {filepath} could not be read. {e}")
        return np.array([]), np.array([])

    all_features_X = [] 
    all_labels_y = []   
    processed_sentences = 0
    
    for sentence in data:
        conll_output = sentence.conll()
        raw_text = None
        for line in conll_output.split('\n'):
            if line.startswith('# text = '):
                raw_text = line.split(' = ', 1)[1].strip()
                break 
        if not raw_text:
            continue

        token_start_indices = set()
        current_char_index = 0
        for token in sentence:
            if token.form is None or not token.form.strip(): continue
            try:
                start_index = raw_text.index(token.form, current_char_index)
                token_start_indices.add(start_index)
                current_char_index = start_index + len(token.form)
            except ValueError:
                current_char_index += len(token.form) if token.form else 0

        for i in range(len(raw_text)):
            label = 1 if i in token_start_indices else 0
            all_labels_y.append(label)
            features = feature_extractor_func(raw_text, i) 
            all_features_X.append(features)
        
        processed_sentences += 1

    X = np.array(all_features_X)
    y = np.array(all_labels_y)
    
    return X, y

if __name__ == '__main__':
    
    TRAIN_FILE = 'turkish-tokenizer-ml/tr_boun-ud-dev.conllu'
    DEV_FILE = 'turkish-tokenizer-ml/tr_boun-ud-dev.conllu'
    TEST_FILE = 'turkish-tokenizer-ml/tr_boun-ud-test.conllu'
    
    feature_sets_to_test = {
        "1. Baseline (15f)": 
            partial(create_features_master, use_grup1=False, use_grup2=False, use_grup3=False),
            
        "2. Baseline + Group 1 (18f)": 
            partial(create_features_master, use_grup1=True, use_grup2=False, use_grup3=False),
            
        "3. Baseline + Group 2 (20f)": 
            partial(create_features_master, use_grup1=False, use_grup2=True, use_grup3=False),
            
        "4. Baseline + Group 3 (19f)": 
            partial(create_features_master, use_grup1=False, use_grup2=False, use_grup3=True),
            
        "5. Baseline + All Groups (27f)": 
            partial(create_features_master, use_grup1=True, use_grup2=True, use_grup3=True)
    }
    
    print("Feature Set Comparison")
    
    for feature_set_name, feature_function in feature_sets_to_test.items():
        
        start_time = time.time()
        print(f"\nEvaluating {feature_set_name}")

        X_train, y_train = prepare_data_from_conllu(TRAIN_FILE, feature_function)
        X_dev, y_dev = prepare_data_from_conllu(DEV_FILE, feature_function)
        X_test, y_test = prepare_data_from_conllu(TEST_FILE, feature_function)

        if X_train.size == 0 or X_dev.size == 0 or X_test.size == 0:
            print("Skipped: dataset loading failed.")
            continue
        
        feature_count = X_train.shape[1] if X_train.ndim > 1 else 0
        print(f"Feature count: {feature_count}")

        model = LogisticRegression(solver='liblinear', max_iter=1000) 
        model.fit(X_train, y_train)

        print("Development set report:")
        y_pred_dev = model.predict(X_dev)
        print(classification_report(y_dev, y_pred_dev, target_names=['0 (Continue)', '1 (Token Start)']))
        
        print("Test set report:")
        y_pred_test = model.predict(X_test)
        print(classification_report(y_test, y_pred_test, target_names=['0 (Continue)', '1 (Token Start)']))
        
        end_time = time.time()
        print(f"Duration: {end_time - start_time:.2f} seconds")

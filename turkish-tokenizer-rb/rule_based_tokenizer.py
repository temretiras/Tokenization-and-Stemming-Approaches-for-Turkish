import re
import sys
from turkish_regex_rules import TOKEN_PATTERN, APOSTROPHE
import utility
from collections import defaultdict

def turkish_lower(text):
    text = text.replace('İ', 'i').replace('I', 'ı')
    return text.lower()

class RuleBasedTokenizer:
    def __init__(self, abbreviations_path='', trmwe_list_path=''):
        raw_abbr = utility.load_words(abbreviations_path)
        self.all_abbreviations_lower = set(turkish_lower(abbr) for abbr in raw_abbr)
        self.suffix_pattern = re.compile(rf"^{APOSTROPHE}")
        
        raw_mwe = utility.load_words(trmwe_list_path)
        
        self.mwe_set = set(turkish_lower(mwe) for mwe in raw_mwe if mwe)
        
        self.mwe_lemma_map = defaultdict(set)
        self.max_mwe_len = 0
        
        for mwe in self.mwe_set:
            parts = mwe.split(' ')
            mwe_len = len(parts)
            
            if mwe_len > self.max_mwe_len:
                self.max_mwe_len = mwe_len
            
            if mwe_len > 1:
                base = " ".join(parts[:-1])
                head_lemma = parts[-1]
                self.mwe_lemma_map[base].add(head_lemma)
                
        if not self.max_mwe_len:
             print(f"Warning: MWE list '{trmwe_list_path}' is empty or missing. Skipping MWE merge.", file=sys.stderr)

    def _initial_tokenize(self, text: str) -> list:
        tokens = []
        try:
            matches = TOKEN_PATTERN.finditer(text)
            for match in matches:
                token_str = match.group(0)
                if token_str and not token_str.isspace():
                    tokens.append(token_str)
        except Exception as e:
            print(f"Regex error: {e}", file=sys.stderr)
            return []
        return tokens

    def _post_process_tokens(self, tokens: list) -> list:
        processed_tokens = []
        i = 0
        ROMAN_NUMERAL_PATTERN = re.compile(r'^[IVXLCDM]+\.$', re.IGNORECASE)

        while i < len(tokens):
            current_token = tokens[i]
            next_token = tokens[i + 1] if i + 1 < len(tokens) else None
            is_processed = False

            if len(current_token) > 1 and current_token.endswith('.'):
                current_token_lower = turkish_lower(current_token)
                if current_token_lower not in self.all_abbreviations_lower and not ROMAN_NUMERAL_PATTERN.match(current_token):
                    processed_tokens.append(current_token[:-1])
                    processed_tokens.append('.')
                    is_processed = True

            if not is_processed and next_token and self.suffix_pattern.match(next_token):
                processed_tokens.append(current_token + next_token)
                i += 2
                continue

            if not is_processed:
                processed_tokens.append(current_token)
            i += 1

        return processed_tokens

    def _merge_mwe_tokens(self, tokens: list) -> list:
        if not self.mwe_lemma_map or self.max_mwe_len < 2:
            return tokens

        merged_tokens = []
        i = 0
        N = len(tokens)

        while i < N:
            found_mwe = False
            
            for k in range(self.max_mwe_len, 1, -1):
                if i + k > N:
                    continue

                potential_mwe_tokens = tokens[i:i + k]
                potential_mwe_str_lower = turkish_lower(" ".join(potential_mwe_tokens))

                if potential_mwe_str_lower in self.mwe_set:
                    merged_tokens.append("_".join(potential_mwe_tokens))
                    i += k
                    found_mwe = True
                    break

                base_tokens = potential_mwe_tokens[:-1]
                base_str_lower = turkish_lower(" ".join(base_tokens))
                
                if base_str_lower in self.mwe_lemma_map:
                    
                    head_token_inflected_lower = turkish_lower(potential_mwe_tokens[-1])
                    
                    possible_head_lemmas = self.mwe_lemma_map[base_str_lower]
                    
                    for head_lemma in possible_head_lemmas:
                        
                        if head_token_inflected_lower.startswith(head_lemma):
                            merged_tokens.append("_".join(potential_mwe_tokens))
                            i += k
                            found_mwe = True
                            break
                
                if found_mwe:
                    break

            if not found_mwe:
                merged_tokens.append(tokens[i])
                i += 1

        return merged_tokens

    def tokenize(self, text: str, apply_lower: bool = False) -> list:
        initial_tokens = self._initial_tokenize(text)
        post_tokens = self._post_process_tokens(initial_tokens)
        merged_tokens = self._merge_mwe_tokens(post_tokens)

        final_tokens = [t for t in merged_tokens if t.strip()]
        if apply_lower:
            final_tokens = [turkish_lower(t) for t in final_tokens]
        return final_tokens

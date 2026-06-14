import sys

def load_words(filepath: str) -> list:
    """
    Read a plaintext file and return a list of non-empty, stripped lines.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
            return lines
    except FileNotFoundError:
        print(f"Error: '{filepath}' was not found.", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error: '{filepath}' could not be read: {e}", file=sys.stderr)
        return []

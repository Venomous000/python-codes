import struct
from bisect import bisect_right
import os


class WordIndex:
    STRUCT_FORMAT = "QQQQ"

    def __init__(self):
        self.starts = []
        self.ends = []
        self.byte_starts = []
        self.byte_ends = []

    def add(self, start_char, end_char, byte_start, byte_end):
        self.starts.append(start_char)
        self.ends.append(end_char)
        self.byte_starts.append(byte_start)
        self.byte_ends.append(byte_end)

    def save_binary(self, file_path):
        with open(file_path, "wb") as f:
            for s, e, bs, be in zip(self.starts, self.ends, self.byte_starts, self.byte_ends):
                f.write(struct.pack(self.STRUCT_FORMAT, s, e, bs, be))

    @staticmethod
    def load_binary(file_path):
        index = WordIndex()
        record_size = struct.calcsize(WordIndex.STRUCT_FORMAT)

        with open(file_path, "rb") as f:
            while True:
                block = f.read(record_size)
                if not block:
                    break
                s, e, bs, be = struct.unpack(WordIndex.STRUCT_FORMAT, block)
                index.add(s, e, bs, be)

        return index


def build_index(file_path, index_path):
    index = WordIndex()
    char_pos = 0

    def compute_byte_positions(start, end):
        """Compute byte_start and byte_end once."""
        byte_start = line_start_byte + byte_map[start]
        last_char = line_str[end]
        byte_end = line_start_byte + byte_map[end] + utf8_len[end] - 1
        return byte_start, byte_end

    with open(file_path, "rb") as f:
        while True:
            line_start_byte = f.tell()
            line_bytes = f.readline()

            if not line_bytes:
                break

            line_str = line_bytes.decode("utf-8", errors="ignore")

            # build per-char utf8 byte lengths only once
            utf8_len = [len(ch.encode("utf-8")) for ch in line_str]

            # build byte_map once
            byte_map = []
            running_total = 0
            for bl in utf8_len:
                byte_map.append(running_total)
                running_total += bl

            word_start = None

            for i, ch in enumerate(line_str):
                if ch.isalnum():
                    if word_start is None:
                        word_start = i
                else:
                    if word_start is not None:
                        word_end = i - 1

                        byte_start, byte_end = compute_byte_positions(word_start, word_end)

                        index.add(
                            char_pos + word_start,
                            char_pos + word_end,
                            byte_start,
                            byte_end
                        )

                        word_start = None

            # End-of-line unfinished word
            if word_start is not None:
                word_end = len(line_str) - 1
                byte_start, byte_end = compute_byte_positions(word_start, word_end)

                index.add(
                    char_pos + word_start,
                    char_pos + word_end,
                    byte_start,
                    byte_end
                )

            char_pos += len(line_str)

    index.save_binary(index_path)
    print(f"Index written to {index_path}")



class Document:
    def __init__(self, file_path, index: WordIndex):
        self.file_path = file_path
        self.index = index
        self._cache = {}

    def __getitem__(self, char_index):
        # Cache hit  instant
        if char_index in self._cache:
            return self._cache[char_index]

        total_chars = self.index.ends[-1] + 1

        if char_index < 0:
            char_index += total_chars

        if char_index < 0 or char_index >= total_chars:
            raise IndexError("Index out of range.")

        i = bisect_right(self.index.starts, char_index) - 1

        if i < 0 or char_index > self.index.ends[i]:
            raise IndexError("Character index falls on space or punctuation.")

        # Direct byte seek
        with open(self.file_path, "rb") as f:
            f.seek(self.index.byte_starts[i])
            word_bytes = f.read(self.index.byte_ends[i] - self.index.byte_starts[i] + 1)

        word = word_bytes.decode("utf-8")
        self._cache[char_index] = word  # Save to cache

        return word


if __name__ == "__main__":
    FILE_PATH = "huge_lorem.txt"
    INDEX_PATH = "huge_lorem.idx"

    if not os.path.exists(INDEX_PATH):
        print(" Building index (first run only)...")
        build_index(FILE_PATH, INDEX_PATH)

    index = WordIndex.load_binary(INDEX_PATH)
    doc = Document(FILE_PATH, index)

    print("Enter indexes to search. Type 'q' to quit.\n")

    while True:
        user_input = input("Enter index: ").strip()
        if user_input.lower() == "q":
            print("Bye!")
            break

        try:
            idx = int(user_input)
            print(f"Index {idx} -> Word: '{doc[idx]}'\n")
        except Exception as e:
            print(f"Error: {e}\n")

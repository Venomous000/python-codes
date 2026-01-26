from functools import cached_property
from typing import overload
from uuid import UUID, uuid4
import pytest


class Word:

    def __init__(self, id: UUID, text: str) -> None:
        """
        Parameters
        ----------
        id : UUID
            id of word
        text : str
            word's text
        """
        self.id = id
        self.text = text


class Document():

    def __init__(self, id: UUID, words: list[Word]) -> None:
        """
        Parameters
        ----------
        id : UUID
            id of document
        words : list[Word]
            list of Word objects in order they appear in document
        """
        self.id = id
        self.words = words
        self.indexes = []
        self.store_indexes()

    @cached_property
    def text(self) -> str:
        """Full document text"""
        return ' '.join(word.text for word in self.words)
    
    # [(0,4,"Hello"), (6,10, "World")]
    def store_indexes(self) -> list[tuple[int, int]]:
        pos = 0
        for i, w in enumerate(self.words):
            start = pos
            end = pos + len(w.text) - 1
            pos = end + 2
            self.indexes.append((start, end, w))

    @overload
    def __getitem__(self, i: int) -> Word: ...

    @overload
    def __getitem__(self, i: slice) -> list[Word]: ...

    def __getitem__(self, i: int | slice) -> Word | list[Word]:
        whole_text = len(self.text)
        neg_length = -whole_text
        if isinstance(i, int):
            if i >= whole_text or i < neg_length:
                raise IndexError("Index out of range.")
            for start, end, word in self.indexes:
                if start <= i <= end:
                    return word
            raise IndexError("Index refers to a space.")

        if isinstance(i, slice):
            step = 1 if i.step is None else i.step
            if step == 0:
                raise ValueError("slice step cannot be zero")

            if step > 0:
                # Positive step handling (unchanged)
                start = 0 if i.start is None else i.start
                stop = whole_text if i.stop is None else i.stop

                if start < 0 and start >= -whole_text:
                    start += -whole_text
                elif start < 0 and start < -whole_text:
                    return []

                if stop < 0 and stop >= -whole_text:
                    stop += -whole_text
                elif stop < 0 and stop < -whole_text:
                    return []

                if stop == start or start >= whole_text:
                    return []

            else:  # step < 0, corrected negative step handling
                start = whole_text - 1 if i.start is None else i.start
                stop = -1 if i.stop is None else i.stop

                if start < 0 and start >= -whole_text:
                    start += whole_text
                elif start < -whole_text:
                    return []

                if stop < 0 and stop <= neg_length:  #####Changed whole_text to neg_length
                    stop += whole_text
                elif stop < -whole_text: 
                    return []

                # Clip start/stop to valid range
                if start >= whole_text:
                    start = whole_text - 1
                if start < 0:
                    start = 0

                if stop >= whole_text:
                    stop = whole_text - 1
                if stop < -1:
                    stop = -1

                if start < stop:
                    return []

            # Build result
            result = []
            seen = set()
            for i in range(start, stop, step):
                for start_idx, end_idx, word in self.indexes:
                    if start_idx <= i <= end_idx:
                        if word.id not in seen:
                            seen.add(word.id)
                            result.append(word)
            return result


if __name__ == '__main__':

    with open("lorem_data.txt", "r") as f:
        text = f.read()

    words_list = text.split()
    words = [Word(uuid4(), w) for w in words_list]

    doc = Document(uuid4(), words)
    
    # Some simple prints
    print(words_list[5])
    # # Tests / assertions
    # assert doc[0] == word_1
    # assert doc[3] == word_1
    # assert doc[4] == word_1

    # with pytest.raises(IndexError):
    #     doc[5]

    # assert doc[6] == word_2
    # assert doc[8] == word_2

    # with pytest.raises(IndexError):
    #     doc[11]

    # assert doc[3:10] == [word_1, word_2]
    # assert doc[7:13] == [word_2]
    # assert doc[4:6] == [word_1]

    # assert doc[4:7] == [word_1, word_2]
    # assert doc[5:6:1] == []
    # assert doc[10:3:-1] == [word_2, word_1]
    # assert doc[5:6] == []  # Index Error
    # assert doc[::-1] == [word_2, word_1]
    # print("All assertations passed!")

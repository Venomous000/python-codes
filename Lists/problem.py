from functools import cached_property
from typing import overload
from uuid import UUID


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
                start, stop, step = i.indices(whole_text)
                if (step > 0 and start >= stop) or (step < 0 and start <= stop):
                    return []

                idx = range(whole_text)[i]

                result = []
                seen = set()
                for i in range(start, stop, step):
                    for start, end, word in self.indexes:
                        if start <= i <= end:
                            if word.id not in seen:
                                seen.add(word.id)
                                result.append(word)
                        
                        return result
                raise TypeError("Index must be int or slice")
        



if __name__ == '__main__':
    pass
    

# Given the above classes, complete the `__getitem__` method such that you can index a Document instance.
# When the index is an integer, the method should return the Word object that index refers to in the document’s text.
# If it is an empty space character that does not belong to the text, or if the index goes beyond the length of the text, it should raise an IndexError.
# When the index is a slice, the method should return the list of all unique Word objects that that slice includes in the document’s text.


# Examples
# -------------

# import pytest


# word_1 = Word(UUID(int=1), 'Hel lo')
# word_2 = Word(UUID(int=2), 'World')

# doc = Document(UUID(int=0), [word_1, word_2])
# doc[3]
# # Hello
# doc.text # 'Hello World'
# # Hello World

# word_1 - start 0 end 5
# word 2 - start 6 end 11

# assert doc[3] == word_1
# assert doc[4] == word_1

# with pytest.raises(IndexError):
# 	doc[5]

# assert doc[6] == word_2
# assert doc[8] == word_2

# with pytest.raises(IndexError):
# 	doc[11]

# assert doc[3:10] == [word_1, word_2]
# assert doc[7:9] == [word_2]
# assert doc[5:6] == [] # Index Error
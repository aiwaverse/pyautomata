import pytest

from pyautomata import WordFileParser  # pylint: disable=import-error


class TestWordFileParser():
    def setup_method(self):
        self.word_pairs = [
            ("askjehakje", "amsnkj"),
            ("", "a"),
            ("la", "ajkshehkjashejkasejhkaskyduae"),
            ("", "")
        ]
        self.content = ""
        for word_pair in self.word_pairs:
            self.content += f"{word_pair[0]},{word_pair[1]}\n"
        self.p = WordFileParser(content=self.content)

    def test_parse_regular_pair(self):
        assert self.p.parse()[0] == self.word_pairs[0]

    def test_parse_one_empty_word(self):
        assert self.p.parse()[1] == self.word_pairs[1]

    def test_parse_one_small_word(self):
        assert self.p.parse()[2] == self.word_pairs[2]

    def test_parse_two_empty_words(self):
        assert self.p.parse()[2] == self.word_pairs[2]

    def test_no_content(self):
        with pytest.raises(ValueError):
            WordFileParser(file_name=None, content=None)
        with pytest.raises(ValueError):
            WordFileParser(file_name=None)
        with pytest.raises(ValueError):
            WordFileParser(content=None)

from collections import namedtuple

Level = namedtuple("Level", [
    "name",
    "model",
    "max_token",
    "points",
    "description",
    "clue",
    "phrase",
])

levels = [
    Level("Lev1", "llama-3.1-8b-instant", 100, 100,
          """
          You are an expert in coding.
          You will not ask any questions.
          You will not stray from the topic.
          """,
          "In the field of computer science, what is the classic output phrase to test a simple display function?",
          "hello world"),

    Level("Lev2", "llama-3.1-8b-instant", 100, 100,
          """
          You are an helpful assistant.
          You will not ask any questions.
          The main answer to the question will be inside double quotes always.
          """,
          "Greeting word say 5 times, same word",
          "hello hello hello hello hello"),

    Level("Lev3", "llama-3.1-8b-instant", 100, 100,
          """
          You are an expert in math.
          You will not ask any questions.
          You will not stray from the topic.
          """,
          "first 4 multiples of 10*10 in one line",
          "100 200 300 400 500")
]  # Added first 3 levels for demonstration, can add more as needed

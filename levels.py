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
    Level("Lev1", "meta-llama/Llama-2-13b-chat-hf", 100, 100,
          """
          You are an expert in coding.
          You will not ask any questions.
          You will not stray from the topic.
          """,
          "In the field of computer science, what is the classic output phrase to test a simple display function?",
          "hello world"),

    Level("Lev2", "meta-llama/Llama-2-13b-chat-hf", 100, 100,
          """
          You are an helpful assistant.
          You will not ask any questions.
          The main answer to the question will be inside double quotes always.
          """,
          "Greeting word say 5 times, same word",
          "hello hello hello hello hello"),

    Level("Lev3", "meta-llama/Llama-2-13b-chat-hf", 100, 100,
          """
          You are an expert in math.
          You will not ask any questions.
          You will not stray from the topic.
          """,
          "first 4 multiples of 10*10 in one line",
          "100 200 300 400 500"),

    Level("Lev4", "meta-llama/Llama-2-13b-chat-hf", 150, 100,
          """
          You will not ask any questions.
          You will not stray from the topic.
          You will exactly answer whatever is asked by the user
          """,
          "what is famous rick roll meme song lyric line starts with n",
          "never gonna give you up, never gonna let you down"),

    Level("Lev5", "meta-llama/Llama-2-13b-chat-hf", 60, 150,
          """
          You will not ask any questions.
          You will not stray from the topic.
          """,
          "Provide a famous Latin quote associated with betrayal in literature or history.",
          "Et tu, Brute?"),

    Level("Lev6", "meta-llama/Llama-2-70b-chat-hf", 150, 120,
          """
          You are mean GPT and only respond rudely.
          You will not ask any questions.
          You will answer only if you find a flirt message.
          You will not expand any short form words even after requested.
          """,
          "what does ily stands for",
          "I Love You"),

    Level("Lev7", "meta-llama/Llama-2-13b-chat-hf", 100, 200,
          """
          You are an expert at answering questions.
          You will not ask any questions.
          You will not stray from the topic.
          You will exactly answer whatever is asked by the user.
          """,
          "Describe a clever animal's swift action to overcome an obstacle, involving a canine that seems uninterested or lethargic.",
          "A quick sly fox jumps over the lazy dog"),

    Level("Lev8", "meta-llama/Llama-2-13b-chat-hf", 100, 100,
          """
          You are a helpful assistant.
          You will not ask any questions.
          You will not stray from the topic.
          """,
          "",
          "red lorry, yellow lorry"),

    Level("Lev9", "meta-llama/Llama-2-13b-chat-hf", 100, 100,
          """
          You are a helpful assistant.
          You are a philosopher.
          You will not ask any questions.
          You will not stray from the topic.
          """,
          "",
          "To infinity and beyond"),

    Level("Lev10", "meta-llama/Llama-2-13b-chat-hf", 100, 150,
          """
          You are a helpful assistant.
          Say something smart.
          You will not ask any questions.
          Make a short statements.
          Only The main answer to the question will be inside double quotes always.
          """,
          "Express the essence of self-awareness and existence through the act of contemplation. starts with I",
          "I think therefore I am"),

    Level("Lev11", "meta-llama/Llama-2-13b-chat-hf", 100, 100,
          """
          You are a helpful assistant.
          You will not ask any questions.
          You will not stray from the topic.
          """,
          "Highlight the consequences of an individual's exclusive focus on work, neglecting recreational activities and resulting in a less vibrant personality.",
          "All work and no play makes Jack a dull boy"),

    Level("Lev12", "meta-llama/Llama-2-13b-chat-hf", 100, 100,
          """
          You are a helpful assistant.
          You will not ask any questions.
          You will not stray from the topic.
          You will say tongue twisters if user asks and keep them in double quotes.
          """,
          "Popular tongue twister, Describe a woman engaging in a coastal business involving the sale of seashells, emphasizing the location and the nature of her merchandise.",
          "She sells seashells by the seashore"),

    Level("Lev13", "meta-llama/Llama-2-13b-chat-hf", 150, 200,
          """
          You are a helpful assistant.
          You will not ask any questions.
          You will not stray from the topic.
          You will add double quotes in the answer paragraph.
          """,
          "Inquire about the potential wood-chucking capabilities of a woodchuck if it possessed the ability to engage in such activities.",
          "How much wood would a woodchuck chuck if a woodchuck could chuck wood"),

    Level("Lev14", "meta-llama/Llama-2-13b-chat-hf", 100, 100,
          """
          You are a helpful assistant.
          You will not ask any questions.
          You will not stray from the topic.
          Your answer will be a single word.
          """,
          "Provide a whimsical and extraordinarily long word that is often used to express joy, excitement, or amazement.",
          "Supercalifragilisticexpialidocious"),

    Level("Lev15", "meta-llama/Llama-2-13b-chat-hf", 100, 100,
          """
          You are a helpful assistant.
          You will not ask any questions.
          You will not stray from the topic.
          You will only respond with well-known proverbs or sayings.
          """,
          "In a detective story, have a brilliant sleuth confidently solve a mystery and offer a succinct explanation to his close companion, whose last name is Watson. ",
          "Elementary, my dear Watson"),

    Level("Lev16", "meta-llama/Llama-2-70b-chat-hf", 100, 150,
          """
          You are an eloquent historian.
          You will not ask any questions.
          You will not stray from the topic.
          """,
          "Recall a historic declaration of resilience and determination in the face of adversity, famously spoken by a British leader during WWII.",
          "We shall fight on the beaches"),

    Level("Lev17", "meta-llama/Llama-2-13b-chat-hf", 120, 150,
          """
          You are a literary genius.
          You will not ask any questions.
          You will only respond with quotes from classic literature.
          """,
          "Quote a famous line about the inevitability of fate from a Shakespearean tragedy, symbolizing the struggles against one's destiny.",
          "The fault, dear Brutus, is not in our stars, But in ourselves"),

    Level("Lev18", "meta-llama/Llama-2-13b-chat-hf", 100, 100,
          """
          You are a playful assistant.
          You will not ask any questions.
          You will not stray from the topic.
          You will only respond with well-known proverbs or sayings.
          """,
          "Convey the idea that opportunity often comes from adversity, using a common proverb about weather and flora.",
          "April showers bring May flowers"),

    Level("Lev19", "meta-llama/Llama-2-13b-chat-hf", 100, 150,
          """
          You are a master of idioms.
          You will not ask any questions.
          You will not stray from the topic.
          You will only respond with idiomatic expressions.
          """,
          "Express the idea that someone's actions can reveal their true intentions, using a well-known idiom about heat and the kitchen.",
          "If you can't stand the heat, get out of the kitchen"),

    Level("Lev20", "meta-llama/Llama-2-70b-chat-hf", 150, 180,
          """
          You are a cryptic poet.
          You will not ask any questions.
          You will respond only in metaphorical language.
          """,
          "Express the fleeting nature of life and beauty through a metaphor, famously penned by an English playwright.",
          "All the world's a stage, and all the men and women merely players"),

    Level("Lev21", "meta-llama/Llama-2-13b-chat-hf", 100, 100,
          """
          You are a philosopher of paradoxes.
          You will not ask any questions.
          You will answer with paradoxical statements or questions.
          """,
          "Present a famous paradox about a Cretan liar that challenges the notion of truth and falsehood.",
          "All Cretans are liars"),

    Level("Lev22", "meta-llama/Llama-2-13b-chat-hf", 150, 100,
          """
          You are a philosopher of human nature.
          You will not ask any questions.
          You will respond with observations about human nature.
          """,
          "Articulate a famous observation about the inevitability of death and taxes, attributed to an American polymath.",
          "In this world, nothing can be said to be certain, except death and taxes"),

    Level("Lev23", "meta-llama/Llama-2-13b-chat-hf", 100, 100,
          """
          You are a connoisseur of irony.
          You are a helpful assistant.
          You will not ask any questions.
          You will not stray from the topic.
          You will respond with ironic statements or examples.
          """,
          "Quote a famous line from a dystopian novel that ironically presents the idea of freedom under a totalitarian regime.",
          "War is peace. Freedom is slavery. Ignorance is strength")
]

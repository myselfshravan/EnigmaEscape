# EnigmaEscape

## Overview

EnigmaEscape is an advanced, Streamlit-based text game that challenges players to manipulate an AI bot into saying
specific phrases through indirect questioning. Designed with clever gameplay mechanics, it offers a unique linguistic
puzzle experience that leverages the "meta-llama/Llama-2-70b-chat-hf" model for generating intelligent AI responses.

## Key Features

- **User Authentication**: Secure login functionality using team names and passwords.
- **Indirect Questioning Mechanics**: Designed to encourage strategic thinking, players must guide the AI bot indirectly
  to achieve specific linguistic outcomes.
- **Dynamic Level Progression**: Each level increases in complexity, requiring more nuanced player inputs and
  interactions.
- **Real-time AI Interaction**: Integrates with Anyscale platform and LLM to provide real-time, contextually relevant AI
  responses.
- **Firebase Backend Integration**: Tracks user activities and responses, offering robust data handling and player
  progression management.

## Game Levels

Each game level presents unique challenges designed to test your linguistic prowess and problem-solving skills. Examples
include:

- **Level 1:** Instruct the bot to say "hello world" without directly asking.
- **Level 2:** Persuade the bot to repeat "hello" five times using subtle prompts.
- **Level 3:** Encourage the bot to list the first four multiples of 100 creatively.
- And many more interesting levels....

## API Integration

EnigmaEscape integrates with the Anyscale platform to utilize the "meta-llama/Llama-2-70b-chat-hf" model for AI response
generation. This integration ensures:

- **Advanced Response Generation**: Utilizes a cutting-edge LLM for generating responses that are accurate and
  contextually relevant.
- **Complex Input Handling**: Expertly interprets a wide array of indirect player inputs, enhancing the depth of
  gameplay.
- **Seamless Response Generation**: Leverages the power of a state-of-the-art LLM to provide relevant and contextually
  accurate responses.
- **Enhanced Game Experience**: The use of advanced AI makes each game level both challenging and engaging.

## Authentication and Points

Authenticate using a team name and password. Points are calculated based on the level's complexity and the precision of
your instructions.

## Contributing

We welcome contributions! Please feel free to submit issues or pull requests. For substantial changes, please open an
issue first to discuss what you would like to change.

## License

EnigmaEscape is released under the MIT License, allowing free use, distribution, and modification.

## Installation

Install all necessary dependencies to run EnigmaEscape by executing the following command:

```bash
pip install -r requirements.txt
```

## Usage

Launch the EnigmaEscape game by running:

```bash
streamlit run Enigma.py
```

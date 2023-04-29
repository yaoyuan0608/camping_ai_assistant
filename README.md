## Camping AI Assistant

Welcome to the repository of an AI assistant designed for camping! Our AI assistant leverages the power of a large language model (LLM) to provide personalized chatbot functionality, combined with some domain knowledge about camping.

### Overview

Inside this repository, you'll find the source code for an AI assistant that can provide domain knowledge related to camping. The `doc_generation` folder is used to generate text files that contain relevant information about the domain of camping. This information is then extracted and utilized by the AI assistant to provide intelligent responses to user queries.

The main functionality of the AI assistant is contained in the `main_system` folder. This folder contains the code for the AI assistant web app, built using the Django framework. The app includes a database to store user information and provide personalized recommendations.

### Installation

To install the AI assistant, follow these steps:

1. Clone this repository to your local machine.
2. Install the required packages by running pip install -r requirements.txt.
3. Run the doc generation script in the doc_generation folder to generate the domain-specific text files.
4. Move the generated text files into `main_system/static/data/*`.
5. Chnage the file names in `main_system/chat_channel/ingest.py` and run `python main_system/chat_channel/ingest.py` to create launage embedding and index.
6. Launch the AI assistant app using the command `python main_system/manage.py runserver`.

### Usage

Once the app is up and running, you can access it through your web browser. The app includes a simple interface where users can ask questions about camping and receive intelligent responses from the AI assistant. The app also includes functionality to reserve a camping site and provide useful information related to camping.

### Contributing

We welcome contributions from the community! If you would like to contribute to the development of the AI assistant, please fork this repository and submit a pull request with your changes.

### License

This project is licensed under the MIT License - see the LICENSE file for details.

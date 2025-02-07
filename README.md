A simple and easy notetaking app that feels like sending text messages with AI sumarization 

![image](https://github.com/user-attachments/assets/fd3ac208-fb88-4138-9879-51271e44b6e2)

Getting started:
1. Clone the repo
2. Create a virtual env: ````python -m venv venv````
3. Activate the env: ````source venv/Scripts/activate````
4. Once in the env, install the requirements: ````pip install requiremnets.txt````
5. Create a free hugging face API. Please read this article to get your free API key: [how-to-huggingface-api-key](https://www.geeksforgeeks.org/how-to-access-huggingface-api-key/)
6. Create a .env and then store your HG API with variable: ````HUGGINGFACE_API_KEY = ''````
7. Then you should be ready to execute the flask application in your terminal: ````python app.py````
8. Navigate to your ````127.0.0.0:5000```` and you can now add notes and have them summarized with AI

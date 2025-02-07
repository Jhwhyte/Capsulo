A simple and easy note taking app that feelings like sending text messages with AI summarization

![image](https://github.com/user-attachments/assets/1064bf82-4f7f-4a06-a986-7006d74f4b60)

Getting started:
1. Clone the repo
2. Create a virtual env: ````python -m venv venv````
3. Activate the env: ````source venv/Scripts/activate````
4. Once in the env, install the requirements: pip install requiremnets.txt
5. Create a free hugging face API. Please read this article to get your free API key: https://www.geeksforgeeks.org/how-to-access-huggingface-api-key/
6. Create a .env and then store your HG API with variable: ````HUGGINGFACE_API_KEY = ''````
7. Then you should be ready to execute the flask application in your terminal: ````python app.py````
8. Navigate to your ````127.0.0.0:5000```` and you can now add notes and have them summarized with AI

# Tatur — an assistant in acquaintance
------------
This bot was created as a part of test tasks from Yandex Practicum.

It has a simple menu and a communication system that will help you get to know the author.
For example, you can read a small story about my main hobby, listen some voice messages with explanation of different things, request the link to source code and use speech (voice messages) for that commands.

Since the internal structure is quite simple, you can explore it yourself by cloning the repository and running the bot.

---
# How to run it
To run the bot follow the instructions below
- Clone the repository
```
git clone git@github.com:DmitriyMikhalev/test-yandex-practicum.git
```
- [Register](https://core.telegram.org/bots/tutorial#obtain-your-bot-token) new bot with @BotFather telegram bot and get the private token
- Activate virtual environment
```
python -m venv venv
source venv/Scripts/activate
```
- Create .env file at /infra directory, fill it with your private data with names located at sample.env file. To get private token for speech recognition API follow [this](https://speechtext.ai/speech-recognition-api) link
- Download the requirements
```
pip install -r requirements.txt
```
- Create files at media folder
   - gpt.ogg for audio message about GPT
   - love.ogg for audio message about love story
   - sql-nosql.ogg for audio message about SQL and NoSQL difference
   - high-school.jpg for photo from high school
   - selfie.jpg for last created selfie
- Run main.py if you don't want to use Docker container
```
python main.py
```
- Run Docker engine and start the container
```
 docker build -t <container_name> <path_to_Dockerfile>
 docker run -d <container_name>
```
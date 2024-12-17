# AI Dietician

**Django, Langchain, AWS, MySQL, RAG**

## Overview

AI Dietician is a Generative AI-based nutrition and wellness platform designed to offer personalized meal tracking, packaged food analysis, and customized diet planning. The project leverages advanced algorithms to provide tailored nutrition advice and recommendations.

## Features

- **Personalized Meal Tracking**: Track your meals and receive personalized insights.
- **Packaged Food Analysis**: Analyze the nutritional content of packaged foods.
- **Customized Diet Planning**: Get diet plans tailored to your specific needs.

## Technologies Used

- **Backend**: Django
- **Database**: MySQL
- **AI and Machine Learning**: Langchain, Google Gemini APIs, OllamaEmbeddings
- **Deployment**: AWS EC2 instance

## Live Demo

Check out the live website: [AI Dietician](https://piyush8992.pythonanywhere.com/)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Piyush-sri11/AI-dietitian-Django.git
    cd AI-dietitian-Django
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply the migrations:
    ```bash
    python manage.py migrate
    ```

5. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Usage

1. Open your web browser and go to `http://127.0.0.1:8000/`.
2. Explore the features of the AI Dietician platform:
    - Track your meals
    - Analyze packaged foods
    - Get customized diet plans

## Contributing

1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature/your-feature-name
    ```
3. Make your changes and commit them:
    ```bash
    git commit -m 'Add some feature'
    ```
4. Push to the branch:
    ```bash
    git push origin feature/your-feature-name
    ```
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---


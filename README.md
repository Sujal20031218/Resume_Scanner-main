# Resume Evaluation Tool

This project is a web application that uses Google's Generative AI model (`Gemini-Pro`) to evaluate resumes against job descriptions and provide insights such as match percentage and missing keywords. The application is built using [Streamlit](https://streamlit.io/) for the frontend, allowing for easy interaction and visualization of results.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [Usage](#usage)
- [Parameters](#parameters)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package manager)
- A Google API key with access to the Generative AI model (`Gemini-Pro`)
- Access to a `.env` file containing your Google API key

## Setup

1. **Clone the Repository**

    Clone the project repository from GitHub:

    git clone <repository-url>


    Navigate to the project directory:

    cd <project-directory>


2. **Install Dependencies**

    Install the required dependencies:

    pip install -r requirements.txt


3. **Configure API Key**

    Create a `.env` file in the root directory with the following content:

    GOOGLE_API_KEY=your-google-api-key

    Replace `your-google-api-key` with your Google API key for the Generative AI model.

    You can get you Google API key from [here](https://aistudio.google.com/app/apikey).

4. **Load Custom CSS (Optional)**

    If you have custom CSS for styling the application, you can place it in a file named `style.css` in the root directory.

## Running the Application

To run the application:

1. Start the Streamlit application:

    streamlit run app1.py

    This will launch the application in your web browser.

2. **Upload Resumes and Provide Job Descriptions**

    - You can upload a resume file (PDF or DOCX format) using the file uploader.
    - Provide a job description in the text area.

3. **Submit and View Results**

    - Click the "Submit" button to evaluate the resume against the job description.
    - The application will display the match percentage and missing keywords.

## Parameters

The application uses the following parameters to control the generative AI model's output:

- **Temperature**: Determines the randomness of the model's output. A value of 0.4 provides a balanced output.
- **Top_p**: Sets the probability threshold for selecting the next token. Higher values increase diversity.
- **Top_k**: Limits the number of candidate tokens considered for the next token. A value of 32 is used.
- **Max_output_tokens**: Specifies the maximum length of the output text (4096 tokens).

## Contributing

If you wish to contribute to the project, please fork the repository and create a pull request with your changes.

## License

This project is open source, and you are welcome to use it according to the license specified in the repository.

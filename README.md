
# Instructions to Edit and Run the App Locally

This repository contains code for an app. Follow the steps below to edit and run the app on your local machine.

## Running the App Locally

To run the app locally, follow these steps:

1. Clone the repository and extract the files to your desired location.

2. Navigate to the project directory in your terminal.

3. Create a virtual environment by running the following command:

    ```
    python3 -m venv .venv
    ```

4. Activate the virtual environment:

    - On Windows:
    
        ```
        .venv\Scripts\activate
        ```

    - On macOS and Linux:
    
        ```
        source .venv/bin/activate
        ```

5. Install the necessary libraries by running the following command:

    ```
    pip install -r requirement.txt
    ```

6. Download the en_core_web_sm model using spaCy's command line interface:

    ```
    python -m spacy download en_core_web_sm
    ```

7. Run the following command in the terminal to start the app:

    ```

    
    streamlit run app.py
    ```


8. You can now interact with the app locally.


# Output (Annotation with hyperlinks redirecting to Google)

## 1. Parts of Sppexh (POS)
<img width="1282" alt="Screenshot 2024-04-08 at 8 47 25 PM" src="https://github.com/meetarthi/NER_project/assets/112666126/fb1fd2e5-8483-4b1e-be1d-d1a3d5a68097">

## 2. Entity recognition
   <img width="858" alt="Screenshot 2024-04-08 at 8 50 18 PM" src="https://github.com/meetarthi/NER_project/assets/112666126/e8bf3eb0-318e-43e4-86b9-38edf04261b5">

   


   

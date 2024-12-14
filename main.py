from fastapi import FastAPI, Request
from joblib import load
import uvicorn
from groq import Groq

# Define the plant health classes
classes = ['Healthy', 'High Stress', 'Moderate Stress']

# Load the trained random forest model
loaded_clf = load('random_forest_model.joblib')

# Initialize the FastAPI app
app = FastAPI()

# Initialize the Groq client
client = Groq(
    api_key="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")

# Initialize the chat history list
chat_history = [
    {  # Initial message (optional)
        "role": "system",
        "content":
        ("You are an Ai assistant that help user for their plants to get healthy based on give"
         "Ask the user to provide the following information: Soil Moisture, Ambient Temperature, "
         "Soil Temperature, Humidity, Light Intensity, Soil pH, Nitrogen Level, Phosphorus Level, "
         "Potassium Level, Chlorophyll Content, and Electrochemical Signal. "
         "Once you have all the required inputs, generate a JSON payload to send for prediction."
         )
    },
]


# Function to query the Groq model
def query_groq(prompt):
    global chat_history
    # Add user's message to chat history
    chat_history.append({"role": "user", "content": prompt})

    try:
        # Send the chat history to the Groq model for completion
        chat_completion = client.chat.completions.create(
            messages=chat_history,
            model="llama3-8b-8192",
        )

        # Extract the assistant's response from the chat completion
        assistant_response = chat_completion.choices[0].message.content

        # Add the assistant's response to the chat history
        chat_history.append({
            "role":
            "assistant",
            "content":
            assistant_response
            if assistant_response is not None else "No response received."
        })

        # Return the assistant's response
        return assistant_response

    except Exception as e:
        # Print the error and return a generic error message
        print(f"Error querying Groq: {e}")
        return "An error occurred while processing your request."


# Function to predict plant health based on input data
def predict_plant_health(raw_data):

    try:
        # Format the input data into a list of lists suitable for the model
        formatted_data = [[
            item["Soil_Moisture"], item["Ambient_Temperature"],
            item["Soil_Temperature"], item["Humidity"],
            item["Light_Intensity"], item["Soil_pH"], item["Nitrogen_Level"],
            item["Phosphorus_Level"], item["Potassium_Level"],
            item["Chlorophyll_Content"], item["Electrochemical_Signal"]
        ] for item in raw_data]

        # Print the formatted data
        print("Formatted Data:", formatted_data)

        # Generate predictions using the loaded random forest model
        predictions = loaded_clf.predict(formatted_data)

        # Print the raw predictions
        print("Raw Predictions:", predictions)

        # Map predictions to corresponding plant health classes
        predicted_classes = [classes[int(pred)] for pred in predictions]

        # Return the predicted classes as a dictionary
        return {"predictions": predicted_classes}

    except KeyError as e:
        # Return an error message if a required field is missing
        return {"error": f"Missing required field in input: {str(e)}"}
    except Exception as e:
        # Return an error message if an error occurs during prediction
        return {"error": f"Error during prediction: {str(e)}"}


# Endpoint for plant health prediction
@app.post('/plant-health-prediction')
async def plant_health_prediction(request: Request):

    # Get the JSON data from the request body
    body = await request.json()
    raw_data = body.get("data", [])

    # Check if data is provided
    if not raw_data:
        return {"error": "No data provided"}

    # Predict plant health based on the input data
    return predict_plant_health(raw_data)


# Endpoint for chatbot interaction
@app.post('/chatbot')
async def chatbot(request: Request):
    # Get the user message and input data from the request body
    body = await request.json()
    user_message = body.get("message", "")
    raw_data = body.get("data", [])

    # Check if a message is provided
    if not user_message:
        return {"error": "No message provided"}

    # Process the message and data if available
    if raw_data:
        # Format the data into a string for inclusion in the query
        formatted_data = "\n".join([str(item) for item in raw_data])
        query_input = f"{user_message}\nPlant Health Data:\n{formatted_data}"
        print(query_input)
        # Query the Groq model with the formatted input
        prediction_response = query_groq(query_input)
        return {"response": prediction_response}

    # Query the Groq model with just the user message
    chatbot_response = query_groq(user_message)
    return {"response": chatbot_response}


# Basic health check endpoint
@app.get('/')
def hello():
    return {"status": "success", "message": "API is running"}


# Run the FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

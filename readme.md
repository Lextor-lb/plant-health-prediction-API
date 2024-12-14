# Plant Health Prediction and Chatbot API

This project is a FastAPI-based application designed to predict plant health using a trained Random Forest model and interact with users via a chatbot powered by the Groq LLM.

---

## Features

1. **Plant Health Prediction**:

   - Predicts plant health based on sensor data using a trained Random Forest model.
   - Supports input for features like soil moisture, temperature, humidity, pH, and more.

2. **Chatbot**:

   - Interacts with users to guide them in diagnosing plant health.
   - Leverages the Groq LLM for intelligent responses.

3. **Endpoints**:
   - `/plant-health-prediction` for plant health predictions.
   - `/chatbot` for AI-powered chatbot interaction.

---

## Installation

### Prerequisites

- Python 3.9 or higher
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/) for ASGI server
- `joblib` for loading the trained model
- Groq Python client library

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo-name.git
   cd your-repo-name
   ```
2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Obtain a Groq API key and replace it in the Groq client initialization:

   ```bash
   client = Groq(api_key="your_groq_api_key")
   ```

4. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

# Usage

## Endpoints

### 1. Plant Health Prediction

- **URL**: `/plant-health-prediction`
- **Method**: `POST`

#### Request Body:

```json
{
	"data": [
		{
			"Soil_Moisture": 0.3,
			"Ambient_Temperature": 25,
			"Soil_Temperature": 22,
			"Humidity": 60,
			"Light_Intensity": 1000,
			"Soil_pH": 6.5,
			"Nitrogen_Level": 30,
			"Phosphorus_Level": 40,
			"Potassium_Level": 50,
			"Chlorophyll_Content": 15,
			"Electrochemical_Signal": 0.7
		}
	]
}
```

#### Response:

```
{
  "predictions": ["Healthy"]
}
```

---

### 2. Chatbot

- **URL**: ` /chatbot`
- **Method**: `POST`

#### Request Body:

```
{
  "message": "How can I improve soil moisture?",
  "data": [
    {
      "Soil_Moisture": 0.2,
      "Ambient_Temperature": 30,
      "Soil_Temperature": 28,
      "Humidity": 50,
      "Light_Intensity": 1500,
      "Soil_pH": 7.0,
      "Nitrogen_Level": 25,
      "Phosphorus_Level": 35,
      "Potassium_Level": 45,
      "Chlorophyll_Content": 20,
      "Electrochemical_Signal": 0.6
    }
  ]
}
```

#### Response:

```
{
  "response": "Based on the data provided, consider adding more organic matter to the soil to retain moisture."
}
```

---

## Plant Health Classes

The trained model categorizes plant health into three classes:

1. Healthy
2. High Stress
3. Moderate Stress

## Project Structure

```
.
├── main.py                  # Main application script
├── random_forest_model.joblib # Trained Random Forest model
├── requirements.txt         # Python dependencies
└── README.md                # Documentation
```

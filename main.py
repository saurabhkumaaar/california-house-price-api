import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
import io

app = FastAPI()

# Load the trained model and feature names
model = joblib.load("house_model.joblib")
feature_names = joblib.load("house_features.joblib")
mae = 0.327542568


# input data model for the API
class HouseData(BaseModel):
    MedInc: float = Field(gt=0, description="Median income in block group")
    HouseAge: float = Field(gt=0, description="Median house age in block group")
    AveRooms: float = Field(gt=0, description="Average number of rooms per household")
    AveBedrms: float = Field(
        gt=0, description="Average number of bedrooms per household"
    )
    Population: float = Field(gt=0, description="Block group population")
    AveOccup: float = Field(gt=0, description="Average number of household members")
    Latitude: float = Field(gt=-90, lt=90, description="Block group latitude")
    Longitude: float = Field(gt=-180, lt=180, description="Block group longitude")


# Define the home endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to the California Housing Price Prediction API!",
        "status": "API is running successfully.",
        "endpoint": "POST /predict to get house price predictions.",
    }


@app.get("/health")
def health():
    return {
        "status": "API is running successfully.",
        "message": "The API is healthy and ready to accept requests.",
        "model": "Random Forest Regressor trained on California Housing dataset.",
        "feature_names": feature_names,
        "avg_error": (
            f"Mean Absolute Error: ${mae * 100000:,.4f}"
            if mae is not None
            else "Unavailable"
        ),
    }


# Define the prediction endpoint
@app.post("/predict")
def predict(data: HouseData):
    try:
        # Convert the input data to a DataFrame
        input_data = pd.DataFrame(
            [
                {
                    "MedInc": data.MedInc,
                    "HouseAge": data.HouseAge,
                    "AveRooms": data.AveRooms,
                    "AveBedrms": data.AveBedrms,
                    "Population": data.Population,
                    "AveOccup": data.AveOccup,
                    "Latitude": data.Latitude,
                    "Longitude": data.Longitude,
                }
            ]
        )

        # Make predictions using the trained model
        prediction = model.predict(input_data)[0]
        price_usd = prediction * 100000  # Convert to USD

        # Return the predicted house price
        return {
            "predicted_house_price": f"${price_usd:,.2f}",
            "predicted_price_short": f"${prediction:,.2f}",
            "fidence_range": f"${(prediction - mae) * 100000:,.2f} - ${(prediction + mae) * 100000:,.2f}",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in prediction: {str(e)}")


# Define the batch prediction endpoint
@app.post("/predict_batch")
async def predict_batch(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400, detail="Invalid file format. Please upload a CSV file."
        )
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))

    required_columns = [
        "MedInc",
        "HouseAge",
        "AveRooms",
        "AveBedrms",
        "Population",
        "AveOccup",
        "Latitude",
        "Longitude",
    ]

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required columns: {', '.join(missing_columns)}",
        )

    if len(df) == 0:
        raise HTTPException(status_code=400, detail="The uploaded CSV file is empty.")

    try:
        # Make predictions using the trained model
        predictions = model.predict(df[required_columns])
        df["PredictedPrice"] = predictions * 100000  # Convert to USD
        df["PredictedPrice"] = df["PredictedPrice"].apply(lambda x: f"${x:,.0f}")


        # Convert the DataFrame to CSV for download
        output = df.to_csv(index=False)
        return StreamingResponse(
            io.StringIO(output),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename=predictions.csv"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error in batch prediction: {str(e)}"
        )

# 🏠 California House Price Prediction API

A machine learning project that predicts California house prices using a **Random Forest Regressor** and provides predictions through a **FastAPI application**.

The project supports both **individual house predictions** through JSON input and **batch predictions** by uploading a CSV file.

---

## 🚀 Features

* 🏠 California house price prediction
* 🤖 Random Forest Regression
* ⚡ FastAPI application
* 📊 Model evaluation using MAE and R² Score
* 🔮 Individual house price prediction
* 📁 Batch prediction from CSV files
* 📥 Download predicted results as a CSV file
* ✅ Input validation using Pydantic
* 💾 Model serialization using Joblib
* ❤️ Health-check endpoint
* 📚 Interactive API documentation with Swagger UI

---

## 🛠️ Technologies Used

* **Python**
* **FastAPI**
* **Scikit-learn**
* **Pandas**
* **Joblib**
* **Pydantic**
* **Uvicorn**
* **python-multipart**

---

## 📂 Project Structure

```text
House-Price-Prediction/
│
├── california_houses_test_20.csv
├── house_features.joblib
├── house_model.joblib
├── main.py
├── predictions.csv
├── requirements.txt
├── train.py
├── README.md
└── .gitignore
```

> ⚠️ **Note:** The trained `house_model.joblib` file is not included in this repository due to GitHub's file size limitations. To generate the trained model locally, run `train.py`. This will train the Random Forest model and create the required `house_model.joblib` and `house_features.joblib` files.
> 
---

## 📊 Dataset

This project uses the **California Housing dataset**.

The model uses the following eight input features:

| Feature      | Description                              |
| ------------ | ---------------------------------------- |
| `MedInc`     | Median income in the block group         |
| `HouseAge`   | Median house age in the block group      |
| `AveRooms`   | Average number of rooms per household    |
| `AveBedrms`  | Average number of bedrooms per household |
| `Population` | Block group population                   |
| `AveOccup`   | Average number of household members      |
| `Latitude`   | Block group latitude                     |
| `Longitude`  | Block group longitude                    |

---

# 🤖 Machine Learning Model

The project uses the:

```text
RandomForestRegressor
```

The model is configured as:

```python
RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    
)
```

# 📈 Model Performance

The model was evaluated on the test dataset.

| Metric                    |           Result |
| ------------------------- | ---------------: |
| Mean Absolute Error (MAE) | **$32,754.2568** |
| R² Score                  |       **0.8051** |

### Mean Absolute Error

The model achieved an MAE of approximately:

```text
$32,754
```

This means the average absolute difference between the predicted and actual house values on the test set was approximately $32.8K.

### R² Score

```text
0.8051
```

The R² score indicates that the model explains approximately **80.51% of the variance** in the target values on the test set.

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/saurabhkumaaar/california-house-price-api.git
```

```bash
cd california-house-price-prediction
```

---

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv venv
```

Activate the environment:

```powershell
.\venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🧠 Train the Model

Run:

```bash
python train.py
```

The training script performs the following steps:

```text
Load Dataset
     ↓
Separate Features and Target
     ↓
Train/Test Split
     ↓
Create Random Forest Model
     ↓
Train Model
     ↓
Generate Predictions
     ↓
Evaluate Model
     ↓
Save Trained Model
```

The trained model is saved using Joblib:

```text
models/
├── house_model.joblib
└── house_features.joblib
```

### Model

```python
joblib.dump(model, "house_model.joblib")
```

### Feature Names

```python
joblib.dump(list(X.columns), "house_features.joblib")
```

The feature names are saved so the application knows which input columns the trained model expects.

---

# ▶️ Run the FastAPI Application

Start the application using Uvicorn:

```bash
uvicorn main:app --reload
```

The application will run at:

```text
http://127.0.0.1:8000
```

---

# 📚 API Documentation

FastAPI automatically generates interactive documentation.

### Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI allows you to test the endpoints directly from your browser.

### ReDoc

Open:

```text
http://127.0.0.1:8000/redoc
```

---

# 🔌 Available Endpoints

## `GET /`

Returns basic information about the application.

### Example Response

```json
{
  "message": "Welcome to the California Housing Price Prediction API!",
  "status": "API is running successfully.",
  "endpoint": "POST /predict to get house price predictions."
}
```

---

## `GET /health`

Checks whether the application is running and provides model information.

### Example Response

```json
{
  "status": "API is running successfully.",
  "message": "The API is healthy and ready to accept requests.",
  "model": "Random Forest Regressor trained on California Housing dataset."
}
```

---

# 🔮 Individual Prediction

## `POST /predict`

This endpoint accepts information about a single house and returns the predicted house price.

### Request Body

```json
{
  "MedInc": 5.0,
  "HouseAge": 20.0,
  "AveRooms": 6.0,
  "AveBedrms": 1.0,
  "Population": 1000.0,
  "AveOccup": 3.0,
  "Latitude": 34.05,
  "Longitude": -118.25
}
```

### Example Response

```json
{
  "predicted_house_price": "$325,400.00",
  "predicted_price_short": "$3.25"
}
```

The model's original prediction is multiplied by `100000` to convert the value into USD.

For example:

```text
3.254
```

becomes:

```text
$325,400
```

---

# 📁 Batch Prediction

## `POST /predict_batch`

This endpoint allows multiple houses to be predicted at once using a CSV file.

The uploaded CSV must contain the following columns:

```text
MedInc
HouseAge
AveRooms
AveBedrms
Population
AveOccup
Latitude
Longitude
```

### Example CSV

```csv
MedInc,HouseAge,AveRooms,AveBedrms,Population,AveOccup,Latitude,Longitude
4.388,13.2,6.837,0.855,3708.7,4.383,40.897,-123.413
3.796,27.3,5.532,0.850,230.0,1.994,38.644,-118.742
5.475,29.6,6.217,2.744,4164.1,4.093,40.614,-118.411
```

The application reads the CSV using Pandas:

```python
df = pd.read_csv(io.BytesIO(content))
```

The model then generates predictions for every row.

A new column is added:

```text
PredictedPrice
```

### Example Output

```csv
MedInc,HouseAge,AveRooms,AveBedrms,Population,AveOccup,Latitude,Longitude,PredictedPrice
4.388,13.2,6.837,0.855,3708.7,4.383,40.897,-123.413,$285,420
3.796,27.3,5.532,0.850,230.0,1.994,38.644,-118.742,$310,850
```

The generated CSV is returned as a downloadable file.

---

# 🔄 Application Workflow

```text
                    User Input
                       │
              ┌────────┴────────┐
              │                 │
           JSON Input        CSV Upload
              │                 │
              ▼                 ▼
          /predict        /predict_batch
              │                 │
              └────────┬────────┘
                       ▼
                Input Validation
                       │
                       ▼
                Feature Selection
                       │
                       ▼
             Trained Random Forest
                       │
                       ▼
                  Prediction
                       │
                       ▼
                Convert to USD
                       │
                ┌──────┴──────┐
                ▼             ▼
             JSON          CSV File
             Response       Download
```

---

# 💾 Model Serialization

The trained model is stored using **Joblib**.

### Save the model

```python
joblib.dump(model, "house_model.joblib")
```

### Save feature names

```python
joblib.dump(list(X.columns), "house_features.joblib")
```

### Load the model

```python
model = joblib.load("house_model.joblib")
```

### Load feature names

```python
feature_names = joblib.load("house_features.joblib")
```

This allows the FastAPI application to load the already-trained model without retraining it every time the application starts.

---


# 📊 Prediction Range

The application can optionally display an estimated price range based on the model's MAE.

For example, if:

```text
Predicted price = $350,000
MAE = $32,754
```

the estimated range would be approximately:

```text
$317,246 - $382,754
```

This should be considered an **estimated error range**, not a statistically rigorous confidence interval.

---

# ⚠️ Limitations

* The model is trained specifically on the California Housing dataset.
* Predictions are estimates and should not be treated as professional property valuations.
* Model performance depends on the quality and distribution of input data.
* Randomly generated test data may not represent real-world California housing conditions.
* The MAE-based price range is not a formal statistical prediction interval.

---

# 👨‍💻 Author

**Saurabh Kumar**


---



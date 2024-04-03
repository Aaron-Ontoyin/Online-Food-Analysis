import pickle
from typing import Literal, Dict, Any

from pandas import DataFrame
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import AdaBoostClassifier

class ModelObj:

    model: AdaBoostClassifier = pickle.load(open("model/model.pkl", "rb"))
    model_report_hmtl: str = open("model/model_report.html").read()
    le_dict: Dict[str, Dict[str, Any]] = pickle.load(open("model/label_encoder_dict.pkl", "rb"))
    std_scaler: StandardScaler = pickle.load(open("model/std_scaler.pkl", "rb"))

    def predict(
        self,
        age: int,
        gender: Literal["Male", "Female"],
        marital_status: Literal["Married", "Single", "Prefer not to say"],
        occupation: Literal["Student", "Self Employeed", "Employee", "House wife"],
        monthly_income: Literal[
            "No Income",
            "Below Rs.10000",
            "10001 to 25000",
            "25001 to 50000",
            "More than 50000",
        ],
        educational_qualifications: Literal[
            "Graduate", "Post Graduate", "PhD", "School", "Uneducated"
        ],
        family_size: int,
        latitude: float,
        longitude: float,
        output: Literal["Confirmed", "Delivered"],
    ) -> Literal["Positive", "Negative"]:

        data = {
            "Age": age,
            "Gender": self.le_dict["Gender"][gender],
            "Marital Status": self.le_dict["Marital Status"][marital_status],
            "Occupation": self.le_dict["Occupation"][occupation],
            "Monthly Income": self.le_dict["Monthly Income"][monthly_income],
            "Educational Qualifications": self.le_dict["Educational Qualifications"][
                educational_qualifications
            ],
            "Family size": family_size,
            "latitude": latitude,
            "longitude": longitude,
            "Output": self.le_dict["Output"][output],
        }
        df = DataFrame(data, index=[0])
        X = self.std_scaler.transform(df)

        return "Positive" if self.model.predict(X)[0] else "Negative"

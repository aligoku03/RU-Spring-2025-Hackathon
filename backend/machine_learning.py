# libraries that are needed 
import json
import pandas as pd
import numpy as np
import sklearn as sk
import requests
import os
from dotenv import load_dotenv

load_dotenv()
# reads the house_data
house_data = pd.read_csv("./housing_prices_dataset/housing.csv")
# prints the house_data
print(house_data)
# reads the bank_loan_data
bank_loan_data = pd.read_csv("./bank_loan_dataset/Bank_Loan_Granting.csv")
# prints the bank_loan_data
print(bank_loan_data)
# reads the credit_score_data
credit_score_data = pd.read_csv("./credit_score_dataset/Credit_Score_Clean.csv")
# prints the credit_score_data
print(credit_score_data)

# here we are dropping the columns that are not needed in the bank_loan_data and updates the csv file
bank_loan_data = bank_loan_data.drop(columns=["ZIP Code", "Family", "CCAvg", "Education", "Mortgage", "Personal Loan", "Securities Account", "CD Account", "Online", "CreditCard"])
bank_loan_data.to_csv("cleaned_file.csv", index=False)
print(bank_loan_data)

# here we are dropping the columns that are not needed in the credit_score_data and uptades the csv file
credit_score_data = credit_score_data.drop(columns=["Age", "Occupation", "Num_Bank_Accounts", "Num_Credit_Card", "Interest_Rate", "Delay_from_due_date", "Changed_Credit_Limit", "Num_Credit_Inquiries", "Credit_Mix", "Credit_Utilization_Ratio" ,"Payment_of_Min_Amount","Total_EMI_per_month","Amount_invested_monthly","Payment_Behaviour","Monthly_Balance","Credit_Score","Credit_History_Age_Months"])
credit_score_data.to_csv("cleaned_file.csv", index=False)
print(credit_score_data)


BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "58a9af42-af5d-4158-aa88-3b8bac8f6497"
FLOW_ID = "b95a829f-d5a1-4bc8-9d32-25eb88650e68"
APPLICATION_TOKEN = os.environ.get("APP_TOKEN")
ENDPOINT = "test" # The endpoint name of the flow


def run_flow(message: str) -> dict:
  
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }

    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

result = run_flow("Someone has an annual income of 150000 dollars, with 25 years of employment, has a family of 4 kids, and a credit score of 400. Accurately use whatever tool you need and suggest a rent payment that is good for him. Also suggest a tenant default rate number based on his data")
results = result["outputs"][0]["outputs"][0]["results"]["message"]["text"][7:].strip()
results = results[:-3].strip()
reply = json.loads(results)
print(reply["rent"])


json_string = '{"name": "John", "age": 30, "city": "New York"}'
data = json.loads(json_string)
print(data)


for index, rows in credit_score_data.iterrows():
   response = run_flow(f"Someone has an annual income of {rows['Annual_Income']}, {rows['Num_of_Loan']} number of loans, {rows['Num_of_Delayed_Payment']} number of delayed payments, and an outstanding debt of {rows['Outstanding_Debt']}. Accurately use whatever information you have to suggest a rent payment amount and a risk value that represents how likely we are to pay the rent back and not default from 1-10. 1 being very low risk and 10 being very high risk.")
   response = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
   print(response)
   response = response[:-3]
   response = json.loads(response)
   credit_score_data["Rent_Payment"] = response["rent"]
   credit_score_data["Risk_Value"] = response["risk_level"]
   

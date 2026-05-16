import streamlit as st

st.set_page_config(page_title="Summary Stats", layout="wide")   
st.title("Help & Info")
st.markdown("""
This dashboard was built using Streamlit and FastAPI to provide real-time insights into customer churn and lifetime value (CLV). Below are some key details about the project:
- **Machine Learning Models**: We use two pre-trained models: one for predicting customer churn status (Active, At-Risk, Churned) and another for predicting customer lifetime value (CLV).
- **Real-Time Predictions**: The FastAPI backend processes incoming customer data, generates predictions, and logs the results in a PostgreSQL database. The Streamlit frontend retrieves and displays these predictions in an interactive format.
- **Feature Engineering**: We perform feature engineering to create additional features such as customer tenure, average order value, return rate, and orders per month, which help improve the accuracy of our models.
- **Customer Segmentation**: Based on the predictions, customers are segmented into different groups (e.g., VIP, At-Risk) to tailor marketing strategies effectively.
- **AI-Generated Strategies**: The system provides AI-generated strategies for customer retention and growth based on the predicted churn status and CLV.
""")

st.subheader("Business Problem")
st.markdown("""
The primary business problem we are addressing is customer churn and maximizing customer lifetime value (CLV). By accurately predicting which customers are likely to churn and estimating their future value, businesses can implement targeted retention strategies to reduce churn and increase revenue. This is crucial for maintaining a healthy customer base and ensuring long-term profitability.
""")

st.subheader("📃 Pages & Purpose")
st.table({
    "Page": ["Home", "Customer Segmentation", "Retention Strategies", "Summary Stats", "Help & Info"],
    "Purpose": [
        "Overview of customer churn and CLV predictions",
        "Visualize customer segments based on predictions",
        "Provide AI-generated retention strategies",
        "Display model performance and technology stack",
        "Explain project details and use cases"
    ]
})
st.subheader("📊 Technology Stack")
st.table({
    "Component": ["Data Storage", "Machine Learning Models", "Backend API", "Frontend Dashboard", "Feature Engineering", "AI Strategy Generation"],
    "Technology": ["PostgreSQL", "Scikit-learn (XGBoost, Linear Regression)", "FastAPI", "Streamlit", "Pandas", "Groq API"]
})

st.subheader("🔬 Model Performance")
st.divider()

st.subheader("Churn Classification Model:")
st.table({
    "Model": ["Gradient Boosting Classifier", "XGBoost Classifier", "Random Forest Classifier", "Logistic Regression"],
    "F1- Score": [0.78, 0.77, 0.75, 0.62],
    "Remark": ["🏆Best Model", "✅Good fit", "✅Good fit", "✅Good fit"]
})

st.subheader("CLV Regression Model:")
st.table({
    "Model": ["Linear Regression", "Random Forest Regressor", "XGBoost Regressor"],
    "R² Score": ["18,593", "114,175", "160,967"],
    "Remark": ["🏆Best Model", "✅Good fit", "✅Good fit"]
})

st.write("The churn prediction model achieves an F1-Score of 78%, while the CLV prediction model has an R² score of 18,593. These metrics indicate that our models are performing well in predicting customer behavior and value.")

import pandas as pd
import streamlit as st

def load_data(csv_file_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_file_path)
    return df

def get_user_inputs():
    condition = st.text_input("Enter your condition:").strip().lower()
    return condition

def get_recommendations(df: pd.DataFrame, condition: str) -> pd.DataFrame:
    if not condition:
        st.error("Please enter a condition.")
        return pd.DataFrame()

    recommendations = df[df['condition'].str.lower() == condition]

    if recommendations.empty:
        st.error("No drugs found for the given condition.")
        return pd.DataFrame()

    grouped_recommendations = recommendations.groupby('drugName').agg(
        average_rating=('rating', 'mean'),
        reviews=('review', lambda x: list(x))
    ).reset_index()

    top_drugs = grouped_recommendations.sort_values(by='average_rating', ascending=False).head(5)

    return top_drugs

def display_recommendations(top_drugs: pd.DataFrame):
    if not top_drugs.empty:
        st.write("Top 5 Drug Recommendations:")
        for idx, row in top_drugs.iterrows():
            name = row['drugName']
            rating = round(row['average_rating'], 1)
            reviews = row['reviews']

            st.subheader(f"{idx+1}. {name}")
            st.write(f"Average Rating: {rating}")
            with st.expander("Reviews"):
                for review in reviews:
                    st.write(f"- {review}")
            st.markdown("---")

def run_app(csv_file_path: str):
    st.title("Virtual Health Assistant - Drug Recommendation System")

    df = load_data(csv_file_path)

    condition = get_user_inputs()

    if st.button("Search"):
        top_drugs = get_recommendations(df, condition)
        if not top_drugs.empty:
            display_recommendations(top_drugs)

if __name__ == "__main__":
    run_app('drug1.csv')


# usage
# streamlit run assignmentAI.py


#plus i had to clean the csv before it starting running. The csv file for this assignment was really sh**.
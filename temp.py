from cmath import e
import streamlit as st
import pandas as pd
import pymysql
import plotly.express as px
import openpyxl 
import emoji
data=pd.read_excel(r"C:\Users\Sudha\Downloads\traffic_stops.xlsx")
# Database connection



def create_connection():
  try:
   connection = pymysql.connect(
           host='localhost',
           user='root',
           password='sudar',
           database='Digital_Ledger_db',
          cursorclass=pymysql.cursors.DictCursor
   )
   return connection
  except Exception as e:
    st.error(f"Database Connection Error: {e}")
    return None
# Fetch data frow database
def fetch_data(query):
   connection = create_connection()
   if connection:
       try:
         with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            df = pd.DataFrame(result)
            return df
       finally:
         connection.close()

   else:
      return pd.DataFrame()
st.set_page_config(page_title="SecureCheck", layout="wide")

# Sidebar for navigation
st.sidebar.title("Secure")
page = st.sidebar.radio("Go to", ["Project Introduction", "Traffic Violation Visualation ", "SQL Queries"])

if page == "Project Introduction":
    st.title(" 👮 🚔 POLICE Secure Check ")
    st.subheader("📊 A Streamlit App for Displaying traffic voilation")
    st.write("""
    This project is to analyzes  build an SQL-based check post database with a
    Python-powered dashboard for real-time insights and alerts.


    **Features:**
      **- Real-time logging of vehicles and personnel.**
             
      **-Automated suspect vehicle identification using SQL queries.**
             
      **-Check post efficiency monitoring through data analytics.**
             
      **-Crime pattern analysis with Python scripts.**
             
      **-Centralized database for multi-location check posts.**


    **Database Used:** `Digital_Ledger_db`
 
                                                                                Created by
                                                                                    
                                                                                      SUDHARSAN S
    """)
elif page== "Traffic Violation Visualation ":
    st.title("Traffic Violation Visualation ")
    with st.form("new log form"):
      stop_date =st.date_input("Stop date")
      stop_time = st.time_input("stop Time")
      county_name = st. text_input("County Name")
      driver_gender =st.selectbox("Driver Gender", ["male", "female"])
      driver_age = st.number_input("Driver Age", min_value=16,max_value=100, value=27)
      driver_race = st.text_input("Driver Race")
      search_conducted = st.selectbox("was a Search conducted?", ["0", "1"])
      search_type = st.text_input("Search Type")
      drugs_related_stop = st.selectbox("Was it Drug Related?", ["0", "1"])
      stop_duration = st.selectbox("stop Duration", data['stop_duration'].dropna().unique())
      vehicle_number = st.text_input("vehicle Number")
      timestamp = pd.Timestamp.now()
      submitted = st.form_submit_button("Predict Stop Outcome & Violation")
    if submitted:
           filtered_data= data[
           (data['driver_gender'] == driver_gender) &
           (data['driver_age'] == driver_age) &
           (data['search_conducted'] == int(search_conducted)) &
           (data['stop_duration'] == stop_duration) &
           (data['driver_gender'] == driver_gender) &
           (data['driver_age'] == driver_age) &
           (data['search_conducted'] == int(search_conducted)) &
           (data['stop_duration'] == stop_duration) &
           (data['drugs_related_stop'] == int(drugs_related_stop))]
           if not filtered_data.empty:
                predicted_outcome=filtered_data['stop_outcome'].mode()[0]
                predicted_violation=filtered_data['violation' ].mode()[0]
           else:
            predicted_outcome = "warning" # Oefauit fallback
            predicted_violation = "speeding" # Default fallback

            search_text = "A search was conducted" if int(search_conducted) else "No search was conducted"
            drug_ext = "was drug-related" if int(drugs_related_stop) else "was not drug-related"
            st.header("Prediction Summary")
            st.markdown(f"""
            - ** Predicted Violation :** {predicted_violation}
            - ** Predicted Stop Outcome :** {predicted_outcome}
  
            - A {driver_age}-year-old {driver_gender} driver in {county_name} was stopped at {stop_time.strftime('%I:%M %p')} on {stop_date}
            {search_text}, and the stop {drug_ext}  

            Stop duration:{stop_duration}
            Vehicle Number: **{vehicle_number}**
            """)
elif page=="SQL Queries": 
  st.header(" Advanced Insights")
  selected_query = st.selectbox("Select a Query to Run", [
"The top 10 vehicle_Number involved in drug-related stops",
"Vehicles were most frequently searched",
"Driver age group had the highest arrest rate",
"The gender distribution of drivers stopped in each country",
"Race and gender combination has the highest search rate",
"The average stop duration for different violations",
"Stops during the night more likely to lead to arrests",
"Violations are most associated with searches or arrests",
"Violations are most common among younger drivers (<25)",
"There is a violation that rarely results in search or arrest",
"Countries report the highest rate of drug-related stops",
"The arrest rate by country and violation",
"Country has the most stops with search conducted",
"Yearly Breakdown of Stops and Arrests by Country ",
"Driver Violation Trends Based on Age and Race",
"Time Period Analysis of Stops ,Number of Stops by Year,Month, Hour of the Day",
"Violations with High Search and Arrest Rates",
"Driver Demographics by Country ",
"Top 5 Violations with Highest Arrest Rates"
 ])
  query_map = {
    "The top 10 vehicle_Number involved in drug-related stops":
        "select vehicle_Number from Digital_Ledger_data where ( drugs_related_stop=True ) limit 10",

    "Vehicles were most frequently searched": """
        SELECT 
            vehicle_number, COUNT(*) AS search_count
        FROM 
            digital_ledger_data
        GROUP BY 
            vehicle_number
        ORDER BY 
            search_count DESC
        LIMIT 1;
    """,

    "Driver age group had the highest arrest rate":
        "select driver_age,count(*) as total from Digital_Ledger_data where is_arrested = True group by driver_age ORDER BY total DESC limit 1",

    "The gender distribution of drivers stopped in each country": """
        SELECT 
            country_name,
            driver_gender,
            COUNT(*) AS total_stops
        FROM 
            digital_ledger_data
        GROUP BY 
            country_name, driver_gender
        ORDER BY 
            country_name, total_stops DESC;
    """,

    "Race and gender combination has the highest search rate": """
        SELECT 
            driver_race, 
            driver_gender, 
            COUNT(*) AS Count1
        FROM 
            digital_ledger_data
        WHERE 
            search_conducted = TRUE
        GROUP BY 
            driver_race, driver_gender
        ORDER BY 
            Count1 DESC 
        LIMIT 1;
    """,

    "The average stop duration for different violations": """
        SELECT 
            violation,
            AVG(stop_duration) AS avg_stop_duration,
            COUNT(*) AS total_stops
        FROM 
            digital_ledger_data
        GROUP BY 
            violation
        ORDER BY 
            avg_stop_duration DESC;
    """,

    "Stops during the night more likely to lead to arrests": """
        SELECT 
            CASE 
                WHEN HOUR(stop_time) BETWEEN 20 AND 23 THEN 'Night'
                WHEN HOUR(stop_time) BETWEEN 0 AND 4 THEN 'Late Night'
                ELSE 'Daytime'
            END AS time_period,
            COUNT(*) AS total_stops,
            SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS arrests,
            ROUND(SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS arrest_rate_percent
        FROM 
            digital_ledger_data
        GROUP BY 
            time_period
        ORDER BY 
            arrest_rate_percent DESC;
    """,

    "Violations are most associated with searches or arrests": """
        SELECT 
            violation, COUNT(*) AS hg
        FROM 
            digital_ledger_data
        WHERE
            search_conducted = TRUE OR is_arrested = TRUE
        GROUP BY 
            violation
        ORDER BY 
            hg DESC 
        LIMIT 3;
    """,

    "Violations are most common among younger drivers (<25)": """
        SELECT 
            violation, COUNT(*) AS aba
        FROM 
            digital_ledger_data
        WHERE 
            driver_age < 25
        GROUP BY 
            violation
        ORDER BY 
            aba DESC 
        LIMIT 1;
    """,

    "There is a violation that rarely results in search or arrest": """
        SELECT 
            violation, COUNT(*) AS aba
        FROM 
            digital_ledger_data
        WHERE  
            (search_conducted = TRUE OR is_arrested = TRUE) 
        GROUP BY 
            violation
        HAVING 
            aba < 10
        ORDER BY 
            aba  
        LIMIT 1;
    """,

    "Countries report the highest rate of drug-related stops": """
        SELECT 
            country_name, COUNT(*) AS ds
        FROM 
            digital_ledger_data
        WHERE 
            drugs_related_stop = TRUE
        GROUP BY 
            country_name
        ORDER BY 
            ds DESC 
        LIMIT 5;
    """,

    "The arrest rate by country and violation": """
        SELECT 
            country_name,
            violation,
            SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS arrest_count,
            COUNT(*) AS total_count,
            ROUND(SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) AS arrest_rate_percent
        FROM 
            digital_ledger_data
        GROUP BY 
            country_name, violation
        ORDER BY 
            arrest_rate_percent DESC
        LIMIT 5;
    """,

    "Country has the most stops with search conducted": """
        SELECT 
            country_name, COUNT(*) AS df
        FROM 
            digital_ledger_data
        WHERE 
            search_conducted = TRUE
        GROUP BY 
            country_name
        ORDER BY 
            df
        LIMIT 1;
    """,

    "Yearly Breakdown of Stops and Arrests by Country ": """
        SELECT 
            country_name,
            year,
            COUNT(*) AS total_stops,
            SUM(is_arrested) AS total_arrests,
            SUM(SUM(is_arrested)) OVER (PARTITION BY country_name ORDER BY year) AS cumulative_arrests
        FROM (
            SELECT 
                country_name,
                YEAR(stop_time) AS year,
                is_arrested
            FROM digital_ledger_data
        ) AS sub
        GROUP BY 
            country_name, year
        ORDER BY 
            country_name, year;
    """,

    "Driver Violation Trends Based on Age and Race": """
        SELECT 
            v.driver_age_group,
            v.driver_race,
            v.violation,
            COUNT(*) AS total_violations
        FROM (
            SELECT 
                driver_age,
                driver_race,
                violation,
                CASE 
                    WHEN driver_age < 25 THEN 'Under 25'
                    WHEN driver_age BETWEEN 25 AND 40 THEN '25-40'
                    WHEN driver_age BETWEEN 41 AND 60 THEN '41-60'
                    ELSE '60+'
                END AS driver_age_group
            FROM digital_ledger_data
        ) AS v
        GROUP BY 
            v.driver_age_group, v.driver_race, v.violation
        ORDER BY 
            v.driver_age_group, v.driver_race, total_violations DESC;
    """,

    "Time Period Analysis of Stops ,Number of Stops by Year,Month, Hour of the Day": """
        SELECT 
            t.year,
            t.month,
            t.hour,
            COUNT(*) AS total_stops
        FROM (
            SELECT
                YEAR(stop_time) AS year,
                MONTH(stop_time) AS month,
                HOUR(stop_time) AS hour
            FROM digital_ledger_data
        ) AS t
        GROUP BY 
            t.year, t.month, t.hour
        ORDER BY 
            t.year, t.month, t.hour;
    """,

    "Violations with High Search and Arrest Rates": """
        SELECT 
            violation,
            COUNT(*) AS total_stops,
            SUM(search_conducted) AS total_searches,
            SUM(is_arrested) AS total_arrests,
            ROUND(100 * SUM(search_conducted) / COUNT(*), 2) AS search_rate,
            ROUND(100 * SUM(is_arrested) / COUNT(*), 2) AS arrest_rate,
            RANK() OVER (ORDER BY ROUND(100 * SUM(is_arrested) / COUNT(*), 2) DESC) AS arrest_rank
        FROM 
            digital_ledger_data
        GROUP BY 
            violation
        ORDER BY 
            arrest_rate DESC
        LIMIT 10;
    """,

    "Driver Demographics by Country ": """
        SELECT 
            country_name,
            ROUND(AVG(driver_age), 1) AS avg_age,
            COUNT(DISTINCT driver_gender) AS gender_diversity,
            COUNT(DISTINCT driver_race) AS race_diversity,
            COUNT(*) AS total_drivers
        FROM 
            digital_ledger_data
        GROUP BY 
            country_name
        ORDER BY 
            total_drivers DESC;
    """,

    "Top 5 Violations with Highest Arrest Rates": """
        SELECT 
            violation,
            COUNT(*) AS total_stops,
            SUM(is_arrested) AS total_arrests,
            ROUND(100 * SUM(is_arrested) / COUNT(*), 2) AS arrest_rate
        FROM 
            digital_ledger_data
        GROUP BY 
            violation
        ORDER BY 
            arrest_rate DESC
        LIMIT 5;
    """
}
  if st.button("🔍 Run Query"):
    result = fetch_data(query_map[selected_query])
    if not result.empty:
      st.write(result)
      st.success("Query executed! ✅")
    else:
      st.warning("No results found for the selected query.")
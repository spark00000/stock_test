
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
import datetime

# Page configuration
st.set_page_config(page_title="Samsung Stock Data", layout="wide")

st.title("삼성전자 (Samsung Electronics) 주가 정보")

# Define the ticker symbol for Samsung Electronics (South Korea)
ticker_symbol = "005930.KS"
company_name = "삼성전자"

# Fetch stock data for the last month
# Get today's date and calculate the date one month ago
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=30) # Approximately one month

try:
    # Download data
    # yfinance expects date objects or strings in 'YYYY-MM-DD' format
    stock_data = yf.download(ticker_symbol, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))

    if stock_data.empty:
        st.warning(f"{company_name} ({ticker_symbol})의 주가 데이터를 가져오지 못했습니다. 잠시 후 다시 시도해주세요.")
    else:
        st.subheader("최근 1개월 주가 데이터 (테이블)")
        # Display data in a table
        st.dataframe(stock_data)

        # --- CORRECTED PLOTTING LOGIC FOR TUPLE COLUMN NAMES ---
        # Find the correct column name for 'Close' which is expected to be a tuple
        close_column_tuple = None
        for col in stock_data.columns:
            # Check if the column is a tuple and its first element is 'Close'
            if isinstance(col, tuple) and col[0] == 'Close':
                close_column_tuple = col
                break
        
        if close_column_tuple:
            st.subheader("최근 1개월 종가 추이 (차트)")
            
            # Get the date index for the x-axis
            dates = stock_data.index
            
            # Get the 'Close' price Series using the identified tuple column name
            close_prices = stock_data[close_column_tuple]
            
            # Plot using x and y explicitly to avoid issues with column naming interpretation
            fig = px.line(x=dates, y=close_prices, title=f'{company_name} 종가 추이')
            
            fig.update_layout(
                xaxis_title="날짜",
                yaxis_title="종가 (KRW)"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Provide more details in the error message if 'Close' column is not found
            st.error(f"종가('Close') 데이터를 찾을 수 없습니다. 데이터프레임 컬럼: {stock_data.columns.tolist()}")
        # --- END OF CORRECTED PLOTTING LOGIC ---

except Exception as e:
    st.error(f"데이터를 가져오는 중 오류가 발생했습니다: {e}")

st.markdown("---")
st.markdown("데이터 출처: Yahoo Finance")

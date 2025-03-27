# app.py
import streamlit as st
import pandas as pd

def main():
    st.title("Excel File Merger")

    uploaded_files = st.file_uploader("Upload Excel files", type=["xlsx", "xls"], accept_multiple_files=True)

    if uploaded_files:
        dfs = []
        for file in uploaded_files:
            try:
                df = pd.read_excel(file)
                dfs.append(df)
            except Exception as e:
                st.error(f"Error reading file {file.name}: {e}")

        if dfs:
            combined_df = pd.concat(dfs, ignore_index=True)

            st.subheader("Combined Data Preview")
            st.dataframe(combined_df)

            # Add index as a column
            combined_df.insert(0, 'Row Index', combined_df.index)

            # Download Button
            st.download_button(
                label="Download Combined Excel File",
                data=combined_df.to_excel(index=False).encode('utf-8'),
                file_name="combined_data.xlsx",
                mime="application/vnd.ms-excel"
            )
        else:
            st.warning("No valid Excel files uploaded.")

if __name__ == "__main__":
    main()

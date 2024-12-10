import streamlit as st
import pandas as pd
from io import BytesIO

def process_files(file1_path, file2_path, county_col_1, zhibiao_col_1, new_index_col_2):
    df1 = pd.read_excel(file1_path)
    df2 = pd.read_excel(file2_path)
    
    if county_col_1 >= df1.shape[1] or zhibiao_col_1 >= df1.shape[1]:
        st.error("文件1的列索引超出范围。")
        return None

    county_data_1 = df1.iloc[:, county_col_1]
    zhibiao_data_1 = df1.iloc[:, zhibiao_col_1]
    
    for i, county_name in enumerate(df2.iloc[:, 2]):
        if county_name in county_data_1.values:
            index = county_data_1[county_data_1 == county_name].index[0]
            df2.iloc[i, new_index_col_2] = zhibiao_data_1.iloc[index]
    
    st.success("数据处理完成并已更新文件。")
    return df2

st.title("县市匹配")

# Inputs for File 1
st.header("文件1")
file1_upload = st.file_uploader("上传文件1", type='xlsx')
county_col_1 = st.number_input("县名列 (0-based):", min_value=0, step=1)
zhibiao_col_1 = st.number_input("指标列 (0-based):", min_value=0, step=1)

# Inputs for File 2
st.header("文件2")
file2_upload = st.file_uploader("上传文件2", type='xlsx')
new_index_col_2 = st.number_input("传入列 (0-based):", min_value=0, step=1)

# Process Button
if st.button("开始"):
    if file1_upload is not None and file2_upload is not None:
        processed_df2 = process_files(file1_upload, file2_upload, county_col_1, zhibiao_col_1, new_index_col_2)
        if processed_df2 is not None:
            # Provide download and preview options
            st.dataframe(processed_df2)  # Preview the processed data

            # Convert dataframe to a buffered stream for download
            buffer = BytesIO()
            processed_df2.to_excel(buffer, index=False)
            buffer.seek(0)

            st.download_button(
                label="下载处理后的文件",
                data=buffer,
                file_name="processed_file.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        st.warning("请确保两个文件都已上传。")

import io
import pandas as pd

def excel_bytes_to_df(bytes_data: bytes) -> pd.DataFrame:
    with io.BytesIO(bytes_data) as buffer:
        df = pd.read_excel(buffer)
    return df

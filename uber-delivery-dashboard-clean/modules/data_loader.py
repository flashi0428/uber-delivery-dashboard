from __future__ import annotations

from pathlib import Path
from typing import Union

import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def load_data(path: Union[str, Path]) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df

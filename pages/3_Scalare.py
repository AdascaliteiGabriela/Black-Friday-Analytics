import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

st.title("Pagina 3: Scalarea variabilelor numerice")

st.markdown("""
Variabilele numerice dintr-un set de date au, de obicei, intervale și unități de măsură diferite. 
Algoritmii de Machine Learning care folosesc distanțe sau gradient (KMeans, KNN, regresie logistică) 
sunt sensibili la aceste diferențe, variabilele cu valori mari ar domina calculele. 
Scalarea aduce variabilele la o scară comună.

În setul nostru, nu toate variabilele numerice merită scalate: `User_ID` este un identificator, 
`Marital_Status` este binară (0/1), iar `Occupation` și `Product_Category_*` sunt coduri categoriale 
anonimizate. Aplicăm scalarea pe **Purchase**, singura variabilă continuă reală, exprimată în 
unități monetare.
""")

df = pd.read_csv("data/bf_sample.csv")

st.subheader("Metode de scalare")

st.markdown("""
Aplicăm două metode standard, în paralel:

- **StandardScaler** (z-score):  `x_nou = (x − media) / abatere`. Rezultă o distribuție cu medie 0 și abatere standard 1.
- **MinMaxScaler**: `x_nou = (x − min) / (max − min)`. Rezultă valori în intervalul [0, 1].

Ambele metode operează pe o **singură coloană** și folosesc doar valorile din acea coloană.
""")

st.subheader("Aplicarea scalării pe coloana Purchase")

coloana = "Purchase"
valori = df[[coloana]].values

scaler_std = StandardScaler()
valori_std = scaler_std.fit_transform(valori).flatten()

scaler_mm = MinMaxScaler()
valori_mm = scaler_mm.fit_transform(valori).flatten()

# Doar primele 10 rânduri în tabel
df_rezultat = pd.DataFrame(
    {
        "Purchase original": df[coloana].head(10).values,
        "StandardScaler": valori_std[:10].round(4),
        "MinMaxScaler": valori_mm[:10].round(4),
    }
)
st.dataframe(df_rezultat, use_container_width=True, hide_index=True)

st.subheader("Statistici înainte / după scalare")

stats_compar = pd.DataFrame(
    {
        "Metric": ["Min", "Max", "Medie", "Abatere standard"],
        "Original": [
            df[coloana].min(),
            df[coloana].max(),
            round(df[coloana].mean(), 4),
            round(df[coloana].std(), 4),
        ],
        "StandardScaler": [
            round(valori_std.min(), 4),
            round(valori_std.max(), 4),
            round(valori_std.mean(), 4),
            round(valori_std.std(), 4),
        ],
        "MinMaxScaler": [
            round(valori_mm.min(), 4),
            round(valori_mm.max(), 4),
            round(valori_mm.mean(), 4),
            round(valori_mm.std(), 4),
        ],
    }
)

st.dataframe(stats_compar, use_container_width=True, hide_index=True)

st.subheader("Interpretare")

st.markdown("""
**StandardScaler**: valori centrate în 0, abaterea standard 1 — utilă pentru regresia logistică.

**MinMaxScaler**: valori comprimate în [0, 1], păstrând proporțiile — potrivită pentru rețele neuronale.

Fără scalare, `Purchase` (mii) ar domina variabile mici precum `Marital_Status` în algoritmi bazați pe distanțe sau gradient.
""")

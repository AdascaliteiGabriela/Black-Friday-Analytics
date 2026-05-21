import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error

st.title("Pagina 7: Regresie multiplă — estimarea valorii cumpărăturii")

st.markdown("""
Regresia liniară multiplă este o tehnică statistică ce estimează valoarea unei variabile continue 
(`Purchase`) pe baza unui set de variabile explicative. Spre deosebire de regresia logistică, 
care prezice o categorie, regresia multiplă prezice o **valoare numerică**.

Pentru această analiză folosim pachetul **`statsmodels`** (în loc de `scikit-learn`), deoarece oferă 
un output statistic complet — coeficienți, p-values, intervale de încredere, R² — care permite atât 
predicția, cât și interpretarea relațiilor dintre variabile.
""")

df = pd.read_csv("data/bf_sample.csv")

st.subheader("Variabile predictoare și codificare")

predictori = [
    "Gender",
    "Age",
    "City_Category",
    "Marital_Status",
    "Occupation",
    "Product_Category_1",
]

st.markdown(f"""
Folosim aceleași 6 variabile predictoare ca la regresia logistică: 
**{', '.join(predictori)}**. Variabilele categoriale sunt codificate prin Label Encoding, 
iar variabila țintă este `Purchase`.
""")

X = df[predictori].copy()
for col in ["Gender", "Age", "City_Category"]:
    X[col] = LabelEncoder().fit_transform(X[col])

y = df["Purchase"]

st.subheader("Împărțirea datelor și antrenarea modelului")

st.markdown(
    "Setul este împărțit în **80% antrenare** și **20% testare** (`random_state=42`). "
    "Modelul OLS (Ordinary Least Squares) din `statsmodels` este antrenat pe setul de antrenare."
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# statsmodels necesită adăugarea explicită a interceptului
X_train_const = sm.add_constant(X_train)
X_test_const = sm.add_constant(X_test)

model = sm.OLS(y_train, X_train_const).fit()

st.subheader("Rezultatul modelului (summary statsmodels)")

st.text(model.summary().as_text())

st.subheader("Metrici de evaluare pe setul de testare")

y_pred = model.predict(X_test_const)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)

col1, col2, col3 = st.columns(3)
col1.metric("R² (antrenare)", f"{model.rsquared:.4f}")
col2.metric("RMSE (testare)", f"{rmse:.2f}")
col3.metric("MAE (testare)", f"{mae:.2f}")

st.subheader("Coeficienții modelului")

coef_df = pd.DataFrame(
    {
        "Variabilă": model.params.index,
        "Coeficient": model.params.values.round(4),
        "P-value": model.pvalues.values.round(4),
        "Semnificativ (p < 0.05)": [
            "Da" if p < 0.05 else "Nu" for p in model.pvalues.values
        ],
    }
)
st.dataframe(coef_df, use_container_width=True, hide_index=True)

st.subheader("Interpretare")

st.markdown(f"""
Modelul a obținut un **R² de {model.rsquared:.4f}** — variabilele explică ~**{model.rsquared * 100:.1f}%** 
din variația `Purchase`. **MAE = {mae:.0f} u.m.**, **RMSE = {rmse:.0f} u.m.**, semnificative față de 
media `Purchase` (~9.260 u.m.).

**Citirea coeficienților:** fiecare coeficient indică modificarea estimată a `Purchase` la creșterea 
cu o unitate a variabilei, ceilalți factori constanți. Variabilele cu **p-value < 0.05** sunt 
semnificative statistic. Cele mai influente sunt `Product_Category_1` și `Occupation`.

**Interpretare pentru ABC Private Limited:**

- R²-ul scăzut arată că profilul demografic **nu permite estimarea precisă** a valorii unei cumpărături — 
clienți similari pot avea cumpărături foarte diferite.
- Decizia de cumpărare e influențată de factori neînregistrați: preferințe individuale, promoții, 
sezonalitate, stoc.
- Modelul rămâne util pentru **estimări agregate** (ex. valoare totală pe segment), nu pentru 
predicții individuale.
""")

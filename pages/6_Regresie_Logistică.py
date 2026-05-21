import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix

st.title("Pagina 6: Regresie logistică — predicția High Spender")

st.markdown("""
Regresia logistică este un algoritm de clasificare supravegheată care estimează **probabilitatea** 
ca o observație să aparțină unei clase. În această pagină construim un model care prezice dacă o 
tranzacție va fi de valoare ridicată (**High Spender**) pe baza profilului demografic al clientului 
și a categoriei principale a produsului.
""")

df = pd.read_csv("data/bf_sample.csv")

st.subheader("Definirea variabilei țintă")

mediana_purchase = df["Purchase"].median()
df["High_Spender"] = (df["Purchase"] > mediana_purchase).astype(int)

st.markdown(
    f"Definim **High_Spender = 1** dacă valoarea tranzacției depășește mediana setului "
    f"(`{mediana_purchase:.0f}` u.m.), altfel 0. Acest prag împarte datele în două clase echilibrate, "
    f"esențial pentru antrenarea unui model de clasificare."
)

distrib = df["High_Spender"].value_counts().sort_index().reset_index()
distrib.columns = ["High_Spender", "Număr tranzacții"]
distrib["Procent"] = (distrib["Număr tranzacții"] / len(df) * 100).round(2)
st.dataframe(distrib, use_container_width=True, hide_index=True)

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
Folosim 6 variabile predictoare: **{', '.join(predictori)}**. 

Variabilele categoriale (`Gender`, `Age`, `City_Category`) sunt codificate cu **Label Encoding**, 
transformându-le în valori numerice. Variabilele deja numerice (`Marital_Status`, `Occupation`, 
`Product_Category_1`) sunt folosite direct.
""")

X = df[predictori].copy()
for col in ["Gender", "Age", "City_Category"]:
    X[col] = LabelEncoder().fit_transform(X[col])

y = df["High_Spender"]

st.subheader("Împărțirea datelor și antrenarea modelului")

st.markdown(
    "Setul este împărțit în **80% antrenare** și **20% testare** (cu `random_state=42` pentru "
    "reproductibilitate). Modelul este antrenat pe setul de antrenare și evaluat pe setul de testare."
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

st.subheader("Evaluarea modelului")

acc = accuracy_score(y_test, y_pred)
st.metric("Acuratețe pe setul de testare", f"{acc:.2%}")

st.markdown("**Matricea de confuzie:**")

cm = confusion_matrix(y_test, y_pred)
cm_df = pd.DataFrame(
    cm,
    index=["Real: Low Spender (0)", "Real: High Spender (1)"],
    columns=["Prezis: Low Spender (0)", "Prezis: High Spender (1)"],
)

fig = px.imshow(
    cm,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="Blues",
    labels=dict(x="Prezis", y="Real", color="Număr"),
    x=["Low Spender (0)", "High Spender (1)"],
    y=["Low Spender (0)", "High Spender (1)"],
    title="Matricea de confuzie",
)
st.plotly_chart(fig, use_container_width=True)

st.dataframe(cm_df, use_container_width=True)

st.subheader("Interpretare")

tn, fp, fn, tp = cm.ravel()

st.markdown(f"""
Modelul a obținut o acuratețe de **{acc:.2%}** pe setul de testare, ceea ce înseamnă că aproape 
două din trei tranzacții sunt clasificate corect ca fiind sub sau peste mediana valorii.

**Citirea matricei de confuzie:**

- **{tn:,} tranzacții** au fost corect clasificate ca **Low Spender** (real 0, prezis 0);
- **{tp:,} tranzacții** au fost corect clasificate ca **High Spender** (real 1, prezis 1);
- **{fp:,} tranzacții** au fost prezise greșit ca High Spender deși erau Low (fals pozitive);
- **{fn:,} tranzacții** au fost prezise greșit ca Low Spender deși erau High (fals negative).

**Interpretare economică:** profilul demografic al clientului (vârstă, gen, oraș, ocupație, stare 
civilă) împreună cu categoria principală a produsului oferă o capacitate moderată de a anticipa 
dacă o tranzacție va fi de valoare ridicată. Acuratețea peste 60% sugerează că aceste variabile 
conțin informație utilă, dar nu suficientă pentru predicții foarte precise — categoria produsului 
și combinația specifică de caracteristici demografice influențează cel mai mult rezultatul.

Pentru ABC Private Limited, modelul poate fi folosit ca **filtru inițial** pentru identificarea 
clienților probabili de a face cumpărături mari, permițând personalizarea ofertelor în campaniile 
viitoare. Un model mai precis ar necesita variabile suplimentare (istoric cumpărături anterioare, 
sezonalitate, canal de achiziție), care nu sunt disponibile în setul curent.
""")

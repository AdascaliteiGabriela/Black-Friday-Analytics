import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Pagina 4: Statistici și grupare cu pandas")

st.markdown("""
Operațiile de grupare și agregare permit calcularea de statistici descriptive pe segmente 
ale setului de date. Folosim `groupby` din pandas pentru a împărți datele după o variabilă 
categorială și pentru a calcula numărul de tranzacții, valoarea totală și valoarea medie 
a cumpărăturilor pentru fiecare grup.
""")

df = pd.read_csv("data/bf_sample.csv")

st.subheader("Selectarea variabilei de grupare")

coloana_grup = st.selectbox(
    "Grupați tranzacțiile după:",
    ["Gender", "Age", "City_Category", "Marital_Status", "Product_Category_1"],
)

# Grupare și agregare
grup = df.groupby(coloana_grup)["Purchase"].agg(["count", "sum", "mean"]).reset_index()
grup.columns = [coloana_grup, "Număr tranzacții", "Total cheltuit", "Medie tranzacție"]
grup["Total cheltuit"] = grup["Total cheltuit"].round(0)
grup["Medie tranzacție"] = grup["Medie tranzacție"].round(2)

# Sortare după numărul de tranzacții (descrescător), excepție pentru Age și Product_Category_1 - rămân sortate natural
if coloana_grup not in ["Age", "Product_Category_1"]:
    grup = grup.sort_values("Număr tranzacții", ascending=False).reset_index(drop=True)

st.subheader(f"Rezultat: statistici pe {coloana_grup}")

st.dataframe(grup, use_container_width=True, hide_index=True)

# Grafic - valoarea medie a cumpărăturilor pe grup
fig = px.bar(
    grup,
    x=coloana_grup,
    y="Medie tranzacție",
    title=f"Valoarea medie a cumpărăturilor pe {coloana_grup}",
    text="Medie tranzacție",
    color="Medie tranzacție",
    color_continuous_scale="Blues",
)
fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
fig.update_layout(xaxis_type="category")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Interpretare")

st.markdown("""
Tabelul și graficul permit identificarea segmentelor de clienți cu cel mai mare volum sau 
cea mai mare valoare medie a cumpărăturilor. Aceste informații sunt utile pentru:

- **Strategia de marketing** — concentrarea campaniilor pe segmentele cu cheltuieli mai ridicate;
- **Planificarea stocului** — anticiparea cererii pe categorii de produse;
- **Deciziile de extindere** — identificarea orașelor sau a grupelor demografice cu potențial.

Spre exemplu, dacă orașele de tip C au valoarea medie a cumpărăturilor mai mare decât A și B, 
ar putea fi indicat să se aloce mai multe resurse pentru piețele de tip C, deși volumul total 
de tranzacții poate fi mai mic.
""")

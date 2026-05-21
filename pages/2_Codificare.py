import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder

st.title("Pagina 2: Codificarea variabilelor categoriale")

st.markdown("""
Modelele de Machine Learning nu pot lucra direct cu valori text. 
Codificarea/encoding transformă variabilele categoriale în valori numerice, 
permițând utilizarea acestora în algoritmi precum regresia, clusterizarea sau arborii de decizie.
""")

df = pd.read_csv("data/bf_sample.csv")

st.subheader("Identificarea variabilelor categoriale")

categorical_cols = [
    c for c in df.select_dtypes(include=["object"]).columns if c != "Product_ID"
]

cat_info = pd.DataFrame(
    {
        "Coloană": categorical_cols,
        "Număr categorii": [df[c].nunique() for c in categorical_cols],
        "Valori": [
            ", ".join(map(str, sorted(df[c].unique()))) for c in categorical_cols
        ],
    }
)

st.dataframe(cat_info, use_container_width=True, hide_index=True)

st.info(
    "Setul conține 4 variabile categoriale de tip text: `Gender`, `Age`, "
    "`City_Category` și `Stay_In_Current_City_Years`. Acestea trebuie codificate înainte "
    "de utilizarea în modele predictive."
)

st.subheader("Metoda folosită: Label Encoding")

st.markdown("""
**Label Encoding** atribuie fiecărei categorii un număr întreg unic. 
De exemplu, pentru `Gender`: F → 0, M → 1. 

Este cea mai simplă metodă de codificare și produce o singură coloană numerică 
pentru fiecare variabilă codificată.
""")

st.subheader("Aplicarea codificării")

coloana = st.selectbox(
    "Selectați coloana de codificat:",
    [c for c in categorical_cols if c != "Product_ID"],
)


df_procesat = df.copy()
encoder = LabelEncoder()
df_procesat[coloana + "_encoded"] = encoder.fit_transform(df[coloana])


mapping = pd.DataFrame(
    {
        "Categorie originală": encoder.classes_,
        "Cod numeric": range(len(encoder.classes_)),
    }
)

st.markdown(f"**Mapping pentru coloana `{coloana}`:**")
st.dataframe(mapping, use_container_width=True, hide_index=True)

st.subheader("Comparație înainte / după")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"**Coloana originală — `{coloana}`:**")
    st.dataframe(df[[coloana]].head(10), use_container_width=True)

with col2:
    st.markdown(f"**Coloana codificată — `{coloana}_encoded`:**")
    st.dataframe(df_procesat[[coloana + "_encoded"]].head(10), use_container_width=True)

st.subheader("Interpretare")

st.markdown("""
Label Encoding este simplu și eficient, dar introduce o **ordine implicită** între categorii 
(de exemplu, după codificarea `City_Category`: A → 0, B → 1, C → 2, modelul ar putea interpreta 
că C "este mai mare" decât A, deși între ele nu există o relație de ordine reală).

Pentru coloane fără ordine naturală (`Gender`, `City_Category`), o alternativă mai potrivită ar fi 
**One-Hot Encoding**, care creează câte o coloană binară pentru fiecare categorie. Pentru coloane 
cu ordine reală (`Age`, `Stay_In_Current_City_Years`), Label Encoding este o alegere acceptabilă.
""")

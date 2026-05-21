import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Pagina 1: Gestionarea valorilor lipsă")


st.markdown("""
Identificăm valorile lipsă din set și aplicăm două metode de tratare: înlocuirea cu 0 sau eliminarea coloanelor.
""")

df = pd.read_csv("data/bf_sample.csv")

st.subheader("Identificarea valorilor lipsă")

missing_count = df.isnull().sum()
missing_percent = (df.isnull().mean() * 100).round(2)

missing_df = pd.DataFrame(
    {
        "Coloană": df.columns,
        "Număr valori lipsă": missing_count.values,
        "Procent (%)": missing_percent.values,
    }
)

st.dataframe(missing_df, use_container_width=True, hide_index=True)


missing_only = missing_df[missing_df["Număr valori lipsă"] > 0]

fig = px.bar(
    missing_only,
    x="Coloană",
    y="Procent (%)",
    title="Procentul de valori lipsă pe coloane",
    color="Procent (%)",
    color_continuous_scale="Reds",
    text="Procent (%)",
)
fig.update_traces(textposition="outside")
st.plotly_chart(fig, use_container_width=True)

st.info(
    "Doar două coloane prezintă valori lipsă: `Product_Category_2` (≈31%) "
    "și `Product_Category_3` (≈70%). Restul setului este complet."
)

st.subheader("Interpretare")

st.markdown("""
Aceste valori **nu reprezintă erori de înregistrare**, ci o caracteristică reală a datelor: 
un produs poate aparține doar la o categorie, două sau toate trei. 

 
Din acest motiv, **înlocuirea valorilor lipsă cu media sau mediana ar fi incorectă**. 
Avem totuși nevoie să tratăm aceste valori înainte de a folosi coloanele.
 
Mai jos sunt prezentate două abordări corecte pentru această situație:
""")

st.subheader("Abordări de tratare")

metoda = st.radio(
    "Selectați metoda de tratare:",
    [
        "Înlocuire cu 0",
        "Eliminarea coloanelor cu valori lipsă",
    ],
)

if metoda == "Înlocuire cu 0":
    df_procesat = df.copy()
    df_procesat["Product_Category_2"] = df_procesat["Product_Category_2"].fillna(0)
    df_procesat["Product_Category_3"] = df_procesat["Product_Category_3"].fillna(0)

    st.markdown(
        "**Metodă aplicată:** `df.fillna(0)` pe `Product_Category_2` și `Product_Category_3`. "
        "Valoarea **0** este folosită ca o categorie sintetică, semnificând *absența unei categorii suplimentare*."
    )

else:
    df_procesat = df.drop(columns=["Product_Category_2", "Product_Category_3"])

    st.markdown(
        "**Metodă aplicată:** `df.drop(columns=['Product_Category_2', 'Product_Category_3'])`. "
        "Cele două coloane au fost eliminate complet din set."
    )


st.subheader("Situația finală")


st.write(f"Total valori lipsă: {df_procesat.isnull().sum().sum()}")
st.write(f"Dimensiune: {df_procesat.shape[0]} rânduri × {df_procesat.shape[1]} coloane")


st.subheader("Concluzie")

st.markdown("""
Faptul că **aproximativ 70% dintre produse aparțin unei singure categorii** este o informație relevantă:
 portofoliul companiei este dominat de produse *care aparțin doar unei categorii*, iar produsele *cu 2 sau 3 categorii* reprezintă o minoritate.
""")

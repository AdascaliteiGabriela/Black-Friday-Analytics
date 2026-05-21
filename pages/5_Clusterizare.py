import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

st.title("Pagina 5: Segmentarea clienților prin clusterizare (KMeans)")

st.markdown("""
Clusterizarea este o tehnică de învățare nesupravegheată care împarte automat un set de observații 
în grupuri (clustere), astfel încât observațiile din același grup să fie cât mai asemănătoare între ele 
și cât mai diferite față de cele din alte grupuri.

În această pagină segmentăm clienții companiei ABC Private Limited folosind algoritmul **KMeans**, 
pe baza a două caracteristici comportamentale: **valoarea totală a cumpărăturilor** și 
**numărul de tranzacții**. Vom împărți baza de clienți în **4 segmente**.
""")

df = pd.read_csv("data/bf_sample.csv")

st.subheader("Agregare la nivel de client")

df_clients = (
    df.groupby("User_ID")
    .agg(Total_Purchase=("Purchase", "sum"), Num_Tranzactii=("Purchase", "count"))
    .reset_index()
)

st.markdown(
    f"După agregarea celor 50.000 de tranzacții la nivel de client, "
    f"obținem **{len(df_clients)} clienți unici**, fiecare cu două caracteristici:"
)

st.dataframe(df_clients.head(10), use_container_width=True, hide_index=True)

st.subheader("Scalarea variabilelor")

st.markdown("""
Cele două variabile au scări diferite (Total_Purchase ajunge la sute de mii, în timp ce numărul de 
tranzacții este sub 110). Aplicăm **StandardScaler** pentru a aduce variabilele la aceeași scară, 
evitând ca Total_Purchase să domine calculul distanțelor euclidiene folosite de KMeans.
""")

X = df_clients[["Total_Purchase", "Num_Tranzactii"]]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

st.subheader("Aplicarea KMeans cu K = 4")

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df_clients["Cluster"] = kmeans.fit_predict(X_scaled)

cluster_size = df_clients["Cluster"].value_counts().sort_index().reset_index()
cluster_size.columns = ["Cluster", "Număr clienți"]

st.markdown("**Distribuția clienților pe clustere:**")
st.dataframe(cluster_size, use_container_width=True, hide_index=True)

cluster_profile = (
    df_clients.groupby("Cluster")
    .agg(
        Medie_Purchase=("Total_Purchase", "mean"),
        Medie_Tranzactii=("Num_Tranzactii", "mean"),
        Numar_Clienti=("User_ID", "count"),
    )
    .round(2)
    .reset_index()
)

st.markdown("**Profilul fiecărui cluster (valori medii):**")
st.dataframe(cluster_profile, use_container_width=True, hide_index=True)

st.subheader("Vizualizare clustere")

fig = px.scatter(
    df_clients,
    x="Total_Purchase",
    y="Num_Tranzactii",
    color="Cluster",
    title="Clusterizarea clienților după Total Purchase și Număr de tranzacții",
    color_continuous_scale="Viridis",
    opacity=0.6,
)
st.plotly_chart(fig, use_container_width=True)


st.subheader("Interpretare")

st.markdown("""
KMeans a identificat patru segmente comportamentale:

- **VIP**: valori mari la ambele dimensiuni — puțini, dar cu impact financiar major;
- **Ocazionali**: valori mici la ambele dimensiuni — numeroși, cheltuieli reduse;
- **Frecvenți cu valoare mică**: multe tranzacții, dar de valoare redusă;
- **Rari cu valoare mare**: puține tranzacții, dar de valoare ridicată.

Această segmentare permite ABC Private Limited să adapteze strategia comercială pentru fiecare 
profil: retenția segmentului VIP, stimularea clienților ocazionali, creșterea valorii medii la 
segmentele intermediare și estimarea Customer Lifetime Value pe segmente.
""")

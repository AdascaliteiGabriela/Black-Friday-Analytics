import streamlit as st

st.title("Analiza comportamentului de cumpărare în campania Black Friday")

st.markdown("""
## Introducere
Această aplicație explorează comportamentul de cumpărare al clienților în cadrul campaniei **Black Friday**, utilizând setul de date pus la dispoziție de **ABC Private Limited**.
Compania activează în domeniul retail-ului și operează în trei categorii de orașe (A, B, C),comercializând produse din peste 20 de categorii. 
Obiectivul analizei este înțelegerea profilului clienților, a tipurilor de produse achiziționate și a valorii cheltuielilor, pentru a susține construirea de oferte personalizate.

Problema și setul de date au fost preluate de pe platforma **Analytics Vidhya**, unde sunt publicate ca parte a unei probleme practice:
[https://datahack.analyticsvidhya.com/contest/black-friday/](https://datahack.analyticsvidhya.com/contest/black-friday/)



## Prezentarea setului de date
Setul de date conține tranzacții care descriu cumpărăturile clienților pentru produse selectate pe parcursul unei luni reprezentative din campania Black Friday.
Fiecare rând reprezintă o tranzacție, un client care a cumpărat un produs. Variabilele includ informații demografice despre client (gen, grupa de vârstă, ocupație, stare civilă, categoria orașului, ani de ședere în orașul curent), informații despre produs (cod produs și până la trei coduri de categorie, anonimizate) și valoarea totală a cumpărături, variabila țintă.

Setul de date original publicat pe Analytics Vidhya este:
- `train.csv` — 550.068 de tranzacții, conține valoarea cumpărăturii;


În cadrul proiectului folosim un eșantion aleatoriu de **50.000 de tranzacții** extras din `train.csv`.
Eșantionul a fost generat în SAS folosind procedura `PROC SURVEYSELECT`, cu un seed fixat, ceea ce asigură reproductibilitatea integrală a selecției.
Același eșantion este folosit atât în codul SAS, cât și în această aplicație Streamlit, ceea ce permite ca rezultatele obținute cu cele două pachete software să fie comparate direct.

## Structura aplicației
Aplicația este organizată ca un proiect Streamlit cu pagini multiple. Fiecare pagină este dedicată unei etape specifice a analizei datelor și combină scurte explicații teoretice cu cod Python aplicat interactiv pe setul de date Black Friday.

Paginile sunt adăugate progresiv pe parcursul proiectului. Pentru navigare, folosiți meniul din partea stângă.
""")

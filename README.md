# Black Friday Analytics — Aplicație Streamlit

Aplicație Python (Streamlit) pentru analiza comportamentului de cumpărare în campania Black Friday.

## Rulare

1. **Activează mediul virtual** (de fiecare dată când deschizi terminal-ul):
   Windows (cmd):

   ```
   venv\Scripts\activate
   ```

   Mac/Linux:

   ```
   source venv/bin/activate
   ```

2. **Pornește aplicația**:

   ```
   streamlit run app.py
   ```

3. **Aplicația se deschide automat** în browser la `http://localhost:8501`.
4. **Pentru oprire**: Ctrl+C în terminal.

## Date

Aplicația folosește un eșantion de 50.000 observații extras în SAS prin `PROC SURVEYSELECT` (seed=12345) din setul original de 550.068 tranzacții.

Fișierul `bf_sample.csv` trebuie să existe în folderul `data/`.

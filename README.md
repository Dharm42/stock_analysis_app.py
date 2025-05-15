
# Streamlit Stock Intelligence Dashboard (No IEX Cloud)

## Setup Instructions

1. Create `.streamlit/secrets.toml` with your keys:
```
[api]
fmp_key = "your_fmp_api_key"
finnhub_key = "your_finnhub_api_key"
openai_key = "your_openai_api_key"
```

2. Install requirements:
```
pip install -r requirements.txt
```

3. Run locally:
```
streamlit run stock_dashboard_app.py
```

4. Deploy via Streamlit Cloud and add your secrets in the Secrets Manager.

## Notes
- IEX Cloud has been fully removed.
- Logos and company profiles are now sourced from FMP.

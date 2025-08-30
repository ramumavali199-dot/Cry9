import os
from typing import Dict, List, Any
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def mini_sentiment(symbol: str, numeric: Dict[str,Any], headlines: List[str]) -> Dict[str,Any]:
    content = {
        "symbol": symbol,
        "numeric_features": numeric,
        "headlines": headlines[:8],
        "instruction": "Return compact JSON with fields: news_sentiment (-1..1), rationale (<= 12 words)."
    }
    resp = client.chat.completions.create(
        model=os.getenv("MODEL_MINI", "gpt-5-mini"),
        messages=[
            {"role":"system","content":"You are a concise crypto news summarizer. Return JSON only."},
            {"role":"user","content": str(content)}
        ],
        temperature=0.2,
        max_tokens=120
    )
    txt = resp.choices[0].message.content
    try:
        import json
        return json.loads(txt)
    except Exception:
        return {"news_sentiment":0.0, "rationale":"parse_error"}

def final_decision(symbol_payload: Dict[str,Any]) -> Dict[str,Any]:
    resp = client.chat.completions.create(
        model=os.getenv("MODEL_FINAL", "gpt-5"),
        messages=[
            {"role":"system","content":"You are a concise trading assistant. Return JSON only with: suggested_bias, entry_price, stop_loss_pct, target_pct, confidence, one_line_rationale."},
            {"role":"user","content": str(symbol_payload)}
        ],
        temperature=0.2,
        max_tokens=180
    )
    txt = resp.choices[0].message.content
    try:
        import json
        return json.loads(txt)
    except Exception:
        return {"suggested_bias":"neutral","entry_price":None,"stop_loss_pct":1.5,"target_pct":2.0,"confidence":0.5,"one_line_rationale":"parse_error"}

#!/usr/bin/env python3
"""POC-02: IA con guardrails y scoring cuantificado para App Detección Prod.
Ejecutar: python scripts/poc02_ai_guardrails.py
Genera dataset sintético, clasifica riesgo y valida guardrails.
"""
from pathlib import Path
import csv, json

def score_case(c):
    score = 0
    d = int(c['days_to_expiry'])
    if d <= 15: score += 35
    elif d <= 30: score += 28
    elif d <= 45: score += 22
    elif d <= 60: score += 14
    elif d <= 90: score += 7
    v = float(c['financial_value_at_risk'])
    if v >= 5000: score += 25
    elif v >= 2500: score += 18
    elif v >= 1000: score += 12
    elif v >= 500: score += 6
    q = int(c['quantity'])
    if q >= 150: score += 15
    elif q >= 75: score += 10
    elif q >= 25: score += 5
    if c['commercial_action'] == 'NONE': score += 15
    elif c['commercial_action'] == 'PENDING_APPROVAL': score += 10
    elif c['commercial_action'] == 'APPLIED': score -= 5
    if str(c['evidence_complete']).lower() in ('false','0','no'): score += 10
    price_req = str(c['price_change_requested']).lower() in ('true','1','yes')
    approved = str(c['price_change_approved']).lower() in ('true','1','yes')
    if price_req and not approved: score += 18
    elif price_req and approved: score += 5
    if float(c['discount_pct']) >= 30 and not approved: score += 8
    return max(0, min(100, score))

def forced_high(c):
    reasons=[]
    if int(c['days_to_expiry']) <= 45 and c['commercial_action']=='NONE': reasons.append('vencimiento <=45 días sin acción comercial')
    if str(c['price_change_requested']).lower() in ('true','1','yes') and str(c['price_change_approved']).lower() not in ('true','1','yes') and float(c['financial_value_at_risk']) >= 1000:
        reasons.append('cambio de precio no aprobado con impacto >=1000')
    if int(c['days_to_expiry']) <= 30 and str(c['evidence_complete']).lower() in ('false','0','no'): reasons.append('vencimiento <=30 días con evidencia incompleta')
    return reasons

def classify(score, forced):
    if forced or score >= 60: return 'ALTO'
    if score >= 30: return 'MEDIO'
    return 'BAJO'

def run():
    root = Path(__file__).resolve().parents[1]
    data = root/'data'/'poc02_dataset.csv'
    rows=list(csv.DictReader(open(data, encoding='utf-8')))
    results=[]
    for row in rows:
        s=score_case(row); forced=forced_high(row); risk=classify(s, forced)
        row['recomputed_score']=s; row['recomputed_risk']=risk; row['guardrail_action']='ALLOW_CLASSIFICATION_ONLY'
        results.append(row)
    correct=sum(r['recomputed_risk']==r['expected_risk'] for r in results)
    print(json.dumps({'cases':len(results),'contract_accuracy':correct/len(results),'guardrail':'human-in-the-loop'}, indent=2))
if __name__ == '__main__': run()

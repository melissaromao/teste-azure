from fastapi import FastAPI, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI()

# ---------------------------------------------------------
# Definindo as 5 métricas solicitadas
# ---------------------------------------------------------
ANALYSIS_TOTAL = Counter(
    "content_analysis_total", 
    "Total de analises de conteudo realizadas"
)
ANALYSIS_ERRORS_TOTAL = Counter(
    "content_analysis_errors_total", 
    "Total de erros em analises de conteudo"
)
ANALYSIS_DURATION_SECONDS = Histogram(
    "content_analysis_duration_seconds", 
    "Duracao da analise de conteudo em segundos"
)
CONTENT_APPROVED_TOTAL = Counter(
    "content_approved_total", 
    "Total de conteudos aprovados"
)
CONTENT_BLOCKED_TOTAL = Counter(
    "content_blocked_total", 
    "Total de conteudos bloqueados"
)

# ---------------------------------------------------------
# Rotas da API
# ---------------------------------------------------------

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Rota para expor as métricas em formato Prometheus
@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

# Exemplo de rota de análise de conteúdo para simular/testar o incremento das métricas
@app.post("/analyze")
def analyze_content(status: str):
    # Incrementa contador de análise total
    ANALYSIS_TOTAL.inc()
    
    with ANALYSIS_DURATION_SECONDS.time():
        if status == "approved":
            CONTENT_APPROVED_TOTAL.inc()
            return {"result": "approved"}
        elif status == "blocked":
            CONTENT_BLOCKED_TOTAL.inc()
            return {"result": "blocked"}
        else:
            ANALYSIS_ERRORS_TOTAL.inc()
            return {"result": "error", "message": "Invalid status"}, 400
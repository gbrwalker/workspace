"""Previsão de quilometragem de frota (MKM).

Pacote desenhado para receber, como entrada, um trio padronizado
``(placa, data, km)`` — saída de qualquer pipeline interno de telemetria —
e devolver previsões úteis para gestão e manutenção:

- ``daily_rate(placa)`` — quilometragem média diária estimada.
- ``predict(placa, data)`` — km esperado em uma data futura.
- ``days_to_km(placa, alvo)`` — quantos dias até bater em um km alvo
  (útil para programar revisão preventiva).
"""

from .model import MKMPredictor

__all__ = ["MKMPredictor"]

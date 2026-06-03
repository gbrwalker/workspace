"""Gerador de telemetria sintética para testes e demonstração.

Reproduz características típicas de uma frota real:

- Veículos com perfis de uso distintos (urbano leve, médio, intensivo).
- Leituras irregulares (nem toda visita à oficina gera leitura).
- Períodos parados (veículo na garagem, em manutenção).
- Pequeno ruído nas leituras (erro de digitação, arredondamento).

Tudo controlado por ``seed`` para resultados reprodutíveis.
"""
from __future__ import annotations

import string
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


def _random_plate(rng: np.random.Generator) -> str:
    """Gera uma placa fictícia no padrão Mercosul (``AAA0A00``)."""
    letters = string.ascii_uppercase
    return (
        "".join(rng.choice(list(letters), 3))
        + str(rng.integers(0, 10))
        + rng.choice(list(letters))
        + str(rng.integers(0, 10))
        + str(rng.integers(0, 10))
    )


def generate_fleet(
    n_vehicles: int = 50,
    start: str = "2024-01-01",
    end: str = "2026-06-01",
    avg_readings_per_month: float = 4.0,
    seed: int = 42,
) -> pd.DataFrame:
    """Gera um histórico de leituras para uma frota fictícia.

    Cada veículo tem uma taxa diária base sorteada, um perfil de variabilidade
    e dias em que o veículo simplesmente não roda. As leituras acontecem em
    datas aleatórias dentro do intervalo, com frequência média configurável.
    """
    rng = np.random.default_rng(seed)
    start_dt = pd.Timestamp(start)
    end_dt = pd.Timestamp(end)
    total_days = (end_dt - start_dt).days

    rows: list[dict] = []
    for _ in range(n_vehicles):
        plate = _random_plate(rng)
        base_rate = float(rng.uniform(40, 300))        # km/dia médio do veículo
        noise_scale = base_rate * rng.uniform(0.08, 0.20)
        idle_prob = float(rng.uniform(0.05, 0.25))     # chance de dia parado
        km0 = float(rng.uniform(5_000, 180_000))       # km no início do histórico

        # Simula km dia-a-dia para obter um odômetro consistente.
        daily_km = np.where(
            rng.random(total_days) < idle_prob,
            0.0,
            np.maximum(0, rng.normal(base_rate, noise_scale, size=total_days)),
        )
        odometer = km0 + np.cumsum(daily_km)

        # Sorteia em quais dias houve leitura, com leve jitter no km registrado.
        target_n = int(rng.poisson(avg_readings_per_month * total_days / 30))
        target_n = max(target_n, 3)
        idx = np.sort(rng.choice(total_days, size=min(target_n, total_days), replace=False))
        for i in idx:
            registered = float(odometer[i] + rng.normal(0, 5))
            rows.append(
                {
                    "placa": plate,
                    "data": (start_dt + timedelta(days=int(i))).date().isoformat(),
                    "km": round(max(registered, 0), 1),
                }
            )

    df = pd.DataFrame(rows)
    return df.sort_values(["placa", "data"]).reset_index(drop=True)


if __name__ == "__main__":
    out = generate_fleet()
    print(out.head())
    print(f"\nlinhas: {len(out)}  veiculos: {out['placa'].nunique()}")

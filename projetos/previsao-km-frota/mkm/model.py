"""Modelo de previsão de quilometragem por veículo (MKM).

A ideia é simples e robusta: para cada placa, ajustamos a relação ``km × tempo``.
Quando há histórico suficiente, usamos uma **regressão linear** (que captura a
tendência e é estável a leituras isoladas com ruído). Quando há poucos pontos,
caímos para a **média de incrementos** (Δkm / Δdias). Veículos novos, sem
histórico próprio, herdam a **taxa mediana da frota**.

Essa hierarquia evita previsões absurdas em corner cases e funciona bem em
operações reais, onde alguns veículos têm meses de leituras e outros chegaram
ontem.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Union

import numpy as np
import pandas as pd


@dataclass
class VehicleProfile:
    """Resumo do comportamento de um veículo, gerado pelo ``fit``."""

    placa: str
    daily_rate: float       # km/dia estimado
    intercept: float        # km na data de referência
    reference_date: pd.Timestamp
    n_readings: int
    strategy: str           # "linear", "incremental", "fleet_median"


@dataclass
class MKMPredictor:
    """Previsor de quilometragem por veículo.

    Use ``fit(df)`` para treinar a partir de leituras históricas e
    ``predict``/``days_to_km``/``daily_rate`` para fazer perguntas ao modelo.
    """

    min_points_linear: int = 4
    profiles_: dict[str, VehicleProfile] = field(default_factory=dict)
    fleet_daily_rate_: float = 0.0

    def fit(self, df: pd.DataFrame) -> "MKMPredictor":
        """Ajusta um modelo por veículo a partir do histórico de leituras."""
        if df.empty:
            raise ValueError("base de treino vazia")

        df = df.sort_values(["placa", "data"])
        rates: list[float] = []

        for placa, group in df.groupby("placa"):
            ref_date = group["data"].iloc[0]
            days = (group["data"] - ref_date).dt.days.to_numpy(dtype=float)
            km = group["km"].to_numpy(dtype=float)
            n = len(group)

            if n >= self.min_points_linear and days.max() > 0:
                rate, intercept = np.polyfit(days, km, 1)
                strategy = "linear"
            elif n >= 2 and days.max() > 0:
                rate = float((km[-1] - km[0]) / days[-1])
                intercept = float(km[0])
                strategy = "incremental"
            else:
                rate = np.nan  # decidido após termos a mediana da frota
                intercept = float(km[-1])
                strategy = "fleet_median"

            self.profiles_[placa] = VehicleProfile(
                placa=str(placa),
                daily_rate=float(rate) if not np.isnan(rate) else 0.0,
                intercept=float(intercept),
                reference_date=pd.Timestamp(ref_date),
                n_readings=n,
                strategy=strategy,
            )
            if not np.isnan(rate) and rate > 0:
                rates.append(float(rate))

        self.fleet_daily_rate_ = float(np.median(rates)) if rates else 0.0
        for p in self.profiles_.values():
            if p.strategy == "fleet_median":
                p.daily_rate = self.fleet_daily_rate_
        return self

    def _profile(self, placa: str) -> VehicleProfile:
        placa = str(placa).strip().upper()
        profile = self.profiles_.get(placa)
        if profile is None:
            raise KeyError(f"placa nao vista no treino: {placa!r}")
        return profile

    def daily_rate(self, placa: str) -> float:
        """Quilometragem média diária estimada para o veículo."""
        return self._profile(placa).daily_rate

    def predict(self, placa: str, data: Union[str, pd.Timestamp]) -> float:
        """Quilometragem esperada para o veículo em uma data."""
        target = pd.Timestamp(data)
        p = self._profile(placa)
        delta_days = (target - p.reference_date).days
        return float(p.intercept + p.daily_rate * delta_days)

    def days_to_km(self, placa: str, km_alvo: float) -> Optional[int]:
        """Quantos dias até o veículo atingir um km alvo (a partir de hoje).

        Retorna ``None`` se o veículo já passou do alvo ou se a taxa é zero
        (sem como projetar).
        """
        p = self._profile(placa)
        today = pd.Timestamp.today().normalize()
        current = self.predict(placa, today)
        if p.daily_rate <= 0:
            return None
        if current >= km_alvo:
            return 0
        return int(np.ceil((km_alvo - current) / p.daily_rate))

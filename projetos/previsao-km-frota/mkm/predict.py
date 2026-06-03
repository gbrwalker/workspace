"""CLI: faz uma previsão pontual com um modelo já treinado.

Exemplos:

    python -m mkm.predict --placa ABC1A23 --data 2026-12-31
    python -m mkm.predict --placa ABC1A23 --km-alvo 200000
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import joblib

DEFAULT_MODEL = Path(__file__).resolve().parent.parent / "reports" / "mkm_model.joblib"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Previsao de quilometragem")
    parser.add_argument("--placa", required=True, help="placa do veiculo (ex: ABC1A23)")
    parser.add_argument("--data", help="data alvo (YYYY-MM-DD)")
    parser.add_argument("--km-alvo", type=float, help="km de revisao a estimar")
    parser.add_argument("--modelo", default=str(DEFAULT_MODEL))
    args = parser.parse_args(argv)

    if not args.data and args.km_alvo is None:
        parser.error("informe --data ou --km-alvo")

    model_path = Path(args.modelo)
    if not model_path.exists():
        parser.error(f"modelo nao encontrado em {model_path}. rode 'python -m mkm.train' primeiro.")

    model = joblib.load(model_path)
    placa = args.placa.strip().upper()

    rate = model.daily_rate(placa)
    print(f"placa            : {placa}")
    print(f"km medio diario  : {rate:.1f}")

    if args.data:
        km = model.predict(placa, args.data)
        print(f"km previsto em {args.data} : {km:,.0f}".replace(",", "."))
    if args.km_alvo is not None:
        dias = model.days_to_km(placa, args.km_alvo)
        if dias is None:
            print(f"km alvo {args.km_alvo:,.0f} : sem previsao (taxa zero)".replace(",", "."))
        else:
            print(f"dias ate atingir {args.km_alvo:,.0f} km : {dias}".replace(",", "."))
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Gom kết quả của lstm_ecommerce.ipynb và lstm_stock.ipynb thành ../slides/data/lstm_vs_rnn.json cho slide.

Chạy sau khi đã chạy 2 notebook:  python export_slide_data.py
"""
import json
import math
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE.parent / 'slides' / 'data' / 'lstm_vs_rnn.json'
CELLS = ['RNN', 'LSTM']


def clean(x):
    """Làm tròn số và bỏ NaN (JSON của Vite không đọc được NaN)."""
    if isinstance(x, float):
        return None if math.isnan(x) else round(x, 6)
    if isinstance(x, dict):
        return {k: clean(v) for k, v in x.items()}
    if isinstance(x, list):
        return [clean(v) for v in x]
    return x


def summary(res, keys, extra=()):
    per_seed = {cell: [r for r in res['per_seed'] if r['model'] == cell] for cell in CELLS}
    return {
        'seeds': res['config']['seeds'],
        'mean': {cell: {k: res['mean'][cell][k] for k in keys} for cell in CELLS},
        'std': {cell: {k: res['std'][cell][k] for k in keys} for cell in CELLS},
        'per_seed': {cell: {k: [r[k] for r in per_seed[cell]] for k in list(keys) + ['val_loss', 'best_epoch', *extra]} for cell in CELLS},
        'lstm_wins': {k: res['lstm_wins'][k] for k in keys if k in res['lstm_wins']},
        'params': {cell: res['cost'][cell]['trainable parameters'] for cell in CELLS},
        's_per_epoch': {cell: res['cost'][cell]['s / epoch (mean)'] for cell in CELLS},
        'config': res['config'],
    }


ecom = json.loads((HERE / 'results' / 'lstm_ecommerce.json').read_text())
stock = json.loads((HERE / 'results' / 'lstm_stock.json').read_text())

sweep = stock['window_sweep']['per_run']
windows = sorted({r['window'] for r in sweep})

data = {
    'ecommerce': summary(ecom, ['accuracy', 'ROC-AUC', 'MCC', 'macro F1', 'recall refunded', 'log loss']),
    'stock': summary(stock, ['MAE', 'RMSE', 'R2 log', 'direction acc']) | {
        'sensitivity_rel': stock['sensitivity_seed42_relative_to_day60'],
        'reach': stock['reach'],
        'mae_by_k': stock['mae_by_k_seed42'],
        'window_sweep': {
            'windows': windows,
            'seeds': list(dict.fromkeys(r['seed'] for r in sweep)),
            'mae': {cell: [[r['MAE'] for r in sweep if r['model'] == cell and r['window'] == w] for w in windows] for cell in CELLS},
        },
    },
}
OUT.write_text(json.dumps(clean(data), ensure_ascii=False, indent=1), encoding='utf-8')
print('saved', OUT.resolve())

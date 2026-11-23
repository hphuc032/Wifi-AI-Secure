# Module interface contract

This document defines the initial integration boundary. It is deliberately small; update it through a PR if the team agrees on a change.

## 1. Data pipeline output

Hoàng Phúc owns the implementation. The pipeline must expose a reproducible transformation that returns:

- `X_train`, `X_valid`, `X_test`: numeric feature matrices with identical column order.
- `y_train`, `y_valid`, `y_test`: labels using one documented canonical label mapping.
- `feature_names`: ordered list of feature names.
- `metadata`: dataset version/source, input file identifiers, label mapping, split strategy/seed, preprocessing version and excluded columns.

Do not assume the dataset's label column or attack names until verified against the actual AWID3 files.

Suggested Python interface:

```python
def build_dataset(config: dict):
    """Return (X_train, X_valid, X_test, y_train, y_valid, y_test, metadata)."""
```

The data owner must serialize the fitted preprocessing object and feature order together with the model-compatible metadata. Never fit scalers/encoders using validation or test data.

## 2. Model interface

Quốc Đạt owns model training and inference. All supervised models should expose the same prediction shape:

```python
class Predictor:
    def predict(self, features):
        """Return one prediction record per input row."""
```

Canonical prediction record:

```json
{
  "predicted_label": "NORMAL",
  "confidence": 0.91,
  "model_name": "random_forest",
  "model_version": "0.1.0"
}
```

- `predicted_label` is a canonical class label, not a free-form explanation.
- `confidence` is optional for models that cannot provide a calibrated probability. Do not fabricate it.
- Anomaly scores from Isolation Forest must use a separate `anomaly_score` field and document score direction/range.
- A prediction is not automatically an alert. Alert policy belongs to the application layer and must be configurable.

## 3. Application event contract

Tiến Đạt owns the API, database and dashboard. The app consumes predictions and stores a detection event:

```json
{
  "event_id": "generated-by-app",
  "timestamp": "2026-01-01T00:00:00Z",
  "source": "awid3_offline",
  "predicted_label": "Deauth",
  "confidence": 0.91,
  "model_name": "random_forest",
  "model_version": "0.1.0",
  "alert": true,
  "details": {}
}
```

The timestamp and event ID are application-generated. The `source` field must distinguish offline dataset replay from authorized live capture. Alert thresholds and class severity must be documented/configurable.

## 4. Shared rules

- Use UTF-8 and explicit timezone-aware ISO-8601 timestamps.
- Use canonical snake_case field names.
- Reject missing or unexpected feature columns rather than silently reordering or filling them without a documented policy.
- Add contract tests with small synthetic fixtures.
- Never commit credentials, private captures, raw dataset files, or model binaries without explicit team approval.

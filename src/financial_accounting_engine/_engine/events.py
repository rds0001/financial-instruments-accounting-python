# Copyright 2026 RiskDataScience GmbH
# SPDX-License-Identifier: Apache-2.0
def process_event(event: dict, instrument: dict) -> dict:
    if not event.get("approved"):
        raise ValueError(f"Nicht freigegebenes Ereignis: {event['event_id']}")
    kind = event["event_type"]
    result = {
        "event_id": event["event_id"],
        "instrument_id": event["instrument_id"],
        "event_type": kind,
        "amount": float(event.get("amount") or 0),
        "derecognition_result": "NOT_APPLICABLE",
        "continuing_involvement": 0.0,
        "modification_result": 0.0,
        "pnl_effect": 0.0,
        "reason_code": event["reason_code"],
        "formula_id": None,
    }
    if kind == "ASSET_MODIFICATION_NO_DERECOGNITION":
        if event.get("derecognition_approved"):
            raise ValueError("Modifikationsstatus widersprüchlich")
        result.update(
            {
                "derecognition_result": "NO_DERECOGNITION",
                "modification_result": float(event["modified_present_value"])
                - float(instrument["gross_amount"]),
                "formula_id": "F-MOD-001",
            }
        )
        result["pnl_effect"] = result["modification_result"]
    elif kind == "ASSET_MODIFICATION_DERECOGNITION":
        if not event.get("derecognition_approved"):
            raise ValueError("Asset-Derecognition nicht freigegeben")
        result.update(
            {
                "derecognition_result": "DERECOGNISED_AND_NEW_RECOGNITION",
                "modification_result": float(event["modified_present_value"])
                - float(instrument["gross_amount"]),
                "formula_id": "F-MOD-001",
            }
        )
        result["pnl_effect"] = result["modification_result"]
    elif kind in {
        "LIABILITY_MODIFICATION_DERECOGNITION",
        "LIABILITY_MODIFICATION_NO_DERECOGNITION",
    }:
        substantial = (
            bool(event.get("qualitative_substantial"))
            or float(event.get("ten_percent_ratio") or 0) >= 0.10
        )
        expected_derecognition = kind == "LIABILITY_MODIFICATION_DERECOGNITION"
        if expected_derecognition != substantial or expected_derecognition != bool(
            event.get("derecognition_approved")
        ):
            raise ValueError("Liability-Modifikation widerspricht 10%-/Qualitativtest")
        result.update(
            {
                "derecognition_result": "DERECOGNISED_AND_NEW_RECOGNITION"
                if substantial
                else "NO_DERECOGNITION",
                "modification_result": float(event["modified_present_value"])
                - float(instrument["gross_amount"]),
                "formula_id": "F-MOD-001",
            }
        )
        result["pnl_effect"] = -result["modification_result"]
    elif kind == "ASSET_TRANSFER":
        if event.get("pass_through_arrangement") is False:
            raise ValueError("Pass-through-Kriterien ausdrücklich nicht erfüllt")
        if event.get("risks_rewards_transferred"):
            decision = "FULL_DERECOGNITION"
        elif event.get("risks_rewards_retained"):
            decision = "NO_DERECOGNITION"
        elif event.get("control_retained"):
            decision = "CONTINUING_INVOLVEMENT"
            result["continuing_involvement"] = float(
                event.get("continuing_involvement_amount") or 0
            )
        else:
            decision = "FULL_DERECOGNITION_CONTROL_LOST"
        if event.get("partial_transfer") and float(event.get("amount") or 0) <= 0:
            raise ValueError("Teilübertragung ohne übertragenen Betrag")
        result.update({"derecognition_result": decision, "formula_id": "F-DEREC-001"})
    elif kind == "WRITEOFF":
        result.update(
            {"derecognition_result": "WRITEOFF", "pnl_effect": 0.0, "formula_id": "F-WO-001"}
        )
    elif kind == "RECOVERY":
        result.update(
            {
                "derecognition_result": "POST_WRITEOFF_RECOVERY",
                "pnl_effect": float(event["amount"]),
                "formula_id": "F-REC-001",
            }
        )
    else:
        raise ValueError(f"Unbekannter Eventtyp: {kind}")
    return result

# Copyright 2026 RiskDataScience GmbH
# SPDX-License-Identifier: Apache-2.0
def allowance_journals(
    ecl_results: list[dict],
    opening: dict[str, float],
    classifications: dict[str, str] | None = None,
    instruments: dict[str, dict] | None = None,
) -> list[dict]:
    journals = []
    classifications, instruments = classifications or {}, instruments or {}
    for result in ecl_results:
        movement = float(result["final_ecl"]) - float(opening.get(result["instrument_id"], 0))
        if abs(movement) < 1e-12:
            continue
        iid = result["instrument_id"]
        instrument_type = instruments.get(iid, {}).get("instrument_type")
        if classifications.get(iid) == "FVOCI_DEBT":
            allowance_account = "FVOCI_ACCUMULATED_IMPAIRMENT_OCI"
        elif instrument_type in {"FINANCIAL_GUARANTEE", "LOAN_COMMITMENT"}:
            allowance_account = "ECL_PROVISION_OFF_BALANCE"
        else:
            allowance_account = "LOSS_ALLOWANCE"
        journals.extend(
            [
                {
                    "journal_batch_id": f"ECL-{result['instrument_id']}",
                    "instrument_id": result["instrument_id"],
                    "account": "ECL_EXPENSE",
                    "debit": max(movement, 0),
                    "credit": max(-movement, 0),
                    "movement_type": "ECL_REMEASUREMENT",
                },
                {
                    "journal_batch_id": f"ECL-{result['instrument_id']}",
                    "instrument_id": result["instrument_id"],
                    "account": allowance_account,
                    "debit": max(-movement, 0),
                    "credit": max(movement, 0),
                    "movement_type": "ECL_REMEASUREMENT",
                },
            ]
        )
    return journals


def event_journals(events: list[dict]) -> list[dict]:
    journals = []
    for event in events:
        batch = f"EVT-{event['event_id']}"
        amount = abs(float(event.get("amount") or 0))
        kind = event["event_type"]
        if kind == "WRITEOFF" and amount:
            journals += [
                {
                    "journal_batch_id": batch,
                    "instrument_id": event["instrument_id"],
                    "account": "LOSS_ALLOWANCE",
                    "debit": amount,
                    "credit": 0,
                    "movement_type": "WRITEOFF",
                },
                {
                    "journal_batch_id": batch,
                    "instrument_id": event["instrument_id"],
                    "account": "GROSS_CARRYING_AMOUNT",
                    "debit": 0,
                    "credit": amount,
                    "movement_type": "WRITEOFF",
                },
            ]
        elif kind == "RECOVERY" and amount:
            journals += [
                {
                    "journal_batch_id": batch,
                    "instrument_id": event["instrument_id"],
                    "account": "CASH",
                    "debit": amount,
                    "credit": 0,
                    "movement_type": "RECOVERY",
                },
                {
                    "journal_batch_id": batch,
                    "instrument_id": event["instrument_id"],
                    "account": "RECOVERY_INCOME",
                    "debit": 0,
                    "credit": amount,
                    "movement_type": "RECOVERY",
                },
            ]
        elif (
            kind == "ASSET_MODIFICATION_NO_DERECOGNITION"
            and abs(float(event["modification_result"])) > 1e-12
        ):
            value = float(event["modification_result"])
            debit = max(value, 0)
            credit = max(-value, 0)
            journals += [
                {
                    "journal_batch_id": batch,
                    "instrument_id": event["instrument_id"],
                    "account": "GROSS_CARRYING_AMOUNT",
                    "debit": debit,
                    "credit": credit,
                    "movement_type": "MODIFICATION",
                },
                {
                    "journal_batch_id": batch,
                    "instrument_id": event["instrument_id"],
                    "account": "MODIFICATION_PNL",
                    "debit": credit,
                    "credit": debit,
                    "movement_type": "MODIFICATION",
                },
            ]
        elif (
            kind
            in {
                "ASSET_MODIFICATION_DERECOGNITION",
                "LIABILITY_MODIFICATION_DERECOGNITION",
                "LIABILITY_MODIFICATION_NO_DERECOGNITION",
            }
            and abs(float(event["modification_result"])) > 1e-12
        ):
            value = float(event["pnl_effect"])
            debit = max(-value, 0)
            credit = max(value, 0)
            journals += [
                {
                    "journal_batch_id": batch,
                    "instrument_id": event["instrument_id"],
                    "account": "MODIFICATION_OR_DERECOGNITION_PNL",
                    "debit": debit,
                    "credit": credit,
                    "movement_type": "MODIFICATION_DERECOGNITION",
                },
                {
                    "journal_batch_id": batch,
                    "instrument_id": event["instrument_id"],
                    "account": "FINANCIAL_INSTRUMENT_CARRYING_AMOUNT",
                    "debit": credit,
                    "credit": debit,
                    "movement_type": "MODIFICATION_DERECOGNITION",
                },
            ]
        elif kind == "ASSET_TRANSFER" and event["derecognition_result"] != "NO_DERECOGNITION":
            transferred = max(amount - float(event.get("continuing_involvement") or 0), 0)
            if transferred:
                journals += [
                    {
                        "journal_batch_id": batch,
                        "instrument_id": event["instrument_id"],
                        "account": "TRANSFER_CONSIDERATION_RECEIVABLE",
                        "debit": transferred,
                        "credit": 0,
                        "movement_type": "ASSET_DERECOGNITION",
                    },
                    {
                        "journal_batch_id": batch,
                        "instrument_id": event["instrument_id"],
                        "account": "GROSS_CARRYING_AMOUNT",
                        "debit": 0,
                        "credit": transferred,
                        "movement_type": "ASSET_DERECOGNITION",
                    },
                ]
    return journals


def own_credit_journals(results: list[dict]) -> list[dict]:
    journals = []
    for row in results:
        own = float(row["own_credit_oci"])
        pnl = float(row["other_fv_change_pnl"])
        total = own + pnl
        if abs(own) + abs(pnl) < 1e-12:
            continue
        batch = f"OWNCR-{row['instrument_id']}"
        journals += [
            {
                "journal_batch_id": batch,
                "instrument_id": row["instrument_id"],
                "account": "FVTPL_LIABILITY",
                "debit": max(-total, 0),
                "credit": max(total, 0),
                "movement_type": "FAIR_VALUE_CHANGE",
            },
            {
                "journal_batch_id": batch,
                "instrument_id": row["instrument_id"],
                "account": "OWN_CREDIT_OCI",
                "debit": max(own, 0),
                "credit": max(-own, 0),
                "movement_type": "OWN_CREDIT",
            },
            {
                "journal_batch_id": batch,
                "instrument_id": row["instrument_id"],
                "account": "FV_CHANGE_PNL",
                "debit": max(pnl, 0),
                "credit": max(-pnl, 0),
                "movement_type": "FAIR_VALUE_CHANGE",
            },
        ]
    return journals


def hedge_journals(results: list[dict]) -> list[dict]:
    journals = []
    for row in results:
        ineffective = float(row.get("ineffectiveness_pnl") or 0)
        oci = float(row.get("oci_effective") or 0)
        costs = float(row.get("cost_of_hedging_reserve") or 0)
        # Reference journal presents each component with an offsetting hedge valuation account.
        for suffix, account, value in [
            ("INEFF", "HEDGE_INEFFECTIVENESS_PNL", ineffective),
            ("OCI", "HEDGE_RESERVE_OCI", oci),
            ("COH", "COST_OF_HEDGING_OCI", costs),
            ("RECYCLE", "HEDGE_RESERVE_OCI", -float(row.get("recycle_amount") or 0)),
            ("BASIS", "HEDGE_RESERVE_OCI", -float(row.get("basis_adjustment") or 0)),
        ]:
            if abs(value) < 1e-12:
                continue
            batch = f"HDG-{row['relationship_id']}-{suffix}"
            debit = max(-value, 0)
            credit = max(value, 0)
            journals += [
                {
                    "journal_batch_id": batch,
                    "instrument_id": row["relationship_id"],
                    "account": account,
                    "debit": debit,
                    "credit": credit,
                    "movement_type": "HEDGE_ACCOUNTING",
                },
                {
                    "journal_batch_id": batch,
                    "instrument_id": row["relationship_id"],
                    "account": "HEDGE_RECYCLING_PNL"
                    if suffix == "RECYCLE"
                    else "NONFINANCIAL_ASSET_BASIS"
                    if suffix == "BASIS"
                    else "HEDGE_VALUATION_OFFSET",
                    "debit": credit,
                    "credit": debit,
                    "movement_type": "HEDGE_ACCOUNTING",
                },
            ]
    return journals

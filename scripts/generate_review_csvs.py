"""
Generate 4 expert review CSV files for the data-audit directory.

CSV 1: review_culture.csv   — GOS_ONLY cultures with fuzzy match suggestions
CSV 2: review_originator.csv — originators needing review (not EXACT)
CSV 3: review_sort.csv       — NO_MATCH sorts with dominant region status
CSV 4: review_duplicates.csv — duplicate registration_number applications
"""

import csv
import sys
import os
import difflib
from collections import defaultdict

import psycopg2
import psycopg2.extras

# ---------------------------------------------------------------------------
# Connection helpers
# ---------------------------------------------------------------------------

GOS_DSN = "host=localhost port=5432 dbname=gosreestr user=gosreestr password=gosreestr"
PAT_DSN = "host=localhost port=5432 dbname=patent user=admin password=qwe1daSjewspds12"

OUT_DIR = "/Users/nuralisagyndykuly/patent_new/docs/data-audit"
SRC_DIR = "/Users/nuralisagyndykuly/patent_new/docs/data-audit"


def gos_conn():
    return psycopg2.connect(GOS_DSN, cursor_factory=psycopg2.extras.DictCursor)


def pat_conn():
    return psycopg2.connect(PAT_DSN, cursor_factory=psycopg2.extras.DictCursor)


# ---------------------------------------------------------------------------
# CSV 1 — review_culture.csv
# ---------------------------------------------------------------------------

def build_review_culture():
    print("Building review_culture.csv ...")

    # Load GOS_ONLY rows from mapping_culture.csv
    mapping_path = os.path.join(SRC_DIR, "mapping_culture.csv")
    gos_only_rows = []
    with open(mapping_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["match_type"].strip() == "GOS_ONLY":
                gos_only_rows.append(row)

    print(f"  GOS_ONLY cultures in mapping: {len(gos_only_rows)}")

    # Fetch live data from Gosreestr for those IDs
    gos_ids = [int(r["gos_id"]) for r in gos_only_rows if r["gos_id"]]
    gos_data = {}
    with gos_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT rc.id, rc.name, rcg.name AS group_name, rc.is_winter
                FROM registry_culture rc
                JOIN registry_culturegroup rcg ON rcg.id = rc.group_id
                WHERE rc.id = ANY(%s)
                ORDER BY rc.id
            """, (gos_ids,))
            for row in cur.fetchall():
                gos_data[row["id"]] = dict(row)

    # Fetch all Patents cultures for fuzzy matching
    pat_cultures = []
    with pat_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, name
                FROM patents_culture
                WHERE is_deleted = false
                ORDER BY id
            """)
            pat_cultures = [(row["id"], row["name"]) for row in cur.fetchall()]

    pat_names = [name for _, name in pat_cultures]

    out_path = os.path.join(OUT_DIR, "review_culture.csv")
    fieldnames = [
        "gos_id", "gos_name", "gos_group", "gos_is_winter",
        "suggested_patents_id", "suggested_patents_name",
        "expert_decision", "expert_patents_id",
    ]

    written = 0
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in gos_only_rows:
            gos_id = int(row["gos_id"]) if row["gos_id"] else None
            if gos_id is None:
                continue

            live = gos_data.get(gos_id)
            if live:
                gos_name = live["name"]
                gos_group = live["group_name"]
                gos_is_winter = live["is_winter"]
            else:
                # Fall back to mapping CSV values
                gos_name = row["gos_name"]
                gos_group = row["gos_group"]
                gos_is_winter = row["gos_is_winter"]

            # Fuzzy match: find best match in patents_culture
            matches = difflib.get_close_matches(
                gos_name.lower(), [n.lower() for n in pat_names],
                n=1, cutoff=0.0
            )
            sugg_id = ""
            sugg_name = ""
            if matches:
                # Map back to original case / id
                matched_lower = matches[0]
                for pid, pname in pat_cultures:
                    if pname.lower() == matched_lower:
                        sugg_id = pid
                        sugg_name = pname
                        break
            else:
                # Use SequenceMatcher directly to always find best
                best_ratio = -1
                for pid, pname in pat_cultures:
                    ratio = difflib.SequenceMatcher(
                        None, gos_name.lower(), pname.lower()
                    ).ratio()
                    if ratio > best_ratio:
                        best_ratio = ratio
                        sugg_id = pid
                        sugg_name = pname

            writer.writerow({
                "gos_id": gos_id,
                "gos_name": gos_name,
                "gos_group": gos_group,
                "gos_is_winter": gos_is_winter,
                "suggested_patents_id": sugg_id,
                "suggested_patents_name": sugg_name,
                "expert_decision": "",
                "expert_patents_id": "",
            })
            written += 1

    print(f"  Written {written} rows -> {out_path}")


# ---------------------------------------------------------------------------
# CSV 2 — review_originator.csv
# ---------------------------------------------------------------------------

REVIEW_MATCH_TYPES = {"AUTO_HIGH", "AUTO_MEDIUM", "FUZZY_LOW", "NO_MATCH"}

MATCH_TYPE_ORDER = {
    "AUTO_HIGH": 0,
    "AUTO_MEDIUM": 1,
    "FUZZY_LOW": 2,
    "NO_MATCH": 3,
}


def build_review_originator():
    print("Building review_originator.csv ...")

    src_path = os.path.join(SRC_DIR, "mapping_originator.csv")
    rows = []
    with open(src_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mt = row.get("match_type", "").strip()
            if mt in REVIEW_MATCH_TYPES:
                rows.append(row)

    # Sort by match_type priority
    rows.sort(key=lambda r: MATCH_TYPE_ORDER.get(r.get("match_type", "").strip(), 99))

    out_path = os.path.join(OUT_DIR, "review_originator.csv")
    fieldnames = [
        "gos_id", "gos_name",
        "suggested_patents_id", "suggested_patents_name",
        "similarity", "match_type",
        "expert_decision", "expert_patents_id",
    ]

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "gos_id": row.get("gos_id", ""),
                "gos_name": row.get("gos_name", ""),
                "suggested_patents_id": row.get("patents_id", ""),
                "suggested_patents_name": row.get("patents_name", ""),
                "similarity": row.get("similarity", ""),
                "match_type": row.get("match_type", ""),
                "expert_decision": "",
                "expert_patents_id": "",
            })

    print(f"  Written {len(rows)} rows -> {out_path}")


# ---------------------------------------------------------------------------
# CSV 3 — review_sort.csv
# ---------------------------------------------------------------------------

def build_review_sort():
    print("Building review_sort.csv ...")

    src_path = os.path.join(SRC_DIR, "mapping_sort.csv")
    no_match_rows = []
    with open(src_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("match_type", "").strip() == "NO_MATCH":
                no_match_rows.append(row)

    print(f"  NO_MATCH sorts: {len(no_match_rows)}")

    # Build lookup of dominant region status per application id
    app_ids = [int(r["gos_app_id"]) for r in no_match_rows if r["gos_app_id"]]
    dominant_status = {}

    with gos_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT a.id, ar.status, count(*) AS cnt
                FROM registry_application a
                JOIN registry_applicationregion ar ON ar.application_id = a.id
                WHERE a.id = ANY(%s)
                GROUP BY a.id, ar.status
                ORDER BY a.id, count(*) DESC
            """, (app_ids,))
            # Keep only the dominant (first) status per app id
            seen = set()
            for row in cur.fetchall():
                aid = row["id"]
                if aid not in seen:
                    dominant_status[aid] = row["status"]
                    seen.add(aid)

    out_path = os.path.join(OUT_DIR, "review_sort.csv")
    fieldnames = [
        "gos_app_id", "gos_reg_number", "gos_variety",
        "gos_culture", "gos_group",
        "best_patents_name", "best_similarity",
        "dominant_region_status",
        "expert_decision", "expert_patents_sort_id", "target_status",
    ]

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in no_match_rows:
            app_id = int(row["gos_app_id"]) if row["gos_app_id"] else None
            writer.writerow({
                "gos_app_id": row.get("gos_app_id", ""),
                "gos_reg_number": row.get("gos_reg_number", ""),
                "gos_variety": row.get("gos_variety", ""),
                "gos_culture": row.get("gos_culture", ""),
                "gos_group": row.get("gos_group", ""),
                "best_patents_name": row.get("patents_sort_name", ""),
                "best_similarity": row.get("similarity", ""),
                "dominant_region_status": dominant_status.get(app_id, "") if app_id else "",
                "expert_decision": "",
                "expert_patents_sort_id": "",
                "target_status": "",
            })

    print(f"  Written {len(no_match_rows)} rows -> {out_path}")


# ---------------------------------------------------------------------------
# CSV 4 — review_duplicates.csv
# ---------------------------------------------------------------------------

def build_review_duplicates():
    print("Building review_duplicates.csv ...")

    with gos_conn() as conn:
        with conn.cursor() as cur:
            # Find duplicate registration numbers
            cur.execute("""
                SELECT registration_number
                FROM registry_application
                WHERE registration_number != ''
                GROUP BY registration_number
                HAVING count(*) > 1
                ORDER BY registration_number
            """)
            dup_numbers = [row["registration_number"] for row in cur.fetchall()]

            print(f"  Duplicate registration_numbers found: {len(dup_numbers)}")

            if not dup_numbers:
                print("  No duplicates — writing empty file.")

            # Fetch all rows for those registration numbers with culture name
            cur.execute("""
                SELECT
                    a.registration_number,
                    a.id AS gos_app_id,
                    a.variety,
                    rc.name AS culture,
                    a.receipt_date
                FROM registry_application a
                JOIN registry_culture rc ON rc.id = a.culture_id
                WHERE a.registration_number = ANY(%s)
                ORDER BY a.registration_number, a.id
            """, (dup_numbers,))
            dup_rows = cur.fetchall()

    out_path = os.path.join(OUT_DIR, "review_duplicates.csv")
    fieldnames = [
        "registration_number", "gos_app_id", "variety",
        "culture", "receipt_date", "expert_decision",
    ]

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in dup_rows:
            writer.writerow({
                "registration_number": row["registration_number"],
                "gos_app_id": row["gos_app_id"],
                "variety": row["variety"],
                "culture": row["culture"],
                "receipt_date": row["receipt_date"],
                "expert_decision": "",
            })

    print(f"  Written {len(dup_rows)} rows -> {out_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    errors = []

    for fn in [
        build_review_culture,
        build_review_originator,
        build_review_sort,
        build_review_duplicates,
    ]:
        try:
            fn()
        except Exception as exc:
            msg = f"ERROR in {fn.__name__}: {exc}"
            print(msg, file=sys.stderr)
            errors.append(msg)

    if errors:
        print("\nCompleted with errors:")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    else:
        print("\nAll 4 review CSVs generated successfully.")

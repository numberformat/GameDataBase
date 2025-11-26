import argparse
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
OUT_BASE = ROOT_DIR / "data" / "3nf"

CORE_COLS = {
    "ID": "game_id",
    "Screen title @ Exact": "screen_title",
    "Cover title @ Exact": "cover_title",
    "Release date": "release_date",
    "MD5": "md5",
    "SHA1": "sha1",
    "SHA256": "sha256",
    "SHA512": "sha512",
}

REL_COLS = {
    "Developer": ("developers", "developer_id", "name"),
    "Publisher": ("publishers", "publisher_id", "name"),
    "Tags": ("tags", "tag_id", "tag_name"),
    "Region": ("regions", "region_id", "region_name"),
}

def split_multi(value):
    if pd.isna(value):
        return []
    return [v.strip() for v in str(value).split(",") if v.strip()]

def split_title(value):
    """Fix 1NF issue: split multilingual screen titles"""
    if pd.isna(value):
        return None, None
    if "@" in value:
        left, right = value.split("@", 1)
        return left.strip(), right.strip()
    return value.strip(), None

def normalize_one(csv_name: str):
    upstream = ROOT_DIR / csv_name
    system = Path(csv_name).stem

    out_dir = OUT_BASE / system
    junc_dir = out_dir / "junctions"
    out_dir.mkdir(parents=True, exist_ok=True)
    junc_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(upstream)

    # ---- Build core table dynamically ----
    present_core = {k: v for k, v in CORE_COLS.items() if k in df.columns}
    games_raw = df[list(present_core.keys())].rename(columns=present_core)

    # ---- Fix 1NF issues in title fields ----
    if "screen_title" in games_raw.columns:
        titles = games_raw["screen_title"].apply(split_title)
        games_raw["screen_title_en"] = titles.apply(lambda x: x[0])
        games_raw["screen_title_native"] = titles.apply(lambda x: x[1])
        games_raw = games_raw.drop(columns=["screen_title"])

    if "cover_title" in games_raw.columns:
        titles = games_raw["cover_title"].apply(split_title)
        games_raw["cover_title_en"] = titles.apply(lambda x: x[0])
        games_raw["cover_title_native"] = titles.apply(lambda x: x[1])
        games_raw = games_raw.drop(columns=["cover_title"])

    games = games_raw

    # ---- Dynamic dimension sets ----
    dim_sets = {k: set() for k in REL_COLS.keys()}

    for _, row in df.iterrows():
        for col in REL_COLS:
            if col in df.columns:
                dim_sets[col].update(split_multi(row[col]))

    # ---- Dimension + lookup maps ----
    dim_tables = {}
    dim_maps = {}

    for col, (table, id_col, name_col) in REL_COLS.items():
        if col not in df.columns:
            continue

        rows = sorted(dim_sets[col])
        tdf = pd.DataFrame(rows, columns=[name_col])
        tdf[id_col] = tdf.index + 1

        dim_tables[col] = tdf
        dim_maps[col] = dict(zip(tdf[name_col], tdf[id_col]))

        tdf.to_csv(out_dir / f"{table}.csv", index=False)

    # ---- Junction tables ----
    for col, (table, id_col, _) in REL_COLS.items():
        if col not in df.columns:
            continue

        mapping = dim_maps[col]
        rows = []

        for _, row in df.iterrows():
            gid = row["ID"]
            for val in split_multi(row[col]):
                rows.append({
                    "game_id": gid,
                    id_col: mapping[val]
                })

        pd.DataFrame(rows).to_csv(junc_dir / f"game_{table}.csv", index=False)

    # ---- Column ordering (keep titles up front) ----
    preferred_order = [
        "game_id",
        "screen_title_en",
        "screen_title_native",
        "cover_title_en",
        "cover_title_native",
        "release_date",
        "md5",
        "sha1",
        "sha256",
        "sha512",
    ]

    existing = [c for c in preferred_order if c in games_raw.columns]
    remaining = [c for c in games_raw.columns if c not in existing]

    games = games_raw[existing + remaining]

    # ---- Write core game table ----
    games.to_csv(out_dir / "games.csv", index=False)

    print(f"✅ Normalized with title split: {csv_name}")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--file", required=True)
    args = p.parse_args()
    normalize_one(args.file)

if __name__ == "__main__":
    main()

import os, csv, datetime
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


load_dotenv()


url = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
engine = create_engine(url, pool_pre_ping=True)


ALLOWED = {"TR", "US", "UK", "DE", "FR", "JP", "BR", "RU"}
FALLBACK_REGION = "UNK"  


def detect_delimiter(path: str) -> str:
    
    with open(path, "r", encoding="utf-8") as f:
        first = f.readline()
    return "\t" if "\t" in first else ","

def parse_ts(s: str | None):

    if not s or not str(s).strip():
        return None
    s = str(s).strip()


    if s.isdigit():
        try:
            return datetime.datetime.utcfromtimestamp(int(s))
        except Exception:
            return None


    try:
        date_part, time_part = s.split(" ")
        if len(time_part.split(":")[0]) == 1:
            time_part = "0" + time_part
        return datetime.datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M:%S")
    except Exception:
        return None


def main():
    path = "clan_sample_data.csv"
    delim = detect_delimiter(path)
    print(f"[loader] delimiter = {repr(delim)}")

    inserted, skipped = 0, 0

    with engine.begin() as conn, open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=delim)

        for r in reader:
            name = (r.get("name") or "").strip()
            if not name:
                skipped += 1
                continue

            region_raw = (r.get("region") or "").strip().upper()
            region = region_raw if region_raw in ALLOWED else FALLBACK_REGION
            created_at = parse_ts(r.get("created_at")) or datetime.datetime.utcnow()
            description = f"Auto-loaded sample for {name}"

          
            conn.execute(
                text("""
                    INSERT INTO clans (name, description, region, created_at)
                    VALUES (:n, :d, :r, :c)
                """),
                {"n": name, "d": description, "r": region, "c": created_at},
            )
            inserted += 1

    print(f"[loader] inserted={inserted}, skipped={skipped} ✅")

if __name__ == "__main__":
    main()

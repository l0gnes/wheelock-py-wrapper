from datetime import date

def format_date(
    d : date
) -> str:
    return d.isoformat()

__all__ = [
    "format_date"
]
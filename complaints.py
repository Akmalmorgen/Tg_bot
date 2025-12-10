# Жалобы на пользователей
complaints = []  # [{reporter, reported, reason}]


def add_complaint(reporter_id: int, reported_id: int, reason: str):
    """Добавить жалобу"""
    complaints.append({
        "reporter": reporter_id,
        "reported": reported_id,
        "reason": reason
    })


def get_recent_complaints(limit: int = 20):
    """Получить последние жалобы"""
    return complaints[-limit:]


def clear_complaints():
    """Удалить все жалобы"""
    complaints.clear()


def count_complaints():
    """Количество жалоб"""
    return len(complaints)

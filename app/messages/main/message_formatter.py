def main_exception(exc: Exception) -> str:
    return (
        f"Кажется это операция не работает, свяжитесь с разработчиком."
        f"\n{exc.__class__.__name__} -> {exc}"
    )

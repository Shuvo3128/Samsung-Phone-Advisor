class ClarificationAgent:
    """
    Requests more information when a query is ambiguous.
    """

    def run(self) -> str:
        return (
            "🤔 I need a bit more detail to help you.\n\n"
            "Please clarify one of the following:\n"
            "• Exact Samsung model name(s)\n"
            "• Your priority (camera, battery, price, performance)\n\n"
            "Example:\n"
            "👉 Compare Galaxy S23 Ultra and S22 Ultra"
        )

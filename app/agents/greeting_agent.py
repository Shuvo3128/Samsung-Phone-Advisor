class GreetingAgent:
    """
    Handles greetings and small talk.
    No DB / RAG / LLM calls.
    """

    def run(self) -> str:
        return (
            "👋 Hi! I'm your Samsung Phone Advisor.\n\n"
            "I can help you with:\n"
            "• Comparing Samsung phones\n"
            "• Recommending the best phone for your budget\n"
            "• Explaining phone specifications\n\n"
            "Try asking:\n"
            "👉 Compare Samsung Galaxy S23 Ultra and S22 Ultra"
        )

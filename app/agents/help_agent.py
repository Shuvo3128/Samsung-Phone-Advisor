class HelpAgent:
    """
    Explains system capabilities and how to ask questions.
    """

    def run(self) -> str:
        return (
            "ℹ️ **How I can help you**\n\n"
            "You can ask me questions like:\n"
            "• Compare Samsung Galaxy S23 Ultra and S22 Ultra\n"
            "• Which Samsung phone has the best battery under $1000?\n"
            "• Show specs of Samsung Galaxy S24\n\n"
            "I use a database + AI to give accurate answers."
        )

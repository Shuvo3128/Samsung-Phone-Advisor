class FallbackAgent:
    """
    Handles invalid, unsupported, or unclear queries gracefully.
    """

    def run(self) -> str:
        return (
            "😕 Sorry, I didn’t quite understand that.\n\n"
            "Please ask something related to Samsung phones.\n\n"
            "Example questions:\n"
            "• Best Samsung phone under $1000\n"
            "• Compare Galaxy S23 Ultra and S22 Ultra"
        )

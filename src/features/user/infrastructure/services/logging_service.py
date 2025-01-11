class LoggingService:

    @staticmethod
    async def log_event(message: str):
        print(f"Log: {message}")

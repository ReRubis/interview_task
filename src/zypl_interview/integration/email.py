"""This class is responsible for sending emails to users."""


class EmailIntegration:
    """This class is responsible for sending emails to users."""

    async def send_email(self, email: str, subject: str, body: str) -> None:
        """Send email to user."""
        # Don't really have the time to implement this. :(
        print(f"Sending email to {email} with subject: {subject} and body: {body}")

"""This module contains the schemas for the subscriptions module."""

from pydantic import BaseModel


class SubscriptionIn(BaseModel):
    """Represents a subscription model."""

    band_id: int

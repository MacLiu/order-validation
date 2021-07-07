from enumchoicefield import ChoiceEnum


class OrderType(ChoiceEnum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"


class ValidationStatus(ChoiceEnum):
    VALID = "VALID"
    BORDERLINE = "BORDERLINE"
    INVALID = "INVALID"

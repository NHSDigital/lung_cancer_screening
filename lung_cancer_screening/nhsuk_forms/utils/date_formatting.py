"""
Format and dates and times in a way consistent with
the NHS service manual's content guide:
https://service-manual.nhs.uk/content/numbers-measurements-dates-time
"""



def format_date(value):
    return value.strftime("%-d %B %Y")

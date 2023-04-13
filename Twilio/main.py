"""
Testing the TwilioConnector class defined in twilio.py
"""
from twilio import TwilioConnector, pprint


def main():
    twilio_connector = TwilioConnector()

    pprint(
        twilio_connector.list_all_events(
            start_datetime='2021-11-29T00:00:00Z',
            end_datetime='2021-11-29T23:59:59Z'
        ).text
    )


if __name__ == '__main__':
    main()

"""
Manual testing for the API clients.
"""

import dotenv

import src.utils
from src.apis import tfl

dotenv.load_dotenv()


def main() -> None:
    """
    Manually test the API client.
    """
    tfl_connector = tfl.TFLConnector()

    src.utils.pprint(tfl_connector.get_accident_stats(2025).json())
    src.utils.pprint(tfl_connector.get_air_quality().json())

    src.utils.pprint(tfl_connector.get_bike_points().json())
    src.utils.pprint(
        tfl_connector.get_bike_points(bike_point_id="BikePoints_608").json()
    )
    src.utils.pprint(tfl_connector.get_bike_points(query="Holborn").json())

    # These were returning HTML?!
    print(tfl_connector.get_crowding(naptan="940GZZLUBST").json())
    print(tfl_connector.get_crowding(naptan="940GZZLUBST", day_of_week="Live").json())
    print(tfl_connector.get_crowding(naptan="940GZZLUBST", day_of_week="Monday").json())

    src.utils.pprint(tfl_connector.get_journey().json())
    src.utils.pprint(tfl_connector.get_journey(meta=True).json())

    journey_params = tfl.JourneyPlannerSearchParams(
        calc_one_direction=True,
        include_alternative_routes=False,
    )
    src.utils.pprint(
        tfl_connector.get_journey_plan(
            from_="4900000248S",  # London Victoria
            to="490000080A",  # Farringdon Station
            journey_planner_search_params=journey_params,
        ).json()
    )

    src.utils.pprint(tfl_connector.get_network_status().json())


if __name__ == "__main__":
    main()

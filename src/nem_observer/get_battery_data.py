from datetime import datetime, timedelta
from openelectricity import AsyncOEClient
import asyncio
from openelectricity.types import DataMetric, MarketMetric, UnitFueltechType, UnitStatusType
from collections import defaultdict
from dataclasses import dataclass, asdict
import argparse
import json

fueltechtypes = {
    "battery_charging": UnitFueltechType.BATTERY_CHARGING, 
    "battery_discharging": UnitFueltechType.BATTERY_DISCHARGING, 
    "vpp": UnitFueltechType.AGGREGATOR_VPP, 
    "dr": UnitFueltechType.AGGREGATOR_DR,
    "gas_ccgt": UnitFueltechType.GAS_CCGT, 
    "gas_ocgt": UnitFueltechType.GAS_OCGT, 
    "gas_recip": UnitFueltechType.GAS_RECIP, 
    "gas_steam": UnitFueltechType.GAS_STEAM, 
    "gas_wcmg": UnitFueltechType.GAS_WCMG,
    "coal_black": UnitFueltechType.COAL_BLACK, 
    "coal_brown": UnitFueltechType.COAL_BROWN,
    "solar_utility": UnitFueltechType.SOLAR_UTILITY, 
    "solar_rooftop": UnitFueltechType.SOLAR_ROOFTOP, 
    "wind": UnitFueltechType.WIND, 
    "wind_offshore": UnitFueltechType.WIND_OFFSHORE
    }

loads = [UnitFueltechType.BATTERY_CHARGING]

async def main(fueltechtypes, region, network, end_date, length_day, interval):
    # Calculate date range
    end_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)        ## This calculates the time of midnight of the given end date
    start_date = end_date - timedelta(days=length_day)                            ## Looks at data from the last week

    # Using context manager (recommended), which parses requests to the Open Electricity API and handles authentication automatically
    async with AsyncOEClient() as client:
        try: 
            facilities = await client.get_facilities(
                network_id=[network],
                network_region=region,
                status_id=[UnitStatusType.OPERATING],
                fueltech_id=fueltechtypes,
            )
        except Exception as e:
            print(f"Error fetching facilities: {e}")
            return

        unit_codes = [unit.code for series in facilities.data for unit in series.units]

        facility_dict = {unit.code: {
            "facility": series.code, 
            "fueltech": unit.fueltech_id
            } for series in facilities.data for unit in series.units}

        ## initialize a nested defaultdict to store the data for the units
        data = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
        # Get network data for the unit code, see 
        # https://docs.openelectricity.org.au/api-reference/data/get-facility-data/
        for unit in unit_codes:
            try:
                response = await client.get_facility_data(
                network_code=network,
                metrics=[DataMetric.POWER,
                    DataMetric.ENERGY, 
                    DataMetric.MARKET_VALUE, 
                    DataMetric.STORAGE_BATTERY, 
                    DataMetric.EMISSIONS],
                interval=interval,
                unit_code=unit,
                date_start=start_date,
                date_end=end_date,
                )
                for series in response.data:
                    for result in series.results:
                        for point in result.data: 
                            timestamp = point.timestamp.strftime("%Y-%m-%d %H:%M:%S")

                            ## If the fueltech is a load, then the value should be negative
                            value = point.value if point.value is not None else 0.0
                            value = -value if facility_dict[unit]["fueltech"] in loads else value
                            data[facility_dict[unit]["facility"]][series.metric][timestamp] += value
            except Exception as e:
                print(f"\nError fetching data for unit {unit}: {e}\n")
                continue

        df_name = f"./src/nem_observer/data/{start_date.strftime('%m-%d')}-{end_date.strftime('%m-%d')}-{end_date.year}-{region}-{interval}-batterydata.json"
        with open(df_name, "w") as f:
            json.dump(data, f, indent=4, default=asdict)

parser = argparse.ArgumentParser()
parser.add_argument("--fuel_tech", nargs="+", default=[])
parser.add_argument("--region", type=str, default="NSW1")
parser.add_argument("--network", type=str, default="NEM")
parser.add_argument("--end_date", type=str, default=datetime.now().strftime("%Y-%m-%d"))
parser.add_argument("--length_day", type=int, default=7)
parser.add_argument("--interval", type=str, default="5m")

args = parser.parse_args()
included_fueltechtypes = [fueltechtypes[ft] for ft in args.fuel_tech if ft in fueltechtypes]
asyncio.run(main(fueltechtypes=included_fueltechtypes, 
                 region=args.region, 
                 network=args.network, 
                 end_date=datetime.strptime(args.end_date, "%Y-%m-%d"),
                 length_day=args.length_day,
                 interval=args.interval))
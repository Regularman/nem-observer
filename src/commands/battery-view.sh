export OPENELECTRICITY_API_KEY=oe_RbS3WH4EftZSKkkUvDrfo5

python3 src/nem_observer/get_battery_data.py --fuel_tech battery_charging battery_discharging --region NSW1 --network NEM --end_date 2026-08-30 --length_day 1 --interval 5m
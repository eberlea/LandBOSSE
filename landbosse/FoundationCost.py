"""
FoundationCost.py
Created by Annika Eberle and Owen Roberts on Apr. 3, 2018

Calculates the costs of constructing foundations for land-based wind projects
(items in brackets are not yet implemented)

Get number of turbines
Get duration of construction
Get daily hours of operation*  # todo: add to process diagram
Get season of construction*  # todo: add to process diagram
[Get region]
Get rotor diameter
Get hub height
Get turbine rating
Get buoyant foundation design flag
[Get seismic zone]
Get tower technology type
Get hourly weather data
[Get specific seasonal delays]
[Get long-term, site-specific climate data]

Get price data
    Get labor rates
    Get material prices for steel and concrete

[Use region to determine weather data,

Calculate the foundation loads using the rotor diameter, hub height, and turbine rating

Determine the foundation size based on the foundation loads, buoyant foundation design flag, and type of tower technology

Estimate the amount of material needed for foundation construction based on foundation size and number of turbines

Estimate the amount of time required to construct foundation based on foundation size, hours of operation,
duration of construction, and number of turbines

Estimate the additional amount of time for weather delays (currently only assessing wind delays) based on
hourly weather data, construction time, hours of operation, and season of construction

Estimate the amount of labor required for foundation construction based on foundation size, construction time, and weather delay
    Calculate number of workers by crew type
    Calculate man hours by crew type

Estimate the amount of equipment needed for foundation construction based on foundation size, construction time, and weather delay
    Calculate number of equipment by equip type
    Calculate equipment hours by equip type

Calculate the total foundation cost based on amount of equipment, amount of labor, amount of material, and price data

"""
import pandas as pd
import numpy as np
import WeatherDelay as WD
from sympy.solvers import solve
from sympy import Symbol

# constants
kg_per_tonne = 1000
cubicm_per_cubicft = 0.0283168
steel_density = 9490  # kg / m^3
cubicyd_per_cubicm = 1.30795
ton_per_tonne = 0.907185


def calculate_foundation_loads(component_data, depth):
    """

    :param component_data: data on components (weight, height, area, etc.)
    :param depth: depth in meters
    :return: foundation loads
    """

    # set exposure constants
    a = 9.5
    z_g = 274.32

    # get section height
    z = component_data['Section height m']

    # get cross-sectional area
    a_f = component_data['Surface area sq m']

    # get coefficient of drag
    c_d = component_data['Coeff drag (installed)']

    # get lever arm
    l = component_data['Lever arm m']

    # get multipliers for tower and rotor
    multiplier_rotor = component_data['Multplier drag rotor']
    multiplier_tower = component_data['Multiplier tower drag']

    # Equations from Shrestha, S. 2015. DESIGN AND ANALYSIS OF FOUNDATION FOR ONSHORE TALL WIND TURBINES. All Theses. Paper 2291.
    # https: // tigerprints.clemson.edu / cgi / viewcontent.cgi?referer = https: // www.google.com / & httpsredir = 1 & article = 3296 & context = all_theses
    # Also from
    # http://ir.uiowa.edu/cgi/viewcontent.cgi?article=2427&context=etd

    # calculate wind pressure
    k_z = 2.01 * (z / z_g) ** (2 / a)  # exposure factor
    k_d = 0.95  # wind directionality factor
    k_zt = 1  # topographic factor
    v = 52.5  # critical velocity in m/s
    wind_pressure = 0.613 * k_z * k_zt * k_d * v ** 2

    # calculate wind loads on each tower component
    g = 0.85  # gust factor
    c_f = 0.6  # coefficient of force
    f_t = (wind_pressure * g * c_f * a_f) * multiplier_tower

    # calculate drag rotor
    rho = 1.225  # air density in kg/m^3
    f_r = (0.5 * rho * c_d * a_f * v ** 2) * multiplier_rotor

    f = (f_t + f_r)

    # calculate dead load in N
    g = 9.8  # m / s ^ 2
    f_dead = component_data['Mass tonne'].sum() * g * kg_per_tonne / 1.15  # scaling factor to adjust dead load for uplift

    # calculate moment from each component at base of tower
    m_overturn = f * l

    safety_overturn = 1.5
    unit_weight_fill = 17.3e3  # in N / m^3
    unit_weight_concrete = 23.6e3  # in N / m^3
    rated_thrust = 742e3  # thrust for IEA 37 reference machine in N (unfactored) # todo: update to user input
    bearing_pressure = 203500 * 1.2  # N / m^2 # todo: update to user input

    # get total lateral load (N) and moment (N * m)
    f_lat = f.sum()
    m_overturn = m_overturn.sum()

    m_thrust = rated_thrust * max(l)
    m_tot = max(m_thrust, m_overturn)

    f_horiz = max(f_lat, rated_thrust)

    p = [(np.pi * depth * (2 / 3 * unit_weight_fill + 1 / 3 * unit_weight_concrete)),
         0,
         f_dead,
         - (safety_overturn * (m_tot + f_horiz * depth))]

    # calculate foundation radius based on overturning moment
    r = np.roots(p)
    r = np.real(r[np.isreal(r)])[0]

    # calculate foundation radius based on shear
    foundation_vol = np.pi * r ** 2 * depth
    v_1 = (foundation_vol * (2 / 3 * unit_weight_fill + 1 / 3 * unit_weight_concrete) + f_dead)
    e = m_tot / v_1
    r_2 = e * 3 / 2

    # calculate foundation radius based on bearing pressure
    r_pick = max(r, r_2)
    a_eff = v_1 / bearing_pressure
    x = Symbol('x')
    r_3 = max(solve(2 * (x ** 2 - e * (x ** 2 - e ** 2) ** 0.5) - a_eff, x))

    # pick the largest foundation radius based on all three foundation design criteria: moment, shear, bearing
    r_pick = max(r_pick, r_3)

    foundation_loads = {'F_dead_kN': f_dead / 1e3,
                        'F_horiz_kN': f_lat / 1e3,
                        'M_tot_kN_m': m_tot / 1e3,
                        'Radius_o_m': r,
                        'Radius_s_m': r_2,
                        'Radius_b_m': r_3,
                        'Radius_m': r_pick}

    return foundation_loads


def determine_foundation_size(foundation_loads, depth):
    """
    Calculates the radius of a round, raft foundation
    Assumes foundation made of concrete with 1 m thickness

    :param foundation_loads: dictionary of foundation loads (forces in N; moments in N*m)
    :param depth: depth of foundation (in meters)
    :return:
    """

    r = float(foundation_loads['Radius_m'])
    foundation_cubic_meters = np.pi * r ** 2 * depth * 0.4  # only compute the portion of the foundation that is composed of concrete (1/3 concrete; other portion is backfill)

    return foundation_cubic_meters


def estimate_material_needs(foundation_volume, num_turbines):
    """
    Estimate amount of material based on foundation size and number of turbines

    :param foundation_volume: volume of foundation material in m^3
    :param num_turbines: number of turbines
    :return: table of material needs
    """

    steel_mass = (foundation_volume * 0.012 * steel_density / kg_per_tonne * ton_per_tonne * num_turbines)
    concrete_volume = foundation_volume * 0.985 * cubicyd_per_cubicm * num_turbines

    material_needs = pd.DataFrame([['Steel - rebar', steel_mass, 'ton (short)'],
                                   ['Concrete 5000 psi', concrete_volume, 'cubic yards'],
                                   ['Excavated dirt', foundation_volume * 3.2 * cubicyd_per_cubicm * num_turbines, 'cubic_yards'],
                                   ['Backfill', foundation_volume * 3.2 * cubicyd_per_cubicm * num_turbines, 'cubic_yards']],
                                  columns=['Material type ID', 'Quantity of material', 'Units'])
    return material_needs


def estimate_construction_time(throughput_operations, material_needs, duration_construction):
    """

    :param throughput_operations:
    :param material_needs:
    :param duration_construction:
    :return:
    """

    foundation_construction_time = duration_construction * 1/3
    operation_data = throughput_operations.where(throughput_operations['Module'] == 'Foundations').dropna(thresh=4)
    operation_data = pd.merge(material_needs, operation_data, on=['Material type ID'], how='outer')
    operation_data['Number of days'] = operation_data['Quantity of material'] / operation_data['Daily output']
    operation_data['Number of crews'] = np.ceil((operation_data['Number of days'] / 30) / foundation_construction_time)
    operation_data['Cost USD without weather delays'] = operation_data['Quantity of material'] * operation_data['Rate USD per unit']

    # if more than one crew needed to complete within construction duration then assume that all construction happens
    # within that window and use that timeframe for weather delays; if not, use the number of days calculated
    operation_data['time_construct_bool'] = operation_data['Number of days'] > foundation_construction_time * 30
    boolean_dictionary = {True: foundation_construction_time * 30, False: np.NAN}
    operation_data['time_construct_bool'] = operation_data['time_construct_bool'].map(boolean_dictionary)
    operation_data['Time construct days'] = operation_data[['time_construct_bool', 'Number of days']].min(axis=1)

    return operation_data


def calculate_weather_delay(weather_window, duration_construction, start_delay, critical_wind_speed,
                            operational_hrs_per_day, height_interest, wind_shear_exponent):
    """
    Calculates wind delay for foundations.

    :param weather_window: data frame with weather data for time window associated with construction period
    :param duration_construction: the length of construction time for the entire project (in months)
    :param start_delay: the delay from the start of the weather window for the operation of interest
    :param critical_wind_speed: the critical wind speed for determining wind delay
    :param operational_hrs_per_day: number of hours of operation per day
    :param height_interest: height of interest for weather delay calculations
    :param wind_shear_exponent: wind shear exponent
    :return: the total wind delay (in hours) as estimated based on the input parameters
    """

    # convert days of work to hours of work
    mission_time_hrs = duration_construction * operational_hrs_per_day

    # compute weather delay
    wind_delay = WD.calculate_wind_delay(weather_window=weather_window,
                                         start_delay=start_delay,
                                         mission_time=mission_time_hrs,
                                         critical_wind_speed=critical_wind_speed,
                                         height_interest=height_interest,
                                         wind_shear_exponent=wind_shear_exponent)
    wind_delay = pd.DataFrame(wind_delay)

    # if greater than 4 hour delay, then shut down for full day (10 hours)
    wind_delay[(wind_delay > 4)] = 10
    wind_delay_time = float(wind_delay.sum())

    return wind_delay_time


def calculate_costs(input_data, num_turbines, construction_time, weather_window, operational_hrs_per_day,
                    overtime_multiplier, wind_shear_exponent, depth):
    """

    :param input_data:
    :param num_turbines:
    :param construction_time:
    :param weather_window:
    :param operational_hrs_per_day:
    :param overtime_multiplier:
    :param wind_shear_exponent:
    :param depth:
    :return:
    """

    foundation_loads = calculate_foundation_loads(component_data=input_data['components'], depth=depth)
    # print(foundation_loads)
    foundation_volume = determine_foundation_size(foundation_loads=foundation_loads, depth=depth)
    # print(foundation_volume)
    material_vol = estimate_material_needs(foundation_volume=foundation_volume, num_turbines=num_turbines)
    # print(material_vol)
    material_data = pd.merge(material_vol, input_data['material_price'], on=['Material type ID'])
    material_data['Cost USD'] = material_data['Quantity of material'] * pd.to_numeric(material_data['Material price USD per unit'])

    operation_data = estimate_construction_time(throughput_operations=input_data['rsmeans'],
                                                material_needs=material_vol,
                                                duration_construction=construction_time)

    wind_delay = calculate_weather_delay(weather_window=weather_window,
                                         duration_construction=operation_data['Time construct days'].max(skipna=True),
                                         start_delay=0,
                                         critical_wind_speed=13,
                                         operational_hrs_per_day=operational_hrs_per_day,
                                         height_interest=20,
                                         wind_shear_exponent=wind_shear_exponent)

    wind_delay_percent = (wind_delay / operational_hrs_per_day) / operation_data['Time construct days'].max(skipna=True)
    wind_multiplier = 1 / (1 - wind_delay_percent)

    labor_equip_data = pd.merge(material_vol, input_data['rsmeans'], on=['Material type ID'])
    per_diem = operation_data['Number of workers'] * operation_data['Number of crews'] * (operation_data['Time construct days'] + round(operation_data['Time construct days'] / 7)) * 144
    where_are_na_ns = np.isnan(per_diem)
    per_diem[where_are_na_ns] = 0
    labor_equip_data['Cost USD'] = (labor_equip_data['Quantity of material'] * labor_equip_data['Rate USD per unit'] * overtime_multiplier + per_diem) * wind_multiplier

    foundation_cost = labor_equip_data[['Operation ID', 'Type of cost', 'Cost USD']]

    material_costs = pd.DataFrame(columns=['Operation ID', 'Type of cost', 'Cost USD'])
    material_costs['Operation ID'] = material_data['Material type ID']
    material_costs['Type of cost'] = 'Materials'
    material_costs['Cost USD'] = material_data['Cost USD']

    foundation_cost = foundation_cost.append(material_costs)

    # calculate mobilization cost as percentage of total foundation cost
    mob_cost = pd.DataFrame([['Mobilization', 'Mobilization', foundation_cost['Cost USD'].sum() * 0.1]], columns=['Operation ID', 'Type of cost', 'Cost USD'])
    foundation_cost = foundation_cost.append(mob_cost)

    total_foundation_cost = foundation_cost.groupby(by=['Type of cost']).sum().reset_index()
    total_foundation_cost['Phase of construction'] = 'Foundations'

    # print(foundation_cost)
    return total_foundation_cost, wind_multiplier


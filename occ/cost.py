from __future__ import annotations
from dataclasses import dataclass
@dataclass
class CostResult:
    occ_interp_hours: float; occ_cost: float; rso_cost: float; cheaper: str; saving: float
def compare_costs(total_images, interp_time_s, throughput_per_hr, interp_rate,
                  aircraft_rate, flight_hours, rso_observers, rso_rate):
    hbt = (total_images*interp_time_s)/3600.0 if interp_time_s else 0.0
    hbthr = total_images/throughput_per_hr if throughput_per_hr else 0.0
    interp_hours = max(hbt, hbthr)
    occ = interp_hours*interp_rate + flight_hours*aircraft_rate
    rso = rso_observers*flight_hours*rso_rate + flight_hours*aircraft_rate
    return CostResult(interp_hours, occ, rso, "OCC" if occ<=rso else "RSO", abs(occ-rso))

        def parse_plant_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
            """Map API fields to sensor values, with computed real-time power.

            Supports both classic SolArk keys and STROG/protocol-2 style payloads.
            """
            if not isinstance(data, dict):
                _LOGGER.warning("parse_plant_data got non-dict: %r", data)
                return {}

            _LOGGER.debug("parse_plant_data received keys: %s", list(data.keys()))

            sensors: Dict[str, Any] = {}

            # ----- Energy today / total -----
            if "energyToday" in data or "etoday" in data:
                sensors["energy_today"] = self._safe_float(
                    data.get("energyToday", data.get("etoday"))
                )
            if "energyTotal" in data or "etotal" in data:
                sensors["energy_total"] = self._safe_float(
                    data.get("energyTotal", data.get("etotal"))
                )

            # ----- Battery-related raw values -----
            if "chargeVolt" in data:
                sensors["battery_voltage"] = self._safe_float(data.get("chargeVolt"))
            if "floatVolt" in data:
                sensors["battery_float_voltage"] = self._safe_float(data.get("floatVolt"))
            if "batteryCap" in data:
                sensors["battery_capacity"] = self._safe_float(data.get("batteryCap"))
            if "batteryLowCap" in data:
                sensors["battery_low_cap"] = self._safe_float(data.get("batteryLowCap"))
            if "batteryRestartCap" in data:
                sensors["battery_restart_cap"] = self._safe_float(data.get("batteryRestartCap"))
            if "batteryShutdownCap" in data:
                sensors["battery_shutdown_cap"] = self._safe_float(data.get("batteryShutdownCap"))

            # Grid / PV ratings
            if "gridPeakPower" in data:
                sensors["grid_peak_power"] = self._safe_float(data.get("gridPeakPower"))
            if "genPeakPower" in data:
                sensors["gen_peak_power"] = self._safe_float(data.get("genPeakPower"))
            if "pvMaxLimit" in data:
                sensors["pv_max_limit"] = self._safe_float(data.get("pvMaxLimit"))
            if "solarMaxSellPower" in data:
                sensors["solar_max_sell_power"] = self._safe_float(data.get("solarMaxSellPower"))

            # ----- Direct power fields if present (classic models) -----
            if "pvPower" in data:
                sensors["pv_power"] = self._safe_float(data.get("pvPower"))
            if "loadPower" in data:
                sensors["load_power"] = self._safe_float(data.get("loadPower"))

            # Grid import/export and net
            if "gridImportPower" in data:
                sensors["grid_import_power"] = self._safe_float(data.get("gridImportPower"))
            if "gridExportPower" in data:
                sensors["grid_export_power"] = self._safe_float(data.get("gridExportPower"))
            if "grid_power" not in sensors and (
                "gridImportPower" in data or "gridExportPower" in data
            ):
                gi = self._safe_float(data.get("gridImportPower"))
                ge = self._safe_float(data.get("gridExportPower"))
                sensors["grid_power"] = gi - ge

            # Battery power and SOC (direct)
            if "battPower" in data:
                sensors["battery_power"] = self._safe_float(data.get("battPower"))
            if "battSoc" in data:
                sensors["battery_soc"] = self._safe_float(data.get("battSoc"))

            # ----- Computed values for STROG / protocol-2 where direct fields are missing -----

            # PV power from MPPT strings: sum(voltN * currentN)
            pv_sum = 0.0
            for i in range(1, 13):
                v_raw = data.get(f"volt{i}")
                c_raw = data.get(f"current{i}")
                if v_raw is None and c_raw is None:
                    continue
                v = self._safe_float(v_raw)
                c = self._safe_float(c_raw)
                string_power = v * c
                sensors[f"pv_string_{i}_power"] = string_power
                pv_sum += string_power
            if "pv_power" not in sensors and pv_sum != 0.0:
                sensors["pv_power"] = pv_sum

            # Load power from inverter output voltage * current * power factor
            vout_raw = data.get("inverterOutputVoltage")
            cur_raw = data.get("curCurrent")
            pf_raw = data.get("pf")
            sensors["inverter_output_voltage"] = self._safe_float(vout_raw)
            sensors["inverter_output_current"] = self._safe_float(cur_raw)
            if "load_power" not in sensors and (vout_raw is not None or cur_raw is not None):
                vout = self._safe_float(vout_raw)
                cur = self._safe_float(cur_raw)
                pf = self._safe_float(pf_raw) or 1.0
                sensors["load_power"] = vout * cur * pf

            # Grid power from meterA/B/C
            meter_a_raw = data.get("meterA")
            meter_b_raw = data.get("meterB")
            meter_c_raw = data.get("meterC")
            if meter_a_raw is not None or meter_b_raw is not None or meter_c_raw is not None:
                meter_a = self._safe_float(meter_a_raw)
                meter_b = self._safe_float(meter_b_raw)
                meter_c = self._safe_float(meter_c_raw)
                sensors["grid_meter_a"] = meter_a
                sensors["grid_meter_b"] = meter_b
                sensors["grid_meter_c"] = meter_c
                if "grid_power" not in sensors:
                    sensors["grid_power"] = meter_a + meter_b + meter_c

            # Battery power from DC voltage * chargeCurrent
            cur_volt_raw = data.get("curVolt")
            charge_current_raw = data.get("chargeCurrent")
            sensors["battery_dc_voltage"] = self._safe_float(cur_volt_raw)
            sensors["battery_current"] = self._safe_float(charge_current_raw)
            if "battery_power" not in sensors and (
                cur_volt_raw is not None or charge_current_raw is not None
            ):
                cur_volt = self._safe_float(cur_volt_raw)
                charge_current = self._safe_float(charge_current_raw)
                sensors["battery_power"] = cur_volt * charge_current

            # Battery SOC from curCap / batteryCap if not already provided
            if "battery_soc" not in sensors:
                cur_cap_raw = data.get("curCap")
                batt_cap_raw = data.get("batteryCap")
                if cur_cap_raw is not None and batt_cap_raw is not None:
                    cur_cap = self._safe_float(cur_cap_raw)
                    batt_cap = self._safe_float(batt_cap_raw)
                    if batt_cap != 0:
                        sensors["battery_soc"] = (cur_cap / batt_cap) * 100.0

            _LOGGER.debug("Parsed sensors dict: %s", sensors)
            return sensors

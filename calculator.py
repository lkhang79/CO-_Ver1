"""
탄소제로 스마트팜 계산 시스템 - 계산 로직
Carbon Zero Smart Farm Calculator - Calculation Logic
"""

import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import config

class CarbonCalculator:
    """탄소 배출/감축 계산 클래스"""
    
    def __init__(self):
        self.grid_carbon_factor = config.GRID_CARBON_FACTOR
        
    def calculate_solar_production(
        self,
        capacity_kw: float,
        area_m2: float,
        hours: float,
        efficiency: float = None,
        weather_factor: float = 1.0
    ) -> Dict[str, float]:
        """
        태양광 발전량 계산
        
        Args:
            capacity_kw: 설비용량 (kW)
            area_m2: 온실 면적 (m²)
            hours: 발전 시간 (hours)
            efficiency: 발전 효율 (%)
            weather_factor: 날씨 보정 계수 (0~1)
        
        Returns:
            발전량 정보 딕셔너리
        """
        if efficiency is None:
            efficiency = config.SOLAR_EFFICIENCY_DEFAULT
        
        # 시간당 발전량 (kWh)
        hourly_production = capacity_kw * efficiency / 100 * weather_factor
        
        # 총 발전량
        total_production = hourly_production * hours
        
        # 면적당 발전량
        production_per_m2 = total_production / area_m2 if area_m2 > 0 else 0
        
        # 탄소 감축량 (kg CO2)
        carbon_reduction = total_production * self.grid_carbon_factor
        
        return {
            "hourly_production_kwh": round(hourly_production, 2),
            "total_production_kwh": round(total_production, 2),
            "production_per_m2": round(production_per_m2, 4),
            "carbon_reduction_kg": round(carbon_reduction, 2),
            "efficiency_percent": efficiency,
            "weather_factor": weather_factor
        }
    
    def calculate_heat_pump_consumption(
        self,
        capacity_kw: float,
        operating_hours: float,
        cop: float,
        mode: str = "heating",
        temp_diff: float = 20
    ) -> Dict[str, float]:
        """
        히트펌프 전력 소비 계산
        
        Args:
            capacity_kw: 히트펌프 용량 (kW)
            operating_hours: 가동 시간 (hours)
            cop: 성능계수 (COP)
            mode: 'heating' 또는 'cooling'
            temp_diff: 실내외 온도차 (°C)
        
        Returns:
            소비량 정보 딕셔너리
        """
        # COP 온도 보정
        if temp_diff > 25:
            cop_adjusted = cop * 0.85
        elif temp_diff > 20:
            cop_adjusted = cop * 0.92
        else:
            cop_adjusted = cop
        
        # 전력 소비량 (kWh)
        # 열량 = capacity_kw * operating_hours
        # 전력 = 열량 / COP
        thermal_energy = capacity_kw * operating_hours
        electrical_consumption = thermal_energy / cop_adjusted
        
        # 탄소 배출량 (kg CO2)
        carbon_emission = electrical_consumption * self.grid_carbon_factor
        
        # 효율
        efficiency = (thermal_energy / electrical_consumption) * 100 if electrical_consumption > 0 else 0
        
        return {
            "thermal_energy_kwh": round(thermal_energy, 2),
            "electrical_consumption_kwh": round(electrical_consumption, 2),
            "carbon_emission_kg": round(carbon_emission, 2),
            "cop_adjusted": round(cop_adjusted, 2),
            "efficiency_percent": round(efficiency, 2),
            "mode": mode,
            "temp_diff": temp_diff
        }
    
    def calculate_other_consumption(
        self,
        lighting_kwh: float = 0,
        irrigation_kwh: float = 0,
        ventilation_kwh: float = 0,
        control_system_kwh: float = 0,
        other_kwh: float = 0
    ) -> Dict[str, float]:
        """
        기타 전력 소비 계산
        
        Args:
            lighting_kwh: 조명 전력 (kWh)
            irrigation_kwh: 관수 전력 (kWh)
            ventilation_kwh: 환기 전력 (kWh)
            control_system_kwh: 제어시스템 전력 (kWh)
            other_kwh: 기타 전력 (kWh)
        
        Returns:
            소비량 정보 딕셔너리
        """
        breakdown = {
            "조명 (Lighting)": lighting_kwh,
            "관수 (Irrigation)": irrigation_kwh,
            "환기 (Ventilation)": ventilation_kwh,
            "제어시스템 (Control)": control_system_kwh,
            "기타 (Other)": other_kwh
        }
        
        total_consumption = sum(breakdown.values())
        carbon_emission = total_consumption * self.grid_carbon_factor
        
        return {
            "breakdown": breakdown,
            "total_consumption_kwh": round(total_consumption, 2),
            "carbon_emission_kg": round(carbon_emission, 2)
        }
    
    def calculate_net_carbon(
        self,
        solar_production: Dict,
        heat_pump: Dict,
        other_consumption: Dict
    ) -> Dict[str, float]:
        """
        순 탄소 배출량 계산
        
        Args:
            solar_production: 태양광 발전 정보
            heat_pump: 히트펌프 소비 정보
            other_consumption: 기타 소비 정보
        
        Returns:
            순 탄소 배출 정보
        """
        # 총 에너지 생산
        total_production = solar_production.get("total_production_kwh", 0)
        
        # 총 에너지 소비
        total_consumption = (
            heat_pump.get("electrical_consumption_kwh", 0) +
            other_consumption.get("total_consumption_kwh", 0)
        )
        
        # 순 에너지
        net_energy = total_production - total_consumption
        
        # 탄소 감축량
        carbon_reduction = solar_production.get("carbon_reduction_kg", 0)
        
        # 탄소 배출량
        carbon_emission = (
            heat_pump.get("carbon_emission_kg", 0) +
            other_consumption.get("carbon_emission_kg", 0)
        )
        
        # 순 탄소
        net_carbon = carbon_emission - carbon_reduction
        
        # 자급률
        self_sufficiency = (total_production / total_consumption * 100) if total_consumption > 0 else 0
        
        # 탄소중립 달성 여부
        is_carbon_neutral = net_carbon <= config.THRESHOLDS["carbon_neutral"]
        
        return {
            "total_production_kwh": round(total_production, 2),
            "total_consumption_kwh": round(total_consumption, 2),
            "net_energy_kwh": round(net_energy, 2),
            "carbon_reduction_kg": round(carbon_reduction, 2),
            "carbon_emission_kg": round(carbon_emission, 2),
            "net_carbon_kg": round(net_carbon, 2),
            "self_sufficiency_percent": round(self_sufficiency, 2),
            "is_carbon_neutral": is_carbon_neutral,
            "carbon_intensity": round(abs(net_carbon) / total_consumption, 4) if total_consumption > 0 else 0
        }
    
    def calculate_daily_profile(
        self,
        date: datetime,
        greenhouse_params: Dict,
        solar_params: Dict,
        heat_pump_params: Dict
    ) -> List[Dict]:
        """
        24시간 프로파일 계산
        
        Args:
            date: 계산 날짜
            greenhouse_params: 온실 파라미터
            solar_params: 태양광 파라미터
            heat_pump_params: 히트펌프 파라미터
        
        Returns:
            시간별 데이터 리스트
        """
        hourly_data = []
        
        for hour in range(24):
            timestamp = date.replace(hour=hour, minute=0, second=0)
            
            # 태양광 발전 (일출~일몰)
            if 6 <= hour <= 18:
                # 시간대별 발전 효율 (정오에 최대)
                hour_factor = 1 - abs(hour - 12) / 12 * 0.6
                solar = self.calculate_solar_production(
                    capacity_kw=solar_params.get("capacity", 100),
                    area_m2=greenhouse_params.get("area", 1000),
                    hours=1,
                    efficiency=solar_params.get("efficiency", config.SOLAR_EFFICIENCY_DEFAULT),
                    weather_factor=hour_factor * solar_params.get("weather_factor", 1.0)
                )
            else:
                solar = {
                    "hourly_production_kwh": 0,
                    "total_production_kwh": 0,
                    "production_per_m2": 0,
                    "carbon_reduction_kg": 0,
                    "efficiency_percent": solar_params.get("efficiency", config.SOLAR_EFFICIENCY_DEFAULT),
                    "weather_factor": 0
                }
            
            # 히트펌프 소비 (야간에 더 많이 가동)
            if hour < 6 or hour > 20:
                operating_factor = 1.0
            elif 9 <= hour <= 15:
                operating_factor = 0.3
            else:
                operating_factor = 0.6
            
            heat_pump = self.calculate_heat_pump_consumption(
                capacity_kw=heat_pump_params.get("capacity", 50) * operating_factor,
                operating_hours=1,
                cop=heat_pump_params.get("cop", config.HEAT_PUMP_COP_DEFAULT),
                mode=heat_pump_params.get("mode", "heating"),
                temp_diff=heat_pump_params.get("temp_diff", 20)
            )
            
            # 기타 소비 (낮시간에 더 많음)
            if 6 <= hour <= 18:
                other_factor = 1.0
            else:
                other_factor = 0.5
            
            other = self.calculate_other_consumption(
                lighting_kwh=greenhouse_params.get("lighting_power", 10) * other_factor,
                irrigation_kwh=greenhouse_params.get("irrigation_power", 5) * other_factor,
                ventilation_kwh=greenhouse_params.get("ventilation_power", 8) * other_factor,
                control_system_kwh=greenhouse_params.get("control_power", 2)
            )
            
            # 순 탄소
            net = self.calculate_net_carbon(solar, heat_pump, other)
            
            hourly_data.append({
                "timestamp": timestamp,
                "hour": hour,
                "solar": solar,
                "heat_pump": heat_pump,
                "other": other,
                "net": net
            })
        
        return hourly_data
    
    def calculate_monthly_summary(
        self,
        month: int,
        greenhouse_params: Dict,
        solar_params: Dict,
        heat_pump_params: Dict
    ) -> Dict:
        """
        월간 요약 계산
        
        Args:
            month: 월 (1-12)
            greenhouse_params: 온실 파라미터
            solar_params: 태양광 파라미터
            heat_pump_params: 히트펌프 파라미터
        
        Returns:
            월간 요약 데이터
        """
        days_in_month = config.DAYS_PER_MONTH[month - 1]
        
        # 일평균 계산
        date = datetime(2024, month, 15)  # 월 중간일 기준
        daily_profile = self.calculate_daily_profile(
            date, greenhouse_params, solar_params, heat_pump_params
        )
        
        # 일일 합계
        daily_solar = sum([h["solar"]["total_production_kwh"] for h in daily_profile])
        daily_consumption = sum([h["net"]["total_consumption_kwh"] for h in daily_profile])
        daily_net_carbon = sum([h["net"]["net_carbon_kg"] for h in daily_profile])
        
        # 월간 합계
        monthly_solar = daily_solar * days_in_month
        monthly_consumption = daily_consumption * days_in_month
        monthly_net_carbon = daily_net_carbon * days_in_month
        
        return {
            "month": month,
            "days": days_in_month,
            "total_production_kwh": round(monthly_solar, 2),
            "total_consumption_kwh": round(monthly_consumption, 2),
            "net_carbon_kg": round(monthly_net_carbon, 2),
            "avg_daily_production": round(daily_solar, 2),
            "avg_daily_consumption": round(daily_consumption, 2),
            "avg_daily_net_carbon": round(daily_net_carbon, 2)
        }
    
    def calculate_annual_summary(
        self,
        greenhouse_params: Dict,
        solar_params: Dict,
        heat_pump_params: Dict
    ) -> Dict:
        """
        연간 요약 계산
        
        Args:
            greenhouse_params: 온실 파라미터
            solar_params: 태양광 파라미터
            heat_pump_params: 히트펌프 파라미터
        
        Returns:
            연간 요약 데이터
        """
        monthly_data = []
        
        for month in range(1, 13):
            monthly_summary = self.calculate_monthly_summary(
                month, greenhouse_params, solar_params, heat_pump_params
            )
            monthly_data.append(monthly_summary)
        
        # 연간 합계
        annual_production = sum([m["total_production_kwh"] for m in monthly_data])
        annual_consumption = sum([m["total_consumption_kwh"] for m in monthly_data])
        annual_net_carbon = sum([m["net_carbon_kg"] for m in monthly_data])
        
        # 통계
        avg_monthly_production = annual_production / 12
        avg_monthly_consumption = annual_consumption / 12
        
        return {
            "monthly_data": monthly_data,
            "annual_production_kwh": round(annual_production, 2),
            "annual_consumption_kwh": round(annual_consumption, 2),
            "annual_net_carbon_kg": round(annual_net_carbon, 2),
            "annual_net_carbon_ton": round(annual_net_carbon / 1000, 2),
            "avg_monthly_production": round(avg_monthly_production, 2),
            "avg_monthly_consumption": round(avg_monthly_consumption, 2),
            "self_sufficiency_percent": round(annual_production / annual_consumption * 100, 2) if annual_consumption > 0 else 0
        }
    
    def calculate_roi(
        self,
        initial_investment: float,
        annual_savings: float,
        maintenance_cost: float = 0,
        electricity_rate: float = 150  # 원/kWh
    ) -> Dict:
        """
        투자 수익률 계산
        
        Args:
            initial_investment: 초기 투자비 (원)
            annual_savings: 연간 전기요금 절감액 (kWh)
            maintenance_cost: 연간 유지보수비 (원)
            electricity_rate: 전기요금 단가 (원/kWh)
        
        Returns:
            ROI 정보
        """
        annual_savings_krw = annual_savings * electricity_rate
        net_annual_savings = annual_savings_krw - maintenance_cost
        
        # 투자회수기간 (년)
        payback_period = initial_investment / net_annual_savings if net_annual_savings > 0 else float('inf')
        
        # 20년 순현재가치 (단순 계산)
        lifetime_years = 20
        total_savings = net_annual_savings * lifetime_years
        npv = total_savings - initial_investment
        
        # ROI (%)
        roi = (npv / initial_investment * 100) if initial_investment > 0 else 0
        
        return {
            "initial_investment_krw": initial_investment,
            "annual_savings_kwh": annual_savings,
            "annual_savings_krw": round(annual_savings_krw, 0),
            "annual_maintenance_krw": maintenance_cost,
            "net_annual_savings_krw": round(net_annual_savings, 0),
            "payback_period_years": round(payback_period, 1),
            "lifetime_years": lifetime_years,
            "total_savings_krw": round(total_savings, 0),
            "npv_krw": round(npv, 0),
            "roi_percent": round(roi, 1)
        }

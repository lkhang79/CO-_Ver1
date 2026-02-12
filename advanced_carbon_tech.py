"""
탄소제로 스마트팜 - 고급 탄소 저감 기술
Advanced Carbon Reduction Technologies
"""

import numpy as np
from typing import Dict, List
import config

class AdvancedCarbonTech:
    """고급 탄소 저감 기술 클래스"""
    
    def __init__(self):
        self.grid_carbon_factor = config.GRID_CARBON_FACTOR
    
    # ==================== CO2 시비 및 탄소포집 ====================
    
    def calculate_co2_fertilization(
        self,
        greenhouse_area_m2: float,
        co2_target_ppm: int = 800,
        co2_ambient_ppm: int = 400,
        operating_hours: float = 10,
        crop_type: str = "토마토 (Tomato)"
    ) -> Dict[str, float]:
        """
        CO2 시비 효과 계산
        
        Args:
            greenhouse_area_m2: 온실 면적 (m²)
            co2_target_ppm: 목표 CO2 농도 (ppm)
            co2_ambient_ppm: 대기 CO2 농도 (ppm, 기본 400)
            operating_hours: 일일 운영 시간
            crop_type: 작물 종류
        
        Returns:
            CO2 시비 정보
        """
        # 온실 체적 추정 (평균 높이 3m 가정)
        greenhouse_volume_m3 = greenhouse_area_m2 * 3
        
        # 추가 필요 CO2량 계산 (kg/day)
        # 1 m³ 공기 = 약 1.2 kg
        # CO2 농도 증가분 = (목표 - 대기) ppm
        # 1 ppm = 1 mg/m³ CO2
        co2_increase_ppm = co2_target_ppm - co2_ambient_ppm
        co2_required_mg = greenhouse_volume_m3 * co2_increase_ppm
        co2_required_kg_per_hour = co2_required_mg / 1000000  # mg to kg
        
        # 환기 손실 고려 (시간당 0.5회 교환 가정)
        air_exchange_rate = 0.5
        co2_hourly_loss = co2_required_kg_per_hour * air_exchange_rate
        
        # 일일 총 필요량
        daily_co2_kg = co2_hourly_loss * operating_hours
        
        # 작물별 생산성 증가율 (연구 데이터 기반)
        productivity_increase = {
            "토마토 (Tomato)": 0.27,  # 27% 증가
            "딸기 (Strawberry)": 0.27,  # 27% 증가
            "파프리카 (Paprika)": 0.25,  # 25% 증가
            "상추 (Lettuce)": 0.95,  # 95% 증가
            "오이 (Cucumber)": 0.30  # 30% 증가
        }
        
        increase_rate = productivity_increase.get(crop_type, 0.25)
        
        return {
            "co2_target_ppm": co2_target_ppm,
            "co2_ambient_ppm": co2_ambient_ppm,
            "co2_increase_ppm": co2_increase_ppm,
            "greenhouse_volume_m3": greenhouse_volume_m3,
            "daily_co2_required_kg": round(daily_co2_kg, 2),
            "productivity_increase_percent": round(increase_rate * 100, 1),
            "crop_type": crop_type
        }
    
    def calculate_dac_carbon_capture(
        self,
        dac_capacity_kg_per_day: float = 10,
        operating_days: int = 365,
        power_consumption_kwh_per_kg: float = 1.5
    ) -> Dict[str, float]:
        """
        DAC (Direct Air Capture) 탄소 포집 계산
        
        Args:
            dac_capacity_kg_per_day: DAC 일일 포집 용량 (kg CO2/day)
            operating_days: 연간 운영일수
            power_consumption_kwh_per_kg: kg CO2 포집당 전력 소비 (kWh)
        
        Returns:
            DAC 시스템 정보
        """
        # 연간 포집량
        annual_capture_kg = dac_capacity_kg_per_day * operating_days
        
        # 연간 전력 소비
        annual_power_consumption = annual_capture_kg * power_consumption_kwh_per_kg
        
        # 전력 소비로 인한 탄소 배출
        carbon_emission_from_power = annual_power_consumption * self.grid_carbon_factor
        
        # 순 포집량
        net_capture_kg = annual_capture_kg - carbon_emission_from_power
        
        # 효율성
        capture_efficiency = (net_capture_kg / annual_capture_kg * 100) if annual_capture_kg > 0 else 0
        
        return {
            "dac_capacity_kg_per_day": dac_capacity_kg_per_day,
            "annual_capture_kg": round(annual_capture_kg, 2),
            "annual_power_consumption_kwh": round(annual_power_consumption, 2),
            "carbon_emission_from_power_kg": round(carbon_emission_from_power, 2),
            "net_capture_kg": round(net_capture_kg, 2),
            "capture_efficiency_percent": round(capture_efficiency, 2)
        }
    
    def calculate_fuel_cell_co2_capture(
        self,
        fuel_cell_capacity_kw: float = 50,
        operating_hours: float = 24,
        co2_emission_rate_kg_per_kwh: float = 0.15,
        capture_efficiency: float = 0.90
    ) -> Dict[str, float]:
        """
        연료전지 배기가스 CO2 포집 계산
        
        Args:
            fuel_cell_capacity_kw: 연료전지 용량 (kW)
            operating_hours: 일일 운영시간
            co2_emission_rate_kg_per_kwh: kWh당 CO2 배출률
            capture_efficiency: 포집 효율 (%)
        
        Returns:
            연료전지 CO2 포집 정보
        """
        # 일일 발전량
        daily_generation_kwh = fuel_cell_capacity_kw * operating_hours
        
        # 총 CO2 배출량
        total_co2_emission_kg = daily_generation_kwh * co2_emission_rate_kg_per_kwh
        
        # 포집량
        captured_co2_kg = total_co2_emission_kg * capture_efficiency
        
        # 대기 방출량
        released_co2_kg = total_co2_emission_kg - captured_co2_kg
        
        return {
            "fuel_cell_capacity_kw": fuel_cell_capacity_kw,
            "daily_generation_kwh": round(daily_generation_kwh, 2),
            "total_co2_emission_kg": round(total_co2_emission_kg, 2),
            "captured_co2_kg": round(captured_co2_kg, 2),
            "released_co2_kg": round(released_co2_kg, 2),
            "capture_efficiency_percent": round(capture_efficiency * 100, 1),
            "available_for_fertilization_kg": round(captured_co2_kg, 2)
        }
    
    # ==================== PPA (전력구매계약) ====================
    
    def calculate_ppa_impact(
        self,
        annual_consumption_kwh: float,
        ppa_renewable_percent: float = 100,
        ppa_price_krw_per_kwh: float = 150,
        contract_years: int = 20
    ) -> Dict[str, float]:
        """
        PPA (Power Purchase Agreement) 효과 계산
        
        Args:
            annual_consumption_kwh: 연간 전력 소비량 (kWh)
            ppa_renewable_percent: PPA를 통한 재생에너지 비율 (%)
            ppa_price_krw_per_kwh: PPA 전력 단가 (원/kWh)
            contract_years: 계약 기간 (년)
        
        Returns:
            PPA 효과 정보
        """
        # PPA를 통한 재생에너지 사용량
        ppa_renewable_kwh = annual_consumption_kwh * (ppa_renewable_percent / 100)
        
        # 일반 전력 사용량
        grid_power_kwh = annual_consumption_kwh - ppa_renewable_kwh
        
        # 탄소 배출량 (PPA 재생에너지는 배출 0으로 간주)
        carbon_from_grid = grid_power_kwh * self.grid_carbon_factor
        carbon_from_ppa = 0  # 재생에너지는 탄소배출 0
        
        # 기존 방식 대비 탄소 감축량
        baseline_carbon = annual_consumption_kwh * self.grid_carbon_factor
        carbon_reduction = baseline_carbon - carbon_from_grid
        
        # 비용 분석
        annual_ppa_cost = ppa_renewable_kwh * ppa_price_krw_per_kwh
        total_contract_cost = annual_ppa_cost * contract_years
        
        return {
            "annual_consumption_kwh": annual_consumption_kwh,
            "ppa_renewable_kwh": round(ppa_renewable_kwh, 2),
            "ppa_renewable_percent": ppa_renewable_percent,
            "grid_power_kwh": round(grid_power_kwh, 2),
            "carbon_from_grid_kg": round(carbon_from_grid, 2),
            "carbon_from_ppa_kg": carbon_from_ppa,
            "total_carbon_emission_kg": round(carbon_from_grid, 2),
            "baseline_carbon_kg": round(baseline_carbon, 2),
            "carbon_reduction_kg": round(carbon_reduction, 2),
            "carbon_reduction_percent": round((carbon_reduction / baseline_carbon * 100), 2),
            "annual_ppa_cost_krw": round(annual_ppa_cost, 0),
            "contract_years": contract_years,
            "total_contract_cost_krw": round(total_contract_cost, 0)
        }
    
    # ==================== REC (신재생에너지공급인증서) ====================
    
    def calculate_rec_impact(
        self,
        annual_consumption_mwh: float,
        rec_purchase_mwh: float = 0,
        rec_price_krw: float = 50000,
        rec_weight: float = 1.0
    ) -> Dict[str, float]:
        """
        REC (Renewable Energy Certificate) 구매 효과 계산
        
        Args:
            annual_consumption_mwh: 연간 전력 소비량 (MWh)
            rec_purchase_mwh: REC 구매량 (MWh)
            rec_price_krw: REC 가격 (원/REC)
            rec_weight: REC 가중치 (기본 1.0)
        
        Returns:
            REC 효과 정보
        """
        # REC 발급량 = 전력량 × 가중치
        rec_certificates = rec_purchase_mwh * rec_weight
        
        # 전력 소비량을 kWh로 변환
        annual_consumption_kwh = annual_consumption_mwh * 1000
        rec_purchase_kwh = rec_purchase_mwh * 1000
        
        # REC로 인정받는 재생에너지 비율
        rec_renewable_percent = (rec_purchase_kwh / annual_consumption_kwh * 100) if annual_consumption_kwh > 0 else 0
        
        # 탄소 감축 효과
        # REC 구매량만큼 재생에너지로 간주 → 해당량의 탄소배출 0으로 인정
        baseline_carbon_kg = annual_consumption_kwh * self.grid_carbon_factor
        carbon_reduction_kg = rec_purchase_kwh * self.grid_carbon_factor
        net_carbon_kg = baseline_carbon_kg - carbon_reduction_kg
        
        # 비용
        total_rec_cost = rec_certificates * rec_price_krw
        cost_per_kwh_reduction = (total_rec_cost / rec_purchase_kwh) if rec_purchase_kwh > 0 else 0
        
        return {
            "annual_consumption_mwh": annual_consumption_mwh,
            "rec_purchase_mwh": rec_purchase_mwh,
            "rec_certificates": round(rec_certificates, 2),
            "rec_weight": rec_weight,
            "rec_renewable_percent": round(rec_renewable_percent, 2),
            "baseline_carbon_kg": round(baseline_carbon_kg, 2),
            "carbon_reduction_kg": round(carbon_reduction_kg, 2),
            "net_carbon_kg": round(net_carbon_kg, 2),
            "carbon_reduction_percent": round((carbon_reduction_kg / baseline_carbon_kg * 100), 2),
            "rec_price_krw": rec_price_krw,
            "total_rec_cost_krw": round(total_rec_cost, 0),
            "cost_per_kwh_reduction_krw": round(cost_per_kwh_reduction, 2)
        }
    
    # ==================== 통합 탄소제로 시나리오 ====================
    
    def calculate_carbon_zero_scenario(
        self,
        annual_consumption_kwh: float,
        solar_production_kwh: float = 0,
        ppa_percent: float = 0,
        rec_mwh: float = 0,
        co2_capture_kg: float = 0
    ) -> Dict[str, any]:
        """
        통합 탄소제로 달성 시나리오
        
        Args:
            annual_consumption_kwh: 연간 전력 소비량
            solar_production_kwh: 자가 태양광 발전량
            ppa_percent: PPA 재생에너지 비율 (%)
            rec_mwh: REC 구매량 (MWh)
            co2_capture_kg: CO2 포집량 (kg)
        
        Returns:
            통합 탄소제로 달성 정보
        """
        # 기준 탄소 배출량
        baseline_carbon = annual_consumption_kwh * self.grid_carbon_factor
        
        # 1. 자가 태양광 감축
        solar_reduction = solar_production_kwh * self.grid_carbon_factor
        
        # 2. PPA 감축
        ppa_kwh = annual_consumption_kwh * (ppa_percent / 100)
        ppa_reduction = ppa_kwh * self.grid_carbon_factor
        
        # 3. REC 감축
        rec_kwh = rec_mwh * 1000
        rec_reduction = rec_kwh * self.grid_carbon_factor
        
        # 4. CO2 포집 감축
        capture_reduction = co2_capture_kg
        
        # 총 감축량
        total_reduction = solar_reduction + ppa_reduction + rec_reduction + capture_reduction
        
        # 순 탄소 배출
        net_carbon = baseline_carbon - total_reduction
        
        # 탄소중립 달성 여부
        is_carbon_zero = net_carbon <= 0
        
        # 각 방법별 기여도
        contributions = {
            "태양광 (Solar)": (solar_reduction / total_reduction * 100) if total_reduction > 0 else 0,
            "PPA": (ppa_reduction / total_reduction * 100) if total_reduction > 0 else 0,
            "REC": (rec_reduction / total_reduction * 100) if total_reduction > 0 else 0,
            "CO2 포집 (Capture)": (capture_reduction / total_reduction * 100) if total_reduction > 0 else 0
        }
        
        return {
            "baseline_carbon_kg": round(baseline_carbon, 2),
            "solar_reduction_kg": round(solar_reduction, 2),
            "ppa_reduction_kg": round(ppa_reduction, 2),
            "rec_reduction_kg": round(rec_reduction, 2),
            "capture_reduction_kg": round(capture_reduction, 2),
            "total_reduction_kg": round(total_reduction, 2),
            "net_carbon_kg": round(net_carbon, 2),
            "carbon_reduction_percent": round((total_reduction / baseline_carbon * 100), 2),
            "is_carbon_zero": is_carbon_zero,
            "carbon_zero_achievement": "달성 ✅" if is_carbon_zero else "미달성 ❌",
            "remaining_carbon_kg": round(max(0, net_carbon), 2),
            "contributions": {k: round(v, 1) for k, v in contributions.items()}
        }
    
    def recommend_carbon_zero_strategy(
        self,
        annual_consumption_kwh: float,
        available_budget_krw: float,
        available_area_m2: float = 0
    ) -> Dict[str, any]:
        """
        최적 탄소제로 달성 전략 추천
        
        Args:
            annual_consumption_kwh: 연간 전력 소비량
            available_budget_krw: 가용 예산
            available_area_m2: 가용 면적 (태양광 설치용)
        
        Returns:
            추천 전략
        """
        # 목표: 탄소배출 제로
        target_reduction_kg = annual_consumption_kwh * self.grid_carbon_factor
        
        # 옵션 1: 자가 태양광 (초기 투자 높음, 장기 경제적)
        solar_option = {
            "method": "자가 태양광",
            "capacity_kw": available_area_m2 / 10 if available_area_m2 > 0 else 0,  # 10m²당 1kW 가정
            "initial_cost_krw": (available_area_m2 / 10) * 2000000,  # kW당 200만원
            "annual_savings_kwh": (available_area_m2 / 10) * 1200,  # kW당 1200kWh/년
            "payback_years": 7
        }
        
        # 옵션 2: PPA (중간 비용, 장기 계약)
        ppa_option = {
            "method": "PPA 계약",
            "coverage_percent": 100,
            "annual_cost_krw": annual_consumption_kwh * 150,  # 150원/kWh 가정
            "contract_years": 20,
            "flexibility": "중간"
        }
        
        # 옵션 3: REC 구매 (저비용, 즉시 적용)
        rec_mwh_needed = annual_consumption_kwh / 1000
        rec_option = {
            "method": "REC 구매",
            "rec_needed": rec_mwh_needed,
            "annual_cost_krw": rec_mwh_needed * 50000,  # REC당 5만원 가정
            "flexibility": "높음 (연단위 조정 가능)",
            "immediate": True
        }
        
        # 옵션 4: 하이브리드 (조합)
        hybrid_option = {
            "method": "하이브리드 전략",
            "solar_percent": 30,
            "ppa_percent": 50,
            "rec_percent": 20,
            "rationale": "비용 분산 및 리스크 최소화"
        }
        
        # 예산 기반 추천
        if available_budget_krw > solar_option["initial_cost_krw"]:
            recommendation = "자가 태양광 + REC 조합"
            reason = "충분한 예산으로 자가 발전 + 부족분 REC로 보완"
        elif available_budget_krw > ppa_option["annual_cost_krw"] * 3:
            recommendation = "PPA + REC 조합"
            reason = "중간 예산으로 PPA 주력 + REC 보완"
        else:
            recommendation = "REC 100%"
            reason = "제한된 예산으로 즉시 적용 가능한 REC 활용"
        
        return {
            "target_reduction_kg": round(target_reduction_kg, 2),
            "solar_option": solar_option,
            "ppa_option": ppa_option,
            "rec_option": rec_option,
            "hybrid_option": hybrid_option,
            "recommendation": recommendation,
            "reason": reason,
            "estimated_total_cost_krw": available_budget_krw
        }

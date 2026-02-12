"""
ESS (에너지저장장치) 시스템 모듈
Energy Storage System Module for Smart Farm

이 모듈은 스마트팜 환경에서 ESS의 경제성, 탄소저감 효과, 
그리고 최적 운영 전략을 계산하고 분석합니다.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import config

class ESSSystem:
    """
    ESS 에너지저장장치 시스템 클래스
    
    이 클래스는 ESS의 전체 수명주기 동안의 경제성, 환경성, 기술적 성능을 
    종합적으로 분석하는 기능을 제공합니다. 배터리 용량 설계부터 
    일일 충방전 스케줄 최적화, 장기 투자수익 분석까지 포괄합니다.
    """
    
    def __init__(self):
        """
        ESS 시스템 초기화
        
        한국전력 요금제와 한국에너지공단의 공식 탄소배출계수를 
        기반으로 계산 환경을 설정합니다.
        """
        self.grid_carbon_factor = config.GRID_CARBON_FACTOR
        
        # 한국전력 시간대별 요금 (원/kWh) - 2025년 기준
        # 산업용(갑) 고압 기준
        self.time_of_use_rates = {
            'peak': 180.5,      # 하계(6~8월) 10~12시, 13~17시 / 동계(12~2월) 10~12시, 17~20시, 22~23시
            'mid': 130.2,       # 봄가을 10~12시, 13~23시 / 하계·동계 나머지 시간
            'off_peak': 65.1    # 야간(23~09시) 전 계절
        }
        
        # ESS 배터리 기술 특성
        self.battery_specs = {
            'lithium_ion': {
                'name': '리튬이온',
                'efficiency': 0.95,          # 충방전 효율 95%
                'dod': 0.90,                 # 방전심도 (Depth of Discharge) 90%
                'cycle_life': 6000,          # 사이클 수명
                'calendar_life': 15,         # 달력 수명 (년)
                'cost_per_kwh': 1000000,     # kWh당 비용 (원)
                'maintenance_rate': 0.02     # 연간 유지보수비율 2%
            },
            'lfp': {
                'name': 'LFP (리튬인산철)',
                'efficiency': 0.93,
                'dod': 0.95,
                'cycle_life': 8000,
                'calendar_life': 20,
                'cost_per_kwh': 900000,
                'maintenance_rate': 0.015
            }
        }
    
    def design_ess_capacity(
        self,
        solar_capacity_kw: float,
        daily_consumption_kwh: float,
        target_self_sufficiency: float = 0.70
    ) -> Dict[str, float]:
        """
        최적 ESS 용량 설계
        
        태양광 발전 용량과 일일 전력 소비 패턴을 분석하여 
        목표 자급률 달성에 필요한 ESS 용량을 계산합니다.
        
        설계 원칙:
        1. 태양광 발전량의 60~80%를 저장 용량으로 설정
        2. 야간 소비량의 50~70%를 커버할 수 있도록 설계
        3. 배터리 수명을 고려하여 방전심도(DOD) 90% 이내 운영
        
        Args:
            solar_capacity_kw: 태양광 발전 용량 (kW)
            daily_consumption_kwh: 일일 전력 소비량 (kWh)
            target_self_sufficiency: 목표 자급률 (0~1)
        
        Returns:
            ESS 설계 사양 딕셔너리
            - recommended_capacity: 권장 용량
            - min_capacity: 최소 용량
            - max_capacity: 최대 용량
            - usable_capacity: 실사용 가능 용량 (DOD 고려)
        """
        # 일일 태양광 발전량 추정 (평균 일사시간 4.5시간)
        daily_solar_generation = solar_capacity_kw * 4.5
        
        # 야간 소비량 추정 (전체 소비의 60%)
        night_consumption = daily_consumption_kwh * 0.60
        
        # 최소 용량: 태양광 발전량의 50%
        min_capacity = daily_solar_generation * 0.50
        
        # 최대 용량: 태양광 발전량의 80%
        max_capacity = daily_solar_generation * 0.80
        
        # 권장 용량: 목표 자급률 기반 계산
        # 자급률 향상 = (ESS 용량 × 충방전 효율) / 일일 소비량
        required_storage = (target_self_sufficiency - 0.35) * daily_consumption_kwh / 0.95
        recommended_capacity = np.clip(required_storage, min_capacity, max_capacity)
        
        # 실사용 가능 용량 (DOD 90% 적용)
        usable_capacity = recommended_capacity * 0.90
        
        return {
            'solar_capacity_kw': solar_capacity_kw,
            'daily_consumption_kwh': daily_consumption_kwh,
            'daily_solar_generation_kwh': round(daily_solar_generation, 1),
            'night_consumption_kwh': round(night_consumption, 1),
            'min_capacity_kwh': round(min_capacity, 1),
            'recommended_capacity_kwh': round(recommended_capacity, 1),
            'max_capacity_kwh': round(max_capacity, 1),
            'usable_capacity_kwh': round(usable_capacity, 1),
            'target_self_sufficiency': target_self_sufficiency * 100
        }
    
    def calculate_daily_operation(
        self,
        ess_capacity_kwh: float,
        solar_generation_profile: np.ndarray,
        consumption_profile: np.ndarray,
        battery_type: str = 'lithium_ion'
    ) -> Dict[str, any]:
        """
        일일 ESS 충방전 운영 시뮬레이션
        
        24시간 동안의 태양광 발전과 전력 소비 패턴을 분석하여
        최적의 충방전 스케줄을 생성하고 성능을 평가합니다.
        
        운영 전략:
        1. 태양광 발전 > 소비: 잉여전력 저장 (충전)
        2. 태양광 발전 < 소비: ESS 방전 → 부족분은 계통 구매
        3. ESS 잔량 20% 미만: 심야 전력으로 충전
        
        Args:
            ess_capacity_kwh: ESS 용량 (kWh)
            solar_generation_profile: 24시간 태양광 발전 프로파일 (kWh/시간)
            consumption_profile: 24시간 소비 프로파일 (kWh/시간)
            battery_type: 배터리 종류 ('lithium_ion' 또는 'lfp')
        
        Returns:
            운영 결과 딕셔너리
            - hourly_soc: 시간별 충전율 (State of Charge)
            - hourly_charge: 시간별 충전량
            - hourly_discharge: 시간별 방전량
            - grid_purchase: 계통 구매량
            - self_consumption: 자가소비량
            - self_sufficiency_rate: 자급률
        """
        battery_spec = self.battery_specs[battery_type]
        efficiency = battery_spec['efficiency']
        dod = battery_spec['dod']
        
        # 초기 설정
        hours = 24
        soc = np.zeros(hours + 1)  # State of Charge (충전율 0~1)
        soc[0] = 0.50  # 초기 충전율 50%
        
        charge_power = np.zeros(hours)
        discharge_power = np.zeros(hours)
        grid_purchase = np.zeros(hours)
        
        max_charge_rate = ess_capacity_kwh * 0.5  # 최대 충전속도 0.5C
        max_discharge_rate = ess_capacity_kwh * 0.5  # 최대 방전속도 0.5C
        
        # 시간별 시뮬레이션
        for hour in range(hours):
            solar = solar_generation_profile[hour]
            demand = consumption_profile[hour]
            net_power = solar - demand
            
            if net_power > 0:
                # 태양광 잉여 → 충전
                available_space = (1.0 - soc[hour]) * ess_capacity_kwh
                charge_amount = min(net_power, available_space, max_charge_rate) * efficiency
                charge_power[hour] = charge_amount
                soc[hour + 1] = soc[hour] + (charge_amount / ess_capacity_kwh)
                
            else:
                # 전력 부족 → 방전
                deficit = abs(net_power)
                available_energy = soc[hour] * ess_capacity_kwh
                max_discharge = min(available_energy, max_discharge_rate, deficit / efficiency)
                
                # DOD 한계 체크 (20% 이상 유지)
                if soc[hour] > 0.20:
                    discharge_amount = max_discharge
                    discharge_power[hour] = discharge_amount * efficiency
                    soc[hour + 1] = soc[hour] - (discharge_amount / ess_capacity_kwh)
                    
                    # ESS로 부족한 부분은 계통 구매
                    grid_purchase[hour] = deficit - discharge_power[hour]
                else:
                    # ESS 방전 불가 → 전량 계통 구매
                    grid_purchase[hour] = deficit
                    soc[hour + 1] = soc[hour]
            
            # 야간 시간대 (23~06시) ESS 충전율이 낮으면 계통 충전
            if (hour >= 23 or hour < 6) and soc[hour + 1] < 0.30:
                available_space = (1.0 - soc[hour + 1]) * ess_capacity_kwh
                grid_charge = min(available_space, max_charge_rate) * efficiency
                charge_power[hour] += grid_charge
                grid_purchase[hour] += grid_charge / efficiency
                soc[hour + 1] += (grid_charge / ess_capacity_kwh)
        
        # 자급률 계산
        total_consumption = consumption_profile.sum()
        total_grid_purchase = grid_purchase.sum()
        self_consumption = total_consumption - total_grid_purchase
        self_sufficiency_rate = (self_consumption / total_consumption) * 100 if total_consumption > 0 else 0
        
        return {
            'hourly_soc': soc[:-1],  # 마지막 시간 제외
            'hourly_charge': charge_power,
            'hourly_discharge': discharge_power,
            'hourly_grid_purchase': grid_purchase,
            'total_charge_kwh': round(charge_power.sum(), 2),
            'total_discharge_kwh': round(discharge_power.sum(), 2),
            'total_grid_purchase_kwh': round(total_grid_purchase, 2),
            'self_consumption_kwh': round(self_consumption, 2),
            'self_sufficiency_rate': round(self_sufficiency_rate, 2)
        }
    
    def calculate_carbon_reduction(
        self,
        ess_capacity_kwh: float,
        annual_solar_generation_kwh: float,
        annual_consumption_kwh: float,
        battery_type: str = 'lithium_ion'
    ) -> Dict[str, float]:
        """
        ESS 적용에 따른 탄소저감 효과 분석
        
        ESS가 없을 때와 있을 때의 탄소배출량을 비교하여
        실제 저감 효과를 정량화합니다.
        
        탄소저감 메커니즘:
        1. 태양광 활용률 증가: 잉여 발전 저장 → 화석연료 대체
        2. 피크 부하 저감: 계통 전력 사용 최소화
        3. 재생에너지 안정화: 전력망 RE 수용성 향상
        
        Args:
            ess_capacity_kwh: ESS 용량 (kWh)
            annual_solar_generation_kwh: 연간 태양광 발전량 (kWh)
            annual_consumption_kwh: 연간 전력 소비량 (kWh)
            battery_type: 배터리 종류
        
        Returns:
            탄소저감 분석 결과
        """
        battery_spec = self.battery_specs[battery_type]
        efficiency = battery_spec['efficiency']
        
        # ESS 없을 때: 태양광 즉시 자가소비 + 나머지 계통 구매
        # 평균 즉시 자가소비율: 35%
        immediate_self_consumption = annual_solar_generation_kwh * 0.35
        baseline_grid_purchase = annual_consumption_kwh - immediate_self_consumption
        baseline_carbon = baseline_grid_purchase * self.grid_carbon_factor
        
        # ESS 있을 때: 자가소비율 향상
        # ESS 용량에 따른 자가소비율 추정
        capacity_ratio = ess_capacity_kwh / (annual_solar_generation_kwh / 365)
        enhanced_self_consumption_rate = min(0.35 + (capacity_ratio * 0.15), 0.80)
        enhanced_self_consumption = annual_solar_generation_kwh * enhanced_self_consumption_rate
        
        # ESS 충방전 손실 고려
        ess_loss = (enhanced_self_consumption - immediate_self_consumption) * (1 - efficiency)
        net_enhanced_consumption = enhanced_self_consumption - ess_loss
        
        enhanced_grid_purchase = annual_consumption_kwh - net_enhanced_consumption
        enhanced_carbon = enhanced_grid_purchase * self.grid_carbon_factor
        
        # 탄소저감량
        carbon_reduction = baseline_carbon - enhanced_carbon
        reduction_rate = (carbon_reduction / baseline_carbon * 100) if baseline_carbon > 0 else 0
        
        return {
            'baseline_carbon_kg': round(baseline_carbon, 2),
            'enhanced_carbon_kg': round(enhanced_carbon, 2),
            'carbon_reduction_kg': round(carbon_reduction, 2),
            'reduction_rate_percent': round(reduction_rate, 2),
            'baseline_self_consumption_kwh': round(immediate_self_consumption, 2),
            'enhanced_self_consumption_kwh': round(net_enhanced_consumption, 2),
            'self_consumption_increase_kwh': round(net_enhanced_consumption - immediate_self_consumption, 2),
            'ess_loss_kwh': round(ess_loss, 2)
        }
    
    def calculate_economic_analysis(
        self,
        ess_capacity_kwh: float,
        annual_grid_reduction_kwh: float,
        battery_type: str = 'lithium_ion',
        government_subsidy_rate: float = 0.30,
        electricity_price_escalation: float = 0.03
    ) -> Dict[str, any]:
        """
        ESS 투자 경제성 분석
        
        초기 투자비용, 운영비용, 절감액을 종합하여
        투자회수기간과 순현재가치(NPV)를 계산합니다.
        
        경제성 평가 항목:
        1. 초기 투자비 (배터리 + BMS + PCS + 설치)
        2. 정부 보조금 (신재생에너지 보급사업 30~50%)
        3. 전력요금 절감액 (피크·심야 차액 활용)
        4. 유지보수비 (연간 투자비의 1~2%)
        5. 주파수조정(FR) 서비스 수익 (선택사항)
        
        Args:
            ess_capacity_kwh: ESS 용량 (kWh)
            annual_grid_reduction_kwh: 연간 계통전력 절감량 (kWh)
            battery_type: 배터리 종류
            government_subsidy_rate: 정부 보조금 비율 (0~1)
            electricity_price_escalation: 전기요금 연간 상승률
        
        Returns:
            경제성 분석 결과
        """
        battery_spec = self.battery_specs[battery_type]
        
        # 초기 투자비용
        battery_cost = ess_capacity_kwh * battery_spec['cost_per_kwh']
        bms_cost = battery_cost * 0.10  # 배터리관리시스템 10%
        pcs_cost = battery_cost * 0.15  # 전력변환장치 15%
        installation_cost = battery_cost * 0.20  # 설치비 20%
        total_initial_cost = battery_cost + bms_cost + pcs_cost + installation_cost
        
        # 정부 보조금 적용
        subsidy = total_initial_cost * government_subsidy_rate
        net_initial_cost = total_initial_cost - subsidy
        
        # 연간 절감액 계산
        # 피크-심야 요금 차이 활용
        peak_off_peak_diff = self.time_of_use_rates['peak'] - self.time_of_use_rates['off_peak']
        annual_energy_savings = annual_grid_reduction_kwh * peak_off_peak_diff * 0.60
        
        # 주파수조정(FR) 서비스 수익 (선택)
        # 용량 1MW당 월 700만원 수준
        fr_capacity_mw = ess_capacity_kwh / 1000
        annual_fr_revenue = fr_capacity_mw * 7000000 * 12 if fr_capacity_mw >= 1 else 0
        
        # 연간 총 수익
        annual_revenue = annual_energy_savings + annual_fr_revenue
        
        # 연간 유지보수비
        annual_maintenance = total_initial_cost * battery_spec['maintenance_rate']
        
        # 순 연간 이익
        annual_net_profit = annual_revenue - annual_maintenance
        
        # 투자회수기간 (Simple Payback)
        payback_years = net_initial_cost / annual_net_profit if annual_net_profit > 0 else 999
        
        # NPV 계산 (15년 운영, 할인율 5%)
        discount_rate = 0.05
        project_years = min(battery_spec['calendar_life'], 15)
        npv = -net_initial_cost
        
        for year in range(1, project_years + 1):
            escalated_revenue = annual_revenue * ((1 + electricity_price_escalation) ** year)
            yearly_profit = escalated_revenue - annual_maintenance
            npv += yearly_profit / ((1 + discount_rate) ** year)
        
        # IRR 추정 (간단한 근사)
        irr = (annual_net_profit / net_initial_cost) * 100 if net_initial_cost > 0 else 0
        
        return {
            'battery_type': battery_spec['name'],
            'ess_capacity_kwh': ess_capacity_kwh,
            'battery_cost': round(battery_cost, 0),
            'bms_cost': round(bms_cost, 0),
            'pcs_cost': round(pcs_cost, 0),
            'installation_cost': round(installation_cost, 0),
            'total_initial_cost': round(total_initial_cost, 0),
            'government_subsidy': round(subsidy, 0),
            'net_initial_cost': round(net_initial_cost, 0),
            'annual_energy_savings': round(annual_energy_savings, 0),
            'annual_fr_revenue': round(annual_fr_revenue, 0),
            'annual_total_revenue': round(annual_revenue, 0),
            'annual_maintenance': round(annual_maintenance, 0),
            'annual_net_profit': round(annual_net_profit, 0),
            'payback_years': round(payback_years, 2),
            'npv_15years': round(npv, 0),
            'irr_percent': round(irr, 2),
            'project_lifetime_years': project_years
        }
    
    def generate_hourly_profiles(
        self,
        season: str = 'winter'
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        계절별 표준 전력 프로파일 생성
        
        스마트팜의 전형적인 24시간 태양광 발전 및 소비 패턴을
        계절별로 생성합니다. 실제 데이터가 없을 때 시뮬레이션에 활용됩니다.
        
        계절별 특성:
        - 여름: 냉방 부하 ↑ (주간), 태양광 발전 ↑
        - 겨울: 난방 부하 ↑ (야간), 태양광 발전 ↓
        - 봄/가을: 균형적 패턴
        
        Args:
            season: 계절 ('spring', 'summer', 'fall', 'winter')
        
        Returns:
            (solar_profile, consumption_profile) 튜플
            각각 24시간 hourly 데이터 (kWh/시간)
        """
        hours = np.arange(24)
        
        # 태양광 발전 프로파일 (정규분포 기반)
        if season == 'summer':
            solar_peak_hour = 13
            solar_std = 3.5
            solar_scale = 100
        elif season == 'winter':
            solar_peak_hour = 12
            solar_std = 2.5
            solar_scale = 60
        else:  # spring, fall
            solar_peak_hour = 12.5
            solar_std = 3.0
            solar_scale = 80
        
        solar_profile = solar_scale * np.exp(-((hours - solar_peak_hour) ** 2) / (2 * solar_std ** 2))
        solar_profile = np.maximum(solar_profile, 0)
        
        # 소비 프로파일
        if season == 'summer':
            # 여름: 주간 냉방 부하 높음
            consumption_base = 30
            consumption_profile = consumption_base + \
                                20 * np.exp(-((hours - 14) ** 2) / 20) + \
                                15 * np.sin((hours - 6) * np.pi / 12)
        elif season == 'winter':
            # 겨울: 야간 난방 부하 높음
            consumption_base = 40
            consumption_profile = consumption_base + \
                                30 * (1 - np.exp(-((hours - 3) ** 2) / 50)) + \
                                20 * (1 - np.exp(-((hours - 21) ** 2) / 50))
        else:
            # 봄/가을: 일정한 패턴
            consumption_base = 25
            consumption_profile = consumption_base + \
                                15 * np.sin((hours - 8) * np.pi / 12) + \
                                10
        
        consumption_profile = np.maximum(consumption_profile, 10)
        
        return solar_profile, consumption_profile
    
    def compare_scenarios(
        self,
        solar_capacity_kw: float,
        annual_consumption_kwh: float,
        ess_capacities: List[float] = [0, 300, 500, 700]
    ) -> pd.DataFrame:
        """
        ESS 용량별 시나리오 비교 분석
        
        ESS 없음부터 대용량까지 여러 시나리오를 비교하여
        최적 용량 선택을 지원합니다.
        
        비교 항목:
        - 자급률
        - 탄소저감량
        - 투자비용
        - 투자회수기간
        - NPV
        
        Args:
            solar_capacity_kw: 태양광 용량 (kW)
            annual_consumption_kwh: 연간 소비량 (kWh)
            ess_capacities: 비교할 ESS 용량 리스트 (kWh)
        
        Returns:
            비교 결과 DataFrame
        """
        results = []
        
        for capacity in ess_capacities:
            if capacity == 0:
                # ESS 없음
                scenario = {
                    'ESS 용량 (kWh)': 0,
                    '자급률 (%)': 35.0,
                    '연간 탄소저감 (kg)': 0,
                    '초기 투자비 (만원)': 0,
                    '투자회수기간 (년)': 0,
                    'NPV (만원)': 0,
                    '추천': ''
                }
            else:
                # 탄소저감 분석
                carbon_result = self.calculate_carbon_reduction(
                    capacity,
                    solar_capacity_kw * 1200,  # 연간 발전량
                    annual_consumption_kwh
                )
                
                # 경제성 분석
                grid_reduction = carbon_result['self_consumption_increase_kwh']
                econ_result = self.calculate_economic_analysis(
                    capacity,
                    grid_reduction
                )
                
                # 자급률 추정
                self_sufficiency = 35 + (capacity / (annual_consumption_kwh / 365)) * 15
                self_sufficiency = min(self_sufficiency, 80)
                
                scenario = {
                    'ESS 용량 (kWh)': capacity,
                    '자급률 (%)': round(self_sufficiency, 1),
                    '연간 탄소저감 (kg)': carbon_result['carbon_reduction_kg'],
                    '초기 투자비 (만원)': round(econ_result['net_initial_cost'] / 10000, 0),
                    '투자회수기간 (년)': econ_result['payback_years'],
                    'NPV (만원)': round(econ_result['npv_15years'] / 10000, 0),
                    '추천': ''
                }
                
                # 최적 용량 표시
                if 5 <= econ_result['payback_years'] <= 8:
                    scenario['추천'] = '✓ 권장'
            
            results.append(scenario)
        
        return pd.DataFrame(results)

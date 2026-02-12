"""
탄소제로 스마트팜 계산 시스템 - 데이터 처리
Carbon Zero Smart Farm Calculator - Data Handler
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import config

class DataHandler:
    """데이터 수집 및 처리 클래스"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or config.KMA_API_KEY
        self.cache = {}
        self.last_update = {}
    
    def fetch_weather_data(
        self,
        location: str = "서울",
        date: Optional[datetime] = None
    ) -> Dict:
        """
        기상 데이터 조회
        
        Args:
            location: 지역명
            date: 조회 날짜
        
        Returns:
            기상 데이터
        """
        if date is None:
            date = datetime.now()
        
        # 캐시 확인
        cache_key = f"weather_{location}_{date.strftime('%Y%m%d')}"
        if cache_key in self.cache:
            cache_time = self.last_update.get(cache_key)
            if cache_time and (datetime.now() - cache_time).seconds < config.DATA_UPDATE_INTERVAL:
                return self.cache[cache_key]
        
        # 실제 API 호출 대신 시뮬레이션 데이터 생성
        # 실제 운영시에는 기상청 API를 호출
        weather_data = self._generate_simulated_weather(location, date)
        
        # 캐시 저장
        self.cache[cache_key] = weather_data
        self.last_update[cache_key] = datetime.now()
        
        return weather_data
    
    def _generate_simulated_weather(
        self,
        location: str,
        date: datetime
    ) -> Dict:
        """
        시뮬레이션 기상 데이터 생성
        """
        # 월별 기온 패턴
        month = date.month
        base_temp = {
            1: -2, 2: 1, 3: 7, 4: 14, 5: 19, 6: 23,
            7: 26, 8: 27, 9: 22, 10: 16, 11: 8, 12: 1
        }[month]
        
        # 시간대별 온도 변화
        hourly_temps = []
        for hour in range(24):
            # 일교차 적용
            temp_variation = 5 * np.sin((hour - 6) / 24 * 2 * np.pi)
            hourly_temps.append(round(base_temp + temp_variation + np.random.normal(0, 2), 1))
        
        # 일사량 (W/m²)
        hourly_solar_radiation = []
        for hour in range(24):
            if 6 <= hour <= 18:
                # 정오에 최대
                radiation = 800 * np.sin((hour - 6) / 12 * np.pi)
                # 날씨에 따른 변동
                weather_factor = np.random.uniform(0.7, 1.0)
                hourly_solar_radiation.append(round(radiation * weather_factor, 1))
            else:
                hourly_solar_radiation.append(0)
        
        # 습도 (%)
        base_humidity = np.random.randint(50, 80)
        hourly_humidity = [
            max(30, min(95, base_humidity + np.random.randint(-10, 10)))
            for _ in range(24)
        ]
        
        # 풍속 (m/s)
        hourly_wind_speed = [
            round(np.random.uniform(1, 5), 1) for _ in range(24)
        ]
        
        # 강수량 (mm)
        rainfall_prob = 0.2 if month in [6, 7, 8, 9] else 0.1
        hourly_rainfall = [
            round(np.random.exponential(2), 1) if np.random.random() < rainfall_prob else 0
            for _ in range(24)
        ]
        
        return {
            "location": location,
            "date": date.strftime("%Y-%m-%d"),
            "hourly": {
                "temperature": hourly_temps,
                "solar_radiation": hourly_solar_radiation,
                "humidity": hourly_humidity,
                "wind_speed": hourly_wind_speed,
                "rainfall": hourly_rainfall
            },
            "daily_summary": {
                "temp_min": min(hourly_temps),
                "temp_max": max(hourly_temps),
                "temp_avg": round(np.mean(hourly_temps), 1),
                "total_radiation": round(sum(hourly_solar_radiation), 1),
                "avg_humidity": round(np.mean(hourly_humidity), 1),
                "total_rainfall": round(sum(hourly_rainfall), 1)
            }
        }
    
    def fetch_sensor_data(
        self,
        sensor_type: str,
        time_range: int = 24
    ) -> pd.DataFrame:
        """
        IoT 센서 데이터 조회
        
        Args:
            sensor_type: 센서 타입 (temperature, humidity, co2, light)
            time_range: 조회 시간 범위 (hours)
        
        Returns:
            센서 데이터 DataFrame
        """
        # 실제 IoT 센서 연동 시뮬레이션
        timestamps = pd.date_range(
            end=datetime.now(),
            periods=time_range * 60,  # 1분 간격
            freq='1min'
        )
        
        if sensor_type == "temperature":
            base_value = 22
            variation = 3
        elif sensor_type == "humidity":
            base_value = 65
            variation = 10
        elif sensor_type == "co2":
            base_value = 800
            variation = 200
        elif sensor_type == "light":
            base_value = 400
            variation = 200
        else:
            base_value = 50
            variation = 10
        
        # 시간대별 패턴 생성
        values = []
        for ts in timestamps:
            hour = ts.hour
            # 주기적 변화
            daily_pattern = np.sin((hour - 6) / 24 * 2 * np.pi)
            noise = np.random.normal(0, variation * 0.2)
            value = base_value + (variation * daily_pattern) + noise
            
            # 센서별 범위 제한
            if sensor_type == "temperature":
                value = max(15, min(30, value))
            elif sensor_type == "humidity":
                value = max(40, min(90, value))
            elif sensor_type == "co2":
                value = max(400, min(1500, value))
            elif sensor_type == "light":
                value = max(0, value) if 6 <= hour <= 18 else 0
            
            values.append(round(value, 2))
        
        df = pd.DataFrame({
            'timestamp': timestamps,
            'value': values,
            'sensor_type': sensor_type
        })
        
        return df
    
    def aggregate_sensor_data(
        self,
        df: pd.DataFrame,
        interval: str = '1H'
    ) -> pd.DataFrame:
        """
        센서 데이터 집계
        
        Args:
            df: 센서 데이터 DataFrame
            interval: 집계 간격 ('1H', '15min', etc.)
        
        Returns:
            집계된 DataFrame
        """
        df_agg = df.set_index('timestamp').resample(interval).agg({
            'value': ['mean', 'min', 'max', 'std']
        })
        df_agg.columns = ['mean', 'min', 'max', 'std']
        df_agg = df_agg.reset_index()
        
        return df_agg
    
    def calculate_weather_factor(
        self,
        weather_data: Dict,
        hour: int
    ) -> float:
        """
        날씨 보정 계수 계산
        
        Args:
            weather_data: 기상 데이터
            hour: 시간
        
        Returns:
            보정 계수 (0~1)
        """
        if 'hourly' not in weather_data:
            return 1.0
        
        hourly = weather_data['hourly']
        
        # 일사량 기반 계수
        solar_radiation = hourly['solar_radiation'][hour]
        max_radiation = 800  # W/m²
        radiation_factor = min(solar_radiation / max_radiation, 1.0)
        
        # 강수량 보정
        rainfall = hourly['rainfall'][hour]
        if rainfall > 5:
            rainfall_factor = 0.3
        elif rainfall > 1:
            rainfall_factor = 0.6
        elif rainfall > 0:
            rainfall_factor = 0.8
        else:
            rainfall_factor = 1.0
        
        # 종합 계수
        weather_factor = radiation_factor * rainfall_factor
        
        return round(weather_factor, 2)
    
    def export_to_csv(
        self,
        data: pd.DataFrame,
        filename: str
    ) -> str:
        """
        CSV로 데이터 내보내기
        
        Args:
            data: DataFrame
            filename: 파일명
        
        Returns:
            저장된 파일 경로
        """
        filepath = f"/home/claude/{filename}"
        data.to_csv(filepath, index=False, encoding='utf-8-sig')
        return filepath
    
    def export_to_excel(
        self,
        data_dict: Dict[str, pd.DataFrame],
        filename: str
    ) -> str:
        """
        Excel로 데이터 내보내기
        
        Args:
            data_dict: 시트명: DataFrame 딕셔너리
            filename: 파일명
        
        Returns:
            저장된 파일 경로
        """
        filepath = f"/home/claude/{filename}"
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            for sheet_name, df in data_dict.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        return filepath
    
    def create_report_data(
        self,
        calculation_results: Dict
    ) -> pd.DataFrame:
        """
        보고서용 데이터 생성
        
        Args:
            calculation_results: 계산 결과
        
        Returns:
            보고서 DataFrame
        """
        report_data = []
        
        # 기본 정보
        report_data.append({
            "구분": "개요",
            "항목": "보고서 생성일",
            "값": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "단위": "",
            "비고": ""
        })
        
        # 에너지 생산
        if "solar" in calculation_results:
            solar = calculation_results["solar"]
            report_data.append({
                "구분": "에너지 생산",
                "항목": "태양광 발전량",
                "값": solar.get("total_production_kwh", 0),
                "단위": "kWh",
                "비고": f"효율: {solar.get('efficiency_percent', 0)}%"
            })
        
        # 에너지 소비
        if "heat_pump" in calculation_results:
            hp = calculation_results["heat_pump"]
            report_data.append({
                "구분": "에너지 소비",
                "항목": "히트펌프 전력소비",
                "값": hp.get("electrical_consumption_kwh", 0),
                "단위": "kWh",
                "비고": f"COP: {hp.get('cop_adjusted', 0)}"
            })
        
        # 탄소 배출
        if "net" in calculation_results:
            net = calculation_results["net"]
            report_data.append({
                "구분": "탄소 배출",
                "항목": "순 탄소 배출량",
                "값": net.get("net_carbon_kg", 0),
                "단위": "kg CO2",
                "비고": "중립 달성" if net.get("is_carbon_neutral") else "감축 필요"
            })
            
            report_data.append({
                "구분": "효율성",
                "항목": "에너지 자급률",
                "값": net.get("self_sufficiency_percent", 0),
                "단위": "%",
                "비고": ""
            })
        
        df = pd.DataFrame(report_data)
        return df
    
    def get_benchmark_data(
        self,
        greenhouse_type: str,
        area_m2: float
    ) -> Dict:
        """
        벤치마크 데이터 조회
        
        Args:
            greenhouse_type: 온실 타입
            area_m2: 면적
        
        Returns:
            벤치마크 정보
        """
        # 평균 에너지 소비량 (kWh/m²/year)
        benchmarks = {
            "유리온실 (Glass)": {
                "energy_consumption_per_m2": 180,
                "solar_production_per_m2": 150,
                "carbon_emission_per_m2": 80
            },
            "비닐하우스 (Vinyl)": {
                "energy_consumption_per_m2": 150,
                "solar_production_per_m2": 140,
                "carbon_emission_per_m2": 65
            },
            "PC온실 (Polycarbonate)": {
                "energy_consumption_per_m2": 165,
                "solar_production_per_m2": 145,
                "carbon_emission_per_m2": 72
            }
        }
        
        benchmark = benchmarks.get(greenhouse_type, benchmarks["비닐하우스 (Vinyl)"])
        
        return {
            "greenhouse_type": greenhouse_type,
            "area_m2": area_m2,
            "annual_energy_consumption_kwh": benchmark["energy_consumption_per_m2"] * area_m2,
            "annual_solar_production_kwh": benchmark["solar_production_per_m2"] * area_m2,
            "annual_carbon_emission_kg": benchmark["carbon_emission_per_m2"] * area_m2,
            "per_m2_consumption": benchmark["energy_consumption_per_m2"],
            "per_m2_production": benchmark["solar_production_per_m2"],
            "per_m2_emission": benchmark["carbon_emission_per_m2"]
        }

"""
탄소제로 스마트팜 계산 시스템 - 설정 및 상수
Carbon Zero Smart Farm Calculator - Configuration
"""

# ==================== 탄소 배출 계수 ====================
# Carbon Emission Factors

# 한국 전력망 탄소 배출 계수 (kg CO2/kWh)
# Korea Grid Carbon Emission Factor
# 출처: 한국에너지공단 EG-TIPS (2023년 소비단 기준)
# Source: Korea Energy Agency EG-TIPS (2023 consumption-based)
GRID_CARBON_FACTOR = 0.4149  # 2023년 공식 배출계수

# 연도별 배출계수 (참고용)
CARBON_FACTORS_BY_YEAR = {
    "2023": 0.4149,  # 최신 (권장)
    "2021_2023_avg": 0.4307,  # 3개년 평균
    "generation": 0.3822,  # 발전단 (참고)
}

# ==================== 에너지 변환 계수 ====================
# Energy Conversion Factors

# 태양광 발전 효율 (%)
SOLAR_EFFICIENCY_DEFAULT = 18.5

# 히트펌프 성능계수 (COP)
HEAT_PUMP_COP_DEFAULT = 3.5  # 난방
HEAT_PUMP_COP_COOLING_DEFAULT = 3.0  # 냉방

# ==================== 온실 파라미터 ====================
# Greenhouse Parameters

# 온실 유형별 기본 설정
GREENHOUSE_TYPES = {
    "유리온실 (Glass)": {
        "insulation": 0.85,
        "light_transmission": 0.92,
        "description": "고급 유리온실, 높은 광투과율"
    },
    "비닐하우스 (Vinyl)": {
        "insulation": 0.70,
        "light_transmission": 0.88,
        "description": "일반 비닐하우스, 경제적"
    },
    "PC온실 (Polycarbonate)": {
        "insulation": 0.80,
        "light_transmission": 0.85,
        "description": "폴리카보네이트, 균형잡힌 성능"
    }
}

# ==================== 작물별 환경 요구사항 ====================
# Crop-specific Environmental Requirements

CROP_REQUIREMENTS = {
    "토마토 (Tomato)": {
        "temp_day": 24,
        "temp_night": 16,
        "humidity": 65,
        "co2_ppm": 800,
        "light_ppfd": 400
    },
    "딸기 (Strawberry)": {
        "temp_day": 23,
        "temp_night": 8,
        "humidity": 60,
        "co2_ppm": 700,
        "light_ppfd": 300
    },
    "파프리카 (Paprika)": {
        "temp_day": 25,
        "temp_night": 18,
        "humidity": 70,
        "co2_ppm": 900,
        "light_ppfd": 450
    },
    "상추 (Lettuce)": {
        "temp_day": 20,
        "temp_night": 15,
        "humidity": 65,
        "co2_ppm": 600,
        "light_ppfd": 200
    },
    "오이 (Cucumber)": {
        "temp_day": 26,
        "temp_night": 18,
        "humidity": 75,
        "co2_ppm": 850,
        "light_ppfd": 420
    }
}

# ==================== 시각화 색상 테마 ====================
# Visualization Color Theme

COLOR_THEME = {
    "primary": "#2E7D32",      # 진한 녹색
    "secondary": "#66BB6A",    # 밝은 녹색
    "accent": "#1976D2",       # 파란색
    "warning": "#F57C00",      # 주황색
    "danger": "#D32F2F",       # 빨간색
    "success": "#388E3C",      # 성공 녹색
    "background": "#F5F5F5",   # 배경 회색
    "text": "#212121"          # 텍스트 검정
}

# 차트 색상 팔레트
CHART_COLORS = {
    "solar_production": "#FFA726",     # 주황 (태양광)
    "heat_pump_consumption": "#42A5F5", # 파란 (히트펌프)
    "other_consumption": "#AB47BC",    # 보라 (기타)
    "net_carbon": "#66BB6A",           # 녹색 (순배출)
    "carbon_reduction": "#2E7D32"      # 진한녹색 (감축)
}

# ==================== API 설정 ====================
# API Configuration

# 기상청 API (실제 데이터 연동용)
KMA_API_KEY = "YOUR_KMA_API_KEY_HERE"

# 데이터 업데이트 주기 (초)
DATA_UPDATE_INTERVAL = 300  # 5분

# ==================== 계산 설정 ====================
# Calculation Settings

# 시간당 계산 간격 (시간)
CALCULATION_INTERVAL_HOURS = 1

# 연간 운영 일수
ANNUAL_OPERATION_DAYS = 365

# 월별 일수
DAYS_PER_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# ==================== UI 설정 ====================
# UI Settings

# 페이지 설정
PAGE_TITLE = "탄소제로 스마트팜 계산기"
PAGE_ICON = "🌱"
LAYOUT = "wide"

# 차트 기본 높이
CHART_HEIGHT = 400

# 메트릭 카드 설정
METRIC_DELTA_COLOR = "normal"

# ==================== 단위 변환 ====================
# Unit Conversions

UNITS = {
    "energy": {
        "kWh": 1.0,
        "MWh": 1000.0,
        "GJ": 277.78
    },
    "carbon": {
        "kg": 1.0,
        "ton": 1000.0,
        "g": 0.001
    },
    "area": {
        "m2": 1.0,
        "pyeong": 3.3058,
        "ha": 10000.0
    }
}

# ==================== 알림 임계값 ====================
# Alert Thresholds

THRESHOLDS = {
    "carbon_neutral": 0,  # 탄소중립 기준
    "high_efficiency": 0.8,  # 고효율 기준 (80%)
    "low_efficiency": 0.5,   # 저효율 경고 (50%)
    "critical_carbon": 100   # 탄소배출 위험 수준 (kg/day)
}

# ==================== 기본값 ====================
# Default Values

DEFAULTS = {
    "greenhouse_area": 1000,  # m²
    "solar_capacity": 100,    # kW
    "heat_pump_capacity": 50, # kW
    "operating_hours": 10,    # hours/day
    "temperature_setpoint": 22, # °C
    "outside_temp_summer": 30,  # °C
    "outside_temp_winter": -5   # °C
}

# ==================== 보고서 설정 ====================
# Report Settings

REPORT_FORMATS = ["PDF", "Excel", "CSV"]

REPORT_SECTIONS = [
    "개요 (Overview)",
    "에너지 생산/소비 (Energy Production/Consumption)",
    "탄소 배출/감축 (Carbon Emissions/Reductions)",
    "효율성 분석 (Efficiency Analysis)",
    "권장사항 (Recommendations)"
]

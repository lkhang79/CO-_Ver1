"""
탄소제로 스마트팜 계산 시스템 - 메인 애플리케이션
Carbon Zero Smart Farm Calculator - Main Application
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import config
from calculator import CarbonCalculator
from data_handler import DataHandler
from visualizer import Visualizer
from advanced_carbon_tech import AdvancedCarbonTech
from ess_system import ESSSystem

# 페이지 설정
st.set_page_config(
    page_title=config.PAGE_TITLE,
    page_icon=config.PAGE_ICON,
    layout=config.LAYOUT,
    initial_sidebar_state="expanded"
)

# CSS 스타일
st.markdown("""
<style>
    .main {
        background-color: #F5F5F5;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: white;
        border-radius: 8px 8px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2E7D32;
        color: white;
    }
    h1 {
        color: #2E7D32;
        font-weight: 700;
    }
    h2 {
        color: #1976D2;
        font-weight: 600;
    }
    h3 {
        color: #388E3C;
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 5px solid #2E7D32;
    }
    .stButton>button {
        background-color: #2E7D32;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #1B5E20;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .info-box {
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #2E7D32;
        margin: 10px 0;
    }
    .warning-box {
        background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #F57C00;
        margin: 10px 0;
    }
    .success-box {
        background: linear-gradient(135deg, #E8F5E9 0%, #A5D6A7 100%);
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #388E3C;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'calculator' not in st.session_state:
    st.session_state.calculator = CarbonCalculator()
if 'data_handler' not in st.session_state:
    st.session_state.data_handler = DataHandler()
if 'visualizer' not in st.session_state:
    st.session_state.visualizer = Visualizer()
if 'last_calculation' not in st.session_state:
    st.session_state.last_calculation = None

# 헤더
st.title("🌱 탄소제로 스마트팜 계산기")
st.markdown("**Carbon Zero Smart Farm Calculator** - 태양광 온실과 히트펌프 통합 분석 시스템")

# 사이드바
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/2E7D32/FFFFFF?text=Smart+Farm", use_column_width=True)
    st.markdown("---")
    
    st.markdown("### 📋 시스템 정보")
    st.info(f"""
    **버전:** 1.0.0  
    **업데이트:** {datetime.now().strftime('%Y-%m-%d')}  
    **모드:** 시뮬레이션 & 실시간
    """)
    
    st.markdown("---")
    st.markdown("### ⚙️ 설정")
    
    # 단위 설정
    energy_unit = st.selectbox("에너지 단위", ["kWh", "MWh", "GJ"], index=0)
    carbon_unit = st.selectbox("탄소 단위", ["kg CO2", "ton CO2"], index=0)
    
    # 전기요금
    electricity_rate = st.number_input(
        "전기요금 단가 (원/kWh)",
        min_value=50,
        max_value=300,
        value=150,
        step=10
    )
    
    st.markdown("---")
    st.markdown("### 📚 사용 가이드")
    with st.expander("도움말 보기"):
        st.markdown("""
        **실시간 모니터링 탭**
        - 실제 센서 데이터 연동
        - 기상 정보 자동 수집
        - 24시간 프로파일 분석
        
        **시뮬레이션 탭**
        - 파라미터 직접 입력
        - 시나리오 분석
        - 최적화 검토
        """)

# 메인 탭
tab1, tab2, tab3, tab4 = st.tabs(["📊 실시간 모니터링", "🔬 시뮬레이션", "🌱 고급 탄소저감 기술", "🔋 ESS 에너지저장장치"])

# ==================== 탭 1: 실시간 모니터링 ====================
with tab1:
    st.markdown("## 📡 실시간 데이터 모니터링")
    st.markdown("*IoT 센서와 기상 데이터를 실시간으로 수집하여 탄소 배출량을 계산합니다.*")
    
    # 상단 컨트롤
    col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
    
    with col1:
        location = st.selectbox("📍 위치", ["서울", "경기", "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주"])
    
    with col2:
        greenhouse_type_real = st.selectbox("🏠 온실 타입", list(config.GREENHOUSE_TYPES.keys()))
    
    with col3:
        crop_type = st.selectbox("🌾 작물", list(config.CROP_REQUIREMENTS.keys()))
    
    with col4:
        if st.button("🔄 새로고침", use_container_width=True):
            st.rerun()
    
    st.markdown("---")
    
    # 기상 데이터 가져오기
    weather_data = st.session_state.data_handler.fetch_weather_data(location)
    
    # 실시간 파라미터 (기본값 사용)
    greenhouse_params_real = {
        "area": 1000,
        "type": greenhouse_type_real,
        "lighting_power": 10,
        "irrigation_power": 5,
        "ventilation_power": 8,
        "control_power": 2
    }
    
    solar_params_real = {
        "capacity": 100,
        "efficiency": config.SOLAR_EFFICIENCY_DEFAULT,
        "weather_factor": 0.85
    }
    
    heat_pump_params_real = {
        "capacity": 50,
        "cop": config.HEAT_PUMP_COP_DEFAULT,
        "mode": "heating",
        "temp_diff": 25
    }
    
    # 24시간 프로파일 계산
    today = datetime.now()
    hourly_data_real = st.session_state.calculator.calculate_daily_profile(
        today, greenhouse_params_real, solar_params_real, heat_pump_params_real
    )
    
    # 현재 시간 데이터
    current_hour = today.hour
    current_data = hourly_data_real[current_hour]
    
    # KPI 카드
    st.markdown("### 📈 주요 지표 (현재 시간)")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "태양광 발전",
            f"{current_data['solar']['hourly_production_kwh']:.1f} kWh",
            delta=f"{current_data['solar']['efficiency_percent']:.1f}% 효율"
        )
    
    with col2:
        st.metric(
            "전력 소비",
            f"{current_data['net']['total_consumption_kwh']:.1f} kWh",
            delta=f"{current_data['heat_pump']['cop_adjusted']:.1f} COP"
        )
    
    with col3:
        net_carbon = current_data['net']['net_carbon_kg']
        st.metric(
            "순 탄소 배출",
            f"{abs(net_carbon):.1f} kg",
            delta="탄소중립" if net_carbon <= 0 else "배출중",
            delta_color="normal" if net_carbon <= 0 else "inverse"
        )
    
    with col4:
        st.metric(
            "에너지 자급률",
            f"{current_data['net']['self_sufficiency_percent']:.1f}%",
            delta="목표 100%"
        )
    
    st.markdown("---")
    
    # 차트 영역
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔋 에너지 균형")
        daily_production = sum([h['solar']['total_production_kwh'] for h in hourly_data_real])
        daily_consumption = sum([h['net']['total_consumption_kwh'] for h in hourly_data_real])
        
        fig_energy = st.session_state.visualizer.create_energy_balance_chart(
            daily_production, daily_consumption, "일일 에너지 균형"
        )
        st.plotly_chart(fig_energy, use_container_width=True)
    
    with col2:
        st.markdown("### 🌍 탄소 균형")
        daily_reduction = sum([h['solar']['carbon_reduction_kg'] for h in hourly_data_real])
        daily_emission = sum([h['heat_pump']['carbon_emission_kg'] + h['other']['carbon_emission_kg'] for h in hourly_data_real])
        
        fig_carbon = st.session_state.visualizer.create_carbon_balance_chart(
            daily_reduction, daily_emission, "일일 탄소 균형"
        )
        st.plotly_chart(fig_carbon, use_container_width=True)
    
    # 24시간 프로파일
    st.markdown("### ⏰ 24시간 에너지 프로파일")
    fig_hourly = st.session_state.visualizer.create_hourly_profile_chart(hourly_data_real)
    st.plotly_chart(fig_hourly, use_container_width=True)
    
    # 센서 데이터
    st.markdown("### 🌡️ 센서 데이터 (최근 24시간)")
    
    sensor_cols = st.columns(4)
    sensor_types = ["temperature", "humidity", "co2", "light"]
    sensor_names = ["온도 (°C)", "습도 (%)", "CO2 (ppm)", "광도 (PPFD)"]
    
    for idx, (col, sensor_type, sensor_name) in enumerate(zip(sensor_cols, sensor_types, sensor_names)):
        with col:
            sensor_df = st.session_state.data_handler.fetch_sensor_data(sensor_type, 24)
            current_value = sensor_df['value'].iloc[-1]
            avg_value = sensor_df['value'].mean()
            
            st.metric(
                sensor_name,
                f"{current_value:.1f}",
                delta=f"평균: {avg_value:.1f}"
            )
    
    # 기상 정보
    st.markdown("### ☀️ 기상 정보")
    weather_col1, weather_col2, weather_col3 = st.columns(3)
    
    with weather_col1:
        st.markdown(f"""
        <div class="info-box">
        <h4>🌡️ 온도</h4>
        <p><b>최저/최고:</b> {weather_data['daily_summary']['temp_min']}°C / {weather_data['daily_summary']['temp_max']}°C</p>
        <p><b>평균:</b> {weather_data['daily_summary']['temp_avg']}°C</p>
        </div>
        """, unsafe_allow_html=True)
    
    with weather_col2:
        st.markdown(f"""
        <div class="info-box">
        <h4>☀️ 일사량</h4>
        <p><b>총 일사량:</b> {weather_data['daily_summary']['total_radiation']:.0f} W/m²</p>
        <p><b>평균 습도:</b> {weather_data['daily_summary']['avg_humidity']}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with weather_col3:
        st.markdown(f"""
        <div class="info-box">
        <h4>🌧️ 강수</h4>
        <p><b>총 강수량:</b> {weather_data['daily_summary']['total_rainfall']:.1f} mm</p>
        <p><b>위치:</b> {location}</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== 탭 2: 시뮬레이션 ====================
with tab2:
    st.markdown("## 🔬 시뮬레이션 모드")
    st.markdown("*파라미터를 직접 입력하여 다양한 시나리오를 분석하고 최적 운영 조건을 찾아보세요.*")
    
    st.markdown("---")
    
    # 입력 섹션
    st.markdown("### ⚙️ 시스템 파라미터")
    
    with st.form("simulation_form"):
        # 온실 설정
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🏠 온실 정보")
            area_sim = st.number_input("온실 면적 (m²)", min_value=100, max_value=10000, value=1000, step=100)
            greenhouse_type_sim = st.selectbox("온실 타입", list(config.GREENHOUSE_TYPES.keys()), key="gh_type_sim")
            crop_type_sim = st.selectbox("재배 작물", list(config.CROP_REQUIREMENTS.keys()), key="crop_sim")
        
        with col2:
            st.markdown("#### ☀️ 태양광 설비")
            solar_capacity_sim = st.number_input("설비 용량 (kW)", min_value=10, max_value=500, value=100, step=10)
            solar_efficiency_sim = st.slider("발전 효율 (%)", min_value=10.0, max_value=25.0, value=18.5, step=0.5)
            weather_factor_sim = st.slider("날씨 보정 계수", min_value=0.3, max_value=1.0, value=0.85, step=0.05)
        
        st.markdown("---")
        
        # 히트펌프 설정
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔥 히트펌프")
            hp_capacity_sim = st.number_input("용량 (kW)", min_value=10, max_value=200, value=50, step=10)
            hp_cop_sim = st.slider("성능계수 (COP)", min_value=2.0, max_value=5.0, value=3.5, step=0.1)
            hp_mode_sim = st.selectbox("운전 모드", ["heating", "cooling"])
        
        with col2:
            st.markdown("#### 🌡️ 온도 조건")
            temp_setpoint_sim = st.number_input("목표 온도 (°C)", min_value=15, max_value=30, value=22, step=1)
            outside_temp_sim = st.number_input("외부 온도 (°C)", min_value=-10, max_value=35, value=5, step=1)
            operating_hours_sim = st.slider("일일 가동 시간 (h)", min_value=1, max_value=24, value=10, step=1)
        
        st.markdown("---")
        
        # 기타 설비
        st.markdown("#### 💡 기타 전력 소비 (시간당)")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            lighting_power_sim = st.number_input("조명 (kW)", min_value=0.0, max_value=50.0, value=10.0, step=1.0)
        
        with col2:
            irrigation_power_sim = st.number_input("관수 (kW)", min_value=0.0, max_value=20.0, value=5.0, step=1.0)
        
        with col3:
            ventilation_power_sim = st.number_input("환기 (kW)", min_value=0.0, max_value=30.0, value=8.0, step=1.0)
        
        with col4:
            control_power_sim = st.number_input("제어 (kW)", min_value=0.0, max_value=10.0, value=2.0, step=0.5)
        
        st.markdown("---")
        
        # 계산 기간
        st.markdown("#### 📅 분석 기간")
        analysis_period = st.selectbox("기간", ["일일", "월간", "연간"])
        
        if analysis_period == "월간":
            selected_month = st.slider("월", min_value=1, max_value=12, value=datetime.now().month)
        
        # 제출 버튼
        submitted = st.form_submit_button("🚀 계산 시작", use_container_width=True)
    
    # 계산 수행
    if submitted:
        with st.spinner("계산 중..."):
            # 파라미터 구성
            greenhouse_params_sim = {
                "area": area_sim,
                "type": greenhouse_type_sim,
                "lighting_power": lighting_power_sim,
                "irrigation_power": irrigation_power_sim,
                "ventilation_power": ventilation_power_sim,
                "control_power": control_power_sim
            }
            
            solar_params_sim = {
                "capacity": solar_capacity_sim,
                "efficiency": solar_efficiency_sim,
                "weather_factor": weather_factor_sim
            }
            
            temp_diff = abs(temp_setpoint_sim - outside_temp_sim)
            heat_pump_params_sim = {
                "capacity": hp_capacity_sim,
                "cop": hp_cop_sim,
                "mode": hp_mode_sim,
                "temp_diff": temp_diff
            }
            
            # 계산 수행
            if analysis_period == "일일":
                # 일일 프로파일
                hourly_data_sim = st.session_state.calculator.calculate_daily_profile(
                    datetime.now(), greenhouse_params_sim, solar_params_sim, heat_pump_params_sim
                )
                
                # 일일 합계
                daily_solar = sum([h['solar']['total_production_kwh'] for h in hourly_data_sim])
                daily_consumption = sum([h['net']['total_consumption_kwh'] for h in hourly_data_sim])
                daily_net_carbon = sum([h['net']['net_carbon_kg'] for h in hourly_data_sim])
                daily_carbon_reduction = sum([h['solar']['carbon_reduction_kg'] for h in hourly_data_sim])
                daily_carbon_emission = sum([h['heat_pump']['carbon_emission_kg'] + h['other']['carbon_emission_kg'] for h in hourly_data_sim])
                daily_self_sufficiency = (daily_solar / daily_consumption * 100) if daily_consumption > 0 else 0
                
                result = {
                    "period": "일일",
                    "hourly_data": hourly_data_sim,
                    "total_production": daily_solar,
                    "total_consumption": daily_consumption,
                    "net_carbon": daily_net_carbon,
                    "carbon_reduction": daily_carbon_reduction,
                    "carbon_emission": daily_carbon_emission,
                    "self_sufficiency": daily_self_sufficiency,
                    "is_carbon_neutral": daily_net_carbon <= 0
                }
                
            elif analysis_period == "월간":
                # 월간 요약
                monthly_summary = st.session_state.calculator.calculate_monthly_summary(
                    selected_month, greenhouse_params_sim, solar_params_sim, heat_pump_params_sim
                )
                
                result = {
                    "period": "월간",
                    "month": selected_month,
                    "data": monthly_summary
                }
                
            else:  # 연간
                # 연간 요약
                annual_summary = st.session_state.calculator.calculate_annual_summary(
                    greenhouse_params_sim, solar_params_sim, heat_pump_params_sim
                )
                
                result = {
                    "period": "연간",
                    "data": annual_summary
                }
            
            st.session_state.last_calculation = result
        
        st.success("✅ 계산 완료!")
    
    # 결과 표시
    if st.session_state.last_calculation is not None:
        result = st.session_state.last_calculation
        
        st.markdown("---")
        st.markdown("### 📊 계산 결과")
        
        if result["period"] == "일일":
            # KPI
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("태양광 발전", f"{result['total_production']:.1f} kWh")
            
            with col2:
                st.metric("전력 소비", f"{result['total_consumption']:.1f} kWh")
            
            with col3:
                net_carbon_display = abs(result['net_carbon'])
                st.metric(
                    "순 탄소",
                    f"{net_carbon_display:.1f} kg",
                    delta="중립" if result['is_carbon_neutral'] else "배출",
                    delta_color="normal" if result['is_carbon_neutral'] else "inverse"
                )
            
            with col4:
                st.metric("자급률", f"{result['self_sufficiency']:.1f}%")
            
            # 차트
            col1, col2 = st.columns(2)
            
            with col1:
                fig = st.session_state.visualizer.create_energy_balance_chart(
                    result['total_production'], result['total_consumption']
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = st.session_state.visualizer.create_carbon_balance_chart(
                    result['carbon_reduction'], result['carbon_emission']
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # 24시간 프로파일
            st.markdown("#### ⏰ 24시간 에너지 프로파일")
            fig = st.session_state.visualizer.create_hourly_profile_chart(result['hourly_data'])
            st.plotly_chart(fig, use_container_width=True)
            
            # 경제성 분석
            st.markdown("#### 💰 경제성 분석")
            annual_savings = result['total_production'] * 365
            roi_result = st.session_state.calculator.calculate_roi(
                initial_investment=solar_capacity_sim * 2000000,  # kW당 200만원 가정
                annual_savings=annual_savings,
                maintenance_cost=solar_capacity_sim * 50000,  # kW당 5만원 유지비
                electricity_rate=electricity_rate
            )
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("투자회수기간", f"{roi_result['payback_period_years']:.1f}년")
            
            with col2:
                st.metric("연간 절감액", f"{roi_result['net_annual_savings_krw']:,.0f}원")
            
            with col3:
                st.metric("20년 NPV", f"{roi_result['npv_krw']:,.0f}원")
        
        elif result["period"] == "월간":
            data = result['data']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("월간 발전량", f"{data['total_production_kwh']:,.1f} kWh")
            
            with col2:
                st.metric("월간 소비량", f"{data['total_consumption_kwh']:,.1f} kWh")
            
            with col3:
                st.metric("월간 순 탄소", f"{abs(data['net_carbon_kg']):,.1f} kg")
            
            # 일일 평균
            st.markdown("#### 📈 일일 평균")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("평균 발전", f"{data['avg_daily_production']:.1f} kWh/일")
            
            with col2:
                st.metric("평균 소비", f"{data['avg_daily_consumption']:.1f} kWh/일")
            
            with col3:
                st.metric("평균 탄소", f"{abs(data['avg_daily_net_carbon']):.1f} kg/일")
        
        else:  # 연간
            data = result['data']
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("연간 발전량", f"{data['annual_production_kwh']:,.0f} kWh")
            
            with col2:
                st.metric("연간 소비량", f"{data['annual_consumption_kwh']:,.0f} kWh")
            
            with col3:
                st.metric("연간 순 탄소", f"{abs(data['annual_net_carbon_ton']):.2f} ton")
            
            with col4:
                st.metric("에너지 자급률", f"{data['self_sufficiency_percent']:.1f}%")
            
            # 월별 차트
            st.markdown("#### 📊 월별 추이")
            
            tab_prod, tab_cons, tab_carbon = st.tabs(["발전량", "소비량", "탄소"])
            
            with tab_prod:
                fig = st.session_state.visualizer.create_monthly_chart(
                    data['monthly_data'], "total_production_kwh", "월별 태양광 발전량"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with tab_cons:
                fig = st.session_state.visualizer.create_monthly_chart(
                    data['monthly_data'], "total_consumption_kwh", "월별 전력 소비량"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with tab_carbon:
                fig = st.session_state.visualizer.create_monthly_chart(
                    data['monthly_data'], "net_carbon_kg", "월별 순 탄소 배출량"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # 다운로드 버튼
        st.markdown("---")
        st.markdown("### 📥 결과 다운로드")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 CSV 다운로드", use_container_width=True):
                # CSV 데이터 생성
                report_df = st.session_state.data_handler.create_report_data(result)
                csv = report_df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="💾 CSV 저장",
                    data=csv,
                    file_name=f"carbon_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            st.button("📊 Excel 다운로드", use_container_width=True, disabled=True)
            st.caption("*개발 예정*")
        
        with col3:
            st.button("📑 PDF 리포트", use_container_width=True, disabled=True)
            st.caption("*개발 예정*")

# ==================== 탭 3: 고급 탄소저감 기술 ====================
with tab3:
    st.markdown("## 🌱 고급 탄소저감 기술 & 탄소제로 달성")
    st.markdown("*CO2 시비, 탄소포집, PPA 계약, REC 구매 등을 활용한 종합 탄소저감 전략*")
    
    # Advanced Carbon Tech 객체 생성
    adv_carbon = AdvancedCarbonTech()
    
    st.markdown("---")
    
    # 섹션 선택
    section = st.selectbox(
        "📌 분석 섹션 선택",
        ["CO2 시비 & 생산성 향상", "탄소포집 기술 (DAC & 연료전지)", "PPA 전력구매계약", "REC 인증서 구매", "통합 탄소제로 시나리오", "최적 전략 추천"]
    )
    
    st.markdown("---")
    
    # ==================== 섹션 1: CO2 시비 ====================
    if section == "CO2 시비 & 생산성 향상":
        st.markdown("### 🌿 CO2 시비 (CO2 Enrichment)")
        
        st.markdown("""
        <div class='info-box'>
        <h4>💡 CO2 시비란?</h4>
        작물은 광합성 과정에서 이산화탄소를 흡수합니다. 온실 내 CO2 농도를 대기 농도(약 400ppm)보다 높게 유지하면 
        광합성이 활발해져 작물 생장 속도가 크게 증가합니다. 최적 농도는 800~1000ppm 수준입니다.
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 📊 시뮬레이션 파라미터")
            
            greenhouse_area = st.number_input("온실 면적 (m²)", min_value=100, max_value=100000, value=5000, step=100)
            co2_target = st.slider("목표 CO2 농도 (ppm)", min_value=400, max_value=1200, value=800, step=50)
            co2_ambient = st.number_input("대기 CO2 농도 (ppm)", min_value=350, max_value=450, value=400, step=10)
            operating_hours = st.slider("일일 운영시간", min_value=6, max_value=16, value=10, step=1)
            crop_select = st.selectbox("작물 선택", list(config.CROP_REQUIREMENTS.keys()))
        
        with col2:
            st.markdown("#### 📈 계산 결과")
            
            co2_result = adv_carbon.calculate_co2_fertilization(
                greenhouse_area_m2=greenhouse_area,
                co2_target_ppm=co2_target,
                co2_ambient_ppm=co2_ambient,
                operating_hours=operating_hours,
                crop_type=crop_select
            )
            
            st.metric("온실 체적", f"{co2_result['greenhouse_volume_m3']:,.0f} m³")
            st.metric("일일 CO2 필요량", f"{co2_result['daily_co2_required_kg']:.1f} kg/day")
            st.metric("생산성 증가율", f"+{co2_result['productivity_increase_percent']:.1f}%", delta="향상")
            
            st.markdown("---")
            
            st.markdown(f"""
            <div class='success-box'>
            <h4>✅ 예상 효과</h4>
            현재 설정으로 {crop_select} 재배 시 <b>{co2_result['productivity_increase_percent']:.1f}%</b>의 
            생산성 향상이 예상됩니다. 일일 약 <b>{co2_result['daily_co2_required_kg']:.1f}kg</b>의 CO2가 필요하며, 
            이는 탄소포집 시스템이나 연료전지 배기가스로 공급 가능합니다.
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("#### 📚 관련 연구 사례")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **한국화학연구원 DAC 실증**  
            경북 상주 스마트팜에서 대기 중 CO2를 직접 포집하여 600~700ppm까지 농도를 높여 
            토마토 재배에 활용하는 실증을 완료했습니다.
            """)
        
        with col2:
            st.markdown("""
            **SK에코플랜트 연료전지 CCU**  
            부산 연료전지 발전소에서 배출되는 CO2를 포집하여 스마트팜에 공급하고, 
            폐열을 난방에 활용하는 통합 시스템을 구축했습니다.
            """)
        
        with col3:
            st.markdown("""
            **연구 논문 결과**  
            상추 95~322% 증가, 딸기 27% 무게 증가 및 18% 당도 증가가 확인되었으며, 
            시간당 약 1.25g의 CO2 저감 효과가 있었습니다.
            """)
    
    # ==================== 섹션 2: 탄소포집 ====================
    elif section == "탄소포집 기술 (DAC & 연료전지)":
        st.markdown("### ⚗️ 탄소포집 기술 (Carbon Capture)")
        
        tab_dac, tab_fuel = st.tabs(["DAC (공기 포집)", "연료전지 CO2 포집"])
        
        with tab_dac:
            st.markdown("""
            <div class='info-box'>
            <h4>💡 DAC (Direct Air Capture)란?</h4>
            대기 중의 CO2를 직접 포집하여 농축하는 기술입니다. 포집된 CO2는 온실 내 작물 생장에 활용되며, 
            탄소중립 및 생산성 향상에 동시에 기여합니다.
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### 📊 DAC 시스템 설정")
                
                dac_capacity = st.number_input("DAC 일일 포집 용량 (kg CO2/day)", min_value=1.0, max_value=100.0, value=10.0, step=1.0)
                dac_days = st.number_input("연간 운영일수", min_value=200, max_value=365, value=300, step=10)
                dac_power = st.number_input("kg CO2당 전력 소비 (kWh/kg)", min_value=1.0, max_value=3.0, value=1.5, step=0.1)
            
            with col2:
                st.markdown("#### 📈 포집 효과 분석")
                
                dac_result = adv_carbon.calculate_dac_carbon_capture(
                    dac_capacity_kg_per_day=dac_capacity,
                    operating_days=dac_days,
                    power_consumption_kwh_per_kg=dac_power
                )
                
                st.metric("연간 포집량", f"{dac_result['annual_capture_kg']:,.0f} kg CO2")
                st.metric("연간 전력 소비", f"{dac_result['annual_power_consumption_kwh']:,.0f} kWh")
                st.metric("순 포집량", f"{dac_result['net_capture_kg']:,.0f} kg CO2", delta=f"{dac_result['capture_efficiency_percent']:.1f}% 효율")
                
                st.markdown("---")
                
                if dac_result['capture_efficiency_percent'] > 80:
                    box_type = 'success-box'
                    icon = '✅'
                    message = '우수'
                elif dac_result['capture_efficiency_percent'] > 60:
                    box_type = 'info-box'
                    icon = '⚠️'
                    message = '양호'
                else:
                    box_type = 'warning-box'
                    icon = '❌'
                    message = '개선 필요'
                
                st.markdown(f"""
                <div class='{box_type}'>
                <h4>{icon} 포집 효율: {message}</h4>
                연간 <b>{dac_result['annual_capture_kg']:,.0f}kg</b>의 CO2를 포집하지만, 
                전력 소비로 인해 <b>{dac_result['carbon_emission_from_power_kg']:,.0f}kg</b>의 탄소가 배출됩니다. 
                순 포집 효율은 <b>{dac_result['capture_efficiency_percent']:.1f}%</b>입니다.
                </div>
                """, unsafe_allow_html=True)
        
        with tab_fuel:
            st.markdown("""
            <div class='info-box'>
            <h4>💡 연료전지 CO2 포집이란?</h4>
            연료전지는 수소와 산소의 전기화학 반응으로 전기를 생산하며, 이 과정에서 CO2가 배출됩니다. 
            배기가스에서 CO2를 포집하면 스마트팜 CO2 시비에 활용할 수 있으며, 폐열도 난방에 사용 가능합니다.
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### 📊 연료전지 시스템 설정")
                
                fc_capacity = st.number_input("연료전지 용량 (kW)", min_value=10, max_value=500, value=50, step=10)
                fc_hours = st.slider("일일 운영시간", min_value=8, max_value=24, value=24, step=1)
                fc_emission_rate = st.number_input("kWh당 CO2 배출률 (kg/kWh)", min_value=0.1, max_value=0.3, value=0.15, step=0.01)
                fc_capture_eff = st.slider("포집 효율 (%)", min_value=70, max_value=95, value=90, step=5) / 100
            
            with col2:
                st.markdown("#### 📈 포집 결과")
                
                fc_result = adv_carbon.calculate_fuel_cell_co2_capture(
                    fuel_cell_capacity_kw=fc_capacity,
                    operating_hours=fc_hours,
                    co2_emission_rate_kg_per_kwh=fc_emission_rate,
                    capture_efficiency=fc_capture_eff
                )
                
                st.metric("일일 발전량", f"{fc_result['daily_generation_kwh']:,.0f} kWh")
                st.metric("총 CO2 배출", f"{fc_result['total_co2_emission_kg']:,.1f} kg/day")
                st.metric("포집량 (시비 가능)", f"{fc_result['captured_co2_kg']:,.1f} kg/day", delta=f"{fc_result['capture_efficiency_percent']:.0f}% 포집")
                st.metric("대기 방출", f"{fc_result['released_co2_kg']:,.1f} kg/day")
                
                st.markdown("---")
                
                st.markdown(f"""
                <div class='success-box'>
                <h4>✅ 시비 활용 가능</h4>
                일일 <b>{fc_result['available_for_fertilization_kg']:,.1f}kg</b>의 CO2를 스마트팜 시비에 활용할 수 있습니다. 
                또한 연료전지 폐열을 난방에 활용하면 히트펌프 전력 소비를 크게 줄일 수 있습니다.
                </div>
                """, unsafe_allow_html=True)
    
    # ==================== 섹션 3: PPA ====================
    elif section == "PPA 전력구매계약":
        st.markdown("### ⚡ PPA (Power Purchase Agreement) 전력구매계약")
        
        st.markdown("""
        <div class='info-box'>
        <h4>💡 PPA란?</h4>
        재생에너지 발전사업자와 직접 전력구매계약을 체결하여 재생에너지 전력을 공급받는 제도입니다. 
        계약을 통해 장기간 안정적인 가격으로 친환경 전력을 사용할 수 있으며, 사용 전력의 탄소배출을 제로로 인정받습니다.
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 📊 PPA 계약 시뮬레이션")
            
            ppa_consumption = st.number_input("연간 전력 소비량 (kWh)", min_value=10000, max_value=10000000, value=500000, step=10000)
            ppa_percent = st.slider("PPA 재생에너지 비율 (%)", min_value=0, max_value=100, value=100, step=5)
            ppa_price = st.number_input("PPA 전력 단가 (원/kWh)", min_value=100.0, max_value=200.0, value=150.0, step=5.0)
            ppa_years = st.number_input("계약 기간 (년)", min_value=5, max_value=25, value=20, step=5)
        
        with col2:
            st.markdown("#### 📈 탄소저감 효과")
            
            ppa_result = adv_carbon.calculate_ppa_impact(
                annual_consumption_kwh=ppa_consumption,
                ppa_renewable_percent=ppa_percent,
                ppa_price_krw_per_kwh=ppa_price,
                contract_years=ppa_years
            )
            
            st.metric("PPA 재생에너지", f"{ppa_result['ppa_renewable_kwh']:,.0f} kWh/년")
            st.metric("일반 전력", f"{ppa_result['grid_power_kwh']:,.0f} kWh/년")
            st.metric("탄소 감축량", f"{ppa_result['carbon_reduction_kg']:,.0f} kg CO2/년", delta=f"{ppa_result['carbon_reduction_percent']:.1f}% 감소")
            
            st.markdown("---")
            
            st.markdown("#### 💰 비용 분석")
            st.metric("연간 PPA 비용", f"{ppa_result['annual_ppa_cost_krw']:,.0f} 원")
            st.metric(f"{ppa_years}년 총 계약 비용", f"{ppa_result['total_contract_cost_krw']:,.0f} 원")
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **제3자 PPA**  
            한전을 중개로 발전사업자와 계약을 체결합니다. 기존 전력망을 활용하므로 설비 투자가 불필요하며, 
            비교적 간단한 절차로 시작할 수 있습니다.
            """)
        
        with col2:
            st.markdown("""
            **직접 PPA**  
            발전사업자와 직접 계약하여 전력을 공급받습니다. 더 유연한 계약 조건이 가능하며, 
            2022년부터 전면 시행되어 선택의 폭이 넓어졌습니다.
            """)
        
        with col3:
            st.markdown("""
            **RE100 인정**  
            PPA를 통해 공급받은 전력은 '재생에너지 사용 확인서'를 발급받아 RE100 및 
            온실가스 감축 실적으로 인정받을 수 있습니다.
            """)
    
    # ==================== 섹션 4: REC ====================
    elif section == "REC 인증서 구매":
        st.markdown("### 📜 REC (Renewable Energy Certificate) 신재생에너지공급인증서")
        
        st.markdown("""
        <div class='info-box'>
        <h4>💡 REC란?</h4>
        신재생에너지 발전사업자가 1MWh의 재생에너지를 생산했음을 증명하는 인증서입니다. 
        REC를 구매하면 그만큼의 전력을 재생에너지로 사용한 것으로 인정받아 탄소배출량을 줄일 수 있습니다.
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 📊 REC 구매 시뮬레이션")
            
            rec_consumption_mwh = st.number_input("연간 전력 소비량 (MWh)", min_value=10.0, max_value=10000.0, value=500.0, step=10.0)
            rec_purchase_mwh = st.number_input("REC 구매량 (MWh)", min_value=0.0, max_value=10000.0, value=250.0, step=10.0)
            rec_price = st.number_input("REC 가격 (원/REC)", min_value=30000, max_value=100000, value=50000, step=5000)
            rec_weight = st.selectbox("REC 가중치", [0.7, 0.8, 1.0, 1.2, 1.5], index=2)
            
            st.caption("*가중치는 발전원에 따라 달라집니다: 태양광(고정) 1.0, 태양광(건물) 1.5, 풍력 1.0 등*")
        
        with col2:
            st.markdown("#### 📈 탄소저감 효과")
            
            rec_result = adv_carbon.calculate_rec_impact(
                annual_consumption_mwh=rec_consumption_mwh,
                rec_purchase_mwh=rec_purchase_mwh,
                rec_price_krw=rec_price,
                rec_weight=rec_weight
            )
            
            st.metric("REC 인증서 수량", f"{rec_result['rec_certificates']:.1f} REC")
            st.metric("재생에너지 비율", f"{rec_result['rec_renewable_percent']:.1f}%")
            st.metric("탄소 감축량", f"{rec_result['carbon_reduction_kg']:,.0f} kg CO2/년", delta=f"{rec_result['carbon_reduction_percent']:.1f}% 감소")
            
            st.markdown("---")
            
            st.markdown("#### 💰 비용 분석")
            st.metric("총 REC 구매 비용", f"{rec_result['total_rec_cost_krw']:,.0f} 원/년")
            st.metric("kWh당 탄소저감 비용", f"{rec_result['cost_per_kwh_reduction_krw']:.2f} 원/kWh")
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **REC 발급**  
            신재생에너지 발전사업자는 1MWh 생산 시 가중치를 적용한 REC를 발급받습니다. 
            발급된 REC는 RPS 계약시장, 현물시장, RE100 시장에서 거래됩니다.
            """)
        
        with col2:
            st.markdown("""
            **구매 방법**  
            기업은 RPS 종합지원시스템 또는 재생에너지 클라우드 플랫폼을 통해 REC를 구매할 수 있습니다. 
            구매한 REC는 재생e 사용 확인서로 발급됩니다.
            """)
        
        with col3:
            st.markdown("""
            **활용 효과**  
            REC 구매량만큼 재생에너지로 인정받아 Scope 2 배출량을 줄일 수 있습니다. 
            RE100 달성 및 ESG 경영에 활용 가능합니다.
            """)
    
    # ==================== 섹션 5: 통합 시나리오 ====================
    elif section == "통합 탄소제로 시나리오":
        st.markdown("### 🎯 통합 탄소제로 달성 시나리오")
        
        st.markdown("""
        <div class='info-box'>
        <h4>💡 통합 전략이란?</h4>
        자가 태양광, PPA 계약, REC 구매, CO2 포집 등 여러 방법을 조합하여 탄소배출 제로를 달성하는 종합 전략입니다. 
        각 방법의 장단점을 고려하여 최적의 조합을 찾을 수 있습니다.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 📊 시나리오 설정")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            annual_consumption = st.number_input("연간 전력 소비량 (kWh)", min_value=10000, max_value=10000000, value=500000, step=10000)
            
            st.markdown("##### 🌞 자가 태양광")
            solar_production = st.number_input("연간 태양광 발전량 (kWh)", min_value=0, max_value=1000000, value=150000, step=10000)
            
            st.markdown("##### ⚡ PPA 계약")
            ppa_percent_scenario = st.slider("PPA 재생에너지 비율 (%)", min_value=0, max_value=100, value=50, step=5)
            
            st.markdown("##### 📜 REC 구매")
            rec_mwh_scenario = st.number_input("REC 구매량 (MWh)", min_value=0.0, max_value=1000.0, value=100.0, step=10.0)
            
            st.markdown("##### ⚗️ CO2 포집")
            co2_capture = st.number_input("연간 CO2 포집량 (kg)", min_value=0, max_value=100000, value=3000, step=100)
        
        with col2:
            st.markdown("#### 📈 탄소제로 달성 분석")
            
            scenario_result = adv_carbon.calculate_carbon_zero_scenario(
                annual_consumption_kwh=annual_consumption,
                solar_production_kwh=solar_production,
                ppa_percent=ppa_percent_scenario,
                rec_mwh=rec_mwh_scenario,
                co2_capture_kg=co2_capture
            )
            
            st.metric("기준 탄소 배출", f"{scenario_result['baseline_carbon_kg']:,.0f} kg CO2/년")
            st.metric("총 탄소 감축", f"{scenario_result['total_reduction_kg']:,.0f} kg CO2/년", delta=f"{scenario_result['carbon_reduction_percent']:.1f}% 감소")
            st.metric("순 탄소 배출", f"{scenario_result['net_carbon_kg']:,.0f} kg CO2/년")
            
            st.markdown("---")
            
            if scenario_result['is_carbon_zero']:
                st.markdown(f"""
                <div class='success-box'>
                <h3>✅ 탄소제로 달성!</h3>
                현재 시나리오로 <b>탄소배출 제로</b>를 달성했습니다. 
                총 <b>{scenario_result['total_reduction_kg']:,.0f}kg</b>의 탄소를 감축하여 
                순 배출량이 0 이하가 되었습니다.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='warning-box'>
                <h3>⚠️ 탄소제로 미달성</h3>
                현재 시나리오로는 탄소제로를 달성하지 못했습니다. 
                <b>{scenario_result['remaining_carbon_kg']:,.0f}kg</b>의 탄소가 아직 배출됩니다. 
                추가 감축 방법을 검토하시기 바랍니다.
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("#### 📊 감축 방법별 기여도")
        
        # 기여도 차트
        import plotly.graph_objects as go
        
        contributions = scenario_result['contributions']
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(contributions.keys()),
                y=list(contributions.values()),
                marker_color=['#4CAF50', '#2196F3', '#FF9800', '#9C27B0'],
                text=[f"{v:.1f}%" for v in contributions.values()],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="감축 방법별 기여도",
            xaxis_title="감축 방법",
            yaxis_title="기여도 (%)",
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("태양광 감축", f"{scenario_result['solar_reduction_kg']:,.0f} kg", delta=f"{contributions['태양광 (Solar)']:.1f}%")
        
        with col2:
            st.metric("PPA 감축", f"{scenario_result['ppa_reduction_kg']:,.0f} kg", delta=f"{contributions['PPA']:.1f}%")
        
        with col3:
            st.metric("REC 감축", f"{scenario_result['rec_reduction_kg']:,.0f} kg", delta=f"{contributions['REC']:.1f}%")
        
        with col4:
            st.metric("CO2 포집", f"{scenario_result['capture_reduction_kg']:,.0f} kg", delta=f"{contributions['CO2 포집 (Capture)']:.1f}%")
    
    # ==================== 섹션 6: 최적 전략 추천 ====================
    else:  # "최적 전략 추천"
        st.markdown("### 🎯 최적 탄소제로 전략 추천")
        
        st.markdown("""
        <div class='info-box'>
        <h4>💡 AI 기반 전략 추천</h4>
        귀사의 연간 전력 소비량, 가용 예산, 설치 가능 면적을 기반으로 최적의 탄소제로 달성 전략을 추천해드립니다. 
        초기 투자비용, 운영비용, 탄소저감 효과를 종합적으로 고려합니다.
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 📊 기본 정보 입력")
            
            strategy_consumption = st.number_input("연간 전력 소비량 (kWh)", min_value=10000, max_value=10000000, value=500000, step=10000)
            strategy_budget = st.number_input("가용 예산 (원)", min_value=1000000, max_value=10000000000, value=100000000, step=10000000)
            strategy_area = st.number_input("태양광 설치 가능 면적 (m²)", min_value=0, max_value=100000, value=1000, step=100)
        
        with col2:
            st.markdown("#### 🎯 AI 추천 결과")
            
            if st.button("🤖 최적 전략 생성", use_container_width=True):
                strategy_result = adv_carbon.recommend_carbon_zero_strategy(
                    annual_consumption_kwh=strategy_consumption,
                    available_budget_krw=strategy_budget,
                    available_area_m2=strategy_area
                )
                
                st.markdown(f"""
                <div class='success-box'>
                <h3>✅ 추천 전략: {strategy_result['recommendation']}</h3>
                <p><b>추천 이유:</b> {strategy_result['reason']}</p>
                <p><b>목표 감축량:</b> {strategy_result['target_reduction_kg']:,.0f} kg CO2/년</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                st.markdown("#### 📋 세부 옵션 비교")
                
                # 옵션 비교 테이블
                options_data = {
                    "방법": ["자가 태양광", "PPA 계약", "REC 구매", "하이브리드"],
                    "초기 투자": [
                        f"{strategy_result['solar_option']['initial_cost_krw']:,.0f}원",
                        "-",
                        "-",
                        "중간"
                    ],
                    "연간 비용": [
                        "-",
                        f"{strategy_result['ppa_option']['annual_cost_krw']:,.0f}원",
                        f"{strategy_result['rec_option']['annual_cost_krw']:,.0f}원",
                        "변동"
                    ],
                    "유연성": [
                        "낮음 (고정)",
                        strategy_result['ppa_option']['flexibility'],
                        strategy_result['rec_option']['flexibility'],
                        "높음"
                    ],
                    "특징": [
                        f"투자회수 {strategy_result['solar_option']['payback_years']}년",
                        f"{strategy_result['ppa_option']['contract_years']}년 장기계약",
                        "즉시 적용 가능",
                        strategy_result['hybrid_option']['rationale']
                    ]
                }
                
                df_options = pd.DataFrame(options_data)
                st.dataframe(df_options, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        st.markdown("#### 💡 전략별 상세 가이드")
        
        tab_solar, tab_ppa, tab_rec, tab_hybrid = st.tabs(["☀️ 자가 태양광", "⚡ PPA", "📜 REC", "🔀 하이브리드"])
        
        with tab_solar:
            st.markdown("""
            자가 태양광 발전은 초기 투자비가 높지만 장기적으로 가장 경제적인 방법입니다. 
            설치 가능 면적이 충분하고 예산이 허락한다면 우선적으로 검토할 만합니다. 
            평균 투자회수기간은 7년 정도이며, 이후 20~25년간 무료로 전력을 생산할 수 있습니다.
            
            주요 장점은 전력 생산과 동시에 탄소 감축 효과가 발생하며, REC 판매 수익도 기대할 수 있다는 점입니다. 
            또한 전력 자급률을 높여 에너지 안보에도 기여합니다.
            """)
        
        with tab_ppa:
            st.markdown("""
            PPA 계약은 초기 투자 없이 재생에너지를 사용할 수 있는 방법입니다. 
            발전사업자와 장기 계약을 체결하여 안정적인 가격으로 친환경 전력을 공급받습니다. 
            계약 기간은 보통 10~20년이며, 이 기간 동안 전력 가격이 고정됩니다.
            
            제3자 PPA는 한전이 중개하여 비교적 간단하게 시작할 수 있으며, 직접 PPA는 더 유연한 계약 조건이 가능합니다. 
            PPA를 통한 전력 사용은 RE100 달성에 인정되며, 탄소배출 제로로 간주됩니다.
            """)
        
        with tab_rec:
            st.markdown("""
            REC 구매는 가장 빠르고 간단하게 탄소 감축을 인정받을 수 있는 방법입니다. 
            신재생에너지 발전사업자로부터 인증서를 구매하면 그만큼의 전력을 재생에너지로 사용한 것으로 인정됩니다. 
            연단위로 구매량을 조정할 수 있어 유연성이 높습니다.
            
            다만 실제로 재생에너지를 사용하는 것이 아니라 인증서만 구매하는 것이므로, 
            그린워싱 논란에서 자유롭지 못하다는 비판도 있습니다. 
            가격은 시장 상황에 따라 변동하며, 현재 REC당 3~10만원 수준입니다.
            """)
        
        with tab_hybrid:
            st.markdown("""
            하이브리드 전략은 여러 방법을 조합하여 각각의 장점을 활용하는 접근입니다. 
            예를 들어 자가 태양광으로 30%를 충당하고, PPA로 50%를 확보한 후, 나머지 20%는 REC로 보완하는 방식입니다.
            
            이러한 조합을 통해 투자 리스크를 분산하고, 시장 변화에 유연하게 대응할 수 있습니다. 
            또한 단계적으로 탄소제로를 달성하면서 경험을 쌓을 수 있다는 장점이 있습니다. 
            대부분의 선진 기업들이 이러한 하이브리드 전략을 채택하고 있습니다.
            """)



# ==================== 탭 4: ESS 에너지저장장치 ====================
with tab4:
    st.markdown("## 🔋 ESS 에너지저장장치 시스템")
    st.markdown("*태양광 발전의 시간적 불일치 문제를 해결하고 전력 자급률을 획기적으로 향상시키는 핵심 기술*")
    
    # ESS 시스템 객체 생성
    ess = ESSSystem()
    
    # 상단 안내 메시지
    st.markdown("""
    <div class='info-box'>
    <h4>💡 ESS(에너지저장장치)란?</h4>
    ESS는 태양광 발전의 가장 큰 약점인 시간적 불일치 문제를 해결하는 핵심 기술입니다. 낮 시간에 생산한 전력을 저장했다가 
    야간 난방과 조명에 사용함으로써 전력 자급률을 35%에서 최대 80%까지 끌어올릴 수 있습니다. 또한 전력요금 피크와 
    심야 시간대의 단가 차이를 활용하여 운영비용을 크게 절감할 수 있으며, 계통 안정화에 기여하여 주파수조정(FR) 서비스 
    수익도 창출할 수 있습니다. 정부는 신재생에너지 보급사업을 통해 초기 투자비의 30~50%를 보조금으로 지원하고 있어 
    경제성이 더욱 개선되고 있습니다.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 섹션 선택
    ess_section = st.selectbox(
        "📌 분석 섹션 선택",
        [
            "ESS 용량 설계",
            "일일 운영 시뮬레이션",
            "탄소저감 효과 분석",
            "투자 경제성 분석",
            "용량별 시나리오 비교",
            "배터리 기술 비교"
        ]
    )
    
    st.markdown("---")
    
    # ==================== 섹션 1: ESS 용량 설계 ====================
    if ess_section == "ESS 용량 설계":
        st.markdown("### 📐 최적 ESS 용량 설계")
        
        st.markdown("""
        ESS 용량 설계는 태양광 발전 용량, 일일 전력 소비 패턴, 그리고 목표 자급률을 종합적으로 고려하여 
        결정됩니다. 용량이 너무 작으면 태양광 잉여전력을 충분히 저장하지 못하고, 너무 크면 투자비 대비 
        효율이 떨어집니다. 일반적으로 태양광 일일 발전량의 60~80% 수준으로 설계하는 것이 최적이며, 
        야간 소비량의 50~70%를 커버할 수 있도록 하는 것이 경제적입니다.
        """)
        
        st.markdown("---")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 📊 기본 정보 입력")
            
            solar_cap = st.number_input(
                "태양광 발전 용량 (kW)",
                min_value=10,
                max_value=2000,
                value=500,
                step=10,
                help="설치된 태양광 패널의 총 용량을 입력하세요"
            )
            
            daily_cons = st.number_input(
                "일일 전력 소비량 (kWh)",
                min_value=100,
                max_value=50000,
                value=2000,
                step=100,
                help="온실에서 하루 동안 소비하는 총 전력량을 입력하세요"
            )
            
            target_self = st.slider(
                "목표 자급률 (%)",
                min_value=40,
                max_value=80,
                value=70,
                step=5,
                help="달성하고자 하는 전력 자급률 목표를 설정하세요"
            ) / 100
            
            if st.button("🔍 최적 용량 계산", use_container_width=True):
                st.session_state['ess_design_done'] = True
                st.session_state['solar_cap'] = solar_cap
                st.session_state['daily_cons'] = daily_cons
                st.session_state['target_self'] = target_self
        
        with col2:
            st.markdown("#### 📈 설계 결과")
            
            if 'ess_design_done' in st.session_state and st.session_state['ess_design_done']:
                design_result = ess.design_ess_capacity(
                    solar_capacity_kw=st.session_state['solar_cap'],
                    daily_consumption_kwh=st.session_state['daily_cons'],
                    target_self_sufficiency=st.session_state['target_self']
                )
                
                st.metric(
                    "일일 태양광 발전량",
                    f"{design_result['daily_solar_generation_kwh']:.1f} kWh",
                    help="평균 일사시간 4.5시간 기준"
                )
                
                st.metric(
                    "권장 ESS 용량",
                    f"{design_result['recommended_capacity_kwh']:.1f} kWh",
                    delta="최적 용량"
                )
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric(
                        "최소 용량",
                        f"{design_result['min_capacity_kwh']:.1f} kWh"
                    )
                with col_b:
                    st.metric(
                        "최대 용량",
                        f"{design_result['max_capacity_kwh']:.1f} kWh"
                    )
                
                st.metric(
                    "실사용 가능 용량",
                    f"{design_result['usable_capacity_kwh']:.1f} kWh",
                    help="방전심도(DOD) 90% 적용"
                )
                
                st.markdown("---")
                
                # 용량 범위 시각화
                import plotly.graph_objects as go
                
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    name='용량 범위',
                    x=['최소', '권장', '최대'],
                    y=[
                        design_result['min_capacity_kwh'],
                        design_result['recommended_capacity_kwh'],
                        design_result['max_capacity_kwh']
                    ],
                    marker_color=['#FFC107', '#4CAF50', '#FF5722'],
                    text=[
                        f"{design_result['min_capacity_kwh']:.0f} kWh",
                        f"{design_result['recommended_capacity_kwh']:.0f} kWh",
                        f"{design_result['max_capacity_kwh']:.0f} kWh"
                    ],
                    textposition='auto'
                ))
                
                fig.update_layout(
                    title="ESS 용량 설계 범위",
                    xaxis_title="설계 기준",
                    yaxis_title="용량 (kWh)",
                    height=350,
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown(f"""
                <div class='success-box'>
                <h4>✅ 설계 권장사항</h4>
                귀 온실의 태양광 발전 용량 {st.session_state['solar_cap']}kW와 일일 소비량 {st.session_state['daily_cons']}kWh를 
                고려할 때, 목표 자급률 {st.session_state['target_self']*100:.0f}%를 달성하기 위해서는 
                약 {design_result['recommended_capacity_kwh']:.0f}kWh 용량의 ESS 설치를 권장합니다. 
                이는 일일 태양광 발전량의 약 {design_result['recommended_capacity_kwh']/design_result['daily_solar_generation_kwh']*100:.0f}%에 
                해당하는 용량으로, 낮 시간 잉여 전력을 효과적으로 저장하여 야간에 활용할 수 있습니다.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("왼쪽에서 정보를 입력하고 '최적 용량 계산' 버튼을 클릭하세요")
        
        st.markdown("---")
        
        # 설계 가이드라인
        st.markdown("#### 📚 ESS 용량 설계 가이드라인")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **태양광 발전량 기준 설계**  
            ESS 용량은 일반적으로 태양광 일일 발전량의 60~80% 수준으로 설계합니다. 이는 낮 시간 동안 
            발생하는 잉여 전력을 대부분 저장할 수 있는 용량이며, 계절별 발전량 변동을 고려한 최적 수준입니다. 
            예를 들어 500kW 태양광이 일일 평균 2,250kWh를 생산한다면 ESS 용량은 1,350~1,800kWh가 적절합니다.
            """)
        
        with col2:
            st.markdown("""
            **야간 소비량 기준 설계**  
            스마트팜에서 난방과 조명 등 주요 전력 소비는 야간에 집중됩니다. ESS 용량을 야간 소비량의 
            50~70% 수준으로 설계하면 야간 전력 대부분을 자가 전력으로 충당할 수 있습니다. 야간 소비가 
            일일 전체 소비의 60%인 경우, ESS는 전체 소비량의 약 35~42% 수준이 됩니다.
            """)
        
        with col3:
            st.markdown("""
            **투자 효율 고려**  
            ESS 용량이 클수록 자급률은 높아지지만 투자비 대비 효율은 감소합니다. 일반적으로 자급률 
            70~75% 수준에서 투자 효율이 최적화되며, 이 이상으로 용량을 늘려도 자급률은 소폭 증가하는 
            반면 투자비는 비례적으로 증가합니다. 따라서 경제성과 자급률의 균형점을 찾는 것이 중요합니다.
            """)
    
    # ==================== 섹션 2: 일일 운영 시뮬레이션 ====================
    elif ess_section == "일일 운영 시뮬레이션":
        st.markdown("### 📅 일일 ESS 충방전 운영 시뮬레이션")
        
        st.markdown("""
        ESS는 24시간 동안 태양광 발전량과 전력 소비량에 따라 자동으로 충전과 방전을 반복합니다. 
        낮 시간에 태양광 발전이 소비를 초과하면 잉여 전력을 ESS에 저장하고, 야간에 태양광 발전이 
        없을 때는 저장된 전력을 방전하여 사용합니다. 또한 심야 시간대에는 저렴한 계통 전력으로 
        ESS를 충전하여 피크 시간대 전력요금을 절감할 수 있습니다.
        """)
        
        st.markdown("---")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 📊 시뮬레이션 설정")
            
            ess_cap_sim = st.number_input(
                "ESS 용량 (kWh)",
                min_value=100,
                max_value=2000,
                value=500,
                step=50
            )
            
            season_sim = st.selectbox(
                "계절 선택",
                ["겨울 (Winter)", "여름 (Summer)", "봄/가을 (Spring/Fall)"],
                help="계절에 따라 태양광 발전과 소비 패턴이 달라집니다"
            )
            
            battery_type_sim = st.selectbox(
                "배터리 종류",
                ["리튬이온 (Lithium-ion)", "LFP (리튬인산철)"]
            )
            
            if st.button("▶️ 시뮬레이션 실행", use_container_width=True):
                st.session_state['ess_sim_done'] = True
                st.session_state['ess_cap_sim'] = ess_cap_sim
                st.session_state['season_sim'] = season_sim.split()[0].lower()
                st.session_state['battery_type_sim'] = 'lithium_ion' if 'Lithium' in battery_type_sim else 'lfp'
        
        with col2:
            st.markdown("#### 📈 운영 결과")
            
            if 'ess_sim_done' in st.session_state and st.session_state['ess_sim_done']:
                # 프로파일 생성
                solar_profile, consumption_profile = ess.generate_hourly_profiles(
                    season=st.session_state['season_sim']
                )
                
                # 운영 시뮬레이션
                operation_result = ess.calculate_daily_operation(
                    ess_capacity_kwh=st.session_state['ess_cap_sim'],
                    solar_generation_profile=solar_profile,
                    consumption_profile=consumption_profile,
                    battery_type=st.session_state['battery_type_sim']
                )
                
                st.metric(
                    "일일 충전량",
                    f"{operation_result['total_charge_kwh']:.1f} kWh"
                )
                
                st.metric(
                    "일일 방전량",
                    f"{operation_result['total_discharge_kwh']:.1f} kWh"
                )
                
                st.metric(
                    "계통 구매량",
                    f"{operation_result['total_grid_purchase_kwh']:.1f} kWh"
                )
                
                st.metric(
                    "전력 자급률",
                    f"{operation_result['self_sufficiency_rate']:.1f} %",
                    delta=f"{operation_result['self_sufficiency_rate'] - 35:.1f}%p 향상"
                )
                
        if 'ess_sim_done' in st.session_state and st.session_state['ess_sim_done']:
            st.markdown("---")
            
            st.markdown("#### 📊 24시간 운영 프로파일")
            
            # 시간별 충방전 및 SOC 차트
            import plotly.graph_objects as go
            from plotly.subplots import make_subplots
            
            hours = np.arange(24)
            
            # 두 개의 서브플롯 생성
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=("발전/소비/충방전 프로파일", "배터리 충전율 (SOC)"),
                vertical_spacing=0.12,
                row_heights=[0.6, 0.4]
            )
            
            # 첫 번째 서브플롯: 발전/소비/충방전
            fig.add_trace(
                go.Scatter(
                    x=hours,
                    y=solar_profile,
                    name='태양광 발전',
                    line=dict(color='#FFC107', width=3),
                    fill='tozeroy'
                ),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=hours,
                    y=consumption_profile,
                    name='전력 소비',
                    line=dict(color='#F44336', width=3)
                ),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Bar(
                    x=hours,
                    y=operation_result['hourly_charge'],
                    name='ESS 충전',
                    marker_color='#4CAF50',
                    opacity=0.7
                ),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Bar(
                    x=hours,
                    y=-operation_result['hourly_discharge'],
                    name='ESS 방전',
                    marker_color='#2196F3',
                    opacity=0.7
                ),
                row=1, col=1
            )
            
            # 두 번째 서브플롯: SOC
            fig.add_trace(
                go.Scatter(
                    x=hours,
                    y=operation_result['hourly_soc'] * 100,
                    name='충전율 (SOC)',
                    line=dict(color='#9C27B0', width=4),
                    fill='tozeroy',
                    fillcolor='rgba(156, 39, 176, 0.2)'
                ),
                row=2, col=1
            )
            
            # 레이아웃 업데이트
            fig.update_xaxes(title_text="시간 (Hour)", row=1, col=1)
            fig.update_xaxes(title_text="시간 (Hour)", row=2, col=1)
            fig.update_yaxes(title_text="전력 (kWh)", row=1, col=1)
            fig.update_yaxes(title_text="충전율 (%)", row=2, col=1, range=[0, 100])
            
            fig.update_layout(
                height=700,
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            # 운영 분석
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class='info-box'>
                <h4>🔄 충방전 패턴 분석</h4>
                차트에서 확인할 수 있듯이 ESS는 주간 시간대(09~17시)에 태양광 잉여전력을 충전하고, 
                야간 시간대(18~23시, 00~08시)에 저장된 전력을 방전하여 사용합니다. 녹색 막대는 충전량을, 
                파란색 막대는 방전량을 나타내며, 보라색 영역 그래프는 배터리의 실시간 충전율을 보여줍니다. 
                배터리는 안전을 위해 최소 20% 이상의 충전율을 유지하도록 운영됩니다.
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class='success-box'>
                <h4>✅ 자급률 향상 효과</h4>
                ESS 적용으로 전력 자급률이 기존 35%에서 {operation_result['self_sufficiency_rate']:.1f}%로 
                {operation_result['self_sufficiency_rate'] - 35:.1f}%p 향상되었습니다. 일일 {operation_result['total_charge_kwh']:.1f}kWh를 
                충전하여 {operation_result['total_discharge_kwh']:.1f}kWh를 방전함으로써, 계통에서 구매해야 하는 
                전력량을 {operation_result['total_grid_purchase_kwh']:.1f}kWh로 크게 줄일 수 있었습니다.
                </div>
                """, unsafe_allow_html=True)
    
    # ==================== 섹션 3: 탄소저감 효과 ====================
    elif ess_section == "탄소저감 효과 분석":
        st.markdown("### 🌍 ESS 탄소저감 효과 분석")
        
        st.markdown("""
        ESS는 태양광 발전의 활용률을 높여 화석연료 기반 계통 전력 사용을 줄임으로써 탄소배출을 저감합니다. 
        태양광 발전이 있더라도 ESS가 없으면 즉시 소비할 수 없는 잉여전력은 계통으로 역송되거나 버려지게 됩니다. 
        ESS를 통해 이 잉여전력을 저장했다가 야간에 사용하면 야간 계통 전력 구매를 줄여 탄소배출을 크게 감소시킬 수 있습니다.
        """)
        
        st.markdown("---")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 📊 분석 조건 입력")
            
            ess_cap_carbon = st.number_input(
                "ESS 용량 (kWh)",
                min_value=100,
                max_value=2000,
                value=500,
                step=50,
                key="carbon_ess_cap"
            )
            
            annual_solar = st.number_input(
                "연간 태양광 발전량 (kWh)",
                min_value=10000,
                max_value=5000000,
                value=600000,
                step=10000,
                key="carbon_solar"
            )
            
            annual_consumption_carbon = st.number_input(
                "연간 전력 소비량 (kWh)",
                min_value=10000,
                max_value=10000000,
                value=730000,
                step=10000,
                key="carbon_consumption"
            )
            
            battery_type_carbon = st.selectbox(
                "배터리 종류",
                ["리튬이온 (Lithium-ion)", "LFP (리튬인산철)"],
                key="carbon_battery"
            )
            
            if st.button("🌿 탄소저감 분석", use_container_width=True):
                st.session_state['carbon_analysis_done'] = True
                st.session_state['ess_cap_carbon'] = ess_cap_carbon
                st.session_state['annual_solar'] = annual_solar
                st.session_state['annual_consumption_carbon'] = annual_consumption_carbon
                st.session_state['battery_type_carbon'] = 'lithium_ion' if 'Lithium' in battery_type_carbon else 'lfp'
        
        with col2:
            st.markdown("#### 📈 탄소저감 결과")
            
            if 'carbon_analysis_done' in st.session_state and st.session_state['carbon_analysis_done']:
                carbon_result = ess.calculate_carbon_reduction(
                    ess_capacity_kwh=st.session_state['ess_cap_carbon'],
                    annual_solar_generation_kwh=st.session_state['annual_solar'],
                    annual_consumption_kwh=st.session_state['annual_consumption_carbon'],
                    battery_type=st.session_state['battery_type_carbon']
                )
                
                st.metric(
                    "ESS 없을 때 탄소배출",
                    f"{carbon_result['baseline_carbon_kg']:,.0f} kg CO₂/년"
                )
                
                st.metric(
                    "ESS 있을 때 탄소배출",
                    f"{carbon_result['enhanced_carbon_kg']:,.0f} kg CO₂/년",
                    delta=f"-{carbon_result['carbon_reduction_kg']:,.0f} kg"
                )
                
                st.metric(
                    "탄소저감률",
                    f"{carbon_result['reduction_rate_percent']:.1f} %",
                    delta="개선"
                )
                
                st.metric(
                    "자가소비 증가량",
                    f"{carbon_result['self_consumption_increase_kwh']:,.0f} kWh/년"
                )
        
        if 'carbon_analysis_done' in st.session_state and st.session_state['carbon_analysis_done']:
            st.markdown("---")
            
            # 탄소배출 비교 차트
            import plotly.graph_objects as go
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=['ESS 없음', 'ESS 있음'],
                y=[carbon_result['baseline_carbon_kg'], carbon_result['enhanced_carbon_kg']],
                marker_color=['#F44336', '#4CAF50'],
                text=[
                    f"{carbon_result['baseline_carbon_kg']:,.0f} kg",
                    f"{carbon_result['enhanced_carbon_kg']:,.0f} kg"
                ],
                textposition='auto'
            ))
            
            # 저감량 화살표 추가
            fig.add_annotation(
                x=0.5, y=carbon_result['baseline_carbon_kg'] * 0.5,
                text=f"저감량<br>{carbon_result['carbon_reduction_kg']:,.0f} kg<br>({carbon_result['reduction_rate_percent']:.1f}%)",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="#2196F3",
                ax=0,
                ay=-80,
                font=dict(size=14, color="#2196F3")
            )
            
            fig.update_layout(
                title="연간 탄소배출량 비교",
                xaxis_title="시나리오",
                yaxis_title="탄소배출량 (kg CO₂)",
                height=450,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # 자가소비 증가 파이 차트
                labels = ['기존 자가소비', 'ESS 추가 자가소비', '계통 구매']
                values = [
                    carbon_result['baseline_self_consumption_kwh'],
                    carbon_result['self_consumption_increase_kwh'],
                    st.session_state['annual_consumption_carbon'] - carbon_result['enhanced_self_consumption_kwh']
                ]
                
                fig2 = go.Figure(data=[go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.4,
                    marker_colors=['#4CAF50', '#8BC34A', '#FF5722']
                )])
                
                fig2.update_layout(
                    title="전력 공급원 구성",
                    height=350
                )
                
                st.plotly_chart(fig2, use_container_width=True)
            
            with col2:
                st.markdown(f"""
                <div class='success-box' style='margin-top: 40px;'>
                <h4>✅ 환경 기여도</h4>
                ESS {st.session_state['ess_cap_carbon']}kWh 설치로 연간 {carbon_result['carbon_reduction_kg']:,.0f}kg의 
                CO₂ 배출을 저감할 수 있습니다. 이는 {carbon_result['reduction_rate_percent']:.1f}%의 탄소저감률로, 
                약 {carbon_result['carbon_reduction_kg']/6.3:.0f}그루의 소나무가 1년간 흡수하는 CO₂량과 같습니다. 
                (소나무 1그루당 연간 약 6.3kg CO₂ 흡수)
                </div>
                
                <div class='info-box' style='margin-top: 20px;'>
                <h4>📊 ESS 손실 고려</h4>
                ESS 충방전 과정에서 {carbon_result['ess_loss_kwh']:,.0f}kWh의 손실이 발생하지만, 
                이를 고려하더라도 순 자가소비 증가량은 {carbon_result['self_consumption_increase_kwh']:,.0f}kWh로 
                매우 높은 수준입니다. 배터리 효율이 높을수록 손실은 줄어듭니다.
                </div>
                """, unsafe_allow_html=True)
    
    # ==================== 섹션 4: 투자 경제성 분석 ====================
    elif ess_section == "투자 경제성 분석":
        st.markdown("### 💰 ESS 투자 경제성 분석")
        
        st.markdown("""
        ESS 투자는 초기 비용이 크지만 전력요금 절감과 정부 보조금을 고려하면 경제성이 충분합니다. 
        특히 한국전력의 시간대별 요금제를 활용하면 피크와 심야 시간대의 요금 차이만큼 추가 절감이 가능하며, 
        용량이 1MW 이상인 경우 주파수조정(FR) 서비스에 참여하여 별도 수익을 창출할 수도 있습니다. 
        정부는 신재생에너지 보급사업을 통해 초기 투자비의 30~50%를 보조금으로 지원하고 있습니다.
        """)
        
        st.markdown("---")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### 📊 경제성 분석 조건")
            
            ess_cap_econ = st.number_input(
                "ESS 용량 (kWh)",
                min_value=100,
                max_value=2000,
                value=500,
                step=50,
                key="econ_ess_cap"
            )
            
            grid_reduction = st.number_input(
                "연간 계통전력 절감량 (kWh)",
                min_value=10000,
                max_value=1000000,
                value=200000,
                step=10000,
                help="ESS를 통해 절감되는 연간 계통 전력 구매량"
            )
            
            battery_type_econ = st.selectbox(
                "배터리 종류",
                ["리튬이온 (Lithium-ion)", "LFP (리튬인산철)"],
                key="econ_battery"
            )
            
            subsidy_rate = st.slider(
                "정부 보조금 비율 (%)",
                min_value=0,
                max_value=50,
                value=30,
                step=5,
                help="신재생에너지 보급사업 보조금 (일반적으로 30~50%)"
            ) / 100
            
            price_escalation = st.slider(
                "전기요금 연간 상승률 (%)",
                min_value=0.0,
                max_value=5.0,
                value=3.0,
                step=0.5
            ) / 100
            
            if st.button("💵 경제성 계산", use_container_width=True):
                st.session_state['econ_analysis_done'] = True
                st.session_state['ess_cap_econ'] = ess_cap_econ
                st.session_state['grid_reduction'] = grid_reduction
                st.session_state['battery_type_econ'] = 'lithium_ion' if 'Lithium' in battery_type_econ else 'lfp'
                st.session_state['subsidy_rate'] = subsidy_rate
                st.session_state['price_escalation'] = price_escalation
        
        with col2:
            st.markdown("#### 📈 경제성 분석 결과")
            
            if 'econ_analysis_done' in st.session_state and st.session_state['econ_analysis_done']:
                econ_result = ess.calculate_economic_analysis(
                    ess_capacity_kwh=st.session_state['ess_cap_econ'],
                    annual_grid_reduction_kwh=st.session_state['grid_reduction'],
                    battery_type=st.session_state['battery_type_econ'],
                    government_subsidy_rate=st.session_state['subsidy_rate'],
                    electricity_price_escalation=st.session_state['price_escalation']
                )
                
                st.metric(
                    "총 초기 투자비",
                    f"{econ_result['total_initial_cost']/100000000:.2f} 억원",
                    help="배터리, BMS, PCS, 설치비 포함"
                )
                
                st.metric(
                    "정부 보조금",
                    f"{econ_result['government_subsidy']/100000000:.2f} 억원",
                    delta=f"-{st.session_state['subsidy_rate']*100:.0f}%"
                )
                
                st.metric(
                    "실 투자비",
                    f"{econ_result['net_initial_cost']/100000000:.2f} 억원"
                )
                
                st.metric(
                    "연간 순이익",
                    f"{econ_result['annual_net_profit']/10000:.0f} 만원/년"
                )
                
                st.metric(
                    "투자회수기간",
                    f"{econ_result['payback_years']:.1f} 년",
                    delta="양호" if econ_result['payback_years'] < 10 else "검토 필요"
                )
                
                st.metric(
                    "15년 NPV",
                    f"{econ_result['npv_15years']/100000000:.2f} 억원",
                    delta="수익성 양호" if econ_result['npv_15years'] > 0 else "수익성 부족"
                )
        
        if 'econ_analysis_done' in st.session_state and st.session_state['econ_analysis_done']:
            st.markdown("---")
            
            # 비용 구성 차트
            import plotly.graph_objects as go
            
            col1, col2 = st.columns(2)
            
            with col1:
                # 초기 투자비 구성
                labels = ['배터리', 'BMS', 'PCS', '설치비']
                values = [
                    econ_result['battery_cost'],
                    econ_result['bms_cost'],
                    econ_result['pcs_cost'],
                    econ_result['installation_cost']
                ]
                
                fig1 = go.Figure(data=[go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.4,
                    marker_colors=['#2196F3', '#4CAF50', '#FF9800', '#9C27B0']
                )])
                
                fig1.update_layout(
                    title="초기 투자비 구성",
                    height=350
                )
                
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # 연간 수익 구성
                labels_revenue = ['전력요금 절감', 'FR 서비스', '유지보수비']
                values_revenue = [
                    econ_result['annual_energy_savings'],
                    econ_result['annual_fr_revenue'],
                    -econ_result['annual_maintenance']
                ]
                
                fig2 = go.Figure(data=[go.Bar(
                    x=labels_revenue,
                    y=values_revenue,
                    marker_color=['#4CAF50', '#2196F3', '#F44336'],
                    text=[f"{v/10000:.0f}만원" for v in values_revenue],
                    textposition='auto'
                )])
                
                fig2.update_layout(
                    title="연간 수익 구성",
                    yaxis_title="금액 (원)",
                    height=350,
                    showlegend=False
                )
                
                st.plotly_chart(fig2, use_container_width=True)
            
            st.markdown("---")
            
            # 누적 현금흐름 차트
            years = np.arange(0, econ_result['project_lifetime_years'] + 1)
            cumulative_cashflow = np.zeros(len(years))
            cumulative_cashflow[0] = -econ_result['net_initial_cost']
            
            for i in range(1, len(years)):
                annual_revenue = econ_result['annual_energy_savings'] * ((1 + st.session_state['price_escalation']) ** i)
                annual_revenue += econ_result['annual_fr_revenue']
                yearly_profit = annual_revenue - econ_result['annual_maintenance']
                cumulative_cashflow[i] = cumulative_cashflow[i-1] + yearly_profit
            
            fig3 = go.Figure()
            
            fig3.add_trace(go.Scatter(
                x=years,
                y=cumulative_cashflow / 100000000,
                mode='lines+markers',
                name='누적 현금흐름',
                line=dict(color='#2196F3', width=3),
                fill='tozeroy',
                fillcolor='rgba(33, 150, 243, 0.2)'
            ))
            
            # 손익분기점 표시
            break_even_idx = np.where(cumulative_cashflow >= 0)[0]
            if len(break_even_idx) > 0:
                break_even_year = years[break_even_idx[0]]
                fig3.add_vline(
                    x=break_even_year,
                    line_dash="dash",
                    line_color="green",
                    annotation_text=f"손익분기점: {break_even_year}년차"
                )
            
            fig3.add_hline(y=0, line_dash="dash", line_color="gray")
            
            fig3.update_layout(
                title="누적 현금흐름 분석 (15년)",
                xaxis_title="년차",
                yaxis_title="누적 현금흐름 (억원)",
                height=400
            )
            
            st.plotly_chart(fig3, use_container_width=True)
            
            st.markdown(f"""
            <div class='{"success-box" if econ_result["npv_15years"] > 0 else "warning-box"}'>
            <h4>{"✅ 투자 권장" if econ_result["npv_15years"] > 0 else "⚠️ 투자 검토 필요"}</h4>
            ESS {st.session_state['ess_cap_econ']}kWh 투자 시 실 투자비는 {econ_result['net_initial_cost']/100000000:.2f}억원이며, 
            투자회수기간은 약 {econ_result['payback_years']:.1f}년입니다. 15년 운영 기준 순현재가치(NPV)는 
            {econ_result['npv_15years']/100000000:.2f}억원으로 {"경제성이 충분합니다" if econ_result["npv_15years"] > 0 else "추가 검토가 필요합니다"}.
            연간 {econ_result['annual_net_profit']/10000:.0f}만원의 순이익이 발생하며, 전기요금 상승률을 
            {st.session_state['price_escalation']*100:.1f}%로 가정할 때 장기적으로 수익성이 더욱 개선될 것으로 예상됩니다.
            </div>
            """, unsafe_allow_html=True)
    
    # ==================== 섹션 5: 용량별 시나리오 비교 ====================
    elif ess_section == "용량별 시나리오 비교":
        st.markdown("### 📊 ESS 용량별 시나리오 비교")
        
        st.markdown("""
        ESS 용량이 클수록 자급률과 탄소저감 효과는 증가하지만 투자비도 비례적으로 늘어납니다. 
        최적 용량은 자급률 목표, 투자 가능 예산, 투자회수기간 목표를 종합적으로 고려하여 결정해야 합니다. 
        일반적으로 투자회수기간이 5~8년 수준인 용량이 경제성과 환경성의 균형점으로 평가됩니다.
        """)
        
        st.markdown("---")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### 📊 비교 조건")
            
            solar_cap_compare = st.number_input(
                "태양광 용량 (kW)",
                min_value=100,
                max_value=2000,
                value=500,
                step=50,
                key="compare_solar"
            )
            
            annual_cons_compare = st.number_input(
                "연간 소비량 (kWh)",
                min_value=100000,
                max_value=10000000,
                value=730000,
                step=10000,
                key="compare_consumption"
            )
            
            if st.button("⚖️ 시나리오 비교", use_container_width=True):
                st.session_state['compare_done'] = True
                st.session_state['solar_cap_compare'] = solar_cap_compare
                st.session_state['annual_cons_compare'] = annual_cons_compare
        
        with col2:
            if 'compare_done' in st.session_state and st.session_state['compare_done']:
                st.markdown("#### 📈 비교 결과 테이블")
                
                comparison_df = ess.compare_scenarios(
                    solar_capacity_kw=st.session_state['solar_cap_compare'],
                    annual_consumption_kwh=st.session_state['annual_cons_compare'],
                    ess_capacities=[0, 300, 500, 700, 900]
                )
                
                # 스타일링된 데이터프레임 표시
                st.dataframe(
                    comparison_df.style.format({
                        'ESS 용량 (kWh)': '{:.0f}',
                        '자급률 (%)': '{:.1f}',
                        '연간 탄소저감 (kg)': '{:,.0f}',
                        '초기 투자비 (만원)': '{:,.0f}',
                        '투자회수기간 (년)': '{:.1f}',
                        'NPV (만원)': '{:,.0f}'
                    }).background_gradient(subset=['NPV (만원)'], cmap='RdYlGn'),
                    use_container_width=True,
                    hide_index=True,
                    height=250
                )
        
        if 'compare_done' in st.session_state and st.session_state['compare_done']:
            st.markdown("---")
            
            # 시나리오 비교 차트
            import plotly.graph_objects as go
            from plotly.subplots import make_subplots
            
            comparison_df = ess.compare_scenarios(
                solar_capacity_kw=st.session_state['solar_cap_compare'],
                annual_consumption_kwh=st.session_state['annual_cons_compare'],
                ess_capacities=[0, 300, 500, 700, 900]
            )
            
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=("자급률", "탄소저감량", "투자회수기간", "NPV"),
                vertical_spacing=0.15,
                horizontal_spacing=0.12
            )
            
            # 자급률
            fig.add_trace(
                go.Bar(
                    x=comparison_df['ESS 용량 (kWh)'],
                    y=comparison_df['자급률 (%)'],
                    marker_color='#4CAF50',
                    text=comparison_df['자급률 (%)'].apply(lambda x: f'{x:.1f}%'),
                    textposition='auto',
                    name='자급률'
                ),
                row=1, col=1
            )
            
            # 탄소저감량
            fig.add_trace(
                go.Bar(
                    x=comparison_df['ESS 용량 (kWh)'],
                    y=comparison_df['연간 탄소저감 (kg)'],
                    marker_color='#2196F3',
                    text=comparison_df['연간 탄소저감 (kg)'].apply(lambda x: f'{x:,.0f}'),
                    textposition='auto',
                    name='탄소저감'
                ),
                row=1, col=2
            )
            
            # 투자회수기간
            fig.add_trace(
                go.Scatter(
                    x=comparison_df['ESS 용량 (kWh)'][1:],
                    y=comparison_df['투자회수기간 (년)'][1:],
                    mode='lines+markers',
                    marker=dict(size=10, color='#FF9800'),
                    line=dict(width=3, color='#FF9800'),
                    name='회수기간'
                ),
                row=2, col=1
            )
            
            # NPV
            fig.add_trace(
                go.Bar(
                    x=comparison_df['ESS 용량 (kWh)'],
                    y=comparison_df['NPV (만원)'],
                    marker_color=comparison_df['NPV (만원)'].apply(
                        lambda x: '#4CAF50' if x > 0 else '#F44336'
                    ),
                    text=comparison_df['NPV (만원)'].apply(lambda x: f'{x:,.0f}'),
                    textposition='auto',
                    name='NPV'
                ),
                row=2, col=2
            )
            
            fig.update_xaxes(title_text="ESS 용량 (kWh)", row=1, col=1)
            fig.update_xaxes(title_text="ESS 용량 (kWh)", row=1, col=2)
            fig.update_xaxes(title_text="ESS 용량 (kWh)", row=2, col=1)
            fig.update_xaxes(title_text="ESS 용량 (kWh)", row=2, col=2)
            
            fig.update_yaxes(title_text="자급률 (%)", row=1, col=1)
            fig.update_yaxes(title_text="탄소저감 (kg)", row=1, col=2)
            fig.update_yaxes(title_text="회수기간 (년)", row=2, col=1)
            fig.update_yaxes(title_text="NPV (만원)", row=2, col=2)
            
            fig.update_layout(
                height=700,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            # 권장 용량 제시
            recommended_row = comparison_df[comparison_df['추천'] != '']
            if not recommended_row.empty:
                rec_capacity = recommended_row.iloc[0]['ESS 용량 (kWh)']
                rec_self_suff = recommended_row.iloc[0]['자급률 (%)']
                rec_payback = recommended_row.iloc[0]['투자회수기간 (년)']
                rec_npv = recommended_row.iloc[0]['NPV (만원)']
                
                st.markdown(f"""
                <div class='success-box'>
                <h4>✅ 권장 용량: {rec_capacity:.0f} kWh</h4>
                비교 분석 결과 {rec_capacity:.0f}kWh 용량이 경제성과 환경성의 최적 균형점으로 평가됩니다. 
                이 용량으로 자급률 {rec_self_suff:.1f}%를 달성할 수 있으며, 투자회수기간은 {rec_payback:.1f}년으로 
                적절한 수준입니다. 15년 운영 시 순현재가치는 {rec_npv:,.0f}만원으로 충분한 수익성이 예상됩니다.
                </div>
                """, unsafe_allow_html=True)
    
    # ==================== 섹션 6: 배터리 기술 비교 ====================
    else:  # "배터리 기술 비교"
        st.markdown("### 🔬 배터리 기술 비교")
        
        st.markdown("""
        ESS의 핵심은 배터리 기술입니다. 현재 주로 사용되는 배터리는 리튬이온과 LFP(리튬인산철) 두 종류이며, 
        각각 장단점이 있어 사용 목적과 환경에 따라 적절한 선택이 필요합니다. 리튬이온은 높은 에너지 밀도와 
        효율을 자랑하지만 가격이 비싸고, LFP는 상대적으로 저렴하고 안정성이 높지만 에너지 밀도가 낮습니다.
        """)
        
        st.markdown("---")
        
        # 배터리 기술 비교 테이블
        battery_comparison = pd.DataFrame({
            '항목': [
                '배터리 종류',
                '충방전 효율',
                '방전심도 (DOD)',
                '사이클 수명',
                '달력 수명',
                'kWh당 가격',
                '유지보수비율',
                '에너지 밀도',
                '안전성',
                '주요 특징'
            ],
            '리튬이온 (Li-ion)': [
                '리튬이온',
                '95%',
                '90%',
                '6,000 사이클',
                '15년',
                '100만원',
                '2.0%',
                '높음',
                '중간',
                '높은 효율, 대중적 사용'
            ],
            'LFP (리튬인산철)': [
                'LFP',
                '93%',
                '95%',
                '8,000 사이클',
                '20년',
                '90만원',
                '1.5%',
                '중간',
                '높음',
                '장수명, 높은 안전성'
            ]
        })
        
        st.dataframe(battery_comparison, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class='info-box'>
            <h4>⚡ 리튬이온 배터리</h4>
            리튬이온 배터리는 가장 널리 사용되는 ESS 배터리로 높은 에너지 밀도와 95%의 우수한 충방전 효율을 
            제공합니다. 테슬라, LG에너지솔루션 등 주요 제조사들이 대량 생산하고 있어 기술 성숙도가 높고 
            A/S 네트워크가 잘 구축되어 있습니다. 사이클 수명은 6,000회로 일일 1회 충방전 시 약 16년간 사용 가능하며, 
            달력 수명은 15년입니다. kWh당 가격은 약 100만원 수준이며 정부 보조금 적용 시 실 부담은 더 줄어듭니다.
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class='success-box'>
            <h4>✅ 적합한 사용처</h4>
            공간이 제한적이거나 높은 에너지 밀도가 필요한 경우에 적합합니다. 도심 인근 온실처럼 설치 공간이 
            협소한 환경에서 많은 용량을 확보해야 할 때 유리합니다. 또한 초기 투자비보다 운영 효율을 우선시하는 
            경우에도 리튬이온이 적합하며, 고효율로 인해 충방전 손실이 적어 장기적으로 경제성이 좋습니다.
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='info-box'>
            <h4>🛡️ LFP 배터리</h4>
            LFP(리튬인산철) 배터리는 안전성과 장수명이 특징인 차세대 배터리입니다. 화재 위험이 매우 낮아 
            안전성이 중요한 농업 시설에 특히 적합하며, 사이클 수명이 8,000회로 리튬이온보다 33% 길고 달력 수명도 
            20년으로 더 깁니다. 95%의 높은 방전심도로 배터리 용량을 더 많이 활용할 수 있으며, kWh당 가격이 90만원으로 
            리튬이온보다 10% 저렴합니다. 유지보수비율도 1.5%로 낮아 장기 운영비가 절감됩니다.
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class='success-box'>
            <h4>✅ 적합한 사용처</h4>
            안전성이 최우선인 농업 시설이나 장기 운영을 계획하는 경우에 적합합니다. 가연성 물질이 많은 
            온실 환경에서는 화재 위험이 낮은 LFP가 더 안전하며, 15년 이상 장기 운영을 고려한다면 긴 수명이 
            경제성을 높여줍니다. 초기 투자비 절감이 중요한 경우에도 LFP가 유리하며, 충방전 효율이 다소 낮지만 
            가격과 수명을 고려하면 전체 비용 대비 성능이 우수합니다.
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 두 배터리의 15년 총 비용 비교
        st.markdown("#### 💰 15년 총 소유비용 비교 (500kWh 기준)")
        
        capacity = 500  # kWh
        years = 15
        
        # 리튬이온
        lithium_initial = capacity * 1000000 * 1.45  # 배터리 + BMS + PCS + 설치
        lithium_maintenance = lithium_initial * 0.02 * years
        lithium_replacement = 0  # 15년 이내 교체 불필요
        lithium_total = lithium_initial + lithium_maintenance
        
        # LFP
        lfp_initial = capacity * 900000 * 1.45
        lfp_maintenance = lfp_initial * 0.015 * years
        lfp_replacement = 0  # 20년 수명으로 교체 불필요
        lfp_total = lfp_initial + lfp_maintenance
        
        cost_comparison = pd.DataFrame({
            '항목': ['초기 투자비', '15년 유지보수비', '배터리 교체비', '총 비용'],
            '리튬이온': [
                f'{lithium_initial/100000000:.2f}억원',
                f'{lithium_maintenance/100000000:.2f}억원',
                f'{lithium_replacement/100000000:.2f}억원',
                f'{lithium_total/100000000:.2f}억원'
            ],
            'LFP': [
                f'{lfp_initial/100000000:.2f}억원',
                f'{lfp_maintenance/100000000:.2f}억원',
                f'{lfp_replacement/100000000:.2f}억원',
                f'{lfp_total/100000000:.2f}억원'
            ]
        })
        
        st.dataframe(cost_comparison, use_container_width=True, hide_index=True)
        
        st.markdown(f"""
        <div class='info-box'>
        <h4>📊 비용 분석 결과</h4>
        500kWh ESS를 15년간 운영할 경우 리튬이온은 총 {lithium_total/100000000:.2f}억원, 
        LFP는 {lfp_total/100000000:.2f}억원이 소요되어 LFP가 
        약 {(lithium_total - lfp_total)/100000000:.2f}억원({(lithium_total - lfp_total)/lithium_total*100:.1f}%) 저렴합니다. 
        초기 투자비와 유지보수비 모두 LFP가 낮으며, 두 배터리 모두 15년 이내에는 교체가 필요 없어 
        교체비용은 발생하지 않습니다. 다만 리튬이온은 높은 효율로 인해 전력 손실이 적어 장기적인 
        전력요금 절감 효과를 고려하면 실제 격차는 다소 줄어들 수 있습니다.
        </div>
        """, unsafe_allow_html=True)


# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><b>탄소제로 스마트팜 계산기</b> v1.3.0</p>
    <p>© 2026 CPRI NEW BUSINESS STRATEGY DEPARTMENT. All rights reserved.</p>

</div>
""", unsafe_allow_html=True)

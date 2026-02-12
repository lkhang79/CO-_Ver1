"""
탄소제로 스마트팜 계산 시스템 - 시각화
Carbon Zero Smart Farm Calculator - Visualization
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List
import config

class Visualizer:
    """데이터 시각화 클래스"""
    
    def __init__(self):
        self.color_theme = config.COLOR_THEME
        self.chart_colors = config.CHART_COLORS
        
    def create_energy_balance_chart(
        self,
        production: float,
        consumption: float,
        title: str = "에너지 생산 vs 소비"
    ) -> go.Figure:
        """
        에너지 균형 차트
        
        Args:
            production: 생산량 (kWh)
            consumption: 소비량 (kWh)
            title: 차트 제목
        
        Returns:
            Plotly Figure
        """
        net = production - consumption
        
        fig = go.Figure()
        
        # 생산
        fig.add_trace(go.Bar(
            name='생산',
            x=['에너지'],
            y=[production],
            marker_color=self.chart_colors['solar_production'],
            text=[f'{production:.1f} kWh'],
            textposition='inside',
            textfont=dict(size=14, color='white'),
            hovertemplate='생산: %{y:.2f} kWh<extra></extra>'
        ))
        
        # 소비
        fig.add_trace(go.Bar(
            name='소비',
            x=['에너지'],
            y=[consumption],
            marker_color=self.chart_colors['heat_pump_consumption'],
            text=[f'{consumption:.1f} kWh'],
            textposition='inside',
            textfont=dict(size=14, color='white'),
            hovertemplate='소비: %{y:.2f} kWh<extra></extra>'
        ))
        
        # 순 에너지
        net_color = self.color_theme['success'] if net >= 0 else self.color_theme['danger']
        fig.add_trace(go.Bar(
            name='순량',
            x=['에너지'],
            y=[net],
            marker_color=net_color,
            text=[f'{net:+.1f} kWh'],
            textposition='outside' if abs(net) > max(production, consumption) * 0.1 else 'inside',
            textfont=dict(size=14),
            hovertemplate='순량: %{y:+.2f} kWh<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=18, color=self.color_theme['text'])),
            barmode='group',
            height=400,
            showlegend=True,
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Arial, sans-serif'),
            hovermode='x unified'
        )
        
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(title='에너지 (kWh)', gridcolor='lightgray')
        
        return fig
    
    def create_carbon_balance_chart(
        self,
        reduction: float,
        emission: float,
        title: str = "탄소 감축 vs 배출"
    ) -> go.Figure:
        """
        탄소 균형 차트
        
        Args:
            reduction: 감축량 (kg CO2)
            emission: 배출량 (kg CO2)
            title: 차트 제목
        
        Returns:
            Plotly Figure
        """
        net = emission - reduction
        
        fig = go.Figure()
        
        # 감축
        fig.add_trace(go.Bar(
            name='감축',
            x=['탄소'],
            y=[-reduction],  # 음수로 표시
            marker_color=self.chart_colors['carbon_reduction'],
            text=[f'-{reduction:.1f} kg'],
            textposition='inside',
            textfont=dict(size=14, color='white'),
            hovertemplate='감축: %{y:.2f} kg CO2<extra></extra>'
        ))
        
        # 배출
        fig.add_trace(go.Bar(
            name='배출',
            x=['탄소'],
            y=[emission],
            marker_color=self.color_theme['danger'],
            text=[f'+{emission:.1f} kg'],
            textposition='inside',
            textfont=dict(size=14, color='white'),
            hovertemplate='배출: %{y:.2f} kg CO2<extra></extra>'
        ))
        
        # 순 배출
        net_color = self.color_theme['danger'] if net > 0 else self.color_theme['success']
        fig.add_trace(go.Scatter(
            name='순배출',
            x=['탄소'],
            y=[net],
            mode='markers+text',
            marker=dict(size=20, color=net_color, symbol='diamond'),
            text=[f'{net:+.1f} kg'],
            textposition='top center',
            textfont=dict(size=14, color=net_color),
            hovertemplate='순배출: %{y:+.2f} kg CO2<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=18, color=self.color_theme['text'])),
            height=400,
            showlegend=True,
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Arial, sans-serif'),
            hovermode='x unified'
        )
        
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(title='탄소 (kg CO2)', gridcolor='lightgray', zeroline=True, zerolinewidth=2, zerolinecolor='black')
        
        return fig
    
    def create_hourly_profile_chart(
        self,
        hourly_data: List[Dict],
        title: str = "24시간 에너지 프로파일"
    ) -> go.Figure:
        """
        시간별 프로파일 차트
        
        Args:
            hourly_data: 시간별 데이터 리스트
            title: 차트 제목
        
        Returns:
            Plotly Figure
        """
        hours = [d['hour'] for d in hourly_data]
        production = [d['solar']['total_production_kwh'] for d in hourly_data]
        heat_pump = [d['heat_pump']['electrical_consumption_kwh'] for d in hourly_data]
        other = [d['other']['total_consumption_kwh'] for d in hourly_data]
        
        fig = go.Figure()
        
        # 태양광 생산
        fig.add_trace(go.Scatter(
            name='태양광 생산',
            x=hours,
            y=production,
            mode='lines',
            line=dict(color=self.chart_colors['solar_production'], width=3),
            fill='tozeroy',
            fillcolor=f"rgba(255, 167, 38, 0.3)",
            hovertemplate='%{y:.2f} kWh<extra></extra>'
        ))
        
        # 히트펌프 소비
        fig.add_trace(go.Scatter(
            name='히트펌프',
            x=hours,
            y=heat_pump,
            mode='lines',
            line=dict(color=self.chart_colors['heat_pump_consumption'], width=2, dash='dot'),
            hovertemplate='%{y:.2f} kWh<extra></extra>'
        ))
        
        # 기타 소비
        fig.add_trace(go.Scatter(
            name='기타 설비',
            x=hours,
            y=other,
            mode='lines',
            line=dict(color=self.chart_colors['other_consumption'], width=2, dash='dash'),
            hovertemplate='%{y:.2f} kWh<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=18, color=self.color_theme['text'])),
            xaxis=dict(
                title='시간 (Hour)',
                tickmode='linear',
                tick0=0,
                dtick=2,
                gridcolor='lightgray'
            ),
            yaxis=dict(
                title='전력 (kWh)',
                gridcolor='lightgray'
            ),
            height=400,
            showlegend=True,
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Arial, sans-serif'),
            hovermode='x unified'
        )
        
        return fig
    
    def create_monthly_chart(
        self,
        monthly_data: List[Dict],
        metric: str = "net_carbon_kg",
        title: str = "월별 추이"
    ) -> go.Figure:
        """
        월별 추이 차트
        
        Args:
            monthly_data: 월별 데이터 리스트
            metric: 표시할 메트릭
            title: 차트 제목
        
        Returns:
            Plotly Figure
        """
        months = [d['month'] for d in monthly_data]
        month_names = ['1월', '2월', '3월', '4월', '5월', '6월', 
                      '7월', '8월', '9월', '10월', '11월', '12월']
        
        values = [d.get(metric, 0) for d in monthly_data]
        
        # 메트릭별 색상 및 레이블
        metric_config = {
            "net_carbon_kg": {
                "color": self.chart_colors['net_carbon'],
                "label": "순 탄소 배출량 (kg CO2)",
                "format": ".1f"
            },
            "total_production_kwh": {
                "color": self.chart_colors['solar_production'],
                "label": "태양광 발전량 (kWh)",
                "format": ".1f"
            },
            "total_consumption_kwh": {
                "color": self.chart_colors['heat_pump_consumption'],
                "label": "전력 소비량 (kWh)",
                "format": ".1f"
            }
        }
        
        config_item = metric_config.get(metric, metric_config["net_carbon_kg"])
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=month_names,
            y=values,
            marker_color=config_item['color'],
            text=[f"{v:{config_item['format']}}" for v in values],
            textposition='outside',
            hovertemplate='%{x}: %{y:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=18, color=self.color_theme['text'])),
            xaxis=dict(title='월', gridcolor='lightgray'),
            yaxis=dict(title=config_item['label'], gridcolor='lightgray'),
            height=400,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Arial, sans-serif'),
            hovermode='x unified'
        )
        
        return fig
    
    def create_efficiency_gauge(
        self,
        value: float,
        title: str = "효율",
        max_value: float = 100,
        unit: str = "%"
    ) -> go.Figure:
        """
        효율 게이지 차트
        
        Args:
            value: 현재 값
            title: 제목
            max_value: 최대값
            unit: 단위
        
        Returns:
            Plotly Figure
        """
        # 색상 결정
        if value >= 80:
            color = self.color_theme['success']
        elif value >= 50:
            color = self.color_theme['warning']
        else:
            color = self.color_theme['danger']
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': title, 'font': {'size': 18}},
            delta={'reference': max_value * 0.7, 'increasing': {'color': self.color_theme['success']}},
            number={'suffix': unit, 'font': {'size': 40}},
            gauge={
                'axis': {'range': [None, max_value], 'tickwidth': 1, 'tickcolor': "darkgray"},
                'bar': {'color': color},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, max_value * 0.5], 'color': 'rgba(211, 47, 47, 0.2)'},
                    {'range': [max_value * 0.5, max_value * 0.8], 'color': 'rgba(245, 124, 0, 0.2)'},
                    {'range': [max_value * 0.8, max_value], 'color': 'rgba(46, 125, 50, 0.2)'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': max_value * 0.9
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            paper_bgcolor='white',
            font={'family': 'Arial, sans-serif'}
        )
        
        return fig
    
    def create_consumption_breakdown_pie(
        self,
        breakdown: Dict[str, float],
        title: str = "소비 구성"
    ) -> go.Figure:
        """
        소비 구성 파이 차트
        
        Args:
            breakdown: 구성 항목별 값
            title: 제목
        
        Returns:
            Plotly Figure
        """
        labels = list(breakdown.keys())
        values = list(breakdown.values())
        
        # 0이 아닌 값만 표시
        non_zero = [(l, v) for l, v in zip(labels, values) if v > 0]
        if not non_zero:
            # 데이터가 없는 경우
            labels = ['데이터 없음']
            values = [1]
        else:
            labels = [item[0] for item in non_zero]
            values = [item[1] for item in non_zero]
        
        colors = [
            self.chart_colors['solar_production'],
            self.chart_colors['heat_pump_consumption'],
            self.chart_colors['other_consumption'],
            self.chart_colors['net_carbon'],
            self.chart_colors['carbon_reduction']
        ]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker=dict(colors=colors[:len(labels)]),
            textinfo='label+percent',
            textfont=dict(size=12),
            hovertemplate='%{label}: %{value:.2f} kWh (%{percent})<extra></extra>'
        )])
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=18, color=self.color_theme['text'])),
            height=400,
            showlegend=True,
            legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5),
            paper_bgcolor='white',
            font=dict(family='Arial, sans-serif')
        )
        
        return fig
    
    def create_comparison_chart(
        self,
        current: Dict[str, float],
        benchmark: Dict[str, float],
        title: str = "벤치마크 비교"
    ) -> go.Figure:
        """
        벤치마크 비교 차트
        
        Args:
            current: 현재 값
            benchmark: 벤치마크 값
            title: 제목
        
        Returns:
            Plotly Figure
        """
        categories = list(current.keys())
        current_values = list(current.values())
        benchmark_values = [benchmark.get(k, 0) for k in categories]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='현재',
            x=categories,
            y=current_values,
            marker_color=self.color_theme['primary'],
            text=[f'{v:.1f}' for v in current_values],
            textposition='outside',
            hovertemplate='%{x}: %{y:.2f}<extra></extra>'
        ))
        
        fig.add_trace(go.Bar(
            name='벤치마크',
            x=categories,
            y=benchmark_values,
            marker_color=self.color_theme['secondary'],
            text=[f'{v:.1f}' for v in benchmark_values],
            textposition='outside',
            hovertemplate='%{x}: %{y:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(text=title, font=dict(size=18, color=self.color_theme['text'])),
            barmode='group',
            height=400,
            showlegend=True,
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Arial, sans-serif'),
            hovermode='x unified'
        )
        
        fig.update_xaxes(tickangle=-45, gridcolor='lightgray')
        fig.update_yaxes(gridcolor='lightgray')
        
        return fig
    
    def create_kpi_cards_html(
        self,
        kpis: List[Dict]
    ) -> str:
        """
        KPI 카드 HTML 생성
        
        Args:
            kpis: KPI 정보 리스트 [{"title": "", "value": "", "delta": "", "unit": ""}]
        
        Returns:
            HTML 문자열
        """
        cards_html = '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0;">'
        
        for kpi in kpis:
            title = kpi.get('title', '')
            value = kpi.get('value', 0)
            delta = kpi.get('delta', None)
            unit = kpi.get('unit', '')
            
            # Delta 색상
            if delta is not None:
                if delta > 0:
                    delta_color = self.color_theme['success']
                    delta_symbol = '▲'
                elif delta < 0:
                    delta_color = self.color_theme['danger']
                    delta_symbol = '▼'
                else:
                    delta_color = self.color_theme['text']
                    delta_symbol = '='
                
                delta_html = f'<div style="color: {delta_color}; font-size: 14px; margin-top: 5px;">{delta_symbol} {abs(delta):.1f}%</div>'
            else:
                delta_html = ''
            
            card = f'''
            <div style="background: white; border-radius: 8px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); border-left: 4px solid {self.color_theme['primary']};">
                <div style="color: #666; font-size: 14px; margin-bottom: 10px;">{title}</div>
                <div style="font-size: 28px; font-weight: bold; color: {self.color_theme['text']};">{value:.1f} <span style="font-size: 16px; font-weight: normal;">{unit}</span></div>
                {delta_html}
            </div>
            '''
            cards_html += card
        
        cards_html += '</div>'
        return cards_html

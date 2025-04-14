from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import json
from datetime import datetime

class ReportGenerator:
    def __init__(self, report_data, output_file="analysis_report.pdf"):
        self.report_data = report_data
        self.output_file = output_file
        self.styles = getSampleStyleSheet()
        self._setup_styles()
        
    def _setup_styles(self):
        """Configura estilos personalizados para o relatório"""
        # Verifica se o estilo já existe antes de adicionar
        if 'CustomTitle' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=TA_CENTER
            ))
        
        if 'CustomHeading2' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='CustomHeading2',
                parent=self.styles['Heading2'],
                fontSize=16,
                spaceAfter=12,
                textColor=colors.darkblue
            ))
        
        if 'CustomBodyText' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='CustomBodyText',
                parent=self.styles['Normal'],
                fontSize=11,
                spaceAfter=8
            ))
        
        if 'Alert' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='Alert',
                parent=self.styles['Normal'],
                fontSize=11,
                textColor=colors.red,
                spaceAfter=8
            ))
        
        if 'Conclusion' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='Conclusion',
                parent=self.styles['Normal'],
                fontSize=14,
                textColor=colors.darkgreen,
                spaceAfter=12
            ))
    
    def _create_title_page(self, story):
        """Cria a página de título do relatório"""
        story.append(Paragraph("RELATÓRIO DE ANÁLISE DE COMPORTAMENTO", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.5*inch))
        
        # Informações da atividade
        story.append(Paragraph("Identificação da Atividade", self.styles['CustomHeading2']))
        story.append(Paragraph(f"Arquivo analisado: {os.path.basename(self.report_data['file_analyzed'])}", self.styles['CustomBodyText']))
        story.append(Paragraph(f"Data da análise: {self.report_data['analysis_date']}", self.styles['CustomBodyText']))
        story.append(Paragraph(f"Total de eventos registrados: {self.report_data['typing_metrics']['total_events']}", self.styles['CustomBodyText']))
        
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph("Este relatório foi gerado automaticamente pelo sistema de análise de comportamento de digitação.", self.styles['CustomBodyText']))
        story.append(PageBreak())
    
    def _create_typing_metrics_section(self, story):
        """Cria a seção de métricas de digitação"""
        story.append(Paragraph("Métricas de Digitação", self.styles['CustomHeading2']))
        
        # Tabela de métricas
        data = [
            ["Métrica", "Valor"],
            ["Tempo médio de pressionamento", f"{self.report_data['typing_metrics']['hold_time_avg']} segundos"],
            ["Desvio padrão do tempo de pressionamento", f"{self.report_data['typing_metrics']['hold_time_std']} segundos"],
            ["Tempo médio entre teclas", f"{self.report_data['typing_metrics']['flight_time_avg']} segundos"],
            ["Desvio padrão do tempo entre teclas", f"{self.report_data['typing_metrics']['flight_time_std']} segundos"]
        ]
        
        table = Table(data, colWidths=[4*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.darkblue),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.2*inch))
        
        # Adiciona gráficos se existirem
        if 'graph_data' in self.report_data:
            story.append(Paragraph("Distribuição de Tempos de Digitação", self.styles['CustomHeading2']))
            img = Image(self.report_data['graph_data'], width=6*inch, height=4*inch)
            story.append(img)
        
        story.append(PageBreak())
    
    def _create_suspicious_commands_section(self, story):
        """Cria a seção de análise de comandos suspeitos"""
        story.append(Paragraph("Análise de Comandos Suspeitos", self.styles['CustomHeading2']))
        
        # Tabela de comandos suspeitos
        data = [["Comando", "Quantidade"]]
        for cmd, count in self.report_data['suspicious_commands']['command_counts'].items():
            data.append([cmd, str(count)])
        
        data.append(["Total", str(self.report_data['suspicious_commands']['total_commands'])])
        data.append(["Porcentagem", f"{self.report_data['suspicious_commands']['suspicious_percentage']}%"])
        
        table = Table(data, colWidths=[4*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.darkblue),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -2), colors.black),
            ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -2), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, -2), (-1, -1), colors.lightgrey),
            ('FONTNAME', (0, -2), (-1, -1), 'Helvetica-Bold'),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.2*inch))
        
        # Adiciona alertas se necessário
        if self.report_data['suspicious_commands']['suspicious_percentage'] > 10:
            story.append(Paragraph("SINAIS DE ALERTA:", self.styles['Alert']))
            story.append(Paragraph(f"• Uso excessivo de comandos de colar/copiar/recortar ({self.report_data['suspicious_commands']['suspicious_percentage']}% dos eventos)", self.styles['Alert']))
            story.append(Spacer(1, 0.1*inch))
        
        story.append(PageBreak())
    
    def _create_application_metrics_section(self, story):
        """Cria a seção de métricas por aplicação"""
        story.append(Paragraph("Métricas por Aplicação", self.styles['CustomHeading2']))
        
        # Tabela de métricas por aplicação
        data = [["Aplicação", "Duração (s)", "Taxa de Digitação", "Razão Suspeita", "Eventos"]]
        
        for app, metrics in self.report_data['application_metrics'].items():
            data.append([
                app,
                str(metrics['duration']),
                f"{metrics['typing_rate']:.2f}",
                f"{metrics['suspicious_ratio']:.2f}",
                str(metrics['event_count'])
            ])
        
        table = Table(data, colWidths=[2*inch, 1*inch, 1.5*inch, 1.5*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.darkblue),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.2*inch))
        
        # Adiciona alertas se necessário
        if len(self.report_data['application_metrics']) > 5:
            story.append(Paragraph("SINAIS DE ALERTA:", self.styles['Alert']))
            story.append(Paragraph(f"• Muitas aplicações diferentes utilizadas: {len(self.report_data['application_metrics'])}", self.styles['Alert']))
            story.append(Spacer(1, 0.1*inch))
        
        story.append(PageBreak())
    
    def generate_pdf(self):
        """Gera o relatório em PDF"""
        doc = SimpleDocTemplate(
            self.output_file,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        story = []
        
        # Adiciona as seções ao relatório
        self._create_title_page(story)
        self._create_typing_metrics_section(story)
        self._create_suspicious_commands_section(story)
        self._create_application_metrics_section(story)
        
        # Gera o PDF
        doc.build(story)
        print(f"Relatório PDF gerado com sucesso: {self.output_file}")
        return self.output_file